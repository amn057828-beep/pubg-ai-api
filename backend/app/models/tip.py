from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class DailyTip(Base):
    __tablename__ = "daily_tips"
    id = Column(Integer, primary_key=True)
    title = Column(String, default="")
    body = Column(String, default="")
    category = Column(String, default="general")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
