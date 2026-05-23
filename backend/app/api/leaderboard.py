from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.leaderboard import Leaderboard

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("/")
def leaderboard(db: Session = Depends(get_db)):
    return db.query(Leaderboard).order_by(Leaderboard.score.desc()).limit(20).all()
