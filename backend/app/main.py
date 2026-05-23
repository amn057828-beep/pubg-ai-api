from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from loguru import logger

from app.core.config import settings
from app.core.database import Base, engine
from app.api import auth, analysis, admin, leaderboard, upgrade, features
import app.models

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"])

app = FastAPI(
    title=settings.APP_NAME,
    description="PUBG Mobile AI Analyzer Arabic SaaS API",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    return await call_next(request)

@app.get("/")
def root():
    return {"name": settings.APP_NAME, "status": "online", "docs": "/docs"}

app.include_router(auth.router)
app.include_router(analysis.router)
app.include_router(admin.router)
app.include_router(leaderboard.router)
app.include_router(upgrade.router)
app.include_router(features.router)
