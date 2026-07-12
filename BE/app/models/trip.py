from sqlalchemy import Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.utils.enums import TripStatus


class Trip(BaseModel):
    __tablename__ = "trips"

    source: Mapped[str] = mapped_column(String(150), nullable=False)
    destination: Mapped[str] = mapped_column(String(150), nullable=False)
    cargo_weight: Mapped[float] = mapped_column(Float, default=0)  # kg
    distance: Mapped[float] = mapped_column(Float, default=0)  # km
    odometer_start: Mapped[float] = mapped_column(Float, nullable=True)
    odometer_end: Mapped[float] = mapped_column(Float, nullable=True)
    fuel_consumed: Mapped[float] = mapped_column(Float, nullable=True)  # liters
    status: Mapped[TripStatus] = mapped_column(
        Enum(TripStatus),
        default=TripStatus.DRAFT,
        nullable=False
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=False
    )
    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id"),
        nullable=False
    )

    vehicle = relationship("Vehicle", back_populates="trips")
    driver = relationship("Driver", back_populates="trips")
    expenses = relationship("Expense", back_populates="trip")
