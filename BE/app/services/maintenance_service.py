"""
Maintenance service — vehicle status cascades.

Business rules (CLAUDE.md §4):
  10. Creating an active maintenance record sets vehicle → In Shop.
  11. Closing a maintenance record restores vehicle → Available
      (unless Retired).
"""

from datetime import date

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, NotFoundException, ValidationException
from app.models.maintenance_log import MaintenanceLog
from app.models.vehicle import Vehicle
from app.utils.enums import VehicleStatus


def open_maintenance(db: Session, data: dict) -> MaintenanceLog:
    """Create a maintenance record and set the vehicle to In Shop.

    Rule #10: Vehicle becomes In Shop, removing it from dispatch pool.
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == data["vehicle_id"]).first()
    if not vehicle:
        raise NotFoundException("Vehicle", data["vehicle_id"])

    if vehicle.status == VehicleStatus.RETIRED:
        raise ValidationException("Cannot open maintenance on a retired vehicle.")
    if vehicle.status == VehicleStatus.IN_SHOP:
        raise ConflictException(
            f"Vehicle '{vehicle.registration_number}' is already in maintenance."
        )
    if vehicle.status == VehicleStatus.ON_TRIP:
        raise ConflictException(
            f"Vehicle '{vehicle.registration_number}' is on a trip — wait for it to return."
        )

    log = MaintenanceLog(**data)
    vehicle.status = VehicleStatus.IN_SHOP

    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def close_maintenance(db: Session, log_id: int) -> MaintenanceLog:
    """Close a maintenance record and restore the vehicle to Available.

    Rule #11: Vehicle → Available unless Retired.
    """
    log = db.query(MaintenanceLog).filter(MaintenanceLog.id == log_id).first()
    if not log:
        raise NotFoundException("MaintenanceLog", log_id)

    if not log.is_active:
        raise ValidationException("Maintenance record is already closed.")

    vehicle = db.query(Vehicle).filter(Vehicle.id == log.vehicle_id).first()
    if not vehicle:
        raise NotFoundException("Vehicle", log.vehicle_id)

    log.end_date = date.today()

    # Rule #11: only set to Available if not retired
    if vehicle.status != VehicleStatus.RETIRED:
        vehicle.status = VehicleStatus.AVAILABLE

    db.commit()
    db.refresh(log)
    return log
