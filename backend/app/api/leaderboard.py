from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.leaderboard import Leaderboard


router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"]
)


@router.get("/")
def get_leaderboard(
    db: Session = Depends(get_db)
):
    rows = db.query(Leaderboard).order_by(
        desc(Leaderboard.score)
    ).limit(20).all()

    return [
        {
            "rank": i + 1,
            "username": row.username,
            "pubg_id": row.pubg_id,
            "score": row.score,
            "badge": row.badge,
        }
        for i, row in enumerate(rows)
    ]
