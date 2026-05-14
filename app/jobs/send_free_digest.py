"""Job to send free group digest of top deals"""

import logging
from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.price_snapshot import PriceSnapshot
from app.models.sent_alert import SentAlert
from app.engines.alert_router import AlertRouter

logger = logging.getLogger(__name__)


async def send_free_digest() -> dict:
    """
    Send compiled digest of top flight deals to free group.
    
    Process:
    1. Get cheapest flights from last 6 hours
    2. Compile top 5 deals
    3. Send to free WhatsApp group
    
    Returns:
        Dictionary with digest results
    """
    result = {
        "deals_compiled": 0,
        "digest_sent": False,
        "error": None,
    }
    
    if AsyncSessionLocal is None:
        result["error"] = "Database not initialized"
        logger.error("Database not initialized")
        return result
    
    router = AlertRouter()
    
    async with AsyncSessionLocal() as db:
        try:
            # Get cheapest deals from last 6 hours not yet in digest
            since = datetime.utcnow() - timedelta(hours=6)
            
            # Get snapshots that aren't already in a digest
            stmt = select(PriceSnapshot).where(
                PriceSnapshot.captured_at >= since
            ).order_by(
                PriceSnapshot.price.asc()
            ).limit(5)
            
            result_obj = await db.execute(stmt)
            snapshots = result_obj.scalars().all()
            
            if not snapshots:
                logger.info("No new deals for digest")
                return result
            
            result["deals_compiled"] = len(snapshots)
            logger.info(f"Compiling digest with {len(snapshots)} deals")
            
            # Send digest
            success = await router.send_free_digest(db, list(snapshots))
            result["digest_sent"] = success
            
            if not success:
                result["error"] = "Failed to send digest to WhatsApp"
        
        except Exception as e:
            logger.error(f"Error in send_free_digest: {e}")
            result["error"] = str(e)
    
    return result
