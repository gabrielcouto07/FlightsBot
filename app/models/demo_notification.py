"""Demo notification model for tracking alert simulation"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from datetime import datetime

from app.models.base import Base


class DemoNotification(Base):
    """
    Log of demo mode notifications - simulates WhatsApp alerts.
    Used to show investors real deal detection and filtering in action.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        user_name: User name (cached for speed)
        user_plan: User plan at time of notification (free/paid)
        deal_json: JSON serialized flight deal
        triggered_at: When the notification was created
    """
    
    __tablename__ = "demo_notifications"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    user_name = Column(String(255), nullable=False)
    user_plan = Column(String(20), nullable=False, index=True)
    deal_json = Column(Text, nullable=False)  # JSON string of flight deal
    triggered_at = Column(DateTime, server_default=func.now(), index=True)
    
    def __repr__(self) -> str:
        return f"<DemoNotification {self.user_name} ({self.user_plan})>"
