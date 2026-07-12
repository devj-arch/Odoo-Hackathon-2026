from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.utils.enums import VehicleStatus


class VehicleCreate(BaseModel):
    registration_number: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)
    max_capacity: float = Field(..., gt=0)
    odometer: float = Field(default=0.0, ge=0)
    acquisition_cost: float = Field(default=0.0, ge=0)
    status: VehicleStatus = VehicleStatus.AVAILABLE


class VehicleUpdate(BaseModel):
    registration_number: Optional[str] = Field(None, min_length=1, max_length=50)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    max_capacity: Optional[float] = Field(None, gt=0)
    odometer: Optional[float] = Field(None, ge=0)
    acquisition_cost: Optional[float] = Field(None, ge=0)
    status: Optional[VehicleStatus] = None


class VehicleOut(BaseModel):
    id: int
    registration_number: str
    model: str
    type: str
    max_capacity: float
    odometer: float
    acquisition_cost: float
    status: VehicleStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
