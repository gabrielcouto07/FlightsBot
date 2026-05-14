"""PriceSnapshot model - captured flight prices"""

from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.sql import func
from datetime import datetime

from app.models.base import Base


class PriceSnapshot(Base):
    """
    Represents a captured flight price snapshot from Kiwi.com.
    Used to detect deals and track price history.
    
    Attributes:
        id: Primary key
        origin: Origin airport IATA code
        destination: Destination airport IATA code
        price: Price in BRL
        currency: Currency code (default "BRL")
        airline: Airline name
        airline_iata: Airline IATA code
        departure_at: Departure datetime (ISO format)
        return_at: Return datetime (ISO format, nullable for one-way)
        duration_minutes: Total flight duration
        booking_url: Direct booking URL from Kiwi.com
        deep_link: Deep link for affiliate tracking
        captured_at: When the price was captured
    """
    
    __tablename__ = "price_snapshots"
    
    id = Column(String, primary_key=True, index=True)
    origin = Column(String(3), nullable=False, index=True)
    destination = Column(String(3), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    currency = Column(String(3), default="BRL")
    airline = Column(String(255), nullable=False)
    airline_iata = Column(String(2), nullable=True, index=True)
    departure_at = Column(DateTime, nullable=False, index=True)
    return_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    booking_url = Column(String(512), nullable=False)
    deep_link = Column(String(512), nullable=False)
    captured_at = Column(DateTime, server_default=func.now(), index=True)
    
    def __repr__(self) -> str:
        return f"<PriceSnapshot {self.origin}-{self.destination} R${self.price}>"
