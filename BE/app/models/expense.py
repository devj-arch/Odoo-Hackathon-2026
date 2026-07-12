from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.utils.enums import ExpenseType


class Expense(BaseModel):
    __tablename__ = "expenses"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=True
    )
    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.id"),
        nullable=True
    )
    type: Mapped[ExpenseType] = mapped_column(Enum(ExpenseType), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    vehicle = relationship("Vehicle", back_populates="expenses")
    trip = relationship("Trip", back_populates="expenses")
