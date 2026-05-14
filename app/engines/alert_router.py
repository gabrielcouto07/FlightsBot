"""Alert router - route deals to free group or paid users."""

import json
import logging
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.demo_notification import DemoNotification
from app.models.price_snapshot import PriceSnapshot
from app.models.user_alert import UserAlert
from app.models.sent_alert import SentAlert
from app.models.user import User
from app.whatsapp.client import WhatsAppClient
from app.whatsapp.formatter import format_free_alert, format_paid_alert
from app.engines.filter_engine import find_matching_user_alerts
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AlertRouter:
    """Routes flight deals to free group or individual paid users."""
    
    def __init__(self):
        """Initialize alert router with WhatsApp client"""
        self.whatsapp = WhatsAppClient()
    
    async def route_deal(
        self,
        db: AsyncSession,
        snapshot: PriceSnapshot,
    ) -> dict:
        """
        Route a flight deal to free group and/or paid users.
        
        Process:
        1. Always add to free group digest buffer
        2. Find matching paid user alerts
        3. Send DM to each matched user
        
        Args:
            db: Database session
            snapshot: PriceSnapshot representing the deal
        
        Returns:
            Dictionary with routing results
        """
        result = {
            "added_to_free_digest": False,
            "users_notified": 0,
            "errors": [],
        }
        
        try:
            # Add to free group digest
            await self._add_to_digest(db, snapshot)
            result["added_to_free_digest"] = True
            logger.info(f"Added deal to free digest: {snapshot.origin}->{snapshot.destination}")
        
        except Exception as e:
            logger.error(f"Error adding to digest: {e}")
            result["errors"].append(f"Free digest: {str(e)}")
        
        # Find and notify paid users
        try:
            matching_alerts = await find_matching_user_alerts(db, snapshot)
            
            for alert in matching_alerts:
                user_id = alert.user_id
                
                try:
                    # Get user details
                    from sqlalchemy import select
                    user_result = await db.execute(
                        select(User).where(User.id == user_id)
                    )
                    user = user_result.scalar_one_or_none()
                    
                    if not user:
                        logger.warning(f"User {user_id} not found")
                        continue
                    
                    # Format and send message
                    message = format_paid_alert(user.name or "usuário", {
                        "origin": snapshot.origin,
                        "destination": snapshot.destination,
                        "price": snapshot.price,
                        "airline": snapshot.airline,
                        "departure_at": snapshot.departure_at,
                        "duration_minutes": snapshot.duration_minutes,
                        "deep_link": snapshot.deep_link,
                    })
                    
                    success = await self.whatsapp.send_dm(
                        user.phone_number,
                        message,
                    )
                    
                    if success:
                        # Log sent alert
                        sent_alert = SentAlert(
                            id=str(uuid.uuid4()),
                            snapshot_id=snapshot.id,
                            user_id=user_id,
                            alert_type="paid_user_dm",
                        )
                        db.add(sent_alert)
                        await self._log_demo_notification(db, user, snapshot)
                        result["users_notified"] += 1
                        logger.info(f"Notified user {user_id} about deal")
                    else:
                        result["errors"].append(f"Failed to send to {user.phone_number}")
                
                except Exception as e:
                    logger.error(f"Error notifying user {user_id}: {e}")
                    result["errors"].append(f"User {user_id}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error finding matching alerts: {e}")
            result["errors"].append(f"Matching: {str(e)}")
        
        await db.commit()
        return result

    async def _log_demo_notification(
        self,
        db: AsyncSession,
        user: User,
        snapshot: PriceSnapshot,
    ) -> None:
        """Persist simulated notifications while WhatsApp delivery is disabled."""
        if not settings.demo_mode or settings.whatsapp_ready:
            return

        payload = {
            "origin": snapshot.origin,
            "destination": snapshot.destination,
            "price": snapshot.price,
            "currency": snapshot.currency,
            "airline": snapshot.airline,
            "departure_at": snapshot.departure_at.isoformat(),
            "deep_link": snapshot.deep_link,
        }
        db.add(
            DemoNotification(
                id=str(uuid.uuid4()),
                user_id=user.id,
                user_name=user.name or user.phone_number,
                user_plan=user.plan,
                deal_json=json.dumps(payload),
            )
        )
    
    async def _add_to_digest(
        self,
        db: AsyncSession,
        snapshot: PriceSnapshot,
    ) -> None:
        """
        Add a snapshot to free group digest.
        
        Args:
            db: Database session
            snapshot: PriceSnapshot to add
        """
        sent_alert = SentAlert(
            id=str(uuid.uuid4()),
            snapshot_id=snapshot.id,
            user_id=None,  # None = free group
            alert_type="free_group",
        )
        db.add(sent_alert)
    
    async def send_free_digest(
        self,
        db: AsyncSession,
        snapshots: list[PriceSnapshot],
    ) -> bool:
        """
        Send compiled free group digest.
        
        Args:
            db: Database session
            snapshots: List of PriceSnapshot objects to include
        
        Returns:
            True if successful
        """
        if not snapshots:
            logger.info("No snapshots for free digest")
            return True
        
        # Format digest message with top deals
        lines = [
            "🌍 *MELHORES PROMOÇÕES DE PASSAGENS AÉREAS* ✈️",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
        ]
        
        for idx, snapshot in enumerate(snapshots[:5], 1):
            price_formatted = f"R$ {snapshot.price:,.0f}".replace(",", ".")
            lines.append(f"{idx}. *{snapshot.origin} → {snapshot.destination}*")
            lines.append(f"   💰 {price_formatted} | 🏢 {snapshot.airline}")
            lines.append(f"   🔗 {snapshot.deep_link}")
            lines.append("")
        
        lines.extend([
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "_Preços podem mudar. Confira antes de comprar._",
            "_Quer alertas personalizados? Digite /premium para saber mais!_",
        ])
        
        message = "\n".join(lines)
        
        try:
            success = await self.whatsapp.send_group_message(
                settings.free_group_jid,
                message,
            )
            
            if success:
                # Log each as sent
                for snapshot in snapshots[:5]:
                    sent_alert = SentAlert(
                        id=str(uuid.uuid4()),
                        snapshot_id=snapshot.id,
                        user_id=None,
                        alert_type="free_group_digest",
                    )
                    db.add(sent_alert)
                
                await db.commit()
                logger.info(f"Free digest sent to {settings.free_group_jid}")
            
            return success
        
        except Exception as e:
            logger.error(f"Error sending free digest: {e}")
            return False
