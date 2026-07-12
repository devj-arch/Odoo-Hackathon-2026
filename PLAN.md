<div align="center">

# � TransitOps

### Smart Transport Operations Platform

A centralized platform to manage the full lifecycle of transport operations —
vehicles, drivers, dispatch, maintenance, fuel, and analytics — with
business rules and role-based access enforced end to end.

`FastAPI` · `PostgreSQL` · `SQLAlchemy` · `React` · `TailwindCSS`

</div>

---

## 1. Overview

Logistics teams still run on spreadsheets and paper logbooks, which leads to
scheduling conflicts, idle vehicles, missed maintenance, expired licenses, and
no clear view of cost. **TransitOps** replaces that with one system where every
vehicle, driver, and trip has a defined status, and the rules that connect them
are enforced automatically.

The platform serves four roles:

| Role | Responsibility |
|:--|:--|
| **Fleet Manager** | Vehicle lifecycle, maintenance, operational efficiency |
| **Dispatcher** | Creates trips, assigns vehicles & drivers, monitors deliveries |
| **Safety Officer** | Driver compliance, license validity, safety scores |
| **Financial Analyst** | Operational expenses, fuel cost, maintenance cost, ROI |

---

## 2. Core Idea

TransitOps is built around a simple principle: **the system is a state machine
over vehicle and driver status.** Nearly every requirement is an automatic
status change that happens when an action is taken.

```
 VEHICLE   Available ──dispatch──▶ On Trip ──complete / cancel──▶ Available
           Available ──maintenance─▶ In Shop ──close──────────▶ Available
           Available ──────────────▶ Retired

 DRIVER    Available ──dispatch──▶ On Trip ──complete / cancel──▶ Available

 TRIP      Draft ──▶ Dispatched ──▶ Completed
                          └───────▶ Cancelled
```

To keep this reliable, **all status logic lives in the backend service layer**
(`services/`). Routes stay thin, services own the rules, and any change that
touches a vehicle, driver, and trip together happens in a single transaction —
so the data can never end up half-updated.

---

## 3. Architecture

```
        React (Vite + Tailwind)                FastAPI
   ┌──────────────────────────────┐    ┌──────────────────────────────┐
   │  pages → components → api/    │    │  routers → services → models │
   │  AuthContext (JWT + role)     │◀──▶│  schemas (validation)        │
   └──────────────────────────────┘    │  core/security (RBAC)        │
                REST / JSON             └──────────────┬───────────────┘
                                                       │
                                              PostgreSQL (SQLAlchemy)
```

**Backend layering** — a request flows one direction, each layer with one job:

`router` (HTTP) → `schema` (validate) → `service` (business rules) → `model` (data)

---

## 4. Project Structure

```
transitops/
├── backend/
│   └── app/
│       ├── main.py            # FastAPI app, CORS, router includes
│       ├── config.py          # settings from .env
│       ├── database.py        # engine, SessionLocal, get_db()
│       ├── models/            # SQLAlchemy tables (vehicle, driver, trip, …)
│       ├── schemas/           # Pydantic request/response shapes
│       ├── routers/           # thin HTTP endpoints
│       ├── services/          # business logic + status transitions
│       ├── core/              # security (JWT/RBAC), exceptions
│       └── utils/enums.py     # Role, VehicleStatus, DriverStatus, TripStatus
│
├── frontend/
│   └── src/
│       ├── api/               # axios client + one module per resource
│       ├── components/        # reusable UI (tables, modals, badges, charts)
│       ├── pages/             # one screen per route
│       ├── context/           # AuthContext (user, token, role)
│       ├── routes/            # protected routing
│       └── utils/             # constants (mirror BE enums), formatters
│
├── db/                        # PostgreSQL notes + optional init.sql
├── docs/er-diagram.png        # entity-relationship diagram
├── seed.py                    # demo data (vehicles, drivers, trips)
└── README.md
```

---

## 5. Data Model

Eight entities, connected by foreign keys so the platform can navigate from a
vehicle to its trips, costs, and maintenance history.

```
USERS ──▶ ROLES

VEHICLES ──┬─▶ TRIPS ◀── DRIVERS
           ├─▶ MAINTENANCE_LOGS
           ├─▶ FUEL_LOGS
           └─▶ EXPENSES
```

| Entity | Key fields |
|:--|:--|
| **Users / Roles** | email, password hash, role |
| **Vehicles** | reg. no *(unique)*, model, type, capacity, odometer, cost, **status** |
| **Drivers** | name, license no, category, expiry, contact, safety score, **status** |
| **Trips** | source, destination, cargo weight, distance, odometer, fuel, **status** |
| **Maintenance Logs** | vehicle, service type, cost, dates, active flag |
| **Fuel Logs** | vehicle, liters, cost, date |
| **Expenses** | vehicle/trip, type (toll / maintenance / other), amount, date |

**Status values**
- Vehicle → `Available` · `On Trip` · `In Shop` · `Retired`
- Driver → `Available` · `On Trip` · `Off Duty` · `Suspended`
- Trip → `Draft` · `Dispatched` · `Completed` · `Cancelled`

---

## 6. Business Rules

These are enforced in the service layer, not the UI, so they hold no matter how
the request arrives.

- ✅ Vehicle registration number must be **unique**.
- � **Retired** and **In Shop** vehicles never appear in dispatch selection.
- � Drivers with **expired licenses** or **Suspended** status cannot be assigned.
- � A vehicle or driver already **On Trip** cannot be assigned to another trip.
- ⚖️ **Cargo weight must not exceed** the vehicle's maximum load capacity.
- � **Dispatch** → vehicle + driver become On Trip *(one transaction)*.
- � **Complete** → vehicle + driver return to Available; odometer & fuel recorded.
- � **Cancel** → dispatched trip restores vehicle + driver to Available.
- � **Open maintenance** → vehicle becomes In Shop and leaves the dispatch pool.
- � **Close maintenance** → vehicle returns to Available *(unless Retired)*.

---

## 7. Analytics

Derived on read from the underlying logs — no separate reporting state.

| Metric | Formula |
|:--|:--|
| **Fuel Efficiency** | distance ÷ fuel consumed |
| **Operational Cost** *(per vehicle)* | fuel cost + maintenance cost |
| **Fleet Utilization** | vehicles On Trip ÷ total active vehicles |
| **Vehicle ROI** | (revenue − maintenance − fuel) ÷ acquisition cost |

Reports support **CSV export** for offline analysis.

---

## 8. Team & Modules

The work is divided into four independent modules that share the same data
foundation and API conventions.

| Area | Scope |
|:--|:--|
| **Foundation & Fleet** | DB setup, models, vehicle registry, maintenance workflow |
| **Auth & Dashboard** | Login, JWT, role-based access, KPI dashboard |
| **Drivers & Expenses** | Driver profiles, license tracking, fuel & expense logs |
| **Trips & Analytics** | Dispatch engine, status transitions, reports & charts |

Shared conventions keep the modules compatible:
REST under `/api`, JSON payloads, JWT auth, and errors returned as
`{ "detail": "message" }`.

---

## 9. Feature Scope

**Core**
> Authentication with RBAC · Vehicle & Driver management · Trip dispatch with
> validation · Automatic status transitions · Maintenance workflow · Fuel &
> expense tracking · KPI dashboard · Analytics with CSV export.

**Enhancements**
> Charts & visual analytics · PDF export · License-expiry reminders ·
> Document management · Search, filter & sort · Dark mode.

---

<div align="center">

**TransitOps** — one system for the full transport operations lifecycle.

</div>
