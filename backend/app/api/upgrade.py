from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.upgrade_request import UpgradeRequest
from app.models.user import User


router = APIRouter(
    prefix="/upgrade",
    tags=["Upgrade"]
)


@router.post("/request")
def request_upgrade(
    body: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    row = UpgradeRequest(
        username=user.username,
        telegram_id=str(user.telegram_id),
        requested_plan=body.get("plan", "pro"),
        contact=body.get("contact", ""),
        status="pending"
    )

    db.add(row)
    db.commit()

    return {
        "success": True,
        "message": "تم إرسال طلب الاشتراك"
    }
