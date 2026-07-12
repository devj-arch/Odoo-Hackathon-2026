"""
Test trip business rules (CLAUDE.md §4, rules #3–#9).

Each test verifies one business rule using the service layer directly
(in-memory SQLite, no network).
"""

from datetime import date, timedelta

import pytest

from app.models.driver import Driver
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.schemas.trip import TripComplete, TripCreate
from app.services import trip_service
from app.utils.enums import DriverStatus, TripStatus, VehicleStatus


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_vehicle(db, **kwargs):
    defaults = {
        "registration_number": "TEST-001",
        "model": "Transit-350",
        "type": "Van",
        "max_capacity": 500.0,
        "odometer": 10000.0,
        "acquisition_cost": 40000.0,
        "status": VehicleStatus.AVAILABLE,
    }
    defaults.update(kwargs)
    v = Vehicle(**defaults)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


def _make_driver(db, **kwargs):
    defaults = {
        "name": "Test Driver",
        "license_number": "DL-TEST-001",
        "license_category": "C",
        "license_expiry": date.today() + timedelta(days=365),
        "contact": "+1-555-0000",
        "safety_score": 90.0,
        "status": DriverStatus.AVAILABLE,
    }
    defaults.update(kwargs)
    d = Driver(**defaults)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


def _make_trip_data(vehicle_id, driver_id, **kwargs):
    defaults = {
        "source": "Warehouse A",
        "destination": "Store B",
        "vehicle_id": vehicle_id,
        "driver_id": driver_id,
        "cargo_weight": 300.0,
        "planned_distance": 100.0,
        "revenue": 500.0,
    }
    defaults.update(kwargs)
    return TripCreate(**defaults)


# ── Rule #6: Capacity exceeded ──────────────────────────────────────────────

def test_capacity_exceeded_blocks_creation(db_session):
    """Cargo weight > max_capacity must raise an error."""
    v = _make_vehicle(db_session, max_capacity=500.0)
    d = _make_driver(db_session)

    data = _make_trip_data(v.id, d.id, cargo_weight=600.0)
    with pytest.raises(Exception) as exc:
        trip_service.create_trip(db_session, data)
    assert "Capacity exceeded" in str(exc.value.detail)
    assert "100.0 kg" in str(exc.value.detail)


def test_capacity_within_limit_succeeds(db_session):
    """Cargo weight ≤ max_capacity should create the trip."""
    v = _make_vehicle(db_session, max_capacity=500.0)
    d = _make_driver(db_session)

    data = _make_trip_data(v.id, d.id, cargo_weight=450.0)
    trip = trip_service.create_trip(db_session, data)
    assert trip.status == TripStatus.DRAFT
    assert trip.cargo_weight == 450.0


# ── Rule #3: Retired / In Shop vehicles excluded ─────────────────────────────

def test_retired_vehicle_blocked(db_session):
    v = _make_vehicle(db_session, status=VehicleStatus.RETIRED)
    d = _make_driver(db_session)
    data = _make_trip_data(v.id, d.id)

    with pytest.raises(Exception) as exc:
        trip_service.create_trip(db_session, data)
    assert "Retired" in str(exc.value.detail)


def test_in_shop_vehicle_blocked(db_session):
    v = _make_vehicle(db_session, status=VehicleStatus.IN_SHOP)
    d = _make_driver(db_session)
    data = _make_trip_data(v.id, d.id)

    with pytest.raises(Exception) as exc:
        trip_service.create_trip(db_session, data)
    assert "In Shop" in str(exc.value.detail)


# ── Rule #4: Expired license / Suspended driver blocked ─────────────────────

def test_expired_license_blocked(db_session):
    v = _make_vehicle(db_session)
    d = _make_driver(db_session, license_expiry=date.today() - timedelta(days=1))
    data = _make_trip_data(v.id, d.id)

    with pytest.raises(Exception) as exc:
        trip_service.create_trip(db_session, data)
    assert "expired license" in str(exc.value.detail).lower()


def test_suspended_driver_blocked(db_session):
    v = _make_vehicle(db_session)
    d = _make_driver(db_session, status=DriverStatus.SUSPENDED)
    data = _make_trip_data(v.id, d.id)

    with pytest.raises(Exception) as exc:
        trip_service.create_trip(db_session, data)
    assert "suspended" in str(exc.value.detail).lower()


# ── Rule #5: Driver/Vehicle already On Trip blocked ─────────────────────────

def test_vehicle_on_trip_blocked(db_session):
    v = _make_vehicle(db_session, status=VehicleStatus.ON_TRIP)
    d = _make_driver(db_session)
    data = _make_trip_data(v.id, d.id)

    with pytest.raises(Exception) as exc:
        trip_service.create_trip(db_session, data)
    assert "already on a trip" in str(exc.value.detail).lower()


def test_driver_on_trip_blocked(db_session):
    v = _make_vehicle(db_session)
    d = _make_driver(db_session, status=DriverStatus.ON_TRIP)
    data = _make_trip_data(v.id, d.id)

    with pytest.raises(Exception) as exc:
        trip_service.create_trip(db_session, data)
    assert "already on a trip" in str(exc.value.detail).lower()


# ── Rule #7: Dispatch sets vehicle + driver → On Trip ────────────────────────

def test_dispatch_sets_statuses(db_session):
    v = _make_vehicle(db_session)
    d = _make_driver(db_session)
    data = _make_trip_data(v.id, d.id)

    trip = trip_service.create_trip(db_session, data)
    assert trip.status == TripStatus.DRAFT

    dispatched = trip_service.dispatch_trip(db_session, trip.id)
    assert dispatched.status == TripStatus.DISPATCHED
    assert dispatched.start_time is not None

    # Re-fetch vehicle and driver to confirm cascading status change
    db_session.refresh(v)
    db_session.refresh(d)
    assert v.status == VehicleStatus.ON_TRIP
    assert d.status == DriverStatus.ON_TRIP


# ── Rule #8: Complete sets vehicle + driver → Available ─────────────────────

def test_complete_sets_statuses(db_session):
    v = _make_vehicle(db_session)
    d = _make_driver(db_session)
    data = _make_trip_data(v.id, d.id)

    trip = trip_service.create_trip(db_session, data)
    trip_service.dispatch_trip(db_session, trip.id)

    completed = trip_service.complete_trip(
        db_session, trip.id, TripComplete(actual_distance=105.0)
    )
    assert completed.status == TripStatus.COMPLETED
    assert completed.actual_distance == 105.0
    assert completed.end_time is not None

    db_session.refresh(v)
    db_session.refresh(d)
    assert v.status == VehicleStatus.AVAILABLE
    assert d.status == DriverStatus.AVAILABLE


# ── Rule #9: Cancel restores vehicle + driver ────────────────────────────────

def test_cancel_dispatched_restores_statuses(db_session):
    v = _make_vehicle(db_session)
    d = _make_driver(db_session)
    data = _make_trip_data(v.id, d.id)

    trip = trip_service.create_trip(db_session, data)
    trip_service.dispatch_trip(db_session, trip.id)

    cancelled = trip_service.cancel_trip(db_session, trip.id)
    assert cancelled.status == TripStatus.CANCELLED

    db_session.refresh(v)
    db_session.refresh(d)
    assert v.status == VehicleStatus.AVAILABLE
    assert d.status == DriverStatus.AVAILABLE


def test_cancel_draft_does_not_need_restore(db_session):
    """Cancelling a Draft trip just sets status to Cancelled."""
    v = _make_vehicle(db_session)
    d = _make_driver(db_session)
    data = _make_trip_data(v.id, d.id)

    trip = trip_service.create_trip(db_session, data)
    cancelled = trip_service.cancel_trip(db_session, trip.id)
    assert cancelled.status == TripStatus.CANCELLED

    db_session.refresh(v)
    db_session.refresh(d)
    # Vehicle + driver were never On Trip, should still be Available
    assert v.status == VehicleStatus.AVAILABLE
    assert d.status == DriverStatus.AVAILABLE
