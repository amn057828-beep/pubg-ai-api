from fastapi import HTTPException
from app.core.config import settings

def plan_limit(plan: str) -> int:
    return {
        "free": settings.FREE_DAILY_LIMIT,
        "pro": settings.PRO_DAILY_LIMIT,
        "premium": settings.PREMIUM_DAILY_LIMIT,
    }.get(plan, settings.FREE_DAILY_LIMIT)

def assert_can_analyze(user):
    limit = plan_limit(user.plan)
    if user.daily_used >= limit:
        raise HTTPException(status_code=402, detail=f"انتهى حد الخطة اليومية: {limit}. قم بالترقية.")
