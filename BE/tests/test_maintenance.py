"""
Test maintenance business rules (CLAUDE.md §4, rules #10–#11).

Rule #10: Creating active maintenance → vehicle In Shop.
Rule #11: Closing maintenance → vehicle Available (unless Retired).
"""

from datetime import date

import pytest

from app.models.maintenance_log import MaintenanceLog
from app.models.vehicle import Vehicle
from app.services import maintenance_service
from app.utils.enums import VehicleStatus


def _make_vehicle(db, **kwargs):
    defaults = {
        "registration_number": "MAINT-001",
        "model": "Transit-350",
        "type": "Van",
        "max_capacity": 500.0,
        "odometer": 50000.0,
        "acquisition_cost": 40000.0,
        "status": VehicleStatus.AVAILABLE,
    }
    defaults.update(kwargs)
    v = Vehicle(**defaults)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


# ── Rule #10: Open maintenance → In Shop ────────────────────────────────────

def test_open_maintenance_sets_vehicle_in_shop(db_session):
    v = _make_vehicle(db_session)
    data = {
        "vehicle_id": v.id,
        "description": "Oil change",
        "maintenance_type": "Oil Change",
        "cost": 150.0,
        "start_date": date.today(),
    }

    log = maintenance_service.open_maintenance(db_session, data)
    assert log.is_active is True

    db_session.refresh(v)
    assert v.status == VehicleStatus.IN_SHOP


def test_open_maintenance_on_retired_vehicle_blocked(db_session):
    v = _make_vehicle(db_session, status=VehicleStatus.RETIRED)
    data = {
        "vehicle_id": v.id,
        "description": "Oil change",
        "maintenance_type": "Oil Change",
        "cost": 150.0,
        "start_date": date.today(),
    }

    with pytest.raises(Exception) as exc:
        maintenance_service.open_maintenance(db_session, data)
    assert "retired" in str(exc.value.detail).lower()


def test_open_maintenance_on_in_shop_vehicle_blocked(db_session):
    v = _make_vehicle(db_session, status=VehicleStatus.IN_SHOP)
    data = {
        "vehicle_id": v.id,
        "description": "Brake job",
        "maintenance_type": "Brake Replacement",
        "cost": 800.0,
        "start_date": date.today(),
    }

    with pytest.raises(Exception) as exc:
        maintenance_service.open_maintenance(db_session, data)
    assert "already in maintenance" in str(exc.value.detail).lower()


# ── Rule #11: Close maintenance → Available (unless Retired) ────────────────

def test_close_maintenance_restores_available(db_session):
    v = _make_vehicle(db_session)
    data = {
        "vehicle_id": v.id,
        "description": "Oil change",
        "maintenance_type": "Oil Change",
        "cost": 150.0,
        "start_date": date.today(),
    }

    log = maintenance_service.open_maintenance(db_session, data)
    db_session.refresh(v)
    assert v.status == VehicleStatus.IN_SHOP

    closed = maintenance_service.close_maintenance(db_session, log.id)
    assert closed.is_active is False
    assert closed.end_date is not None

    db_session.refresh(v)
    assert v.status == VehicleStatus.AVAILABLE


def test_close_maintenance_on_retired_stays_retired(db_session):
    """Rule #11: If vehicle has been retired while in maintenance,
    closing the log should NOT set it to Available."""
    v = _make_vehicle(db_session)
    data = {
        "vehicle_id": v.id,
        "description": "Oil change",
        "maintenance_type": "Oil Change",
        "cost": 150.0,
        "start_date": date.today(),
    }

    log = maintenance_service.open_maintenance(db_session, data)
    # Manually retire the vehicle while it's in the shop
    v.status = VehicleStatus.RETIRED
    db_session.commit()

    closed = maintenance_service.close_maintenance(db_session, log.id)
    assert closed.is_active is False

    db_session.refresh(v)
    # Must stay Retired, not flip to Available
    assert v.status == VehicleStatus.RETIRED
