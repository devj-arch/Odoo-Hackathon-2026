from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Integer, DateTime
from datetime import datetime
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id")
    )

    role = relationship(
        "Role",
        back_populates="users"
    )

    

    failed_login_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    is_locked: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    reset_token: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    reset_token_expiry: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
