from pydantic import BaseModel
from typing import Optional

class UpgradeRequestCreate(BaseModel):
    requested_plan: str
    contact: Optional[str] = None
    payment_note: Optional[str] = None

class UpgradeDecision(BaseModel):
    status: str
    admin_note: str | None = None
