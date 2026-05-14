"""Price detection engine - identify flight deals."""

import logging
from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price_snapshot import PriceSnapshot
from app.models.route import Route
from app.models.sent_alert import SentAlert
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _parse_snapshot_datetime(value: datetime | str | None) -> datetime | None:
    """Normalize ISO datetime strings before persisting snapshots."""
    if value is None or isinstance(value, datetime):
        return value

    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    raise TypeError(f"Unsupported datetime value: {type(value)!r}")


async def is_deal(snapshot: PriceSnapshot, route: Route) -> bool:
    """
    Determine if a price snapshot is a deal compared to route threshold.
    
    Args:
        snapshot: PriceSnapshot to evaluate
        route: Route with threshold price
    
    Returns:
        True if snapshot.price <= route.threshold_price
    """
    return snapshot.price <= route.threshold_price


async def save_snapshot_if_deal(
    db: AsyncSession,
    snapshot_data: dict,
    route: Route,
) -> PriceSnapshot | None:
    """
    Save a price snapshot if it's a deal and not duplicate.
    
    Checks:
    1. Is the price a deal (below threshold)?
    2. Has a duplicate alert been sent in the last ALERT_COOLDOWN_HOURS?
    
    Args:
        db: Database session
        snapshot_data: Normalized flight data from scraper
        route: Route model with threshold price
    
    Returns:
        PriceSnapshot if saved, None otherwise
    """
    # Check if it's a deal
    normalized_snapshot_data = {
        **snapshot_data,
        "departure_at": _parse_snapshot_datetime(snapshot_data.get("departure_at")),
        "return_at": _parse_snapshot_datetime(snapshot_data.get("return_at")),
    }
    snapshot = PriceSnapshot(**normalized_snapshot_data)
    
    if not await is_deal(snapshot, route):
        logger.debug(f"Price {snapshot.price} is not a deal (threshold: {route.threshold_price})")
        return None
    
    # Check for duplicate alerts (cooldown period)
    cooldown_hours = settings.alert_cooldown_hours
    since = datetime.utcnow() - timedelta(hours=cooldown_hours)
    
    # Generate unique snapshot ID based on route and departure date
    departure_date = snapshot.departure_at[:10] if isinstance(snapshot.departure_at, str) else str(snapshot.departure_at)[:10]
    snapshot_id = f"{route.origin_iata}_{route.destination_iata}_{departure_date}_{int(snapshot.price)}"
    snapshot.id = snapshot_id
    
    # Check if we've already sent an alert for this route in cooldown period
    stmt = select(SentAlert).where(
        and_(
            SentAlert.snapshot_id.like(f"{route.origin_iata}_{route.destination_iata}_{departure_date}_%"),
            SentAlert.sent_at >= since,
        )
    )
    
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        logger.info(f"Cooldown active for {route.origin_iata}->{route.destination_iata} on {departure_date}")
        return None
    
    # Save the snapshot
    db.add(snapshot)
    await db.flush()
    
    logger.info(f"Deal saved: {snapshot.origin}->{snapshot.destination} R${snapshot.price}")
    return snapshot


async def get_cheapest_by_route(
    db: AsyncSession,
    origin: str,
    destination: str,
    days: int = 7,
) -> PriceSnapshot | None:
    """
    Get the cheapest flight snapshot for a route in the last N days.
    
    Args:
        db: Database session
        origin: Origin IATA code
        destination: Destination IATA code
        days: Look back period in days
    
    Returns:
        Cheapest PriceSnapshot or None
    """
    since = datetime.utcnow() - timedelta(days=days)
    
    stmt = select(PriceSnapshot).where(
        and_(
            PriceSnapshot.origin == origin,
            PriceSnapshot.destination == destination,
            PriceSnapshot.captured_at >= since,
        )
    ).order_by(PriceSnapshot.price.asc()).limit(1)
    
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
