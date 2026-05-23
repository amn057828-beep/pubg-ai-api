from fastapi import APIRouter
from app.schemas.compare import CompareRequest
from app.services.ai_engine import analyze_player
from app.services.tips import random_tip

router = APIRouter(prefix="/features", tags=["Viral Features"])

@router.get("/daily-tip")
def daily_tip():
    return random_tip()

@router.post("/compare")
def compare_players(payload: CompareRequest):
    a = analyze_player(payload.player_a.model_dump())
    b = analyze_player(payload.player_b.model_dump())

    if a["score"] > b["score"]:
        winner = "player_a"
        summary = "اللاعب الأول أفضل إجمالاً من حيث المؤشرات الرقمية."
    elif b["score"] > a["score"]:
        winner = "player_b"
        summary = "اللاعب الثاني أفضل إجمالاً من حيث المؤشرات الرقمية."
    else:
        winner = "draw"
        summary = "المستوى متقارب جداً بين اللاعبين."

    return {
        "winner": winner,
        "summary": summary,
        "player_a": a,
        "player_b": b,
        "difference": round(abs(a["score"] - b["score"]), 2)
    }
