import os
import sys
from logging.config import fileConfig

# Ensure the BE directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import engine_from_config, pool

from alembic import context

# Alembic Config object
config = context.config

# Set up Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── Import our models so autogenerate can detect them ────────────────────────
from app.core.config import settings  # noqa: E402
from app.core.database import Base  # noqa: E402
from app.models.base import BaseModel  # noqa: F401 — ensures Base is populated
from app.models.driver import Driver  # noqa: F401
from app.models.expense import Expense  # noqa: F401
from app.models.fuel_log import FuelLog  # noqa: F401
from app.models.maintenance_log import MaintenanceLog  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.trip import Trip  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.vehicle import Vehicle  # noqa: F401

target_metadata = Base.metadata

# Override sqlalchemy.url from our settings (not hardcoded in alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
