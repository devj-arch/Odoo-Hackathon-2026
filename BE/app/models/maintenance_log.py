from datetime import date
from typing import Optional

from sqlalchemy import Date, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class MaintenanceLog(BaseModel):
    __tablename__ = "maintenance_logs"

    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    maintenance_type: Mapped[str] = mapped_column(String(100), nullable=False)
    cost: Mapped[float] = mapped_column(Float, default=0.0)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    vehicle = relationship("Vehicle", lazy="joined")

    @property
    def is_active(self) -> bool:
        """A maintenance record is active if it has no end_date."""
        return self.end_date is None

    def __repr__(self) -> str:
        return f"<MaintenanceLog(id={self.id}, type='{self.maintenance_type}', active={self.is_active})>"
