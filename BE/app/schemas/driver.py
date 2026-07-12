from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.utils.enums import DriverStatus


class DriverCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    license_number: str = Field(..., min_length=1, max_length=100)
    license_category: str = Field(..., min_length=1, max_length=50)
    license_expiry: date
    contact: str = Field(..., min_length=1, max_length=100)
    safety_score: float = Field(default=100.0, ge=0, le=100)
    status: DriverStatus = DriverStatus.AVAILABLE


class DriverUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    license_number: Optional[str] = Field(None, min_length=1, max_length=100)
    license_category: Optional[str] = Field(None, min_length=1, max_length=50)
    license_expiry: Optional[date] = None
    contact: Optional[str] = Field(None, min_length=1, max_length=100)
    safety_score: Optional[float] = Field(None, ge=0, le=100)
    status: Optional[DriverStatus] = None


class DriverOut(BaseModel):
    id: int
    name: str
    license_number: str
    license_category: str
    license_expiry: date
    contact: str
    safety_score: float
    status: DriverStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
