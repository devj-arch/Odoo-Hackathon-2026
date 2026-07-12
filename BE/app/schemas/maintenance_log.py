from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.vehicle import VehicleOut


class MaintenanceLogCreate(BaseModel):
    vehicle_id: int
    description: str = Field(..., min_length=1, max_length=255)
    maintenance_type: str = Field(..., min_length=1, max_length=100)
    cost: float = Field(default=0.0, ge=0)
    start_date: date
    notes: Optional[str] = None


class MaintenanceLogUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    maintenance_type: Optional[str] = Field(None, min_length=1, max_length=100)
    cost: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class MaintenanceLogOut(BaseModel):
    id: int
    vehicle_id: int
    description: str
    maintenance_type: str
    cost: float
    start_date: date
    end_date: Optional[date]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    vehicle: Optional[VehicleOut] = None

    model_config = {"from_attributes": True}
