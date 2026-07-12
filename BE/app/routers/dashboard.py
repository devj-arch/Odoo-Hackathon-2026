"""Dashboard and reporting endpoints — read-only aggregation."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import require_roles
from app.services import report_service
from app.utils.enums import Role


router = APIRouter(prefix="/dashboard", tags=["dashboard"], dependencies=[
    Depends(
        require_roles(
            Role.DISPATCHER.value,
            Role.FINANCIAL_ANALYST.value,
        )
    )
],)



@router.get("/kpis")
def get_kpis(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            Role.FLEET_MANAGER.value,
            Role.DISPATCHER.value,
            Role.SAFETY_OFFICER.value,
            Role.FINANCIAL_ANALYST.value,
        )
    ),
):
    """Dashboard KPI cards: vehicle counts, trip counts, utilization."""
    return report_service.get_dashboard_kpis(db)


@router.get("/vehicles/{vehicle_id}/operational-cost")
def get_vehicle_operational_cost(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            Role.FLEET_MANAGER.value,
            Role.DISPATCHER.value,
            Role.SAFETY_OFFICER.value,
            Role.FINANCIAL_ANALYST.value,
        )
    ),
):
    """Total operational cost breakdown for a vehicle."""
    return report_service.get_operational_cost(db, vehicle_id)


@router.get("/vehicles/{vehicle_id}/roi")
def get_vehicle_roi(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            Role.FLEET_MANAGER.value,
            Role.DISPATCHER.value,
            Role.SAFETY_OFFICER.value,
            Role.FINANCIAL_ANALYST.value,
        )
    ),
):
    """ROI calculation for a vehicle."""
    return report_service.get_vehicle_roi(db, vehicle_id)


@router.get("/vehicles/{vehicle_id}/fuel-efficiency")
def get_vehicle_fuel_efficiency(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            Role.FLEET_MANAGER.value,
            Role.DISPATCHER.value,
            Role.SAFETY_OFFICER.value,
            Role.FINANCIAL_ANALYST.value,
        )
    ),
):
    """Fuel efficiency (km/L) for a vehicle."""
    return report_service.get_fuel_efficiency(db, vehicle_id)
