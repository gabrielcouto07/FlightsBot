"""Streamlit control panel for Flight Bot."""

from __future__ import annotations

import os
from datetime import date, datetime, timedelta
from typing import Any, Optional

import httpx
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from app.utils.airports import get_all_airports

APP_TITLE = "FlightsBot Console"
DEFAULT_BACKEND_BASE_URL = ""
DEFAULT_TIMEOUT_SECONDS = 15


def _read_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    """Read a value from Streamlit secrets or environment variables."""
    try:
        if name in st.secrets:
            value = st.secrets.get(name)
            if value is not None:
                return str(value)
    except StreamlitSecretNotFoundError:
        pass

    value = os.getenv(name)
    if value is not None:
        return value

    return default


def get_backend_base_url() -> str:
    """Resolve the backend base URL without an /api suffix."""
    raw_value = (
        st.session_state.get("backend_base_url_override")
        or _read_secret("BACKEND_BASE_URL")
        or _read_secret("API_URL")
        or DEFAULT_BACKEND_BASE_URL
    )
    raw_value = str(raw_value or "").strip()

    if not raw_value:
        return ""

    normalized = raw_value.rstrip("/")
    if normalized.endswith("/api"):
        normalized = normalized[:-4]

    return normalized.rstrip("/")


def get_api_base_url() -> str:
    """Return the backend API base URL."""
    if not get_backend_base_url():
        return ""
    return f"{get_backend_base_url()}/api"


def get_health_url() -> str:
    """Return the health check endpoint."""
    if not get_backend_base_url():
        return ""
    return f"{get_backend_base_url()}/health"


def get_timeout_seconds() -> int:
    """Resolve request timeout from secrets or environment."""
    raw_value = _read_secret("REQUEST_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS))
    try:
        return max(int(str(raw_value)), 5)
    except (TypeError, ValueError):
        return DEFAULT_TIMEOUT_SECONDS


def build_client() -> httpx.Client:
    """Create a synchronous HTTP client for backend calls."""
    return httpx.Client(timeout=get_timeout_seconds())


def build_airport_options() -> list[dict[str, str]]:
    """Build airport options for selectors."""
    airports = list(get_all_airports())

    def sort_key(item: dict[str, str]) -> tuple[int, str, str]:
        is_brazil = 0 if item.get("country") == "Brazil" else 1
        return (is_brazil, item.get("city", ""), item.get("code", ""))

    return sorted(airports, key=sort_key)


AIRPORT_OPTIONS = build_airport_options()
AIRPORT_LABELS = {
    airport["code"]: (
        f'{airport.get("flag", "🌍")} {airport["code"]} - '
        f'{airport.get("city", "Unknown")}, {airport.get("country", "Unknown")}'
    )
    for airport in AIRPORT_OPTIONS
}


def airport_label(code: Optional[str]) -> str:
    """Return a human-friendly airport label."""
    if not code:
        return "Qualquer destino"

    normalized = code.upper()
    if normalized == "ANYWHERE":
        return "🌍 ANYWHERE - Qualquer destino"

    return AIRPORT_LABELS.get(normalized, normalized)


def format_currency(value: Optional[float]) -> str:
    """Format values in BRL style."""
    if value is None:
        return "-"
    return f"R$ {value:,.0f}".replace(",", ".")


def format_percent(value: Optional[float]) -> str:
    """Format percentage values."""
    if value is None:
        return "-"
    return f"{value:.1f}%"


def format_datetime(value: Optional[str]) -> str:
    """Render ISO-like datetimes in a compact format."""
    if not value:
        return "-"

    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        return parsed.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return value


def request_json(
    method: str,
    path: str,
    *,
    params: Optional[dict[str, Any]] = None,
    json_body: Optional[dict[str, Any]] = None,
) -> Any:
    """Send an HTTP request to the backend and return JSON."""
    if not get_backend_base_url():
        raise RuntimeError(
            "Backend nao configurado. Defina `BACKEND_BASE_URL` nos secrets "
            "ou informe uma URL temporaria na barra lateral."
        )

    url = f"{get_api_base_url()}{path}"

    try:
        with build_client() as client:
            response = client.request(method, url, params=params, json=json_body)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        message = exc.response.text.strip() or exc.response.reason_phrase
        raise RuntimeError(
            f"{exc.response.status_code} ao chamar {path}: {message}"
        ) from exc
    except httpx.HTTPError as exc:
        raise RuntimeError(
            f"Falha ao conectar no backend em {get_backend_base_url()}."
        ) from exc

    if not response.content:
        return {}

    return response.json()


@st.cache_data(ttl=30, show_spinner=False)
def fetch_health() -> dict[str, Any]:
    """Fetch backend health."""
    if not get_backend_base_url():
        return {"status": "not_configured"}

    try:
        with build_client() as client:
            response = client.get(get_health_url())
        response.raise_for_status()
        return response.json()
    except Exception as exc:  # noqa: BLE001
        return {"status": "offline", "error": str(exc)}


@st.cache_data(ttl=60, show_spinner=False)
def fetch_routes() -> dict[str, Any]:
    """Fetch routes."""
    return request_json("GET", "/routes", params={"limit": 200, "active_only": False})


@st.cache_data(ttl=60, show_spinner=False)
def fetch_users() -> dict[str, Any]:
    """Fetch users."""
    return request_json("GET", "/users", params={"limit": 200, "active_only": False})


@st.cache_data(ttl=60, show_spinner=False)
def fetch_alerts() -> dict[str, Any]:
    """Fetch alerts."""
    return request_json("GET", "/alerts", params={"limit": 200, "active_only": False})


@st.cache_data(ttl=60, show_spinner=False)
def fetch_notifications() -> dict[str, Any]:
    """Fetch recent demo notifications."""
    return request_json("GET", "/demo/notifications", params={"limit": 50})


@st.cache_data(ttl=90, show_spinner=False)
def fetch_deals(params: tuple[tuple[str, Any], ...]) -> dict[str, Any]:
    """Fetch searchable flight deals."""
    request_params = {key: value for key, value in params if value not in (None, "", [])}
    return request_json("GET", "/search/deals", params=request_params)


def clear_cached_api_data() -> None:
    """Clear Streamlit API caches after writes."""
    fetch_health.clear()
    fetch_routes.clear()
    fetch_users.clear()
    fetch_alerts.clear()
    fetch_notifications.clear()
    fetch_deals.clear()


def rerun_app() -> None:
    """Rerun the app across Streamlit versions."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def render_backend_banner() -> None:
    """Render backend connectivity status at the top of the page."""
    health = fetch_health()
    status = str(health.get("status", "offline")).lower()

    if status == "not_configured":
        st.info(
            "Configure a URL do backend para ativar o painel. "
            "Voce pode definir `BACKEND_BASE_URL` nos secrets do Streamlit "
            "ou informar uma URL temporaria na barra lateral."
        )
        return

    if status == "healthy":
        st.success(f"Backend conectado em `{get_backend_base_url()}`.")
        return

    detail = health.get("error") or "Sem resposta do endpoint /health."
    st.warning(
        "O painel abriu, mas o backend nao respondeu. "
        "Verifique `BACKEND_BASE_URL` nos secrets ou teste uma URL temporaria.\n\n"
        f"Detalhe: `{detail}`"
    )


def render_sidebar() -> str:
    """Render navigation and deployment controls."""
    with st.sidebar:
        st.title("FlightsBot")
        st.caption("Painel Streamlit pronto para Community Cloud")

        health = fetch_health()
        status = str(health.get("status", "offline")).lower()
        current_backend = get_backend_base_url()
        st.markdown("### Status")
        st.write(f"Backend: `{current_backend or 'nao configurado'}`")
        st.write(f"API: `{get_api_base_url() or 'nao configurada'}`")
        st.write(f"Timeout: `{get_timeout_seconds()}s`")
        st.write(f"Health: `{status}`")

        override_value = st.text_input(
            "URL temporaria do backend",
            value=st.session_state.get("backend_base_url_override", ""),
            placeholder="https://seu-backend.exemplo.com",
            help="Use para testar uma URL de backend sem editar os secrets do app.",
        )
        normalized_override = override_value.strip()
        if normalized_override != st.session_state.get("backend_base_url_override", ""):
            st.session_state["backend_base_url_override"] = normalized_override
            clear_cached_api_data()
            rerun_app()

        if st.button("Limpar cache", use_container_width=True):
            clear_cached_api_data()
            rerun_app()

        st.markdown("### Navegacao")
        return st.radio(
            "Pagina",
            (
                "Visao geral",
                "Buscar ofertas",
                "Rotas monitoradas",
                "Usuarios",
                "Alertas",
                "Notificacoes demo",
                "Deploy",
            ),
            label_visibility="collapsed",
        )


def render_overview() -> None:
    """Render the summary page."""
    st.header("Visao geral")
    st.caption("Resumo do backend e dos recursos principais do bot.")

    routes_data = fetch_routes()
    users_data = fetch_users()
    alerts_data = fetch_alerts()
    notifications_data = fetch_notifications()

    routes = routes_data.get("routes", [])
    users = users_data.get("users", [])
    alerts = alerts_data.get("alerts", [])
    notifications = notifications_data.get("notifications", [])

    active_routes = sum(1 for route in routes if route.get("is_active"))
    active_users = sum(1 for user in users if user.get("is_active"))
    active_alerts = sum(1 for alert in alerts if alert.get("is_active"))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rotas", str(len(routes)), delta=f"{active_routes} ativas")
    col2.metric("Usuarios", str(len(users)), delta=f"{active_users} ativos")
    col3.metric("Alertas", str(len(alerts)), delta=f"{active_alerts} ativos")
    col4.metric("Notif. demo", str(len(notifications)), delta="ultimas 50")

    st.markdown("### Ultimas notificacoes")
    if notifications:
        st.dataframe(notifications, use_container_width=True)
    else:
        st.info("Nenhuma notificacao demo encontrada ainda.")


def render_search() -> None:
    """Render search UI backed by /api/search/deals."""
    st.header("Buscar ofertas")
    st.caption("Consulta direta ao endpoint `/api/search/deals` do backend.")

    airport_codes = [airport["code"] for airport in AIRPORT_OPTIONS]
    destination_codes = ["ANYWHERE", *airport_codes]

    with st.form("search_deals_form"):
        row1 = st.columns([1.2, 1.2, 1, 1])
        origin = row1[0].selectbox(
            "Origem",
            options=airport_codes,
            index=airport_codes.index("GRU") if "GRU" in airport_codes else 0,
            format_func=airport_label,
        )
        destination = row1[1].selectbox(
            "Destino",
            options=destination_codes,
            index=0,
            format_func=airport_label,
        )
        date_from = row1[2].date_input("Data de ida", value=date.today(), min_value=date.today())
        date_to = row1[3].date_input(
            "Data de volta ou janela",
            value=date.today() + timedelta(days=60),
            min_value=date.today(),
        )

        row2 = st.columns([1, 1, 1, 1, 1.2])
        trip_type = row2[0].selectbox("Tipo", options=["round_trip", "one_way"], format_func=lambda item: "Ida e volta" if item == "round_trip" else "So ida")
        adults = row2[1].number_input("Adultos", min_value=1, max_value=9, value=1, step=1)
        max_price = row2[2].number_input("Preco maximo", min_value=0, value=0, step=50)
        nights_min = row2[3].number_input("Noites min", min_value=0, max_value=60, value=0, step=1)
        nights_max = row2[4].number_input("Noites max", min_value=0, max_value=60, value=14, step=1)

        submitted = st.form_submit_button("Buscar ofertas", use_container_width=True)

    if not submitted:
        st.info("Preencha os filtros e clique em buscar para carregar as ofertas.")
        return

    if date_to < date_from:
        st.error("A data final nao pode ser anterior a data inicial.")
        return

    params = (
        ("fly_from", origin),
        ("fly_to", destination.lower() if destination == "ANYWHERE" else destination),
        ("date_from", date_from.isoformat()),
        ("date_to", date_to.isoformat()),
        ("trip_type", trip_type),
        ("adults", adults),
        ("nights_min", nights_min),
        ("nights_max", max(nights_max, nights_min)),
        ("max_price", max_price or None),
    )

    with st.spinner("Buscando ofertas no backend..."):
        try:
            response = fetch_deals(params)
        except RuntimeError as exc:
            st.error(str(exc))
            return

    results = response.get("results", [])
    kpis = response.get("kpis", {})
    meta = response.get("search_meta", {})

    kpi_cols = st.columns(4)
    kpi_cols[0].metric("Tarifas analisadas", str(kpis.get("total_scanned_24h", 0)))
    kpi_cols[1].metric("Alertas ativos", str(kpis.get("active_alerts", 0)))
    kpi_cols[2].metric("CPM medio", str(kpis.get("average_cpm", "-")))
    kpi_cols[3].metric("Maior economia", format_percent(kpis.get("top_saving_percent")))

    st.caption(
        f"Fonte: {meta.get('source', '-')} | "
        f"Links acionaveis: {meta.get('actionable_link_rate', 0)}% | "
        f"Buscado em: {format_datetime(meta.get('searched_at'))}"
    )

    if not results:
        st.warning("Nenhuma oferta retornada com os filtros atuais.")
        return

    for deal in results:
        st.markdown("---")
        with st.container():
            top = st.columns([2.2, 1.4, 1.2])
            top[0].subheader(f"{deal.get('origin')} -> {deal.get('destination')}")
            top[0].caption(
                f"{deal.get('origin_city', '-')} -> {deal.get('destination_city', '-')}"
            )
            top[1].metric("Preco", format_currency(deal.get("price")))
            top[1].caption(deal.get("deal_badge") or "Melhor opcao")
            top[2].metric("Companhia", deal.get("airline_iata", "-"))
            top[2].caption(deal.get("airline", "-"))

            details = st.columns(4)
            details[0].write(f"Ida: {format_datetime(deal.get('departure_at'))}")
            details[1].write(f"Volta: {format_datetime(deal.get('return_at'))}")
            details[2].write(f"Duracao: {deal.get('duration_minutes', 0)} min")
            details[3].write(f"Paradas: {deal.get('stops', 0)}")

            st.write(
                f"Reserva: {deal.get('booking_source_label', deal.get('booking_source', '-'))}"
            )
            link = deal.get("deeplink_url") or deal.get("purchase_url")
            if link:
                st.markdown(f"[Abrir link de compra]({link})")
            else:
                st.warning("Oferta sem deeplink retornado pelo backend.")


def render_routes() -> None:
    """Render routes page."""
    st.header("Rotas monitoradas")
    st.caption("Cadastro das rotas usadas pelo scanner do bot.")

    route_options = [airport["code"] for airport in AIRPORT_OPTIONS]

    with st.form("create_route_form"):
        cols = st.columns(3)
        origin = cols[0].selectbox("Origem", route_options, format_func=airport_label)
        destination = cols[1].selectbox(
            "Destino",
            route_options,
            index=route_options.index("SSA") if "SSA" in route_options else 0,
            format_func=airport_label,
        )
        threshold = cols[2].number_input(
            "Teto de preco (BRL)",
            min_value=1.0,
            value=299.0,
            step=50.0,
        )
        create_route = st.form_submit_button("Criar rota", use_container_width=True)

    if create_route:
        try:
            request_json(
                "POST",
                "/routes",
                json_body={
                    "origin_iata": origin,
                    "destination_iata": destination,
                    "threshold_price": threshold,
                },
            )
            clear_cached_api_data()
            st.success("Rota criada com sucesso.")
            rerun_app()
        except RuntimeError as exc:
            st.error(str(exc))

    routes_data = fetch_routes()
    routes = routes_data.get("routes", [])
    if routes:
        st.dataframe(routes, use_container_width=True)
    else:
        st.info("Nenhuma rota cadastrada.")


def render_users() -> None:
    """Render users page."""
    st.header("Usuarios")
    st.caption("Gestao de assinantes e usuarios do bot.")

    with st.form("create_user_form"):
        cols = st.columns(3)
        phone_number = cols[0].text_input("WhatsApp", placeholder="5511999999999")
        name = cols[1].text_input("Nome", placeholder="Ana Lima")
        plan = cols[2].selectbox("Plano", options=["free", "paid"])
        create_user = st.form_submit_button("Criar usuario", use_container_width=True)

    if create_user:
        try:
            request_json(
                "POST",
                "/users",
                json_body={
                    "phone_number": phone_number,
                    "name": name or None,
                    "plan": plan,
                },
            )
            clear_cached_api_data()
            st.success("Usuario criado com sucesso.")
            rerun_app()
        except RuntimeError as exc:
            st.error(str(exc))

    users_data = fetch_users()
    users = users_data.get("users", [])
    if users:
        st.dataframe(users, use_container_width=True)
    else:
        st.info("Nenhum usuario cadastrado.")


def render_alerts() -> None:
    """Render alerts page."""
    st.header("Alertas")
    st.caption("Cadastro de alertas personalizados por usuario.")

    users = fetch_users().get("users", [])
    if not users:
        st.info("Crie pelo menos um usuario antes de cadastrar alertas.")
        return

    user_map = {
        f"{user.get('name') or 'Sem nome'} - {user.get('phone_number')}": user
        for user in users
    }

    destination_options = ["ANYWHERE", *[airport["code"] for airport in AIRPORT_OPTIONS]]

    with st.form("create_alert_form"):
        cols = st.columns(5)
        user_label = cols[0].selectbox("Usuario", options=list(user_map))
        origin = cols[1].selectbox("Origem", options=[airport["code"] for airport in AIRPORT_OPTIONS], format_func=airport_label)
        destination = cols[2].selectbox("Destino", options=destination_options, format_func=airport_label)
        date_from = cols[3].date_input("Data inicial", value=date.today())
        date_to = cols[4].date_input("Data final", value=date.today() + timedelta(days=60))
        max_price = st.number_input("Preco maximo", min_value=1.0, value=1200.0, step=50.0)
        create_alert = st.form_submit_button("Criar alerta", use_container_width=True)

    if create_alert:
        user = user_map[user_label]
        try:
            request_json(
                "POST",
                "/alerts",
                params={"user_id": user["id"]},
                json_body={
                    "origin_iata": origin,
                    "destination_iata": None if destination == "ANYWHERE" else destination,
                    "date_from": date_from.isoformat(),
                    "date_to": date_to.isoformat(),
                    "max_price": max_price,
                },
            )
            clear_cached_api_data()
            st.success("Alerta criado com sucesso.")
            rerun_app()
        except RuntimeError as exc:
            st.error(str(exc))

    alerts_data = fetch_alerts()
    alerts = alerts_data.get("alerts", [])
    if alerts:
        st.dataframe(alerts, use_container_width=True)
    else:
        st.info("Nenhum alerta cadastrado.")


def render_demo() -> None:
    """Render demo notifications page."""
    st.header("Notificacoes demo")
    st.caption("Util para validar o fluxo sem depender do WhatsApp em producao.")

    col1, col2 = st.columns([1, 2])
    if col1.button("Popular dados demo", use_container_width=True):
        try:
            request_json("POST", "/demo/seed")
            clear_cached_api_data()
            st.success("Base demo populada com sucesso.")
            rerun_app()
        except RuntimeError as exc:
            st.error(str(exc))

    if col2.button("Atualizar notificacoes", use_container_width=True):
        clear_cached_api_data()
        rerun_app()

    notifications = fetch_notifications().get("notifications", [])
    if notifications:
        st.dataframe(notifications, use_container_width=True)
    else:
        st.info("Nenhuma notificacao demo registrada.")


def render_deploy() -> None:
    """Render deployment guidance page."""
    st.header("Deploy no Streamlit Community Cloud")
    st.caption("Checklist final para publicar este app em `share.streamlit.io`.")

    st.markdown(
        """
1. Publique este repositório no GitHub.
2. No Streamlit Community Cloud, escolha o arquivo de entrada `streamlit_app.py`.
3. Em **Advanced settings**, selecione **Python 3.11**.
4. Cole os secrets abaixo ajustando a URL do backend.
5. Garanta que o backend FastAPI esteja publicado separadamente e exponha `/health` e `/api/*`.
        """
    )

    st.code(
        '# Exemplo para os secrets do Community Cloud\n\n'
        'BACKEND_BASE_URL = "https://seu-backend.exemplo.com"\n'
        'REQUEST_TIMEOUT_SECONDS = 15\n',
        language="toml",
    )

    st.info(
        "Este deploy publica apenas o app Streamlit. "
        "O FastAPI, banco de dados, Redis e schedulers continuam como servicos separados."
    )

    st.write("Entrypoint:", "`streamlit_app.py`")
    st.write("Backend atual:", f"`{get_backend_base_url()}`")
    st.write("Health atual:", f"`{get_health_url()}`")


def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title(APP_TITLE)
    st.caption("Painel de operacao e busca para o backend do FlightsBot.")
    render_backend_banner()
    page = render_sidebar()

    try:
        if page == "Visao geral":
            render_overview()
        elif page == "Buscar ofertas":
            render_search()
        elif page == "Rotas monitoradas":
            render_routes()
        elif page == "Usuarios":
            render_users()
        elif page == "Alertas":
            render_alerts()
        elif page == "Notificacoes demo":
            render_demo()
        else:
            render_deploy()
    except RuntimeError as exc:
        st.error(str(exc))


if __name__ == "__main__":
    main()
