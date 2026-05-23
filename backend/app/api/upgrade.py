from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.upgrade_request import UpgradeRequest


router = APIRouter(
    prefix="/upgrade",
    tags=["Upgrade"]
)


@router.post("/telegram-request")
def telegram_upgrade_request(
    body: dict,
    db: Session = Depends(get_db)
):

    row = UpgradeRequest(
        telegram_id=str(body.get("telegram_id", "")),
        username=body.get("username", ""),
        requested_plan=body.get("plan", "Pro"),
        contact=body.get("contact", ""),
        status="pending"
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "success": True,
        "request_id": row.id
    }
