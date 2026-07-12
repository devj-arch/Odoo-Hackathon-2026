from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.fuel_log import FuelLog
from app.schemas.fuel_log import FuelLogCreate, FuelLogOut

router = APIRouter(prefix="/fuel-logs", tags=["fuel-logs"])


@router.get("/", response_model=list[FuelLogOut])
def list_fuel_logs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List all fuel logs."""
    return db.query(FuelLog).order_by(FuelLog.created_at.desc()).all()


@router.get("/{log_id}", response_model=FuelLogOut)
def get_fuel_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Get a single fuel log by ID."""
    log = db.query(FuelLog).filter(FuelLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fuel log not found.")
    return log


@router.post("/", response_model=FuelLogOut, status_code=status.HTTP_201_CREATED)
def create_fuel_log(
    data: FuelLogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Log a fuel purchase."""
    log = FuelLog(**data.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fuel_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a fuel log."""
    log = db.query(FuelLog).filter(FuelLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fuel log not found.")
    db.delete(log)
    db.commit()
