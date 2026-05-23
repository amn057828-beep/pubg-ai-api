from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    pubg_id = Column(String, index=True)
    score = Column(Float, default=0)
    badge = Column(String, default="Training Mode")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
