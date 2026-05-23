from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    pubg_id = Column(String, nullable=True, index=True)
    kd = Column(Float, default=0)
    damage = Column(Float, default=0)
    accuracy = Column(Float, default=0)
    survival_time = Column(Float, default=0)
    headshots = Column(Float, default=0)
    win_rate = Column(Float, default=0)
    score = Column(Float, default=0)
    title = Column(String, default="")
    badge = Column(String, default="")
    report = Column(String, default="")
    raw_data = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
