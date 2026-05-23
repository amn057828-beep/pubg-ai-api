from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.upgrade_request import UpgradeRequest


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/upgrade-requests")
def get_upgrade_requests(
    db: Session = Depends(get_db)
):
    rows = db.query(UpgradeRequest).all()

    result = []

    for row in rows:
        result.append({
            "id": row.id,
            "username": row.username,
            "plan": row.requested_plan,
            "contact": row.contact,
            "status": row.status
        })

    return result


@router.post("/approve/{request_id}")
def approve_request(
    request_id: int,
    db: Session = Depends(get_db)
):

    row = db.query(UpgradeRequest).filter(
        UpgradeRequest.id == request_id
    ).first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    row.status = "approved"

    db.commit()

    return {
        "success": True,
        "message": "Request approved"
    }


@router.post("/reject/{request_id}")
def reject_request(
    request_id: int,
    db: Session = Depends(get_db)
):

    row = db.query(UpgradeRequest).filter(
        UpgradeRequest.id == request_id
    ).first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    row.status = "rejected"

    db.commit()

    return {
        "success": True,
        "message": "Request rejected"
    }
