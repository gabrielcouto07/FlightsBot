"""SentAlert model - deduplication log for alerts"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime

from app.models.base import Base


class SentAlert(Base):
    """
    Log of sent alerts - used to prevent duplicate alerts
    and track free group digest messages.
    
    Attributes:
        id: Primary key
        snapshot_id: Foreign key to PriceSnapshot
        user_id: Foreign key to User (NULL for free group alerts)
        alert_type: Type of alert ("free_group" or "paid_user_dm")
        sent_at: When the alert was sent
    """
    
    __tablename__ = "sent_alerts"
    
    id = Column(String, primary_key=True, index=True)
    snapshot_id = Column(String, ForeignKey("price_snapshots.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    alert_type = Column(String(50), nullable=False, index=True)  # "free_group" or "paid_user_dm"
    sent_at = Column(DateTime, server_default=func.now(), index=True)
    
    def __repr__(self) -> str:
        return f"<SentAlert {self.alert_type} at {self.sent_at}>"
