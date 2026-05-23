from pydantic import BaseModel
from app.schemas.analysis import PlayerStats

class CompareRequest(BaseModel):
    player_a: PlayerStats
    player_b: PlayerStats
