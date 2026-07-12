from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


def signup(db: Session, data: UserCreate) -> User:
    """Register a new user. Raises ValueError on duplicate email."""
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ValueError("A user with this email already exists.")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        name=data.full_name,
        role_id=data.role_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User | None:
    """Return the User if credentials are valid, otherwise None."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
