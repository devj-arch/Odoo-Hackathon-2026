from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.repository.user_repository import UserRepository
<<<<<<< Updated upstream
from app.core.security import verify_password, create_access_token
from datetime import datetime, timedelta
=======

>>>>>>> Stashed changes

class AuthService:

    @staticmethod
    def login(db: Session, email: str, password: str, role: str) -> dict | None:
        """Authenticate user with email, password, and role.

        Returns a dict with access_token, token_type, and user info,
        or None if credentials are invalid.
        """
        user = UserRepository.get_by_email(db, email)

        if user is None:
            return None

        # Check if account is locked
        if user.is_locked:

            if user.locked_until and datetime.utcnow() < user.locked_until:
                raise Exception("Account locked after 5 failed attempts. Try again later.")

            # Lock expired
            user.is_locked = False
            user.failed_login_attempts = 0
            user.locked_until = None
            db.commit()

        # Wrong password
        if not verify_password(password, user.password_hash):

            user.failed_login_attempts += 1

            if user.failed_login_attempts >= 5:
                user.is_locked = True
                user.locked_until = datetime.utcnow() + timedelta(minutes=15)

            db.commit()

            return None

        if user.role.name != role:
            return None

        # Successful login
        user.failed_login_attempts = 0
        user.is_locked = False
        user.locked_until = None

        db.commit()

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
