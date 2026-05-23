from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

ALGORITHM = "HS256"

# استبدال bcrypt بـ pbkdf2_sha256
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

security = HTTPBearer()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=7)

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=ALGORITHM
    )

def decode_access_token(token: str):
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[ALGORITHM]
    )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(credentials.credentials)

        user = db.query(User).filter(
            User.id == payload.get("user_id")
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
