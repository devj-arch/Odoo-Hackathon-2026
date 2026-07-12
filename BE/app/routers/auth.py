from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.role import Role as RoleModel
from app.utils.enums import Role as RoleEnum
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    MessageResponse,
    ResetPasswordRequest,
)
from app.schemas.user import UserCreate
from app.services.auth_services import AuthService

from app.dependencies.auth import require_roles


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    # Verify the role exists
    role = db.query(RoleModel).filter(RoleModel.id == data.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with id '{data.role_id}' not found.",
        )

    try:
        user = AuthService.signup(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.name,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate and return a JWT access token.

    Requires email, password, AND role — all three must match.
    """
    result = AuthService.login(
        db=db,
        email=request.email,
        password=request.password,
        role=request.role,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email, password or role",
        )

    return result


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role.name,
    }


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Send a password-reset email if the account exists.

    Always returns the same message to avoid revealing which emails are registered.
    """
    AuthService.forgot_password(db, request.email)
    return {"message": "If that email is registered, a reset link has been sent."}


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using a valid reset token."""
    success = AuthService.reset_password(db, request.token, request.new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token.",
        )
    return {"message": "Password has been reset successfully."}
