"""Flight search API - search deals and preview user matches."""

from __future__ import annotations

import logging
import math
import random
from collections import defaultdict
from datetime import date, datetime, timedelta
from statistics import mean
from typing import Optional
from urllib.parse import quote_plus, urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.models.price_snapshot import PriceSnapshot
from app.models.user import User
from app.models.user_alert import UserAlert
from app.scrapers.kiwi import KiwiScraper
from app.utils.airports import (
    AIRPORTS,
    get_airport_info,
    get_all_airports,
    is_domestic,
    normalize_airport_code,
)

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/search", tags=["search"])

DEMO_AIRLINES = [
    {"name": "LATAM", "iata": "LA"},
    {"name": "GOL", "iata": "G3"},
    {"name": "Azul", "iata": "AD"},
    {"name": "TAP Air Portugal", "iata": "TP"},
    {"name": "American Airlines", "iata": "AA"},
    {"name": "Delta Air Lines", "iata": "DL"},
    {"name": "Iberia", "iata": "IB"},
]

AIRLINE_BOOKING_URLS = {
    "LA": ("LATAM", "https://www.latamairlines.com/br/pt"),
    "G3": ("GOL", "https://www.voegol.com.br/pt"),
    "AD": ("Azul", "https://www.voeazul.com.br/br/pt/home"),
    "TP": ("TAP Air Portugal", "https://www.flytap.com/en-br"),
    "AA": ("American Airlines", "https://www.aa.com/"),
    "DL": ("Delta Air Lines", "https://www.delta.com/"),
    "IB": ("Iberia", "https://www.iberia.com/br/"),
}

AIRPORT_COORDS = {
    "GRU": (-23.4356, -46.4731),
    "CGH": (-23.6261, -46.6566),
    "GIG": (-22.8090, -43.2506),
    "SSA": (-12.9109, -38.3310),
    "REC": (-8.1265, -34.9236),
    "FOR": (-3.7763, -38.5326),
    "BSB": (-15.8692, -47.9208),
    "CWB": (-25.5317, -49.1761),
    "MIA": (25.7959, -80.2871),
    "JFK": (40.6413, -73.7781),
    "LIS": (38.7742, -9.1342),
    "BCN": (41.2974, 2.0833),
    "MAD": (40.4983, -3.5676),
    "EZE": (-34.8222, -58.5358),
    "CUN": (21.0365, -86.8771),
    "LHR": (51.4700, -0.4543),
}

DEMO_DESTINATIONS = {
    "GRU": ["SSA", "REC", "FOR", "MIA", "LIS", "BCN", "EZE", "CUN"],
    "GIG": ["SSA", "REC", "BSB", "MIA", "LIS", "MAD"],
    "SSA": ["GRU", "REC", "FOR", "LIS", "MIA"],
    "REC": ["GRU", "FOR", "SSA", "LIS", "MIA"],
}


class SearchKpisResponse(BaseModel):
    """Topline KPI cards shown on the dashboard."""

    total_scanned_24h: int
    active_alerts: int
    average_cpm: Optional[float]
    top_saving_percent: float


class DealResponse(BaseModel):
    """Flight deal response schema."""

    origin: str
    destination: str
    origin_city: str
    origin_country: str
    destination_city: str
    destination_country: str
    price: float
    currency: str
    airline: str
    airline_iata: str
    airline_logo_url: str
    departure_at: str
    return_at: Optional[str]
    duration_minutes: int
    stops: int
    booking_token: Optional[str] = None
    deeplink_url: str
    booking_source: str
    booking_source_label: str
    provider_code: str
    booking_url: str
    deep_link: str
    provider_name: str
    booking_source_type: str
    deeplink_tier: int
    provider_itinerary_id: Optional[str] = None
    fare_token: Optional[str] = None
    fare_last_seen_at: str
    purchase_url: str
    purchase_label: str
    secondary_purchase_url: str
    secondary_purchase_label: str
    official_airline_url: str
    official_airline_label: str
    historical_avg_price: float
    historical_low_price: float
    savings_percent: float
    trend_change_7d: float
    price_history_7d: list[float]
    opportunity_score: int
    opportunity_badges: list[str]
    distance_miles: Optional[int] = None
    cpm: Optional[float] = None
    is_deal: bool
    deal_badge: Optional[str] = None


class SearchMetaResponse(BaseModel):
    """Search metadata."""

    fly_from: str
    fly_to: str
    searched_at: str
    source: str
    actionable_link_rate: float
    source_confidence_note: str


class SearchDealsResponse(BaseModel):
    """Search deals response."""

    results: list[DealResponse]
    total: int
    search_meta: SearchMetaResponse
    kpis: SearchKpisResponse


class AirportOptionResponse(BaseModel):
    """Airport option for search UIs."""

    code: str
    city: str
    country: str
    flag: str


class MatchedAlert(BaseModel):
    """User alert with match info."""

    id: str
    origin_iata: Optional[str]
    destination_iata: Optional[str]
    date_from: date
    date_to: date
    max_price: float
    matched_deal_count: int


class MatchPreviewResponse(BaseModel):
    """Preview match response."""

    user: dict
    matched_deals: list[DealResponse]
    matched_alerts: list[MatchedAlert]
    unmatched_count: int
    active_alerts: int


def _build_market_search_link(origin: str, destination: str, departure_date: date) -> str:
    """Build a Google Flights fallback that preserves route and dates."""
    query = f"flights from {origin} to {destination} on {departure_date.isoformat()}"
    return f"https://www.google.com/travel/flights?q={quote_plus(query)}"


def _build_google_flights_link(
    origin: str,
    destination: str,
    departure_date: date,
    return_date: Optional[date] = None,
) -> str:
    """Build a universal Google Flights search link."""
    query = f"flights from {origin} to {destination} on {departure_date.isoformat()}"
    if return_date:
        query = f"{query} returning {return_date.isoformat()}"
    return f"https://www.google.com/travel/flights?q={quote_plus(query)}"


def _get_airline_booking_details(airline_iata: str) -> tuple[str, str]:
    """Map airline code to official booking entrypoint."""
    name, url = AIRLINE_BOOKING_URLS.get(
        airline_iata.upper(),
        ("Airline website", "https://www.google.com/travel/flights"),
    )
    return url, f"Open {name}"


def _build_direct_airline_link(
    *,
    airline_iata: str,
    origin: str,
    destination: str,
    departure_date: date,
    return_date: Optional[date],
    adults: int,
) -> Optional[str]:
    """Build confirmed airline booking links when the pattern is known."""
    if return_date:
        return None

    departure_iso = departure_date.isoformat()
    passengers = max(adults, 1)
    airline_iata = airline_iata.upper()

    if airline_iata == "LA":
        return (
            "https://www.latamairlines.com/br/pt/oferta-voos?"
            + urlencode(
                {
                    "origin": origin,
                    "destination": destination,
                    "outbound": departure_iso,
                    "adt": passengers,
                    "trip": "OW",
                }
            )
        )
    if airline_iata == "G3":
        return (
            "https://www.voegol.com.br/pt/passagens-aereas?"
            + urlencode(
                {
                    "origin": origin,
                    "destination": destination,
                    "departureDate": departure_iso,
                    "adults": passengers,
                }
            )
        )
    if airline_iata == "AD":
        return (
            "https://www.voeazul.com.br/tudo-sobre-azul/passagens?"
            + urlencode(
                {
                    "origin": origin,
                    "destination": destination,
                    "departureDate": departure_iso,
                }
            )
        )
    if airline_iata == "AA":
        return (
            f"https://www.aa.com/booking/search#/air/"
            f"{origin}/{destination}/oneWay/{departure_iso}/{passengers}/0/0/Business"
        )
    if airline_iata == "DL":
        return (
            "https://www.delta.com/us/en/flight-search/book-a-flight?"
            + urlencode(
                {
                    "origin": origin,
                    "destination": destination,
                    "departureDate": departure_iso,
                }
            )
        )
    if airline_iata == "TP":
        return (
            "https://www.tapair.pt/en/flight-results?"
            + urlencode(
                {
                    "origin": origin,
                    "destination": destination,
                    "departureDate": departure_iso,
                    "adults": passengers,
                }
            )
        )
    if airline_iata == "IB":
        return (
            "https://www.iberia.com/web/portal/search/flightResults?"
            + urlencode(
                {
                    "origin": origin,
                    "destination": destination,
                    "departDate": departure_iso,
                    "adults": passengers,
                }
            )
        )
    return None


def _pick_demo_destinations(origin: str, limit: int) -> list[str]:
    """Pick plausible demo destinations from the airport catalog."""
    preferred = DEMO_DESTINATIONS.get(origin)
    if preferred:
        return preferred[:limit]

    fallback = [code for code in AIRPORTS if code != origin]
    return fallback[:limit]


def _haversine_miles(origin: str, destination: str) -> Optional[int]:
    """Estimate route distance in miles for KPI and CPM calculations."""
    origin_coords = AIRPORT_COORDS.get(origin)
    destination_coords = AIRPORT_COORDS.get(destination)
    if not origin_coords or not destination_coords:
        return None

    lat1, lon1 = map(math.radians, origin_coords)
    lat2, lon2 = map(math.radians, destination_coords)
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return int(3958.8 * c)


def _build_synthetic_history(price: float, seed_key: str) -> list[float]:
    """Build stable synthetic history when DB history is unavailable."""
    rng = random.Random(seed_key)
    values: list[float] = []
    for offset in range(7):
        multiplier = 1.18 - (offset * 0.028) + rng.uniform(-0.03, 0.03)
        values.append(round(max(price * multiplier, price * 0.88), 2))
    values[-1] = round(price, 2)
    return values


async def _load_route_history(
    db: AsyncSession,
    origin: str,
    destination: str,
    current_price: float,
    seed_key: str,
) -> tuple[list[float], float, float]:
    """Load 7-day history, a 30-day average, and a 45-day low watermark."""
    since = datetime.utcnow() - timedelta(days=45)
    stmt = (
        select(PriceSnapshot.price, PriceSnapshot.captured_at)
        .where(
            PriceSnapshot.origin == origin,
            PriceSnapshot.destination == destination,
            PriceSnapshot.captured_at >= since,
        )
        .order_by(PriceSnapshot.captured_at.asc())
    )
    result = await db.execute(stmt)
    rows = result.all()

    if not rows:
        synthetic = _build_synthetic_history(current_price, seed_key)
        return synthetic, round(mean(synthetic) * 1.08, 2), round(min(synthetic), 2)

    all_prices = [float(row.price) for row in rows]
    recent_30d_cutoff = datetime.utcnow() - timedelta(days=30)
    recent_30d_prices = [
        float(row.price)
        for row in rows
        if row.captured_at >= recent_30d_cutoff
    ]
    by_day: dict[date, list[float]] = defaultdict(list)
    for row in rows:
        by_day[row.captured_at.date()].append(float(row.price))

    history: list[float] = []
    for day_offset in range(6, -1, -1):
        day_key = (datetime.utcnow() - timedelta(days=day_offset)).date()
        day_prices = by_day.get(day_key)
        if day_prices:
            history.append(round(min(day_prices), 2))
        elif history:
            history.append(history[-1])
        else:
            history.append(round(current_price * 1.05, 2))

    history[-1] = round(current_price, 2)
    average_prices = recent_30d_prices or all_prices
    return history, round(mean(average_prices), 2), round(min(all_prices), 2)


def _build_purchase_links(
    *,
    flight: dict,
    departure_date: date,
    return_date: Optional[date],
    adults: int,
) -> tuple[str, str, str, str, str, str, str, int]:
    """Choose the strongest available itinerary-preserving booking path."""
    origin = flight.get("origin", "")
    destination = flight.get("destination", "")
    airline_iata = (flight.get("airline_iata") or "").upper()
    raw_booking_source = str(flight.get("booking_source") or "")
    provider_name, official_airline_url = AIRLINE_BOOKING_URLS.get(
        airline_iata,
        (flight.get("airline", "Airline"), "https://www.google.com/travel/flights"),
    )
    official_airline_label = f"Open {provider_name}"
    google_flights_url = _build_google_flights_link(origin, destination, departure_date, return_date)
    kiwi_url = flight.get("deeplink_url") or flight.get("deep_link") or flight.get("booking_url") or ""

    if raw_booking_source == "kiwi" and kiwi_url:
        secondary_url = _build_direct_airline_link(
            airline_iata=airline_iata,
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            adults=adults,
        ) or google_flights_url
        secondary_label = (
            f"Check {provider_name}" if secondary_url != google_flights_url else "Search on Google Flights"
        )
        return (
            kiwi_url,
            "kiwi",
            provider_name,
            official_airline_url,
            official_airline_label,
            secondary_url,
            secondary_label,
            1,
        )

    direct_url = _build_direct_airline_link(
        airline_iata=airline_iata,
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        adults=adults,
    )
    if direct_url:
        return (
            direct_url,
            "direct_airline",
            provider_name,
            official_airline_url,
            official_airline_label,
            google_flights_url,
            "Search on Google Flights",
            2,
        )

    if google_flights_url:
        return (
            google_flights_url,
            "google_flights",
            provider_name,
            official_airline_url,
            official_airline_label,
            official_airline_url,
            official_airline_label,
            3,
        )

    return (
        official_airline_url,
        "airline_homepage",
        provider_name,
        official_airline_url,
        official_airline_label,
        official_airline_url,
        official_airline_label,
        4,
    )


def _compute_intelligence(
    *,
    price: float,
    threshold: float,
    history: list[float],
    historical_avg_price: float,
    historical_low_price: float,
    cpm: Optional[float],
) -> tuple[bool, Optional[str], float, float, int, list[str]]:
    """Compute ranking signals and opportunity badges."""
    savings_percent = round(((historical_avg_price - price) / historical_avg_price) * 100, 1) if historical_avg_price else 0.0
    trend_change_7d = 0.0
    if history and history[0]:
        trend_change_7d = round(((price - history[0]) / history[0]) * 100, 1)

    badges: list[str] = []
    if savings_percent >= 30:
        badges.append("30% Below Average")
    if price <= historical_low_price:
        badges.append("Lowest in 30 Days")
    if trend_change_7d <= -10:
        badges.append("Fast Drop")
    if price <= threshold * 0.72:
        badges.append("Error Fare Watch")
    if cpm is not None and cpm <= 0.12:
        badges.append("High Value")

    opportunity_score = max(
        10,
        min(
            99,
            int(55 + (savings_percent * 1.1) + max(-trend_change_7d, 0) + (8 if price <= threshold else 0)),
        ),
    )

    is_deal = price <= threshold
    deal_badge = None
    if is_deal:
        if badges:
            deal_badge = badges[0]
        elif price < threshold * 0.85:
            deal_badge = "Best price today"
        else:
            deal_badge = "Good deal"

    return is_deal, deal_badge, savings_percent, trend_change_7d, opportunity_score, badges


def _generate_demo_flights(
    *,
    fly_from: str,
    fly_to: str,
    date_from_obj: datetime,
    date_to_obj: datetime,
    max_price: Optional[float],
    trip_type: str,
    nights_min: int,
    nights_max: int,
    adults: int,
    limit: int,
) -> list[dict]:
    """Generate curated demo fares when live Kiwi data is unavailable."""
    window_days = max((date_to_obj - date_from_obj).days, 0)
    rng = random.Random(
        f"{fly_from}:{fly_to}:{date_from_obj.date()}:{date_to_obj.date()}:{max_price}:{trip_type}:{adults}:{limit}"
    )
    destinations = (
        [fly_to] * limit if fly_to != "anywhere" else _pick_demo_destinations(fly_from, max(limit, 8))
    )

    results: list[dict] = []
    for index in range(limit):
        destination = destinations[index % len(destinations)]
        domestic = is_domestic(fly_from, destination)
        departure_offset = min(window_days, (index * 3) + rng.randint(0, 3))
        departure_date = date_from_obj.date() + timedelta(days=departure_offset)
        departure_time = datetime.combine(departure_date, datetime.min.time()) + timedelta(
            hours=6 + ((index * 2) % 11),
            minutes=rng.choice([0, 20, 35, 50]),
        )

        airline = DEMO_AIRLINES[index % len(DEMO_AIRLINES)]
        duration_minutes = (
            95 + (index * 18) + rng.randint(0, 35)
            if domestic
            else 540 + (index * 27) + rng.randint(0, 80)
        )
        base_price = (
            220 + (index * 48) + rng.randint(0, 55)
            if domestic
            else 1480 + (index * 125) + rng.randint(0, 120)
        )
        if max_price is not None:
            softness = 0.74 + (index * 0.03)
            capped_target = max(max_price * min(softness, 0.92), 129 if domestic else 699)
            price = round(min(base_price, capped_target), 2)
        else:
            price = float(base_price)

        if trip_type == "roundtrip":
            stay_length = max(nights_min, 3)
            stay_length = min(stay_length + (index % max(nights_max - nights_min + 1, 1)), nights_max)
            return_at = (departure_time + timedelta(days=stay_length, hours=2)).isoformat()
        else:
            return_at = None

        market_search = _build_market_search_link(fly_from, destination, departure_date)
        results.append(
            {
                "origin": fly_from,
                "destination": destination,
                "price": price,
                "currency": "BRL",
                "airline": airline["name"],
                "airline_iata": airline["iata"],
                "departure_at": departure_time.isoformat(),
                "return_at": return_at,
                "duration_minutes": duration_minutes,
                "stops": 0 if domestic else index % 2,
                "booking_url": market_search,
                "deep_link": "",
                "deeplink_url": "",
                "booking_source": "google_flights",
                "provider_name": airline["iata"],
                "provider_code": airline["iata"],
                "provider_itinerary_id": f"demo-{fly_from}-{destination}-{departure_date.isoformat()}-{index}",
                "booking_token": None,
                "fare_token": None,
            }
        )

    return results


@router.get("/airports", response_model=list[AirportOptionResponse])
async def list_airports() -> list[AirportOptionResponse]:
    """Expose airport options for search UIs."""
    airports = sorted(get_all_airports(), key=lambda item: (item["country"], item["city"]))
    return [AirportOptionResponse(**airport) for airport in airports]


@router.get("/deals", response_model=SearchDealsResponse)
async def search_deals(
    fly_from: str = Query(..., description="Origin IATA code (e.g., GRU)"),
    fly_to: str = Query("anywhere", description="Destination IATA code or 'anywhere'"),
    date_from: str = Query(None, description="Start date in YYYY-MM-DD format"),
    date_to: str = Query(None, description="End date in YYYY-MM-DD format"),
    max_price: Optional[float] = Query(None, description="Max price filter"),
    trip_type: str = Query("oneway", description="Trip type: oneway or roundtrip"),
    nights_min: int = Query(3, description="Min nights at destination"),
    nights_max: int = Query(14, description="Max nights at destination"),
    adults: int = Query(1, description="Number of adults"),
    airline: Optional[str] = Query(None, description="Airline IATA code or partial airline name"),
    limit: int = Query(20, ge=1, le=50, description="Result limit"),
    db: AsyncSession = Depends(get_db),
) -> SearchDealsResponse:
    """Search for flight deals and enrich them with intelligence signals."""
    try:
        fly_from = normalize_airport_code(fly_from)
        fly_to = "anywhere" if fly_to.lower().strip() == "anywhere" else normalize_airport_code(fly_to)
        airline_filter = airline.upper().strip() if airline else None
        trip_type = trip_type.lower().strip()

        if trip_type not in {"oneway", "roundtrip"}:
            raise HTTPException(status_code=400, detail="trip_type must be 'oneway' or 'roundtrip'")
        if not fly_from:
            raise HTTPException(status_code=400, detail="fly_from is required")

        if not date_from:
            date_from = datetime.now().strftime("%Y-%m-%d")
        if not date_to:
            date_to = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")

        date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
        date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
        if date_to_obj < date_from_obj:
            raise HTTPException(status_code=400, detail="date_to must be on or after date_from")

        kiwi_departure_end = date_to_obj
        return_date_for_link: Optional[date] = None
        kiwi_nights_min = 0
        kiwi_nights_max = 0

        if trip_type == "roundtrip":
            return_date_for_link = date_to_obj.date()
            exact_nights = max((return_date_for_link - date_from_obj.date()).days, 1)
            kiwi_departure_end = date_from_obj
            kiwi_nights_min = exact_nights
            kiwi_nights_max = exact_nights

        date_from_kiwi = date_from_obj.strftime("%d/%m/%Y")
        date_to_kiwi = kiwi_departure_end.strftime("%d/%m/%Y")

        flights: list[dict] = []
        source = "kiwi.com"
        confidence_note = (
            "Live results come from Kiwi metasearch. When a booking token is present, the primary "
            "CTA opens the exact Kiwi itinerary. Otherwise the API falls back to a confirmed airline "
            "search link or Google Flights with route and date context preserved."
        )

        if settings.kiwi_enabled:
            scraper = KiwiScraper()
            if fly_to == "anywhere":
                flights = await scraper.search_anywhere(
                    fly_from=fly_from,
                    date_from=date_from_kiwi,
                    date_to=date_to_kiwi,
                    max_price=max_price,
                    adults=adults,
                    nights_in_dst_from=kiwi_nights_min,
                    nights_in_dst_to=kiwi_nights_max,
                    limit=limit,
                )
            else:
                flights = await scraper.search_route(
                    fly_from=fly_from,
                    fly_to=fly_to,
                    date_from=date_from_kiwi,
                    date_to=date_to_kiwi,
                    nights_in_dst_from=kiwi_nights_min,
                    nights_in_dst_to=kiwi_nights_max,
                    adults=adults,
                    limit=limit,
                )

        if airline_filter:
            flights = [
                flight
                for flight in flights
                if airline_filter in (flight.get("airline_iata") or "").upper()
                or airline_filter in (flight.get("airline") or "").upper()
            ]

        if not flights and settings.demo_mode:
            flights = _generate_demo_flights(
                fly_from=fly_from,
                fly_to=fly_to,
                date_from_obj=date_from_obj,
                date_to_obj=date_to_obj,
                max_price=max_price,
                trip_type=trip_type,
                nights_min=nights_min,
                nights_max=nights_max,
                adults=adults,
                limit=limit,
            )
            source = "demo-curated"
            confidence_note = (
                "Curated demo fares are shown because live Kiwi data is unavailable. Booking links "
                "still preserve route and date context through direct airline links when possible, "
                "otherwise Google Flights."
            )

        enriched_deals: list[DealResponse] = []
        for index, flight in enumerate(flights[:limit]):
            origin = flight.get("origin", "")
            destination = flight.get("destination", "")
            origin_info = get_airport_info(origin)
            destination_info = get_airport_info(destination)
            route_is_domestic = is_domestic(origin, destination)
            threshold = (
                settings.default_threshold_domestic
                if route_is_domestic
                else settings.default_threshold_intl
            )
            price = float(flight.get("price", 0))
            airline_iata = (flight.get("airline_iata") or "").upper()
            airline_name = AIRLINE_BOOKING_URLS.get(
                airline_iata,
                (flight.get("airline", "Airline"), ""),
            )[0]
            airline_logo_url = (
                f"https://cdn.kiwi.com/airlines/128/{airline_iata}.png" if airline_iata else ""
            )

            departure_iso = flight.get("departure_at", "")
            try:
                departure_date = datetime.fromisoformat(departure_iso.replace("Z", "+00:00")).date()
            except Exception:
                departure_date = date_from_obj.date()
            try:
                parsed_return_date = (
                    datetime.fromisoformat(str(flight.get("return_at")).replace("Z", "+00:00")).date()
                    if flight.get("return_at")
                    else None
                )
            except Exception:
                parsed_return_date = return_date_for_link

            history, historical_avg_price, historical_low_price = await _load_route_history(
                db,
                origin,
                destination,
                price,
                seed_key=f"{origin}:{destination}:{departure_iso}:{index}",
            )
            distance_miles = _haversine_miles(origin, destination)
            cpm = round(price / distance_miles, 3) if distance_miles else None

            is_deal, deal_badge, savings_percent, trend_change_7d, opportunity_score, badges = (
                _compute_intelligence(
                    price=price,
                    threshold=threshold,
                    history=history,
                    historical_avg_price=historical_avg_price,
                    historical_low_price=historical_low_price,
                    cpm=cpm,
                )
            )

            (
                deeplink_url,
                booking_source,
                provider_name,
                official_airline_url,
                official_airline_label,
                secondary_url,
                secondary_label,
                deeplink_tier,
            ) = _build_purchase_links(
                flight=flight,
                departure_date=departure_date,
                return_date=parsed_return_date,
                adults=adults,
            )
            if booking_source == "kiwi":
                booking_source_label = "via kiwi.com"
            elif booking_source == "direct_airline":
                booking_source_label = f"direct: {provider_name}"
            elif booking_source == "google_flights":
                booking_source_label = "via Google Flights"
            else:
                booking_source_label = f"airline: {provider_name}"
            fare_last_seen_at = datetime.now().isoformat()
            booking_token = flight.get("booking_token") or flight.get("fare_token")

            enriched_deals.append(
                DealResponse(
                    origin=origin,
                    destination=destination,
                    origin_city=origin_info.get("city", ""),
                    origin_country=origin_info.get("country", ""),
                    destination_city=destination_info.get("city", ""),
                    destination_country=destination_info.get("country", ""),
                    price=price,
                    currency=flight.get("currency", "BRL"),
                    airline=airline_name,
                    airline_iata=airline_iata,
                    airline_logo_url=airline_logo_url,
                    departure_at=departure_iso,
                    return_at=flight.get("return_at"),
                    duration_minutes=int(flight.get("duration_minutes", 0)),
                    stops=int(flight.get("stops", 0)),
                    booking_token=booking_token,
                    deeplink_url=deeplink_url,
                    booking_source=booking_source,
                    booking_source_label=booking_source_label,
                    provider_code=airline_iata or str(flight.get("provider_code") or ""),
                    booking_url=deeplink_url,
                    deep_link=flight.get("deep_link", "") or deeplink_url,
                    provider_name=provider_name,
                    booking_source_type=booking_source,
                    deeplink_tier=deeplink_tier,
                    provider_itinerary_id=flight.get("provider_itinerary_id"),
                    fare_token=booking_token,
                    fare_last_seen_at=fare_last_seen_at,
                    purchase_url=deeplink_url,
                    purchase_label="Book Now →",
                    secondary_purchase_url=secondary_url,
                    secondary_purchase_label=secondary_label,
                    official_airline_url=official_airline_url,
                    official_airline_label=official_airline_label,
                    historical_avg_price=historical_avg_price,
                    historical_low_price=historical_low_price,
                    savings_percent=savings_percent,
                    trend_change_7d=trend_change_7d,
                    price_history_7d=history,
                    opportunity_score=opportunity_score,
                    opportunity_badges=badges,
                    distance_miles=distance_miles,
                    cpm=cpm,
                    is_deal=is_deal,
                    deal_badge=deal_badge,
                )
            )

        total_scanned_stmt = select(func.count()).select_from(PriceSnapshot).where(
            PriceSnapshot.captured_at >= datetime.utcnow() - timedelta(hours=24)
        )
        alerts_stmt = select(func.count()).select_from(UserAlert).where(UserAlert.is_active.is_(True))
        total_scanned_result = await db.execute(total_scanned_stmt)
        alerts_result = await db.execute(alerts_stmt)

        average_cpm = None
        cpm_values = [deal.cpm for deal in enriched_deals if deal.cpm]
        if cpm_values:
            average_cpm = round(mean(cpm_values), 3)

        top_saving = max((deal.savings_percent for deal in enriched_deals), default=0.0)
        actionable_count = sum(1 for deal in enriched_deals if deal.deeplink_tier <= 2)
        actionable_link_rate = round((actionable_count / len(enriched_deals)) * 100, 1) if enriched_deals else 0.0

        return SearchDealsResponse(
            results=enriched_deals,
            total=len(enriched_deals),
            search_meta=SearchMetaResponse(
                fly_from=fly_from,
                fly_to=fly_to if fly_to != "anywhere" else "Anywhere",
                searched_at=datetime.now().isoformat(),
                source=source,
                actionable_link_rate=actionable_link_rate,
                source_confidence_note=confidence_note,
            ),
            kpis=SearchKpisResponse(
                total_scanned_24h=int(total_scanned_result.scalar() or 0),
                active_alerts=int(alerts_result.scalar() or 0),
                average_cpm=average_cpm,
                top_saving_percent=round(top_saving, 1),
            ),
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Search error: %s", exc, exc_info=True)
        return SearchDealsResponse(
            results=[],
            total=0,
            search_meta=SearchMetaResponse(
                fly_from=fly_from,
                fly_to=fly_to,
                searched_at=datetime.now().isoformat(),
                source="kiwi.com",
                actionable_link_rate=0.0,
                source_confidence_note="Search failed before fare enrichment completed.",
            ),
            kpis=SearchKpisResponse(
                total_scanned_24h=0,
                active_alerts=0,
                average_cpm=None,
                top_saving_percent=0.0,
            ),
        )


class PreviewMatchRequest(BaseModel):
    """Request to preview deal matches."""

    user_id: str
    deals: list[DealResponse]


@router.post("/preview-match", response_model=MatchPreviewResponse)
async def preview_match(
    request: PreviewMatchRequest,
    db: AsyncSession = Depends(get_db),
) -> MatchPreviewResponse:
    """Preview which deals match a user's active alerts."""
    try:
        stmt = select(User).where(User.id == request.user_id)
        user_result = await db.execute(stmt)
        user = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        stmt = select(UserAlert).where(
            (UserAlert.user_id == request.user_id) & (UserAlert.is_active.is_(True))
        )
        alerts_result = await db.execute(stmt)
        alerts = list(alerts_result.scalars().all())

        matched_deals = []
        matched_alerts_map = {}
        for deal in request.deals:
            try:
                deal_date = datetime.fromisoformat(deal.departure_at.replace("Z", "+00:00")).date()
            except Exception:
                deal_date = date.today()

            for alert in alerts:
                origin_match = alert.origin_iata is None or alert.origin_iata == deal.origin
                dest_match = alert.destination_iata is None or alert.destination_iata == deal.destination
                price_match = deal.price <= alert.max_price
                date_match = (
                    (alert.date_from is None or deal_date >= alert.date_from)
                    and (alert.date_to is None or deal_date <= alert.date_to)
                )

                if origin_match and dest_match and price_match and date_match:
                    matched_deals.append(deal)
                    if alert.id not in matched_alerts_map:
                        matched_alerts_map[alert.id] = {"alert": alert, "count": 0}
                    matched_alerts_map[alert.id]["count"] += 1
                    break

        matched_alerts = [
            MatchedAlert(
                id=data["alert"].id,
                origin_iata=data["alert"].origin_iata,
                destination_iata=data["alert"].destination_iata,
                date_from=data["alert"].date_from,
                date_to=data["alert"].date_to,
                max_price=data["alert"].max_price,
                matched_deal_count=data["count"],
            )
            for data in matched_alerts_map.values()
        ]

        return MatchPreviewResponse(
            user={"id": user.id, "name": user.name or "User", "plan": user.plan},
            matched_deals=matched_deals,
            matched_alerts=matched_alerts,
            unmatched_count=len(request.deals) - len(matched_deals),
            active_alerts=len(alerts),
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Match preview error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
