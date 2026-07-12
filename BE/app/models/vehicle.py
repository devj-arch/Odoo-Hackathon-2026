from sqlalchemy import Enum, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.utils.enums import VehicleStatus


class Vehicle(BaseModel):
    __tablename__ = "vehicles"

    reg_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[float] = mapped_column(Float, nullable=False)  # max load in kg
    odometer: Mapped[float] = mapped_column(Float, default=0)
    acquisition_cost: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[VehicleStatus] = mapped_column(
        Enum(VehicleStatus),
        default=VehicleStatus.AVAILABLE,
        nullable=False
    )

    trips = relationship("Trip", back_populates="vehicle")
    maintenance_logs = relationship("MaintenanceLog", back_populates="vehicle")
    fuel_logs = relationship("FuelLog", back_populates="vehicle")
    expenses = relationship("Expense", back_populates="vehicle")
