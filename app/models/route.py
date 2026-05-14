"""Route model - monitored flight routes"""

from sqlalchemy import Column, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from datetime import datetime

from app.models.base import Base


class Route(Base):
    """
    Represents a flight route to monitor for price deals.
    
    Attributes:
        id: Primary key
        origin_iata: Origin airport IATA code (e.g., "GRU")
        destination_iata: Destination airport IATA code (e.g., "MIA")
        threshold_price: Price threshold in BRL - deal triggered if price <= threshold
        is_active: Whether this route is actively monitored
        created_at: Timestamp when route was added
        updated_at: Timestamp of last update
    """
    
    __tablename__ = "routes"
    
    id = Column(String, primary_key=True, index=True)
    origin_iata = Column(String(3), nullable=False, index=True)
    destination_iata = Column(String(3), nullable=False, index=True)
    threshold_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Route {self.origin_iata}-{self.destination_iata} R${self.threshold_price}>"
