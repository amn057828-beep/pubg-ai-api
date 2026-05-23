from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.models.subscription import Subscription
from app.models.upgrade_request import UpgradeRequest

from app.core.security import get_current_user


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    users_count = db.query(User).count()

    analyses_count = db.query(Analysis).count()

    avg_score = db.query(
        func.avg(Analysis.score)
    ).scalar() or 0

    paid_subs = db.query(Subscription).filter(
        Subscription.plan != "free"
    ).count()

    revenue_estimate = (
        paid_subs * 10
    )

    return {
        "users": users_count,
        "analyses": analyses_count,
        "avg_score": round(avg_score, 2),
        "revenue_estimate_usd": revenue_estimate,
    }


@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    users = db.query(User).all()

    result = []

    for u in users:
        result.append({
            "id": u.id,
            "username": u.username,
            "telegram_id": u.telegram_id,
            "plan": u.plan,
            "daily_used": u.daily_used,
            "is_banned": u.is_banned,
        })

    return result


@router.post("/users/{user_id}/ban")
def ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user:
        user.is_banned = True
        db.commit()

    return {"success": True}


@router.post("/users/{user_id}/plan/{plan}")
def set_plan(
    user_id: int,
    plan: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user:
        user.plan = plan
        db.commit()

    return {"success": True}


@router.get("/upgrade-requests")
def get_upgrade_requests(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    rows = db.query(UpgradeRequest).all()

    result = []

    for r in rows:
        result.append({
            "id": r.id,
            "username": r.username,
            "telegram_id": r.telegram_id,
            "requested_plan": r.requested_plan,
            "contact": r.contact,
            "status": r.status,
        })

    return result


@router.post("/upgrade-requests/{request_id}/decision")
def decision(
    request_id: int,
    body: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    row = db.query(UpgradeRequest).filter(
        UpgradeRequest.id == request_id
    ).first()

    if not row:
        return {"success": False}

    row.status = body.get("status", "approved")

    db.commit()

    return {"success": True}
