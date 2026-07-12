import sys
from pathlib import Path

# Ensure BE/ is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.base import BaseModel  # noqa: F401
from app.models.driver import Driver  # noqa: F401
from app.models.expense import Expense  # noqa: F401
from app.models.fuel_log import FuelLog  # noqa: F401
from app.models.maintenance_log import MaintenanceLog  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.trip import Trip  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.vehicle import Vehicle  # noqa: F401


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh in-memory SQLite database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI test client with the test DB session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
