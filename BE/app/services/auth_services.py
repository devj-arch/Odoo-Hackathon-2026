from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    generate_reset_token,
    hash_password,
    verify_password,
)
from app.repository.user_repository import UserRepository
from app.utils.email import send_password_reset_email

from app.core.security import verify_password, create_access_token
from datetime import datetime, timedelta

class AuthService:

    @staticmethod
    def login(db: Session, email: str, password: str, role: str):

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

        # Wrong role
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

    @staticmethod
    def forgot_password(db: Session, email: str) -> None:
        """
        If a user with this email exists, generate a reset token and email
        them a reset link. Silently does nothing otherwise, so the router
        can always return the same generic response and avoid revealing
        which emails are registered.
        """

        user = UserRepository.get_by_email(db, email)

        if user is None:
            return

        user.reset_token = generate_reset_token()
        user.reset_token_expiry = datetime.utcnow() + timedelta(
            minutes=settings.RESET_TOKEN_EXPIRE_MINUTES
        )

        db.commit()

        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={user.reset_token}"

        send_password_reset_email(user.email, reset_link)

    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> bool:
        """
        Validate the reset token and set a new password.
        Returns False if the token is missing, unknown, or expired.
        """

        user = UserRepository.get_by_reset_token(db, token)

        if user is None:
            return False

        if user.reset_token_expiry is None or datetime.utcnow() > user.reset_token_expiry:
            return False

        user.password_hash = hash_password(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        user.failed_login_attempts = 0
        user.is_locked = False
        user.locked_until = None

        db.commit()

        return True