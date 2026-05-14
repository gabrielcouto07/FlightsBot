"""WhatsApp webhook router for receiving and processing messages"""

import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User, UserPlan
from app.whatsapp.commands import parse_command
from app.whatsapp.formatter import format_help_message, format_status_message
from app.whatsapp.client import WhatsAppClient
from app.engines.filter_engine import get_matching_alerts_for_user
from app.models.user_alert import UserAlert
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/whatsapp")
async def whatsapp_webhook(
    body: dict,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Webhook to receive and process WhatsApp messages.
    
    Evolution API will POST message events here.
    Processes commands for paid users.
    """
    
    try:
        # Extract message data (Evolution API format)
        message_data = body.get("data", {})
        from_jid = message_data.get("from", {}).get("jid", "")
        message_text = message_data.get("body", "")
        
        if not from_jid or not message_text:
            logger.warning("Invalid webhook payload")
            return {"status": "ignored"}
        
        # Extract phone number from JID
        phone_number = from_jid.replace("@c.us", "").replace("@g.us", "")
        
        logger.info(f"Received message from {phone_number}: {message_text[:50]}")
        
        # Get or create user
        stmt = select(User).where(User.phone_number == phone_number)
        user_result = await db.execute(stmt)
        user = user_result.scalar_one_or_none()
        
        if not user:
            # Create new free user
            user = User(
                id=str(uuid.uuid4()),
                phone_number=phone_number,
                plan=UserPlan.FREE,
                is_active=True,
            )
            db.add(user)
            await db.flush()
            logger.info(f"Created new user: {phone_number}")
        
        # Only process commands for paid users
        if user.plan != UserPlan.PAID:
            logger.info(f"User {phone_number} is not paid, ignoring command")
            return {"status": "ignored_free_user"}
        
        # Parse command
        result = parse_command(message_text)
        whatsapp = WhatsAppClient()
        
        if not result.is_valid():
            # Send error message
            await whatsapp.send_dm(phone_number, f"❌ {result.error_message}")
            return {"status": "error", "message": result.error_message}
        
        # Process command
        if result.command_type == "ajuda":
            response = format_help_message()
            await whatsapp.send_dm(phone_number, response)
        
        elif result.command_type == "status":
            alerts = await get_matching_alerts_for_user(db, user.id)
            response = format_status_message(user.name or "usuário", user.plan, len(alerts))
            await whatsapp.send_dm(phone_number, response)
        
        elif result.command_type == "listar":
            alerts = await get_matching_alerts_for_user(db, user.id)
            if not alerts:
                response = "Você não tem alertas ativos. Use /alerta para criar um."
            else:
                lines = ["📋 *SEUS ALERTAS:*\n"]
                for idx, alert in enumerate(alerts, 1):
                    origin = alert.origin_iata or "Qualquer"
                    dest = alert.destination_iata or "Qualquer"
                    lines.append(f"{idx}. {origin} → {dest}")
                    lines.append(f"   💰 Máx: R$ {alert.max_price}")
                    lines.append(f"   📅 {alert.date_from} a {alert.date_to}")
                response = "\n".join(lines)
            await whatsapp.send_dm(phone_number, response)
        
        elif result.command_type == "pausar":
            alert_id = result.params.get("alert_id")
            # Find and pause alert
            alert = await db.get(UserAlert, alert_id)
            if alert and alert.user_id == user.id:
                alert.is_active = False
                await db.commit()
                await whatsapp.send_dm(phone_number, f"✅ Alerta #{alert_id} pausado.")
            else:
                await whatsapp.send_dm(phone_number, f"❌ Alerta não encontrado.")
        
        elif result.command_type == "deletar":
            alert_id = result.params.get("alert_id")
            # Find and delete alert
            alert = await db.get(UserAlert, alert_id)
            if alert and alert.user_id == user.id:
                await db.delete(alert)
                await db.commit()
                await whatsapp.send_dm(phone_number, f"✅ Alerta #{alert_id} deletado.")
            else:
                await whatsapp.send_dm(phone_number, f"❌ Alerta não encontrado.")
        
        elif result.command_type == "alerta":
            params = result.params
            alert = UserAlert(
                id=str(uuid.uuid4()),
                user_id=user.id,
                origin_iata=params.get("origin_iata"),
                destination_iata=params.get("destination_iata"),
                date_from=params.get("date_from"),
                date_to=params.get("date_to"),
                max_price=params.get("max_price"),
                is_active=True,
            )
            db.add(alert)
            await db.commit()
            
            origin = params.get("origin_iata") or "Qualquer"
            dest = params.get("destination_iata") or "Qualquer"
            response = f"✅ Alerta criado para {origin} → {dest} até R$ {params.get('max_price')}"
            await whatsapp.send_dm(phone_number, response)
        
        await db.commit()
        return {"status": "success"}
    
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}


@router.get("/whatsapp")
async def whatsapp_webhook_verify(
    hub_mode: str = None,
    hub_challenge: str = None,
    hub_verify_token: str = None,
) -> str:
    """
    Verify webhook for WhatsApp API.
    
    Evolution API may use this for verification.
    """
    # In production, validate hub_verify_token
    if hub_challenge:
        return hub_challenge
    return "ok"
