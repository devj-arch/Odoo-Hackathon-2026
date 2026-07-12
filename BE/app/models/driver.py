from datetime import date

from sqlalchemy import Date, Enum, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel
from app.utils.enums import DriverStatus


class Driver(BaseModel):
    __tablename__ = "drivers"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    license_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    license_category: Mapped[str] = mapped_column(String(50), nullable=False)
    license_expiry: Mapped[date] = mapped_column(Date, nullable=False)
    contact: Mapped[str] = mapped_column(String(100), nullable=False)
    safety_score: Mapped[float] = mapped_column(Float, default=100.0)
    status: Mapped[DriverStatus] = mapped_column(Enum(DriverStatus), nullable=False, default=DriverStatus.AVAILABLE)

    def __repr__(self) -> str:
        return f"<Driver(id={self.id}, name='{self.name}', status='{self.status}')>"
