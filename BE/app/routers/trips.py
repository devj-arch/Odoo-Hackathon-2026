from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import AppException
from app.dependencies.auth import require_roles
from app.models.trip import Trip
from app.schemas.trip import TripComplete, TripCreate, TripListOut, TripOut
from app.services import trip_service
from app.utils.enums import Role

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("/", response_model=list[TripListOut])
def list_trips(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(Role.DISPATCHER.value)),
):
    """List all trips."""
    return db.query(Trip).order_by(Trip.created_at.desc()).all()


@router.get("/{trip_id}", response_model=TripOut)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(Role.DISPATCHER.value)),
):
    """Get a single trip by ID, including nested vehicle/driver."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found.")
    return trip


@router.post("/", response_model=TripOut, status_code=status.HTTP_201_CREATED)
def create_trip(
    data: TripCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(Role.DISPATCHER.value)),
):
    """Create a new trip in Draft status.

    Runs all pre-dispatch validations (vehicle availability, driver license,
    capacity check, etc.) so the user sees errors before they try to dispatch.
    """
    try:
        trip = trip_service.create_trip(db, data)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return trip


@router.post("/{trip_id}/dispatch", response_model=TripOut)
def dispatch_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(Role.DISPATCHER.value)),
):
    """Dispatch a Draft trip — vehicle and driver set to On Trip."""
    try:
        trip = trip_service.dispatch_trip(db, trip_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return trip


@router.post("/{trip_id}/complete", response_model=TripOut)
def complete_trip(
    trip_id: int,
    data: TripComplete,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(Role.DISPATCHER.value)),
):
    """Complete a Dispatched trip — vehicle and driver set back to Available."""
    try:
        trip = trip_service.complete_trip(db, trip_id, data)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return trip


@router.post("/{trip_id}/cancel", response_model=TripOut)
def cancel_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(Role.DISPATCHER.value)),
):
    """Cancel a trip. Restores vehicle/driver if already dispatched."""
    try:
        trip = trip_service.cancel_trip(db, trip_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return trip
