from collections.abc import Callable

from fastapi import Depends, HTTPException

from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.utils.enums import Role


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = UserRepository.get_by_id(db, int(user_id))

    if user is None:
        raise credentials_exception

    return user


def require_roles(*allowed_roles: str) -> Callable[..., User]:
    """
    Enforce route access by role name.

    Admin is always allowed as a global override.
    """

    allowed = {Role.ADMIN.value, *allowed_roles}

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role = current_user.role.name

        if user_role not in allowed:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{user_role}' is not allowed to access this resource.",
            )

        return current_user

    return role_checker
