"""Streamlit admin dashboard for Flight Bot"""

import os

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import requests
import json

# Page config
st.set_page_config(
    page_title="Flight Bot Admin",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for navigation
st.sidebar.title("✈️ Flight Bot Admin")

page = st.sidebar.radio(
    "Navegação",
    ["🗺️ Rotas", "👥 Usuários", "📊 Histórico de Preços", "📨 Alertas Enviados", "⚙️ Configurações"],
)

# API base URL.
# Streamlit Cloud can use the deployed backend by default, while local runs
# still work with a localhost override.
API_URL = os.getenv("API_URL", "https://flights-bot-cwv7.vercel.app").rstrip("/") + "/api"
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "15"))


def get_routes_data():
    """Fetch routes from API"""
    try:
        response = requests.get(f"{API_URL}/routes?limit=1000", timeout=REQUEST_TIMEOUT_SECONDS)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar rotas: {e}")
    return {"total": 0, "routes": []}


def get_users_data(plan=None):
    """Fetch users from API"""
    try:
        url = f"{API_URL}/users?limit=1000"
        if plan:
            url += f"&plan={plan}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar usuários: {e}")
    return {"total": 0, "users": []}


def get_alerts_data(user_id=None):
    """Fetch alerts from API"""
    try:
        url = f"{API_URL}/alerts?limit=1000"
        if user_id:
            url += f"&user_id={user_id}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar alertas: {e}")
    return {"total": 0, "alerts": []}


# 🗺️ Rotas Page
if page == "🗺️ Rotas":
    st.title("🗺️ Rotas Monitoradas")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("Gerencie as rotas de voos a monitorar.")
    
    with col2:
        if st.button("➕ Nova Rota", key="new_route"):
            st.session_state.show_new_route = True
    
    # Form for new route
    if st.session_state.get("show_new_route"):
        with st.form("new_route_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                origin = st.text_input("Origem (IATA)", max_chars=3).upper()
            with col2:
                destination = st.text_input("Destino (IATA)", max_chars=3).upper()
            with col3:
                threshold = st.number_input("Preço Máximo (R$)", min_value=0.0, step=100.0)
            
            if st.form_submit_button("✅ Criar Rota"):
                if origin and destination and threshold > 0:
                    try:
                        payload = {
                            "origin_iata": origin,
                            "destination_iata": destination,
                            "threshold_price": threshold,
                        }
                        response = requests.post(
                            f"{API_URL}/routes",
                            json=payload,
                            timeout=REQUEST_TIMEOUT_SECONDS,
                        )
                        if response.status_code == 200:
                            st.success(f"Rota {origin}-{destination} criada com sucesso!")
                            st.session_state.show_new_route = False
                        else:
                            st.error(f"Erro: {response.json()}")
                    except Exception as e:
                        st.error(f"Erro: {e}")
    
    # Routes table
    data = get_routes_data()
    if data["total"] > 0:
        routes_df = pd.DataFrame(data["routes"])
        routes_df = routes_df[["origin_iata", "destination_iata", "threshold_price", "is_active", "created_at"]]
        routes_df.columns = ["Origem", "Destino", "Preço Máximo (R$)", "Ativa", "Criada em"]
        
        st.dataframe(
            routes_df,
            use_container_width=True,
            height=400,
        )
    else:
        st.info("Nenhuma rota monitorada. Crie uma nova rota para começar.")

# 👥 Usuários Page
elif page == "👥 Usuários":
    st.title("👥 Usuários")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        plan_filter = st.selectbox("Filtrar por plano", ["Todos", "free", "paid"])
    
    with col2:
        st.markdown("")  # Spacing
    
    with col3:
        if st.button("➕ Novo Usuário"):
            st.session_state.show_new_user = True
    
    # Form for new user
    if st.session_state.get("show_new_user"):
        with st.form("new_user_form"):
            phone = st.text_input("Número WhatsApp", placeholder="55XXXXXXXXXXXXX")
            name = st.text_input("Nome")
            plan = st.selectbox("Plano", ["free", "paid"])
            
            if st.form_submit_button("✅ Criar Usuário"):
                if phone:
                    try:
                        payload = {
                            "phone_number": phone,
                            "name": name,
                            "plan": plan,
                        }
                        response = requests.post(
                            f"{API_URL}/users",
                            json=payload,
                            timeout=REQUEST_TIMEOUT_SECONDS,
                        )
                        if response.status_code == 200:
                            st.success(f"Usuário {phone} criado com sucesso!")
                            st.session_state.show_new_user = False
                        else:
                            st.error(f"Erro: {response.json()}")
                    except Exception as e:
                        st.error(f"Erro: {e}")
    
    # Users table
    plan_param = None if plan_filter == "Todos" else plan_filter
    data = get_users_data(plan=plan_param)
    
    if data["total"] > 0:
        users_df = pd.DataFrame(data["users"])
        users_df = users_df[["phone_number", "name", "plan", "is_active", "created_at"]]
        users_df.columns = ["Telefone", "Nome", "Plano", "Ativo", "Criado em"]
        
        st.metric("Total de Usuários", data["total"])
        st.dataframe(users_df, use_container_width=True, height=400)
    else:
        st.info("Nenhum usuário encontrado.")

# 📊 Histórico de Preços Page
elif page == "📊 Histórico de Preços":
    st.title("📊 Histórico de Preços")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        origin = st.text_input("Origem (IATA)", max_chars=3).upper()
    with col2:
        destination = st.text_input("Destino (IATA)", max_chars=3).upper()
    with col3:
        days = st.slider("Últimos N dias", min_value=1, max_value=90, value=7)
    
    if origin and destination:
        st.info(f"Gráfico de preços para {origin} → {destination} nos últimos {days} dias")
        
        # Placeholder for chart
        with st.spinner("Carregando dados..."):
            st.markdown("_Gráfico de histórico será exibido aqui_")

# 📨 Alertas Enviados Page
elif page == "📨 Alertas Enviados":
    st.title("📨 Alertas Enviados")
    
    col1, col2 = st.columns(2)
    with col1:
        alert_type = st.selectbox("Tipo de alerta", ["Todos", "free_group", "paid_user_dm"])
    with col2:
        days = st.slider("Últimos N dias", min_value=1, max_value=30, value=7)
    
    st.markdown(f"Alertas dos últimos {days} dias")
    
    # Placeholder for alerts table
    st.markdown("_Tabela de alertas enviados será exibida aqui_")

# ⚙️ Configurações Page
elif page == "⚙️ Configurações":
    st.title("⚙️ Configurações")
    
    with st.form("settings_form"):
        st.markdown("### Agendador")
        scan_interval = st.number_input(
            "Intervalo de Scan (minutos)",
            min_value=30,
            max_value=1440,
            value=120,
        )
        digest_interval = st.number_input(
            "Intervalo do Digest (horas)",
            min_value=1,
            max_value=24,
            value=6,
        )
        
        st.markdown("### Limiares de Preço Padrão")
        domestic_threshold = st.number_input(
            "Limiar Doméstico (R$)",
            min_value=0.0,
            value=299.0,
            step=50.0,
        )
        intl_threshold = st.number_input(
            "Limiar Internacional (R$)",
            min_value=0.0,
            value=1499.0,
            step=100.0,
        )
        
        st.markdown("### Cooldown")
        cooldown_hours = st.number_input(
            "Cooldown entre alertas (horas)",
            min_value=1,
            max_value=72,
            value=24,
        )
        
        if st.form_submit_button("💾 Salvar Configurações"):
            st.success("Configurações salvas com sucesso!")
    
    st.markdown("---")
    st.markdown("### Informações do Sistema")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", "✅ Ativo")
    with col2:
        st.metric("Versão", "1.0.0")
    with col3:
        st.metric("Banco de Dados", "SQLite")
