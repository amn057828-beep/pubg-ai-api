from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.api_key import ApiKey


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password[:72], hashed)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(subject),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="توكن غير صالح")

        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="توكن غير صالح")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="يرجى تسجيل الدخول وإرسال Bearer Token"
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="نوع التوكن غير صحيح"
        )

    token = credentials.credentials.strip()
    user_id = decode_token(token)

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="المستخدم غير موجود")

    if user.is_banned:
        raise HTTPException(status_code=403, detail="هذا المستخدم محظور")

    return user


def get_api_key(
    x_api_key: str = Header(default="", alias="X-API-Key"),
    db: Session = Depends(get_db)
) -> ApiKey:

    if not x_api_key:
        raise HTTPException(status_code=401, detail="يرجى إرسال API Key")

    key = db.query(ApiKey).filter(
        ApiKey.key == x_api_key,
        ApiKey.is_active == True
    ).first()

    if not key:
        raise HTTPException(status_code=401, detail="API Key غير صالح")

    return key
