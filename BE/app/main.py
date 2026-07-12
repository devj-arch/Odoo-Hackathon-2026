import sys
from pathlib import Path

# Ensure BE/ is on sys.path so `app.*` imports work from any CWD
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, dashboard, drivers, expenses, fuel_logs, maintenance, trips, vehicles

app = FastAPI(title=settings.APP_NAME, docs_url="/docs", redoc_url="/redoc")

# CORS — lock to frontend origin in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(trips.router)
app.include_router(maintenance.router)
app.include_router(fuel_logs.router)
app.include_router(expenses.router)
app.include_router(dashboard.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
