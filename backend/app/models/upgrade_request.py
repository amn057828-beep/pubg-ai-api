from sqlalchemy import Column, Integer, String

from app.core.database import Base


class UpgradeRequest(Base):
    __tablename__ = "upgrade_requests"

    id = Column(Integer, primary_key=True, index=True)

    telegram_id = Column(String)

    username = Column(String)

    requested_plan = Column(String)

    contact = Column(String)

    status = Column(String, default="pending")
