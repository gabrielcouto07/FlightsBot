"""User alert schemas for CRUD operations"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


class UserAlertCreate(BaseModel):
    """Schema for creating a user alert"""
    origin_iata: Optional[str] = Field(None, min_length=3, max_length=3)
    destination_iata: Optional[str] = Field(None, min_length=3, max_length=3)
    date_from: date
    date_to: date
    max_price: float = Field(..., gt=0)


class UserAlertUpdate(BaseModel):
    """Schema for updating a user alert"""
    max_price: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


class UserAlertResponse(BaseModel):
    """Schema for user alert responses"""
    id: str
    user_id: str
    origin_iata: Optional[str]
    destination_iata: Optional[str]
    date_from: date
    date_to: date
    max_price: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class UserAlertListResponse(BaseModel):
    """Schema for alerts list response"""
    total: int
    alerts: list[UserAlertResponse]
