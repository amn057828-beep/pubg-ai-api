import os, tempfile
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_api_key
from app.models.user import User
from app.models.analysis import Analysis
from app.models.leaderboard import Leaderboard
from app.schemas.analysis import PlayerStats, AnalysisResponse
from app.services.ai_engine import analyze_player
from app.services.ocr_service import extract_text_from_image, parse_pubg_stats
from app.services.limits import assert_can_analyze
from app.services.share_card import create_share_card

router = APIRouter(prefix="/analyze", tags=["Analysis"])

def save_result(db: Session, user_id, stats: dict, result: dict):
    db.add(Analysis(
        user_id=user_id,
        pubg_id=stats.get("pubg_id"),
        kd=stats.get("kd", 0),
        damage=stats.get("damage", 0),
        accuracy=stats.get("accuracy", 0),
        survival_time=stats.get("survival_time", 0),
        headshots=stats.get("headshots", 0),
        win_rate=stats.get("win_rate", 0),
        score=result["score"],
        title=result["title"],
        badge=result["badge"],
        report=result["report"],
        raw_data=stats
    ))
    db.add(Leaderboard(
        username=f"user_{user_id}" if user_id else "api_user",
        pubg_id=stats.get("pubg_id") or "unknown",
        score=result["score"],
        badge=result["badge"]
    ))
    db.commit()

@router.post("/stats", response_model=AnalysisResponse)
def analyze_stats(payload: PlayerStats, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    assert_can_analyze(user)
    stats = payload.model_dump()
    result = analyze_player(stats)
    user.daily_used += 1
    save_result(db, user.id, stats, result)
    db.commit()
    return result

@router.post("/image", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    assert_can_analyze(user)
    suffix = os.path.splitext(file.filename or "image.png")[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        path = tmp.name
    text = extract_text_from_image(path)
    stats = parse_pubg_stats(text)
    result = analyze_player(stats)
    user.daily_used += 1
    save_result(db, user.id, stats, result)
    db.commit()
    return result

@router.post("/api-key/stats", response_model=AnalysisResponse)
def api_key_analyze(payload: PlayerStats, db: Session = Depends(get_db), key=Depends(get_api_key)):
    stats = payload.model_dump()
    result = analyze_player(stats)
    save_result(db, key.user_id, stats, result)
    return result


@router.post("/share-card")
def share_card(payload: PlayerStats, user: User = Depends(get_current_user)):
    stats = payload.model_dump()
    result = analyze_player(stats)
    path = create_share_card(
        title=result["title"],
        score=result["score"],
        badge=result["badge"],
        username=user.username or f"user_{user.id}"
    )
    return FileResponse(path, media_type="image/png", filename="pubg-ai-result.png")
