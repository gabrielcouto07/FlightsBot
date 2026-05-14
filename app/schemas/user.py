"""User schemas for CRUD operations"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    phone_number: str = Field(..., min_length=10)
    name: Optional[str] = None
    plan: str = Field(default="free")


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    name: Optional[str] = None
    plan: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """Schema for user responses"""
    id: str
    phone_number: str
    name: Optional[str]
    plan: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    """Schema for users list response"""
    total: int
    users: list[UserResponse]
