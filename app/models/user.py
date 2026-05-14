"""User model - WhatsApp users"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.models.base import Base


class UserPlan(str, enum.Enum):
    """User subscription plan"""
    FREE = "free"
    PAID = "paid"


class User(Base):
    """
    Represents a WhatsApp user of the flight bot.
    
    Attributes:
        id: Primary key (WhatsApp phone number or user ID)
        phone_number: WhatsApp phone number in format 55XXXXXXXXXXXXX
        name: User's name
        plan: Subscription plan (free or paid)
        is_active: Whether the user account is active
        created_at: Timestamp when user was added
        updated_at: Timestamp of last update
    """
    
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    plan = Column(String, default=UserPlan.FREE, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<User {self.phone_number} ({self.plan})>"
