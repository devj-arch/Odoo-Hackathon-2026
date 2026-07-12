from sqlalchemy import Enum, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel
from app.utils.enums import VehicleStatus


class Vehicle(BaseModel):
    __tablename__ = "vehicles"

    registration_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    max_capacity: Mapped[float] = mapped_column(Float, nullable=False)
    odometer: Mapped[float] = mapped_column(Float, default=0.0)
    acquisition_cost: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[VehicleStatus] = mapped_column(Enum(VehicleStatus), nullable=False, default=VehicleStatus.AVAILABLE)

    def __repr__(self) -> str:
        return f"<Vehicle(id={self.id}, reg='{self.registration_number}', status='{self.status}')>"
