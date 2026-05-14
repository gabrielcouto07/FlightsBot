"""WhatsApp Evolution API client"""

import logging
import httpx
from typing import Optional

from app.config import get_settings

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """
    WhatsApp messaging client using Evolution API.
    
    Can be swapped with Z-API, Twilio, or other WhatsApp API providers.
    """
    
    def __init__(self):
        """Initialize WhatsApp client with Evolution API credentials"""
        self.settings = get_settings()
        self.base_url = self.settings.evolution_api_url
        self.api_key = self.settings.evolution_api_key
        self.instance_name = self.settings.evolution_instance_name
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[dict] = None,
        **kwargs,
    ) -> dict:
        """
        Make async request to Evolution API.
        
        Args:
            method: HTTP method ("GET", "POST", etc.)
            endpoint: API endpoint (e.g., "/message/sendText")
            json_data: JSON payload for POST requests
        
        Returns:
            Response JSON
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json",
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    json=json_data,
                    **kwargs,
                )
                response.raise_for_status()
                return response.json() if response.content else {}
        
        except httpx.HTTPError as e:
            logger.error(f"Evolution API error: {e}")
            raise
    
    async def send_message(
        self,
        jid: str,
        message: str,
        typing_delay: int = 1000,
    ) -> bool:
        """
        Send a text message via WhatsApp.
        
        Args:
            jid: Recipient JID (format: "55XXXXXXXXXXXXX@c.us" or "120363xxx@g.us")
            message: Message text
            typing_delay: Simulated typing delay in milliseconds
        
        Returns:
            True if successful, False otherwise
        """
        payload = {
            "number": jid.replace("@c.us", "").replace("@g.us", ""),
            "message": message,
        }
        
        try:
            logger.info(f"Sending message to {jid}")
            endpoint = f"/message/sendText/{self.instance_name}"
            await self._request("POST", endpoint, payload)
            logger.info(f"Message sent successfully to {jid}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send message to {jid}: {e}")
            return False
    
    async def send_group_message(
        self,
        group_jid: str,
        message: str,
    ) -> bool:
        """
        Send a message to a WhatsApp group.
        
        Args:
            group_jid: Group JID (format: "120363xxx@g.us")
            message: Message text
        
        Returns:
            True if successful
        """
        return await self.send_message(group_jid, message)
    
    async def send_dm(
        self,
        phone_number: str,
        message: str,
    ) -> bool:
        """
        Send a direct message to a WhatsApp user.
        
        Args:
            phone_number: WhatsApp phone number (55XXXXXXXXXXXXX format)
            message: Message text
        
        Returns:
            True if successful
        """
        jid = f"{phone_number}@c.us"
        return await self.send_message(jid, message)
    
    async def send_image_message(
        self,
        jid: str,
        image_url: str,
        caption: Optional[str] = None,
    ) -> bool:
        """
        Send an image message via WhatsApp.
        
        Args:
            jid: Recipient JID
            image_url: URL of the image to send
            caption: Optional caption for the image
        
        Returns:
            True if successful
        """
        payload = {
            "number": jid.replace("@c.us", "").replace("@g.us", ""),
            "image": image_url,
        }
        
        if caption:
            payload["caption"] = caption
        
        try:
            logger.info(f"Sending image to {jid}")
            endpoint = f"/message/sendImage/{self.instance_name}"
            await self._request("POST", endpoint, payload)
            logger.info(f"Image sent successfully to {jid}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send image to {jid}: {e}")
            return False
    
    async def send_button_message(
        self,
        jid: str,
        title: str,
        description: str,
        buttons: list[dict],
    ) -> bool:
        """
        Send a message with action buttons.
        
        Args:
            jid: Recipient JID
            title: Message title
            description: Message description
            buttons: List of button dicts with "id", "text", "type"
        
        Returns:
            True if successful
        """
        payload = {
            "number": jid.replace("@c.us", "").replace("@g.us", ""),
            "title": title,
            "description": description,
            "buttons": buttons,
        }
        
        try:
            logger.info(f"Sending button message to {jid}")
            endpoint = f"/message/sendButtons/{self.instance_name}"
            await self._request("POST", endpoint, payload)
            logger.info(f"Button message sent successfully to {jid}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send button message to {jid}: {e}")
            return False
