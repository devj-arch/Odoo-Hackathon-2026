from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    vehicle_id: int
    trip_id: Optional[int] = None
    description: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)
    expense_date: date
    category: str = Field(..., min_length=1, max_length=100)


class ExpenseOut(BaseModel):
    id: int
    vehicle_id: int
    trip_id: Optional[int]
    description: str
    amount: float
    expense_date: date
    category: str
    created_at: datetime

    model_config = {"from_attributes": True}
