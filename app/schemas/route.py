"""Route schemas for CRUD operations"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RouteCreate(BaseModel):
    """Schema for creating a new route"""
    origin_iata: str = Field(..., min_length=3, max_length=3)
    destination_iata: str = Field(..., min_length=3, max_length=3)
    threshold_price: float = Field(..., gt=0)


class RouteUpdate(BaseModel):
    """Schema for updating an existing route"""
    threshold_price: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


class RouteResponse(BaseModel):
    """Schema for route responses"""
    id: str
    origin_iata: str
    destination_iata: str
    threshold_price: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class RouteListResponse(BaseModel):
    """Schema for routes list response"""
    total: int
    routes: list[RouteResponse]
