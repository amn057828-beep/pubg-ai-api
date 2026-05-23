from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.analysis import Analysis
from app.models.upgrade_request import UpgradeRequest
from app.models.subscription import Subscription
from app.models.tip import DailyTip
from app.schemas.upgrade import UpgradeDecision

router = APIRouter(prefix="/admin", tags=["Admin"])

def require_admin(user: User):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="صلاحية المدير فقط")

@router.get("/stats")
def stats(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    users = db.query(User).count()
    analyses = db.query(Analysis).count()
    avg_score = db.query(func.avg(Analysis.score)).scalar() or 0
    paid_users = db.query(User).filter(User.plan.in_(["pro", "premium"])).count()
    return {
        "users": users,
        "analyses": analyses,
        "avg_score": round(float(avg_score), 2),
        "revenue_estimate_usd": paid_users * 5,
    }

@router.get("/users")
def users(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    return db.query(User).order_by(User.id.desc()).limit(100).all()

@router.post("/users/{user_id}/ban")
def ban_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    target.is_banned = True
    db.commit()
    return {"ok": True}


@router.get("/upgrade-requests")
def upgrade_requests(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    return db.query(UpgradeRequest).order_by(UpgradeRequest.id.desc()).limit(200).all()

@router.post("/upgrade-requests/{request_id}/decision")
def decide_upgrade(request_id: int, payload: UpgradeDecision, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    req = db.query(UpgradeRequest).filter(UpgradeRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="طلب الترقية غير موجود")

    req.status = payload.status
    req.admin_note = payload.admin_note

    if payload.status == "approved" and req.user_id:
        target = db.query(User).filter(User.id == req.user_id).first()
        if target:
            target.plan = req.requested_plan
            db.add(Subscription(user_id=target.id, plan=req.requested_plan, status="active"))

    db.commit()
    return {"ok": True, "message": "تم تحديث طلب الترقية"}

@router.post("/users/{user_id}/plan/{plan}")
def set_user_plan(user_id: int, plan: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    if plan not in ["free", "pro", "premium"]:
        raise HTTPException(status_code=400, detail="الخطة غير صحيحة")
    target.plan = plan
    db.add(Subscription(user_id=target.id, plan=plan, status="active"))
    db.commit()
    return {"ok": True, "plan": plan}

@router.post("/tips")
def create_tip(title: str, body: str, category: str = "general", db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_admin(user)
    tip = DailyTip(title=title, body=body, category=category)
    db.add(tip)
    db.commit()
    db.refresh(tip)
    return tip
