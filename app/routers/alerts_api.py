"""Alerts API - CRUD for user flight alerts"""

import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user_alert import UserAlert
from app.models.user import User
from app.schemas.alert import UserAlertCreate, UserAlertUpdate, UserAlertResponse, UserAlertListResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.post("", response_model=UserAlertResponse)
async def create_alert(
    user_id: str,
    alert_data: UserAlertCreate,
    db: AsyncSession = Depends(get_db),
) -> UserAlert:
    """Create a new user alert"""
    
    # Verify user exists
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    alert = UserAlert(
        id=str(uuid.uuid4()),
        user_id=user_id,
        origin_iata=alert_data.origin_iata,
        destination_iata=alert_data.destination_iata,
        date_from=alert_data.date_from,
        date_to=alert_data.date_to,
        max_price=alert_data.max_price,
        is_active=True,
    )
    
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    
    logger.info(f"Created alert for user {user_id}: {alert.id}")
    return alert


@router.get("", response_model=UserAlertListResponse)
async def list_alerts(
    user_id: str = None,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """List user alerts"""
    
    stmt = select(UserAlert)
    
    if user_id:
        stmt = stmt.where(UserAlert.user_id == user_id)
    
    if active_only:
        stmt = stmt.where(UserAlert.is_active == True)
    
    stmt = stmt.offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    alerts = result.scalars().all()
    
    # Get total count
    count_stmt = select(func.count()).select_from(UserAlert)
    if user_id:
        count_stmt = count_stmt.where(UserAlert.user_id == user_id)
    if active_only:
        count_stmt = count_stmt.where(UserAlert.is_active == True)
    
    count_result = await db.execute(count_stmt)
    total = count_result.scalar()
    
    return {"total": total, "alerts": alerts}


@router.get("/{alert_id}", response_model=UserAlertResponse)
async def get_alert(
    alert_id: str,
    db: AsyncSession = Depends(get_db),
) -> UserAlert:
    """Get a specific alert"""
    
    alert = await db.get(UserAlert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return alert


@router.put("/{alert_id}", response_model=UserAlertResponse)
async def update_alert(
    alert_id: str,
    alert_data: UserAlertUpdate,
    db: AsyncSession = Depends(get_db),
) -> UserAlert:
    """Update an alert"""
    
    alert = await db.get(UserAlert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    if alert_data.max_price is not None:
        alert.max_price = alert_data.max_price
    if alert_data.is_active is not None:
        alert.is_active = alert_data.is_active
    
    await db.commit()
    await db.refresh(alert)
    
    logger.info(f"Updated alert: {alert_id}")
    return alert


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete an alert"""
    
    alert = await db.get(UserAlert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    await db.delete(alert)
    await db.commit()
    
    logger.info(f"Deleted alert: {alert_id}")
    return {"detail": "Alert deleted"}
