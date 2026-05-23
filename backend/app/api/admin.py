from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.models.upgrade_request import UpgradeRequest
from app.models.subscription import Subscription

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "analyses": db.query(Analysis).count(),
        "avg_score": round(float(db.query(func.avg(Analysis.score)).scalar() or 0), 2),
        "revenue_estimate_usd": db.query(Subscription).filter(Subscription.plan != "free").count() * 10
    }


@router.get("/users")
def users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id.desc()).limit(200).all()


@router.get("/upgrade-requests")
def upgrade_requests(db: Session = Depends(get_db)):
    rows = db.query(UpgradeRequest).order_by(UpgradeRequest.id.desc()).all()
    return [
        {
            "id": r.id,
            "username": r.username,
            "telegram_id": r.telegram_id,
            "requested_plan": r.requested_plan,
            "plan": r.requested_plan,
            "contact": r.contact,
            "status": r.status,
        }
        for r in rows
    ]


def set_request_status(request_id: int, status: str, db: Session):
    row = db.query(UpgradeRequest).filter(UpgradeRequest.id == request_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Request not found")

    row.status = status

    if status == "approved" and row.telegram_id:
        user = db.query(User).filter(User.telegram_id == str(row.telegram_id)).first()
        if user:
            user.plan = row.requested_plan or "pro"

    db.commit()
    return {"success": True, "status": status}


@router.post("/approve/{request_id}")
def approve(request_id: int, db: Session = Depends(get_db)):
    return set_request_status(request_id, "approved", db)


@router.post("/reject/{request_id}")
def reject(request_id: int, db: Session = Depends(get_db)):
    return set_request_status(request_id, "rejected", db)


@router.post("/upgrade-requests/{request_id}/decision")
def decision(request_id: int, body: dict, db: Session = Depends(get_db)):
    status = body.get("status", "approved")
    return set_request_status(request_id, status, db)


@router.post("/users/{user_id}/ban")
def ban_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_banned = True
        db.commit()
    return {"success": True}


@router.post("/users/{user_id}/plan/{plan}")
def set_plan(user_id: int, plan: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.plan = plan
        db.add(Subscription(user_id=user.id, plan=plan, status="active"))
        db.commit()
    return {"success": True}
