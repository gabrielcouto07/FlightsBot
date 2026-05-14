"""Users API - CRUD for WhatsApp users"""

import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Create a new user"""
    
    # Check if phone number already exists
    stmt = select(User).where(User.phone_number == user_data.phone_number)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User with this phone number already exists")
    
    user = User(
        id=str(uuid.uuid4()),
        phone_number=user_data.phone_number,
        name=user_data.name,
        plan=user_data.plan,
        is_active=True,
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    logger.info(f"Created user: {user.phone_number}")
    return user


@router.get("", response_model=UserListResponse)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    plan: str = None,
    active_only: bool = False,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """List all users"""
    
    stmt = select(User)
    
    if active_only:
        stmt = stmt.where(User.is_active == True)
    
    if plan:
        stmt = stmt.where(User.plan == plan)
    
    stmt = stmt.offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    users = result.scalars().all()
    
    # Get total count
    count_stmt = select(func.count()).select_from(User)
    if active_only:
        count_stmt = count_stmt.where(User.is_active == True)
    if plan:
        count_stmt = count_stmt.where(User.plan == plan)
    
    count_result = await db.execute(count_stmt)
    total = count_result.scalar()
    
    return {"total": total, "users": users}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get a specific user"""
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Update a user"""
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.plan is not None:
        user.plan = user_data.plan
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    
    await db.commit()
    await db.refresh(user)
    
    logger.info(f"Updated user: {user_id}")
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete a user"""
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    
    logger.info(f"Deleted user: {user_id}")
    return {"detail": "User deleted"}
