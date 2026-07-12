from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.utils.enums import TripStatus


class Trip(BaseModel):
    __tablename__ = "trips"

    source: Mapped[str] = mapped_column(String(255), nullable=False)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo_weight: Mapped[float] = mapped_column(Float, nullable=False)
    planned_distance: Mapped[float] = mapped_column(Float, nullable=False)
    actual_distance: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)

    status: Mapped[TripStatus] = mapped_column(Enum(TripStatus), nullable=False, default=TripStatus.DRAFT)

    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=False)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), nullable=False)

    # Relationships
    vehicle = relationship("Vehicle", lazy="joined")
    driver = relationship("Driver", lazy="joined")

    def __repr__(self) -> str:
        return f"<Trip(id={self.id}, status='{self.status}', vehicle={self.vehicle_id})>"
