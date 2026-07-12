from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}')>"
