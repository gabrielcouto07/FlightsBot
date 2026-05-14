"""Routes API - CRUD for monitored flight routes"""

import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.route import Route
from app.schemas.route import RouteCreate, RouteUpdate, RouteResponse, RouteListResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.post("", response_model=RouteResponse)
async def create_route(
    route_data: RouteCreate,
    db: AsyncSession = Depends(get_db),
) -> Route:
    """Create a new monitored route"""
    
    # Generate ID
    route_id = f"{route_data.origin_iata}_{route_data.destination_iata}"
    
    # Check if already exists
    stmt = select(Route).where(Route.id == route_id)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Route already exists")
    
    route = Route(
        id=route_id,
        origin_iata=route_data.origin_iata.upper(),
        destination_iata=route_data.destination_iata.upper(),
        threshold_price=route_data.threshold_price,
        is_active=True,
    )
    
    db.add(route)
    await db.commit()
    await db.refresh(route)
    
    logger.info(f"Created route: {route_id}")
    return route


@router.get("", response_model=RouteListResponse)
async def list_routes(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """List all monitored routes"""
    
    stmt = select(Route)
    if active_only:
        stmt = stmt.where(Route.is_active == True)
    stmt = stmt.offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    routes = result.scalars().all()
    
    # Get total count
    count_stmt = select(func.count()).select_from(Route)
    if active_only:
        count_stmt = count_stmt.where(Route.is_active == True)
    count_result = await db.execute(count_stmt)
    total = count_result.scalar()
    
    return {"total": total, "routes": routes}


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: str,
    db: AsyncSession = Depends(get_db),
) -> Route:
    """Get a specific route"""
    
    stmt = select(Route).where(Route.id == route_id)
    result = await db.execute(stmt)
    route = result.scalar_one_or_none()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    return route


@router.put("/{route_id}", response_model=RouteResponse)
async def update_route(
    route_id: str,
    route_data: RouteUpdate,
    db: AsyncSession = Depends(get_db),
) -> Route:
    """Update a route"""
    
    stmt = select(Route).where(Route.id == route_id)
    result = await db.execute(stmt)
    route = result.scalar_one_or_none()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    if route_data.threshold_price is not None:
        route.threshold_price = route_data.threshold_price
    if route_data.is_active is not None:
        route.is_active = route_data.is_active
    
    await db.commit()
    await db.refresh(route)
    
    logger.info(f"Updated route: {route_id}")
    return route


@router.delete("/{route_id}")
async def delete_route(
    route_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete a route"""
    
    stmt = select(Route).where(Route.id == route_id)
    result = await db.execute(stmt)
    route = result.scalar_one_or_none()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    await db.delete(route)
    await db.commit()
    
    logger.info(f"Deleted route: {route_id}")
    return {"detail": "Route deleted"}
