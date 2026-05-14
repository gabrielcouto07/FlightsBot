"""Kiwi.com Tequila API scraper implementation"""

import logging
import asyncio
from typing import Optional
from datetime import datetime
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
        url = f"{self.base_url}{endpoint}"
        params["apikey"] = self.api_key
        
        max_retries = 3
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, params=params)
                    
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
    
    def _normalize_flight(self, result: dict) -> dict:
        """
        Normalize a flight result from Kiwi API to standard format.
        
        Args:
            result: Raw flight data from Kiwi API
        
        Returns:
            Normalized flight dictionary
        """
        # Extract route info
        route = result.get("route", [{}])[0]
        
        return {
            "origin": result.get("flyFrom", ""),
            "destination": result.get("flyTo", ""),
            "price": result.get("price", 0),
            "currency": result.get("currency", "BRL"),
            "airline": result.get("airlines", ["Unknown"])[0] if result.get("airlines") else "Unknown",
            "airline_iata": result.get("airlines", [""])[0] if result.get("airlines") else None,
            "departure_at": result.get("local_departure", ""),
            "return_at": result.get("local_return", "") if result.get("local_return") else None,
            "duration_minutes": result.get("duration", {}).get("total", 0),
            "booking_url": result.get("deep_link", ""),
            "deep_link": result.get("deep_link", ""),
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
            "nights_in_dst_from": nights_in_dst_from,
            "nights_in_dst_to": nights_in_dst_to,
            "adults": adults,
            "curr": currency,
            "limit": limit,
            "sort": sort,
            "vehicle_type": "aircraft",
        }
        
        try:
            logger.info(f"Searching route {fly_from}->{fly_to} from {date_from} to {date_to}")
            response = await self._request("/v2/search", params)
            
            flights = []
            for result in response.get("data", []):
                try:
                    flight = self._normalize_flight(result)
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
            "adults": 1,
            "curr": currency,
            "limit": limit,
            "sort": "price",
            "vehicle_type": "aircraft",
        }
        
        if max_price:
            params["max_price"] = max_price
        
        try:
            logger.info(f"Searching anywhere deals from {fly_from}")
            response = await self._request("/v2/search", params)
            
            flights = []
            for result in response.get("data", []):
                try:
                    flight = self._normalize_flight(result)
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
