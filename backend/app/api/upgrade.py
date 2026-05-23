from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.upgrade_request import UpgradeRequest
from app.schemas.upgrade import UpgradeRequestCreate

router = APIRouter(prefix="/upgrade", tags=["Manual Upgrade"])

@router.post("/request")
def request_upgrade(payload: UpgradeRequestCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    req = UpgradeRequest(
        user_id=user.id,
        username=user.username,
        requested_plan=payload.requested_plan,
        contact=payload.contact,
        payment_note=payload.payment_note,
        status="pending"
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return {
        "ok": True,
        "message": "تم إرسال طلب الترقية. سيراجعه المدير ويفعل الاشتراك يدوياً.",
        "request_id": req.id
    }

@router.get("/my-requests")
def my_requests(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(UpgradeRequest).filter(UpgradeRequest.user_id == user.id).order_by(UpgradeRequest.id.desc()).all()
