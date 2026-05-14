"""Demo API - seed data and notification tracking."""

import json
import logging
import uuid
from datetime import timedelta, date

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User, UserPlan
from app.models.route import Route
from app.models.user_alert import UserAlert
from app.models.demo_notification import DemoNotification
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/demo", tags=["demo"])


class DemoSeedResponse(BaseModel):
    """Response for demo seed operation"""
    message: str
    counts: dict


class DemoNotificationRow(BaseModel):
    """Demo notification for display"""
    id: str
    user_name: str
    user_plan: str
    deal_summary: str
    triggered_at: str


class DemoNotificationsResponse(BaseModel):
    """List of demo notifications"""
    notifications: list[DemoNotificationRow]
    total: int


@router.post("/seed", response_model=DemoSeedResponse)
async def seed_demo_data(
    db: AsyncSession = Depends(get_db),
) -> DemoSeedResponse:
    """
    Seed demo database with sample users, routes, and alerts.
    
    Only works if DEMO_MODE=True.
    Safe to call multiple times (skips existing data).
    """
    
    if not settings.demo_mode:
        raise HTTPException(status_code=403, detail="Demo mode is disabled")
    
    counts = {
        "users_created": 0,
        "routes_created": 0,
        "alerts_created": 0,
    }
    
    try:
        # Create demo users
        demo_users = [
            {"name": "Ana Lima", "phone": "5511999990001", "plan": UserPlan.FREE},
            {"name": "Carlos Souza", "phone": "5511999990002", "plan": UserPlan.FREE},
            {"name": "Maria Fernandes", "phone": "5511999990003", "plan": UserPlan.FREE},
            {"name": "Roberto Alves", "phone": "5511999990004", "plan": UserPlan.PAID},
            {"name": "Fernanda Costa", "phone": "5511999990005", "plan": UserPlan.PAID},
        ]
        
        user_map = {}
        for user_data in demo_users:
            # Check if user exists
            stmt = select(User).where(User.phone_number == user_data["phone"])
            existing = await db.execute(stmt)
            existing_user = existing.scalar_one_or_none()
            if existing_user:
                user_map[user_data["name"]] = existing_user
                continue
            
            user = User(
                id=str(uuid.uuid4()),
                phone_number=user_data["phone"],
                name=user_data["name"],
                plan=user_data["plan"],
                is_active=True,
            )
            db.add(user)
            user_map[user_data["name"]] = user
            counts["users_created"] += 1
        
        await db.flush()
        
        # Create demo routes
        demo_routes = [
            {"origin": "GRU", "destination": "SSA", "threshold": 299},
            {"origin": "GRU", "destination": "REC", "threshold": 349},
            {"origin": "GRU", "destination": "FOR", "threshold": 379},
            {"origin": "GRU", "destination": "BSB", "threshold": 199},
            {"origin": "GRU", "destination": "CWB", "threshold": 179},
            {"origin": "GRU", "destination": "MIA", "threshold": 1499},
            {"origin": "GRU", "destination": "LIS", "threshold": 1899},
            {"origin": "GRU", "destination": "BCN", "threshold": 1799},
        ]
        
        for route_data in demo_routes:
            route_id = f"{route_data['origin']}_{route_data['destination']}"
            stmt = select(Route).where(Route.id == route_id)
            existing = await db.execute(stmt)
            if existing.scalar_one_or_none():
                continue
            
            route = Route(
                id=route_id,
                origin_iata=route_data["origin"],
                destination_iata=route_data["destination"],
                threshold_price=route_data["threshold"],
                is_active=True,
            )
            db.add(route)
            counts["routes_created"] += 1
        
        await db.flush()
        
        # Create alerts for paid users
        demo_alerts = [
            {
                "user_name": "Roberto Alves",
                "origin": "GRU",
                "destination": "MIA",
                "date_from_offset": 30,
                "date_to_offset": 60,
                "max_price": 1600,
            },
            {
                "user_name": "Roberto Alves",
                "origin": "GRU",
                "destination": "LIS",
                "date_from_offset": None,
                "date_to_offset": None,
                "max_price": 2000,
            },
            {
                "user_name": "Fernanda Costa",
                "origin": "GRU",
                "destination": "BCN",
                "date_from_offset": 15,
                "date_to_offset": 45,
                "max_price": 1900,
            },
            {
                "user_name": "Fernanda Costa",
                "origin": "GRU",
                "destination": "SSA",
                "date_from_offset": None,
                "date_to_offset": None,
                "max_price": 400,
            },
        ]
        
        for alert_data in demo_alerts:
            user = user_map.get(alert_data["user_name"])
            if not user:
                continue
            
            # Check if alert exists
            stmt = select(UserAlert).where(
                (UserAlert.user_id == user.id) &
                (UserAlert.origin_iata == alert_data["origin"]) &
                (UserAlert.destination_iata == alert_data["destination"])
            )
            existing = await db.execute(stmt)
            if existing.scalar_one_or_none():
                continue
            
            today = date.today()
            date_from = None
            date_to = None
            
            if alert_data["date_from_offset"]:
                date_from = today + timedelta(days=alert_data["date_from_offset"])
            if alert_data["date_to_offset"]:
                date_to = today + timedelta(days=alert_data["date_to_offset"])
            
            # If no explicit dates set, use 60 days from today
            if not date_from:
                date_from = today
            if not date_to:
                date_to = today + timedelta(days=60)
            
            alert = UserAlert(
                id=str(uuid.uuid4()),
                user_id=user.id,
                origin_iata=alert_data["origin"],
                destination_iata=alert_data["destination"],
                date_from=date_from,
                date_to=date_to,
                max_price=alert_data["max_price"],
                is_active=True,
            )
            db.add(alert)
            counts["alerts_created"] += 1
        
        await db.commit()
        
        logger.info(f"Demo data seeded: {counts}")
        return DemoSeedResponse(
            message="Demo data seeded successfully",
            counts=counts,
        )
    
    except Exception as e:
        await db.rollback()
        logger.error(f"Error seeding demo data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notifications", response_model=DemoNotificationsResponse)
async def get_demo_notifications(
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> DemoNotificationsResponse:
    """
    Get recent demo notifications (simulated WhatsApp alerts).
    
    Shows what deals have been detected and which users they would be sent to.
    """
    
    try:
        stmt = select(DemoNotification).order_by(
            desc(DemoNotification.triggered_at)
        ).limit(limit)
        
        result = await db.execute(stmt)
        notifications = result.scalars().all()
        
        # Parse deal JSON and format
        rows = []
        for notif in notifications:
            try:
                deal_data = json.loads(notif.deal_json)
                deal_summary = f"{deal_data.get('origin', '?')} → {deal_data.get('destination', '?')} • R$ {deal_data.get('price', 0):,.0f}"
            except:
                deal_summary = "Unknown deal"
            
            row = DemoNotificationRow(
                id=notif.id,
                user_name=notif.user_name,
                user_plan=notif.user_plan,
                deal_summary=deal_summary,
                triggered_at=notif.triggered_at.isoformat() if notif.triggered_at else "",
            )
            rows.append(row)
        
        return DemoNotificationsResponse(
            notifications=rows,
            total=len(rows),
        )
    
    except Exception as e:
        logger.error(f"Error fetching demo notifications: {e}")
        return DemoNotificationsResponse(
            notifications=[],
            total=0,
        )
