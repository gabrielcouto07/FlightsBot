"""Abstract base scraper class"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseScraper(ABC):
    """
    Abstract base class for flight scrapers.
    Defines the interface that all scrapers must implement.
    """
    
    @abstractmethod
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
        Search for flights on a specific route.
        
        Args:
            fly_from: Origin IATA code (e.g., "GRU")
            fly_to: Destination IATA code (e.g., "MIA") or "anywhere"
            date_from: Start date in "dd/mm/yyyy" format
            date_to: End date in "dd/mm/yyyy" format
            nights_in_dst_from: Minimum nights at destination
            nights_in_dst_to: Maximum nights at destination
            adults: Number of adult passengers
            currency: Currency code (default "BRL")
            limit: Maximum number of results
            sort: Sort by "price", "duration", or "date"
        
        Returns:
            List of flight dictionaries with normalized keys
        """
        pass
    
    @abstractmethod
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
        
        Args:
            fly_from: Origin IATA code
            date_from: Start date in "dd/mm/yyyy" format
            date_to: End date in "dd/mm/yyyy" format
            max_price: Maximum price filter (optional)
            currency: Currency code (default "BRL")
            limit: Maximum number of results
        
        Returns:
            List of flight dictionaries
        """
        pass
    
    @abstractmethod
    async def search_calendar(
        self,
        fly_from: str,
        fly_to: str,
        date_from: str,
        date_to: str,
        currency: str = "BRL",
    ) -> dict:
        """
        Search for cheapest flights across a date range (calendar view).
        
        Args:
            fly_from: Origin IATA code
            fly_to: Destination IATA code
            date_from: Start date in "dd/mm/yyyy" format
            date_to: End date in "dd/mm/yyyy" format
            currency: Currency code (default "BRL")
        
        Returns:
            Dictionary with prices per date
        """
        pass
