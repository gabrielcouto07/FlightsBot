"""UserAlert model - paid user flight alerts"""

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from datetime import datetime, date

from app.models.base import Base


class UserAlert(Base):
    """
    Represents a personalized flight alert for paid users.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        origin_iata: Origin airport IATA code (or NULL for any)
        destination_iata: Destination airport IATA code (or NULL for any)
        date_from: Search start date
        date_to: Search end date
        max_price: Maximum acceptable price in BRL
        is_active: Whether the alert is active
        created_at: Timestamp when alert was created
        updated_at: Timestamp of last update
    """
    
    __tablename__ = "user_alerts"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    origin_iata = Column(String(3), nullable=True, index=True)  # NULL = any
    destination_iata = Column(String(3), nullable=True, index=True)  # NULL = any
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    max_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        origin = self.origin_iata or "ANY"
        dest = self.destination_iata or "ANY"
        return f"<UserAlert {origin}-{dest} R${self.max_price}>"
