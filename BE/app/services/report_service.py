"""
Report service — read-only aggregation queries for KPIs, costs, and ROI.

Business rules (CLAUDE.md §4):
  12. Operational cost per vehicle = Fuel logs + Maintenance logs
      (computed, not stored).
  13. Vehicle ROI = (Revenue − (Maintenance + Fuel)) / Acquisition Cost
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.fuel_log import FuelLog
from app.models.maintenance_log import MaintenanceLog
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.utils.enums import TripStatus, VehicleStatus


def get_dashboard_kpis(db: Session) -> dict:
    """Return the dashboard KPI card numbers."""
    total_vehicles = db.query(func.count(Vehicle.id)).scalar()
    active_vehicles = db.query(func.count(Vehicle.id)).filter(
        Vehicle.status == VehicleStatus.ON_TRIP
    ).scalar()
    available_vehicles = db.query(func.count(Vehicle.id)).filter(
        Vehicle.status == VehicleStatus.AVAILABLE
    ).scalar()
    in_maintenance = db.query(func.count(Vehicle.id)).filter(
        Vehicle.status == VehicleStatus.IN_SHOP
    ).scalar()

    active_trips = db.query(func.count(Trip.id)).filter(
        Trip.status == TripStatus.DISPATCHED
    ).scalar()
    pending_trips = db.query(func.count(Trip.id)).filter(
        Trip.status == TripStatus.DRAFT
    ).scalar()

    # Drivers on duty = Available + On Trip (not Off Duty or Suspended)
    from app.models.driver import Driver
    from app.utils.enums import DriverStatus

    drivers_on_duty = db.query(func.count(Driver.id)).filter(
        Driver.status.in_([DriverStatus.AVAILABLE, DriverStatus.ON_TRIP])
    ).scalar()

    # Fleet utilization: active / non-retired vehicles
    non_retired = db.query(func.count(Vehicle.id)).filter(
        Vehicle.status != VehicleStatus.RETIRED
    ).scalar()
    utilization_pct = round((active_vehicles / non_retired * 100), 1) if non_retired else 0.0

    return {
        "total_vehicles": total_vehicles or 0,
        "active_vehicles": active_vehicles or 0,
        "available_vehicles": available_vehicles or 0,
        "vehicles_in_maintenance": in_maintenance or 0,
        "active_trips": active_trips or 0,
        "pending_trips": pending_trips or 0,
        "drivers_on_duty": drivers_on_duty or 0,
        "fleet_utilization_pct": utilization_pct,
    }


def get_operational_cost(db: Session, vehicle_id: int) -> dict:
    """Compute total operational cost for a vehicle (Rule #12)."""
    fuel_total = (
        db.query(func.coalesce(func.sum(FuelLog.cost), 0))
        .filter(FuelLog.vehicle_id == vehicle_id)
        .scalar()
    )
    maintenance_total = (
        db.query(func.coalesce(func.sum(MaintenanceLog.cost), 0))
        .filter(MaintenanceLog.vehicle_id == vehicle_id)
        .scalar()
    )
    expense_total = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.vehicle_id == vehicle_id)
        .scalar()
    )

    return {
        "vehicle_id": vehicle_id,
        "fuel_cost": float(fuel_total or 0),
        "maintenance_cost": float(maintenance_total or 0),
        "other_expenses": float(expense_total or 0),
        "total_operational_cost": float((fuel_total or 0) + (maintenance_total or 0) + (expense_total or 0)),
    }


def get_vehicle_roi(db: Session, vehicle_id: int) -> dict:
    """Compute ROI for a vehicle (Rule #13).

    ROI = (Revenue − (Maintenance + Fuel)) / Acquisition Cost
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        return {"vehicle_id": vehicle_id, "roi": 0.0, "error": "Vehicle not found"}

    total_revenue = (
        db.query(func.coalesce(func.sum(Trip.revenue), 0))
        .filter(Trip.vehicle_id == vehicle_id, Trip.status == TripStatus.COMPLETED)
        .scalar()
    )
    fuel_cost = (
        db.query(func.coalesce(func.sum(FuelLog.cost), 0))
        .filter(FuelLog.vehicle_id == vehicle_id)
        .scalar()
    )
    maintenance_cost = (
        db.query(func.coalesce(func.sum(MaintenanceLog.cost), 0))
        .filter(MaintenanceLog.vehicle_id == vehicle_id)
        .scalar()
    )

    total_costs = (fuel_cost or 0) + (maintenance_cost or 0)
    net_return = (total_revenue or 0) - total_costs

    if vehicle.acquisition_cost and vehicle.acquisition_cost > 0:
        roi = round((net_return / vehicle.acquisition_cost) * 100, 2)
    else:
        roi = 0.0

    return {
        "vehicle_id": vehicle_id,
        "registration_number": vehicle.registration_number,
        "total_revenue": float(total_revenue or 0),
        "total_costs": float(total_costs),
        "net_return": float(net_return),
        "acquisition_cost": float(vehicle.acquisition_cost),
        "roi_pct": roi,
    }


def get_fuel_efficiency(db: Session, vehicle_id: int) -> dict:
    """Compute fuel efficiency (distance / fuel) for a vehicle."""
    total_distance = (
        db.query(func.coalesce(func.sum(Trip.actual_distance), 0))
        .filter(Trip.vehicle_id == vehicle_id, Trip.status == TripStatus.COMPLETED)
        .scalar()
    )
    total_fuel = (
        db.query(func.coalesce(func.sum(FuelLog.liters), 0))
        .filter(FuelLog.vehicle_id == vehicle_id)
        .scalar()
    )

    if total_fuel and total_fuel > 0:
        efficiency = round(float(total_distance) / float(total_fuel), 2)
    else:
        efficiency = 0.0

    return {
        "vehicle_id": vehicle_id,
        "total_distance_km": float(total_distance or 0),
        "total_fuel_liters": float(total_fuel or 0),
        "fuel_efficiency_km_per_liter": efficiency,
    }
