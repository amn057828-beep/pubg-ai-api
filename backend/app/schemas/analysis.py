from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class PlayerStats(BaseModel):
    pubg_id: Optional[str] = None
    kd: float = Field(default=0, ge=0)
    damage: float = Field(default=0, ge=0)
    accuracy: float = Field(default=0, ge=0, le=100)
    survival_time: float = Field(default=0, ge=0)
    headshots: float = Field(default=0, ge=0)
    win_rate: float = Field(default=0, ge=0, le=100)

class AnalysisResponse(BaseModel):
    score: float
    title: str
    badge: str
    report: str
    data: Dict[str, Any]
