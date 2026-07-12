"""
Trip service — all business logic for trip lifecycle.

Business rules enforced here (numbers match CLAUDE.md §4):
  3. Retired / In Shop vehicles excluded from dispatch.
  4. Expired license / Suspended drivers excluded from dispatch.
  5. Driver or vehicle already On Trip cannot be assigned.
  6. Cargo weight must not exceed vehicle max_capacity.
  7. Dispatch atomically sets vehicle + driver → On Trip.
  8. Complete atomically sets vehicle + driver → Available,
     records actual_distance + end_time.
  9. Cancel a dispatched trip restores vehicle + driver → Available.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import (
    CapacityExceededException,
    ConflictException,
    NotFoundException,
    ValidationException,
)
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.schemas.trip import TripComplete, TripCreate
from app.utils.enums import DriverStatus, TripStatus, VehicleStatus


# ── Validation helpers ───────────────────────────────────────────────────────

def _get_vehicle(db: Session, vehicle_id: int) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise NotFoundException("Vehicle", vehicle_id)
    return vehicle


def _get_driver(db: Session, driver_id: int) -> Driver:
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise NotFoundException("Driver", driver_id)
    return driver


# ── Trip creation ────────────────────────────────────────────────────────────

def create_trip(db: Session, data: TripCreate) -> Trip:
    """Create a new trip in Draft status after running all validations."""

    vehicle = _get_vehicle(db, data.vehicle_id)
    driver = _get_driver(db, data.driver_id)

    # Rule #3: Retired or In Shop vehicles never appear in dispatch selection
    if vehicle.status in (VehicleStatus.RETIRED, VehicleStatus.IN_SHOP):
        raise ValidationException(
            f"Vehicle '{vehicle.registration_number}' is {vehicle.status.value} and cannot be assigned.",
        )

    # Rule #4: Drivers with expired license or Suspended cannot be assigned
    today = datetime.now(timezone.utc).date()
    if driver.license_expiry < today:
        raise ValidationException(
            f"Driver '{driver.name}' has an expired license (expired {driver.license_expiry}).",
        )
    if driver.status == DriverStatus.SUSPENDED:
        raise ValidationException(
            f"Driver '{driver.name}' is suspended and cannot be assigned.",
        )

    # Rule #5: A driver or vehicle already On Trip cannot be assigned to another
    if vehicle.status == VehicleStatus.ON_TRIP:
        raise ConflictException(
            f"Vehicle '{vehicle.registration_number}' is already on a trip.",
        )
    if driver.status == DriverStatus.ON_TRIP:
        raise ConflictException(
            f"Driver '{driver.name}' is already on a trip.",
        )

    # Rule #6: cargo_weight must not exceed vehicle max_capacity
    if data.cargo_weight > vehicle.max_capacity:
        excess = data.cargo_weight - vehicle.max_capacity
        raise CapacityExceededException(excess)

    trip = Trip(**data.model_dump())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


# ── Trip lifecycle actions ───────────────────────────────────────────────────

def dispatch_trip(db: Session, trip_id: int) -> Trip:
    """Dispatch a Draft trip → Dispatched.

    Rule #7: Atomically sets vehicle + driver status → On Trip.
    Re-runs all validation checks in case the world changed since Draft.
    """
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException("Trip", trip_id)

    if trip.status != TripStatus.DRAFT:
        raise ValidationException(
            f"Only Draft trips can be dispatched. Current status: {trip.status.value}.",
        )

    vehicle = _get_vehicle(db, trip.vehicle_id)
    driver = _get_driver(db, trip.driver_id)

    # Re-validate (rules #3–#6)
    if vehicle.status in (VehicleStatus.RETIRED, VehicleStatus.IN_SHOP):
        raise ValidationException(
            f"Vehicle '{vehicle.registration_number}' is {vehicle.status.value}.",
        )

    today = datetime.now(timezone.utc).date()
    if driver.license_expiry < today:
        raise ValidationException(
            f"Driver '{driver.name}' license expired on {driver.license_expiry}.",
        )
    if driver.status == DriverStatus.SUSPENDED:
        raise ValidationException(f"Driver '{driver.name}' is suspended.")
    if driver.status == DriverStatus.ON_TRIP:
        raise ConflictException(f"Driver '{driver.name}' is already on a trip.")
    if vehicle.status == VehicleStatus.ON_TRIP:
        raise ConflictException(
            f"Vehicle '{vehicle.registration_number}' is already on a trip.",
        )

    if trip.cargo_weight > vehicle.max_capacity:
        excess = trip.cargo_weight - vehicle.max_capacity
        raise CapacityExceededException(excess)

    # Atomic update: trip, vehicle, driver in one transaction
    trip.status = TripStatus.DISPATCHED
    trip.start_time = datetime.now(timezone.utc)
    vehicle.status = VehicleStatus.ON_TRIP
    driver.status = DriverStatus.ON_TRIP

    db.commit()
    db.refresh(trip)
    return trip


def complete_trip(db: Session, trip_id: int, data: TripComplete) -> Trip:
    """Complete a Dispatched trip → Completed.

    Rule #8: Atomically sets vehicle + driver → Available,
    records actual_distance + end_time.
    """
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException("Trip", trip_id)

    if trip.status != TripStatus.DISPATCHED:
        raise ValidationException(
            f"Only Dispatched trips can be completed. Current status: {trip.status.value}.",
        )

    vehicle = _get_vehicle(db, trip.vehicle_id)
    driver = _get_driver(db, trip.driver_id)

    # Atomic update
    trip.status = TripStatus.COMPLETED
    trip.actual_distance = data.actual_distance
    trip.end_time = datetime.now(timezone.utc)
    vehicle.status = VehicleStatus.AVAILABLE
    driver.status = DriverStatus.AVAILABLE

    db.commit()
    db.refresh(trip)
    return trip


def cancel_trip(db: Session, trip_id: int) -> Trip:
    """Cancel a trip.

    Rule #9: If the trip was Dispatched, restores vehicle + driver → Available.
    Draft trips are simply cancelled without status changes.
    """
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException("Trip", trip_id)

    if trip.status not in (TripStatus.DRAFT, TripStatus.DISPATCHED):
        raise ValidationException(
            f"Cannot cancel a trip with status '{trip.status.value}'.",
        )

    # Restore vehicle and driver if the trip was already dispatched
    if trip.status == TripStatus.DISPATCHED:
        vehicle = _get_vehicle(db, trip.vehicle_id)
        driver = _get_driver(db, trip.driver_id)
        vehicle.status = VehicleStatus.AVAILABLE
        driver.status = DriverStatus.AVAILABLE

    trip.status = TripStatus.CANCELLED
    db.commit()
    db.refresh(trip)
    return trip
