from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class UpgradeRequest(Base):
    __tablename__ = "upgrade_requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    telegram_id = Column(String, nullable=True, index=True)
    username = Column(String, nullable=True)
    requested_plan = Column(String, default="pro")
    contact = Column(String, nullable=True)
    payment_note = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, approved, rejected
    admin_note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
