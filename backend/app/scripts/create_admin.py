from app.core.database import Base, engine, SessionLocal
from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User
import app.models

Base.metadata.create_all(bind=engine)
db = SessionLocal()

user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
if not user:
    user = User(
        username=settings.ADMIN_USERNAME,
        password_hash=hash_password(settings.ADMIN_PASSWORD),
        is_admin=True,
        plan="premium"
    )
    db.add(user)
    print("Admin created")
else:
    user.is_admin = True
    user.plan = "premium"
    print("Admin updated")

db.commit()
db.close()
