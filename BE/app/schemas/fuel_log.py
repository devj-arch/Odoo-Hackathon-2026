from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class FuelLogCreate(BaseModel):
    vehicle_id: int
    trip_id: Optional[int] = None
    liters: float = Field(..., gt=0)
    cost: float = Field(..., gt=0)
    fuel_date: date


class FuelLogOut(BaseModel):
    id: int
    vehicle_id: int
    trip_id: Optional[int]
    liters: float
    cost: float
    fuel_date: date
    created_at: datetime

    model_config = {"from_attributes": True}
