from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    auth,
    analysis,
    admin,
    leaderboard,
    upgrade,
)

app = FastAPI(
    title="PUBG AI Analyzer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(analysis.router)
app.include_router(admin.router)
app.include_router(leaderboard.router)
app.include_router(upgrade.router)


@app.get("/")
def root():
    return {
        "message": "PUBG AI Analyzer API Running"
    }
