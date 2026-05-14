"""Airport database with IATA codes, cities, and country information"""

from typing import Dict

AIRPORTS: Dict[str, Dict[str, str]] = {
    # Brazilian Airports
    "GRU": {"city": "São Paulo", "country": "Brazil", "flag": "🇧🇷"},
    "GIG": {"city": "Rio de Janeiro", "country": "Brazil", "flag": "🇧🇷"},
    "CGH": {"city": "São Paulo (Congonhas)", "country": "Brazil", "flag": "🇧🇷"},
    "CNF": {"city": "Belo Horizonte", "country": "Brazil", "flag": "🇧🇷"},
    "SSA": {"city": "Salvador", "country": "Brazil", "flag": "🇧🇷"},
    "REC": {"city": "Recife", "country": "Brazil", "flag": "🇧🇷"},
    "FOR": {"city": "Fortaleza", "country": "Brazil", "flag": "🇧🇷"},
    "BSB": {"city": "Brasília", "country": "Brazil", "flag": "🇧🇷"},
    "FLN": {"city": "Florianópolis", "country": "Brazil", "flag": "🇧🇷"},
    "POA": {"city": "Porto Alegre", "country": "Brazil", "flag": "🇧🇷"},
    "CWB": {"city": "Curitiba", "country": "Brazil", "flag": "🇧🇷"},
    "VCP": {"city": "Campinas", "country": "Brazil", "flag": "🇧🇷"},
    "SDU": {"city": "Rio de Janeiro (Santos Dumont)", "country": "Brazil", "flag": "🇧🇷"},
    "MCZ": {"city": "Maceió", "country": "Brazil", "flag": "🇧🇷"},
    "NAT": {"city": "Natal", "country": "Brazil", "flag": "🇧🇷"},
    "JPA": {"city": "João Pessoa", "country": "Brazil", "flag": "🇧🇷"},
    "AJU": {"city": "Aracaju", "country": "Brazil", "flag": "🇧🇷"},
    "BEL": {"city": "Belém", "country": "Brazil", "flag": "🇧🇷"},
    "MAO": {"city": "Manaus", "country": "Brazil", "flag": "🇧🇷"},
    "CGB": {"city": "Cuiabá", "country": "Brazil", "flag": "🇧🇷"},
    "GYN": {"city": "Goiânia", "country": "Brazil", "flag": "🇧🇷"},
    "THE": {"city": "Teresina", "country": "Brazil", "flag": "🇧🇷"},
    "SLZ": {"city": "São Luís", "country": "Brazil", "flag": "🇧🇷"},
    "IMP": {"city": "Imperatriz", "country": "Brazil", "flag": "🇧🇷"},
    "PVH": {"city": "Porto Velho", "country": "Brazil", "flag": "🇧🇷"},
    "CGR": {"city": "Campo Grande", "country": "Brazil", "flag": "🇧🇷"},
    "UDI": {"city": "Uberlândia", "country": "Brazil", "flag": "🇧🇷"},
    "RAO": {"city": "Ribeirão Preto", "country": "Brazil", "flag": "🇧🇷"},
    "LDB": {"city": "Londrina", "country": "Brazil", "flag": "🇧🇷"},
    
    # International Airports
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
    "BOG": {"city": "Bogotá", "country": "Colombia", "flag": "🇨🇴"},
    "LIM": {"city": "Lima", "country": "Peru", "flag": "🇵🇪"},
    "CUN": {"city": "Cancún", "country": "Mexico", "flag": "🇲🇽"},
    "PTY": {"city": "Panama City", "country": "Panama", "flag": "🇵🇦"},
    
    "DXB": {"city": "Dubai", "country": "United Arab Emirates", "flag": "🇦🇪"},
    "DOH": {"city": "Doha", "country": "Qatar", "flag": "🇶🇦"},
    "SYD": {"city": "Sydney", "country": "Australia", "flag": "🇦🇺"},
    "NRT": {"city": "Tokyo", "country": "Japan", "flag": "🇯🇵"},
    "SIN": {"city": "Singapore", "country": "Singapore", "flag": "🇸🇬"},
    "BKK": {"city": "Bangkok", "country": "Thailand", "flag": "🇹🇭"},
    "HND": {"city": "Tokyo (Haneda)", "country": "Japan", "flag": "🇯🇵"},
}

BRAZILIAN_AIRPORTS = {code for code, info in AIRPORTS.items() if info["country"] == "Brazil"}


def is_domestic(origin: str, destination: str) -> bool:
    """
    Check if a flight route is domestic (both airports in Brazil).
    
    Args:
        origin: Origin IATA code
        destination: Destination IATA code
    
    Returns:
        True if both airports are in Brazil, False otherwise
    """
    return origin in BRAZILIAN_AIRPORTS and destination in BRAZILIAN_AIRPORTS


def get_airport_info(iata: str) -> dict:
    """
    Get airport information by IATA code.
    
    Args:
        iata: IATA code
    
    Returns:
        Airport info dict or default dict if not found
    """
    return AIRPORTS.get(
        iata,
        {"city": "Unknown", "country": "Unknown", "flag": "🌍"}
    )


def get_brazilian_airports() -> list[dict]:
    """Get list of Brazilian airports with their info"""
    return [
        {"code": code, **info}
        for code, info in AIRPORTS.items()
        if code in BRAZILIAN_AIRPORTS
    ]


def get_all_airports() -> list[dict]:
    """Get list of all airports with their info"""
    return [
        {"code": code, **info}
        for code, info in AIRPORTS.items()
    ]
