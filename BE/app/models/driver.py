from datetime import date

from sqlalchemy import Date, Enum, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.utils.enums import DriverStatus


class Driver(BaseModel):
    __tablename__ = "drivers"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    license_no: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
    license_category: Mapped[str] = mapped_column(String(20), nullable=False)
    license_expiry: Mapped[date] = mapped_column(Date, nullable=False)
    contact: Mapped[str] = mapped_column(String(30), nullable=True)
    safety_score: Mapped[float] = mapped_column(Float, default=100)
    status: Mapped[DriverStatus] = mapped_column(
        Enum(DriverStatus),
        default=DriverStatus.AVAILABLE,
        nullable=False
    )

    trips = relationship("Trip", back_populates="driver")
