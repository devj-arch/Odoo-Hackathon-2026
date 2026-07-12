from sqlalchemy.orm import Session

from app.repository.user_repository import UserRepository
from app.core.security import verify_password, create_access_token


class AuthService:

    @staticmethod
    def login(db: Session, email: str, password: str, role: str):

        user = UserRepository.get_by_email(db, email)

        if user is None:
            return None

        if not verify_password(password, user.password_hash):
            return None

        
        if user.role.name != role:
            return None

        token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role.name,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.name,
            },
        }