from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.driver import DriverOut
from app.schemas.vehicle import VehicleOut
from app.utils.enums import TripStatus


# ── Request schemas ──────────────────────────────────────────────────────────

class TripCreate(BaseModel):
    """Create a new trip in Draft status."""

    source: str = Field(..., min_length=1, max_length=255)
    destination: str = Field(..., min_length=1, max_length=255)
    vehicle_id: int
    driver_id: int
    cargo_weight: float = Field(..., gt=0)
    planned_distance: float = Field(..., gt=0)
    revenue: float = Field(default=0.0, ge=0)


class TripComplete(BaseModel):
    """Data required to complete a dispatched trip."""

    actual_distance: float = Field(..., gt=0)


# ── Response schemas ─────────────────────────────────────────────────────────

class TripOut(BaseModel):
    id: int
    source: str
    destination: str
    vehicle_id: int
    driver_id: int
    cargo_weight: float
    planned_distance: float
    actual_distance: Optional[float]
    revenue: float
    status: TripStatus
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    # Nested objects for display
    vehicle: Optional[VehicleOut] = None
    driver: Optional[DriverOut] = None

    model_config = {"from_attributes": True}


class TripListOut(BaseModel):
    """Lightweight trip list item — no nested objects."""

    id: int
    source: str
    destination: str
    vehicle_id: int
    driver_id: int
    cargo_weight: float
    planned_distance: float
    actual_distance: Optional[float]
    revenue: float
    status: TripStatus
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}