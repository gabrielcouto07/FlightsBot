"""Airport lookup helpers used by search and UI endpoints."""

from __future__ import annotations

from typing import Dict

AirportInfo = Dict[str, str]

AIRPORTS: Dict[str, AirportInfo] = {
    "GRU": {"city": "Sao Paulo", "country": "Brazil", "flag": "🇧🇷"},
    "GIG": {"city": "Rio de Janeiro", "country": "Brazil", "flag": "🇧🇷"},
    "CGH": {"city": "Sao Paulo (Congonhas)", "country": "Brazil", "flag": "🇧🇷"},
    "CNF": {"city": "Belo Horizonte", "country": "Brazil", "flag": "🇧🇷"},
    "SSA": {"city": "Salvador", "country": "Brazil", "flag": "🇧🇷"},
    "REC": {"city": "Recife", "country": "Brazil", "flag": "🇧🇷"},
    "FOR": {"city": "Fortaleza", "country": "Brazil", "flag": "🇧🇷"},
    "BSB": {"city": "Brasilia", "country": "Brazil", "flag": "🇧🇷"},
    "FLN": {"city": "Florianopolis", "country": "Brazil", "flag": "🇧🇷"},
    "POA": {"city": "Porto Alegre", "country": "Brazil", "flag": "🇧🇷"},
    "CWB": {"city": "Curitiba", "country": "Brazil", "flag": "🇧🇷"},
    "VCP": {"city": "Campinas", "country": "Brazil", "flag": "🇧🇷"},
    "SDU": {"city": "Rio de Janeiro (Santos Dumont)", "country": "Brazil", "flag": "🇧🇷"},
    "MCZ": {"city": "Maceio", "country": "Brazil", "flag": "🇧🇷"},
    "NAT": {"city": "Natal", "country": "Brazil", "flag": "🇧🇷"},
    "JPA": {"city": "Joao Pessoa", "country": "Brazil", "flag": "🇧🇷"},
    "AJU": {"city": "Aracaju", "country": "Brazil", "flag": "🇧🇷"},
    "BEL": {"city": "Belem", "country": "Brazil", "flag": "🇧🇷"},
    "MAO": {"city": "Manaus", "country": "Brazil", "flag": "🇧🇷"},
    "CGB": {"city": "Cuiaba", "country": "Brazil", "flag": "🇧🇷"},
    "GYN": {"city": "Goiania", "country": "Brazil", "flag": "🇧🇷"},
    "THE": {"city": "Teresina", "country": "Brazil", "flag": "🇧🇷"},
    "SLZ": {"city": "Sao Luis", "country": "Brazil", "flag": "🇧🇷"},
    "IMP": {"city": "Imperatriz", "country": "Brazil", "flag": "🇧🇷"},
    "PVH": {"city": "Porto Velho", "country": "Brazil", "flag": "🇧🇷"},
    "CGR": {"city": "Campo Grande", "country": "Brazil", "flag": "🇧🇷"},
    "UDI": {"city": "Uberlandia", "country": "Brazil", "flag": "🇧🇷"},
    "RAO": {"city": "Ribeirao Preto", "country": "Brazil", "flag": "🇧🇷"},
    "LDB": {"city": "Londrina", "country": "Brazil", "flag": "🇧🇷"},
    "MIA": {"city": "Miami", "country": "United States", "flag": "🇺🇸"},
    "JFK": {"city": "New York", "country": "United States", "flag": "🇺🇸"},
    "LAX": {"city": "Los Angeles", "country": "United States", "flag": "🇺🇸"},
    "ORD": {"city": "Chicago", "country": "United States", "flag": "🇺🇸"},
    "DEN": {"city": "Denver", "country": "United States", "flag": "🇺🇸"},
    "ATL": {"city": "Atlanta", "country": "United States", "flag": "🇺🇸"},
    "LIS": {"city": "Lisbon", "country": "Portugal", "flag": "🇵🇹"},
    "MAD": {"city": "Madrid", "country": "Spain", "flag": "🇪🇸"},
    "BCN": {"city": "Barcelona", "country": "Spain", "flag": "🇪🇸"},
    "CDG": {"city": "Paris", "country": "France", "flag": "🇫🇷"},
    "LHR": {"city": "London", "country": "United Kingdom", "flag": "🇬🇧"},
    "FRA": {"city": "Frankfurt", "country": "Germany", "flag": "🇩🇪"},
    "AMS": {"city": "Amsterdam", "country": "Netherlands", "flag": "🇳🇱"},
    "VIE": {"city": "Vienna", "country": "Austria", "flag": "🇦🇹"},
    "ZRH": {"city": "Zurich", "country": "Switzerland", "flag": "🇨🇭"},
    "FCO": {"city": "Rome", "country": "Italy", "flag": "🇮🇹"},
    "PRG": {"city": "Prague", "country": "Czech Republic", "flag": "🇨🇿"},
    "BUD": {"city": "Budapest", "country": "Hungary", "flag": "🇭🇺"},
    "WAW": {"city": "Warsaw", "country": "Poland", "flag": "🇵🇱"},
    "ORY": {"city": "Paris (Orly)", "country": "France", "flag": "🇫🇷"},
    "NCE": {"city": "Nice", "country": "France", "flag": "🇫🇷"},
    "ARN": {"city": "Stockholm", "country": "Sweden", "flag": "🇸🇪"},
    "CPH": {"city": "Copenhagen", "country": "Denmark", "flag": "🇩🇰"},
    "EZE": {"city": "Buenos Aires", "country": "Argentina", "flag": "🇦🇷"},
    "SCL": {"city": "Santiago", "country": "Chile", "flag": "🇨🇱"},
    "BOG": {"city": "Bogota", "country": "Colombia", "flag": "🇨🇴"},
    "LIM": {"city": "Lima", "country": "Peru", "flag": "🇵🇪"},
    "CUN": {"city": "Cancun", "country": "Mexico", "flag": "🇲🇽"},
    "PTY": {"city": "Panama City", "country": "Panama", "flag": "🇵🇦"},
    "DXB": {"city": "Dubai", "country": "United Arab Emirates", "flag": "🇦🇪"},
    "DOH": {"city": "Doha", "country": "Qatar", "flag": "🇶🇦"},
    "SYD": {"city": "Sydney", "country": "Australia", "flag": "🇦🇺"},
    "NRT": {"city": "Tokyo", "country": "Japan", "flag": "🇯🇵"},
    "SIN": {"city": "Singapore", "country": "Singapore", "flag": "🇸🇬"},
    "BKK": {"city": "Bangkok", "country": "Thailand", "flag": "🇹🇭"},
    "HND": {"city": "Tokyo (Haneda)", "country": "Japan", "flag": "🇯🇵"},
}

UNKNOWN_AIRPORT: AirportInfo = {
    "city": "Unknown",
    "country": "Unknown",
    "flag": "🌍",
}

BRAZILIAN_AIRPORTS = {
    code
    for code, info in AIRPORTS.items()
    if info["country"] == "Brazil"
}


def normalize_airport_code(value: str | None) -> str:
    """Normalize an airport-like value into a clean IATA code."""
    if not value:
        return ""

    normalized = value.strip().upper()
    if normalized == "ANYWHERE":
        return "ANYWHERE"

    return normalized[:3]


def is_domestic(origin: str, destination: str) -> bool:
    """Check whether both endpoints are Brazilian airports."""
    return (
        normalize_airport_code(origin) in BRAZILIAN_AIRPORTS
        and normalize_airport_code(destination) in BRAZILIAN_AIRPORTS
    )


def get_airport_info(iata: str) -> AirportInfo:
    """Return airport metadata or a safe unknown fallback."""
    return AIRPORTS.get(normalize_airport_code(iata), UNKNOWN_AIRPORT.copy())


def get_brazilian_airports() -> list[dict[str, str]]:
    """Return Brazilian airports for selector UIs."""
    return [
        {"code": code, **info}
        for code, info in AIRPORTS.items()
        if code in BRAZILIAN_AIRPORTS
    ]


def get_all_airports() -> list[dict[str, str]]:
    """Return all known airport options."""
    return [{"code": code, **info} for code, info in AIRPORTS.items()]
