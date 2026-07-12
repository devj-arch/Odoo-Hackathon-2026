from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ── Request schemas ──────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=255)
    role_id: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ── Response schemas ─────────────────────────────────────────────────────────

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str  # role name (e.g. "Fleet Manager")
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
    role: str
