# TransitOps

A centralized fleet operations platform that replaces spreadsheets and paper logbooks with one console for vehicle, driver, dispatch, maintenance, and expense management.

![TransitOps Login](images/login-screen.png)

## The Problem It Solves

Transport and logistics teams commonly run operations out of scattered spreadsheets, which leads to double-booked vehicles, drivers dispatched on expired licenses, missed maintenance windows, inaccurate cost tracking, and no real-time visibility into fleet health. TransitOps digitizes the full transport lifecycle — from registering a vehicle to closing out a trip — and enforces the business rules that spreadsheets can't:

- Vehicles that are `Retired` or `In Shop` are automatically excluded from dispatch.
- Drivers with expired licenses or a `Suspended` status can't be assigned to trips.
- A vehicle or driver already `On Trip` can't be double-booked.
- Cargo weight is validated against a vehicle's maximum load capacity before dispatch.
- Dispatching, completing, and cancelling a trip automatically flips vehicle/driver status (`Available` ↔ `On Trip`).
- Opening a maintenance record automatically moves a vehicle to `In Shop`; closing it restores `Available`.
- Dashboards and reports (fuel efficiency, fleet utilization, operational cost, vehicle ROI) are computed from live trip, fuel, and maintenance data instead of manual reconciliation.

Role-based access (Fleet Manager, Dispatcher/Driver, Safety Officer, Financial Analyst) ensures each user only sees and acts on what's relevant to their job.

![Driver Management screen](images/driver-management.png)

## Tech Stack

**Frontend**
- React 19 + React Router 7
- Vite 8 (build tool / dev server)
- Tailwind CSS 4

**Backend**
- FastAPI (Python)
- SQLAlchemy 2 ORM + Alembic (migrations)
- PostgreSQL (via `psycopg2`)
- JWT-based authentication (`python-jose`, `passlib`, `bcrypt`)
- Pydantic v2 for request/response validation
- Uvicorn as the ASGI server

## Project Structure

```
Odoo-Hackathon-2026-main/
├── BE/                     # FastAPI backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy models (User, Vehicle, Driver, Trip, Maintenance, FuelLog, Expense, Role)
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── routers/        # API routes (auth, vehicles, drivers, trips, maintenance, fuel_logs, expenses, dashboard)
│   │   ├── services/       # Business logic (trip, maintenance, report, auth services)
│   │   ├── repository/     # Data access layer
│   │   ├── core/           # config, database session, security
│   │   └── seed/           # demo data seeding
│   ├── alembic/             # DB migrations
│   └── requirements.txt
└── FE/                      # React frontend
    ├── src/
    │   ├── pages/           # Dashboard, VehicleRegistry, DriverManagement, TripDispatcher, MaintenanceLog, FuelExpenseManagement, Reports, Login
    │   ├── components/      # Sidebar, Modal, ProtectedRoute, FormField, RouteMap, etc.
    │   └── lib/              # api client, auth helpers, roles, formatting
    └── package.json
```

## Setup

### Prerequisites
- Node.js (18+ recommended)
- Python 3.10+
- PostgreSQL running locally or a hosted connection string

### 1. Clone and enter the project
```bash
git clone <repo-url>
cd Odoo-Hackathon-2026-main
```

### 2. Backend setup
```bash
cd BE
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then fill in .env:
#   DATABASE_URL=postgresql://user:password@localhost:5432/transitops
#   SECRET_KEY=<a-long-random-string>
#   FRONTEND_URL=http://localhost:5173
#   (SMTP_* values only needed if you're testing email features)

python create_tables.py       # creates tables from the models
python seed.py                # optional: loads demo data (vehicles, drivers, the Van-05/Alex example trip)

uvicorn app.main:app --reload --port 8000
```
The API will be live at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### 3. Frontend setup
```bash
cd ../FE
npm install

cp .env.example .env
# VITE_API_URL=http://localhost:8000

npm run dev
```
The app will be live at `http://localhost:5173`.

### 4. Log in
Use a seeded account (see `BE/app/seed/seed.py`) or register a user via the `/auth` endpoints, then sign in from the console, selecting the role matching your account (Fleet Manager, Dispatcher, Safety Officer, or Financial Analyst).

## Core Modules

| Module | What it does |
|---|---|
| **Dashboard** | KPIs — active/available vehicles, vehicles in maintenance, active/pending trips, drivers on duty, fleet utilization % |
| **Vehicle Registry** | CRUD for vehicles with unique registration numbers, load capacity, odometer, acquisition cost, and status |
| **Driver Management** | Driver profiles with license category/expiry, safety score, and status |
| **Trips** | Create and dispatch trips with automatic vehicle/driver/cargo validation |
| **Maintenance** | Log and close maintenance records, with automatic vehicle status transitions |
| **Fuel & Expenses** | Track fuel logs and other costs, rolled up into per-vehicle operational cost |
| **Reports** | Fuel efficiency, fleet utilization, operational cost, and vehicle ROI, with CSV export |