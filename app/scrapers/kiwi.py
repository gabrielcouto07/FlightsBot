"""Kiwi.com Tequila API scraper implementation."""

import logging
import asyncio
from typing import Optional
from urllib.parse import urlencode
import httpx

from app.scrapers.base import BaseScraper
from app.config import get_settings

logger = logging.getLogger(__name__)


class KiwiScraper(BaseScraper):
    """
    Scraper for Kiwi.com Tequila API.
    Searches across 750+ airlines globally for the best flight prices.
    """
    
    def __init__(self):
        """Initialize Kiwi scraper with API credentials"""
        self.settings = get_settings()
        self.base_url = self.settings.kiwi_api_base
        self.api_key = self.settings.kiwi_api_key
        self.timeout = self.settings.kiwi_request_timeout

    @staticmethod
    def _build_kiwi_deeplink(
        *,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str],
        adults: int,
        booking_token: Optional[str],
        fallback_url: str,
    ) -> str:
        """Build the strongest Kiwi itinerary link available."""
        if not booking_token or not origin or not destination or not departure_date:
            return fallback_url

        params = {
            "from": origin,
            "to": destination,
            "departure": departure_date.replace("-", ""),
            "adults": max(adults, 1),
            "token": booking_token,
        }
        if return_date:
            params["return"] = return_date.replace("-", "")

        return f"https://www.kiwi.com/deep?{urlencode(params)}"
    
    async def _request(self, endpoint: str, params: dict) -> dict:
        """
        Make async request to Kiwi API with error handling and retries.
        
        Args:
            endpoint: API endpoint (e.g., "/v2/search")
            params: Query parameters
        
        Returns:
            Response JSON as dictionary
        
        Raises:
            Exception: On API errors or network issues
        """
        if not self.api_key:
            logger.warning("Kiwi API key is not configured; skipping request")
            return {}

        url = f"{self.base_url}{endpoint}"
        headers = {"apikey": self.api_key}
        
        max_retries = 3
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, params=params, headers=headers)
                    
                    # Handle rate limiting
                    if response.status_code == 429:
                        delay = base_delay * (2 ** attempt)
                        logger.warning(f"Rate limited. Retrying in {delay}s (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(delay)
                        continue
                    
                    response.raise_for_status()
                    return response.json()
            
            except httpx.TimeoutException:
                logger.error(f"Timeout on attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(base_delay * (2 ** attempt))
                    continue
                raise
            
            except httpx.HTTPError as e:
                logger.error(f"HTTP error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(base_delay * (2 ** attempt))
                    continue
                raise
        
        raise Exception(f"Failed after {max_retries} attempts")
    
    def _normalize_flight(self, result: dict, adults: int) -> dict:
        """
        Normalize a flight result from Kiwi API to standard format.
        
        Args:
            result: Raw flight data from Kiwi API
        
        Returns:
            Normalized flight dictionary
        """
        route = result.get("route", [])
        duration_total = result.get("duration", {}).get("total", 0)
        departure_at = result.get("local_departure", "")
        return_at = result.get("local_return", "") if result.get("local_return") else None
        departure_date = departure_at[:10] if departure_at else ""
        return_date = return_at[:10] if return_at else None
        airline_iata = result.get("airlines", [""])[0] if result.get("airlines") else ""
        booking_token = result.get("booking_token")
        raw_deep_link = result.get("deep_link", "")
        deeplink_url = self._build_kiwi_deeplink(
            origin=result.get("flyFrom", ""),
            destination=result.get("flyTo", ""),
            departure_date=departure_date,
            return_date=return_date,
            adults=adults,
            booking_token=booking_token,
            fallback_url=raw_deep_link,
        )

        return {
            "origin": result.get("flyFrom", ""),
            "destination": result.get("flyTo", ""),
            "price": result.get("price", 0),
            "currency": result.get("currency", "BRL"),
            "airline": route[0].get("airline", "Unknown") if route else "Unknown",
            "airline_iata": airline_iata or None,
            "departure_at": departure_at,
            "return_at": return_at,
            "duration_minutes": int(duration_total / 60) if duration_total else 0,
            "stops": max(len(route) - 1, 0),
            "booking_url": deeplink_url,
            "deep_link": raw_deep_link,
            "deeplink_url": deeplink_url,
            "booking_source": "kiwi",
            "provider_name": airline_iata or "Unknown",
            "provider_code": airline_iata or "Unknown",
            "provider_itinerary_id": result.get("id"),
            "booking_token": booking_token,
            "fare_token": booking_token,
        }
    
    async def search_route(
        self,
        fly_from: str,
        fly_to: str,
        date_from: str,
        date_to: str,
        nights_in_dst_from: int = 1,
        nights_in_dst_to: int = 30,
        adults: int = 1,
        currency: str = "BRL",
        limit: int = 10,
        sort: str = "price",
    ) -> list[dict]:
        """
        Search for flights on a specific route via Kiwi.com.
        
        Uses the search endpoint to find the cheapest flights between two airports.
        """
        params = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "adults": adults,
            "curr": currency,
            "limit": limit,
            "sort": sort,
            "vehicle_type": "aircraft",
        }
        if nights_in_dst_from > 0 and nights_in_dst_to > 0:
            params["flight_type"] = "round"
            params["nights_in_dst_from"] = nights_in_dst_from
            params["nights_in_dst_to"] = nights_in_dst_to
        else:
            params["flight_type"] = "oneway"
        
        try:
            logger.info(f"Searching route {fly_from}->{fly_to} from {date_from} to {date_to}")
            response = await self._request("/v2/search", params)
            
            flights = []
            for result in response.get("data", []):
                try:
                    flight = self._normalize_flight(result, adults)
                    flights.append(flight)
                except Exception as e:
                    logger.warning(f"Failed to normalize flight: {e}")
                    continue
            
            logger.info(f"Found {len(flights)} flights for {fly_from}->{fly_to}")
            return flights
        
        except Exception as e:
            logger.error(f"Error searching route {fly_from}->{fly_to}: {e}")
            return []
    
    async def search_anywhere(
        self,
        fly_from: str,
        date_from: str,
        date_to: str,
        max_price: Optional[float] = None,
        adults: int = 1,
        nights_in_dst_from: int = 0,
        nights_in_dst_to: int = 0,
        currency: str = "BRL",
        limit: int = 20,
    ) -> list[dict]:
        """
        Search for "fly anywhere" deals from a given origin.
        
        Returns the cheapest flights to various destinations from the origin.
        """
        params = {
            "fly_from": fly_from,
            "fly_to": "anywhere",
            "date_from": date_from,
            "date_to": date_to,
            "adults": adults,
            "curr": currency,
            "limit": limit,
            "sort": "price",
            "vehicle_type": "aircraft",
        }
        if nights_in_dst_from > 0 and nights_in_dst_to > 0:
            params["flight_type"] = "round"
            params["nights_in_dst_from"] = nights_in_dst_from
            params["nights_in_dst_to"] = nights_in_dst_to
        else:
            params["flight_type"] = "oneway"
        
        if max_price:
            params["max_price"] = max_price
        
        try:
            logger.info(f"Searching anywhere deals from {fly_from}")
            response = await self._request("/v2/search", params)
            
            flights = []
            for result in response.get("data", []):
                try:
                    flight = self._normalize_flight(result, adults)
                    flights.append(flight)
                except Exception as e:
                    logger.warning(f"Failed to normalize anywhere flight: {e}")
                    continue
            
            logger.info(f"Found {len(flights)} anywhere deals from {fly_from}")
            return flights
        
        except Exception as e:
            logger.error(f"Error searching anywhere deals from {fly_from}: {e}")
            return []
    
    async def search_calendar(
        self,
        fly_from: str,
        fly_to: str,
        date_from: str,
        date_to: str,
        currency: str = "BRL",
    ) -> dict:
        """
        Search for cheapest flights across a date range using calendar endpoint.
        
        Returns a grid of prices for different departure and return dates.
        """
        params = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "adults": 1,
            "curr": currency,
            "sort": "price",
            "vehicle_type": "aircraft",
        }
        
        try:
            logger.info(f"Searching calendar for {fly_from}->{fly_to}")
            response = await self._request("/v2/search", params)
            
            # Extract and organize price data by date
            calendar_data = {}
            for result in response.get("data", []):
                dep_date = result.get("local_departure", "")[:10]
                price = result.get("price", 0)
                
                if dep_date not in calendar_data or price < calendar_data[dep_date]:
                    calendar_data[dep_date] = price
            
            logger.info(f"Found {len(calendar_data)} dates with prices")
            return calendar_data
        
        except Exception as e:
            logger.error(f"Error searching calendar for {fly_from}->{fly_to}: {e}")
            return {}
