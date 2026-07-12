from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    MessageResponse,
    ResetPasswordRequest,
)
from app.services.auth_services import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    try:
        result = AuthService.login(
            db=db,
            email=request.email,
            password=request.password,
            role=request.role,
        )

    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email, password or role"
        )

    return result


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role.name,
    }


@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    current_user: User = Depends(get_current_user),
):
    """
    Protected route: requires a valid Bearer token, same as any other
    authenticated endpoint. JWTs are stateless so there's nothing to
    invalidate server-side yet - the client is expected to discard the
    token on its end. This endpoint is the natural place to plug in a
    token-blacklist / refresh-token revocation later if that's added.
    """

    return {"message": "Logged out successfully."}


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Always returns the same generic message whether or not the email
    exists in the DB, so the API can't be used to enumerate registered
    accounts. The actual email is only sent when the account exists
    (checked inside AuthService.forgot_password).
    """

    AuthService.forgot_password(db=db, email=request.email)

    return {
        "message": "If an account exists for that email, a reset link is on its way."
    }


@router.post(
    "/reset-password",
    response_model=MessageResponse,
)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):

    success = AuthService.reset_password(
        db=db,
        token=request.token,
        new_password=request.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="This reset link is invalid or has expired.",
        )

    return {"message": "Password updated. You can now sign in."}