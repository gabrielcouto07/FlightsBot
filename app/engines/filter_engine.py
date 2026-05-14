"""Filter engine - match user alerts with flight deals"""

import logging
from datetime import datetime, date
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_alert import UserAlert
from app.models.price_snapshot import PriceSnapshot
from app.models.user import User

logger = logging.getLogger(__name__)


async def find_matching_user_alerts(
    db: AsyncSession,
    snapshot: PriceSnapshot,
) -> list[UserAlert]:
    """
    Find all paid user alerts that match a price snapshot.
    
    Matching criteria:
    - (alert.origin_iata == snapshot.origin) OR (alert.origin_iata IS NULL)
    - (alert.destination_iata == snapshot.destination) OR (alert.destination_iata IS NULL)
    - snapshot.price <= alert.max_price
    - snapshot.departure_at BETWEEN alert.date_from AND alert.date_to
    - alert.is_active == True
    - user.plan == 'paid'
    - user.is_active == True
    
    Args:
        db: Database session
        snapshot: PriceSnapshot to match against
    
    Returns:
        List of matching UserAlert objects
    """
    
    # Parse departure date from snapshot
    try:
        if isinstance(snapshot.departure_at, str):
            dep_date = datetime.fromisoformat(snapshot.departure_at.replace("Z", "+00:00")).date()
        else:
            dep_date = snapshot.departure_at.date() if hasattr(snapshot.departure_at, 'date') else snapshot.departure_at
    except Exception as e:
        logger.error(f"Error parsing departure date: {e}")
        return []
    
    # Build query
    stmt = select(UserAlert).join(
        User, UserAlert.user_id == User.id
    ).where(
        and_(
            # Route matching (null = any)
            or_(
                UserAlert.origin_iata == snapshot.origin,
                UserAlert.origin_iata.is_(None),
            ),
            or_(
                UserAlert.destination_iata == snapshot.destination,
                UserAlert.destination_iata.is_(None),
            ),
            # Price threshold
            snapshot.price <= UserAlert.max_price,
            # Date range
            dep_date >= UserAlert.date_from,
            dep_date <= UserAlert.date_to,
            # Alert is active
            UserAlert.is_active == True,
            # User is paid and active
            User.plan == "paid",
            User.is_active == True,
        )
    )
    
    result = await db.execute(stmt)
    alerts = result.scalars().all()
    
    logger.info(f"Found {len(alerts)} matching user alerts for {snapshot.origin}->{snapshot.destination}")
    return list(alerts)


async def get_matching_alerts_for_user(
    db: AsyncSession,
    user_id: str,
) -> list[UserAlert]:
    """
    Get all active alerts for a specific user.
    
    Args:
        db: Database session
        user_id: User ID
    
    Returns:
        List of UserAlert objects
    """
    stmt = select(UserAlert).where(
        and_(
            UserAlert.user_id == user_id,
            UserAlert.is_active == True,
        )
    ).order_by(UserAlert.created_at.desc())
    
    result = await db.execute(stmt)
    return list(result.scalars().all())
