```
transitops/
├── frontend/
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── api/
│   │   │   ├── axiosClient.js          # base axios instance, baseURL = import.meta.env.VITE_API_URL
│   │   │   ├── auth.js                 # login, signup, /me
│   │   │   ├── vehicles.js
│   │   │   ├── drivers.js
│   │   │   ├── trips.js
│   │   │   ├── maintenance.js
│   │   │   ├── fuelLogs.js
│   │   │   └── expenses.js
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── ProtectedRoute.jsx  # wraps routes, checks JWT + role
│   │   │   │   ├── Modal.jsx
│   │   │   │   ├── DataTable.jsx
│   │   │   │   └── StatusBadge.jsx
│   │   │   ├── dashboard/
│   │   │   │   ├── KpiCard.jsx
│   │   │   │   └── FleetUtilChart.jsx
│   │   │   ├── vehicles/
│   │   │   │   ├── VehicleForm.jsx
│   │   │   │   └── VehicleTable.jsx
│   │   │   ├── drivers/
│   │   │   │   ├── DriverForm.jsx
│   │   │   │   └── DriverTable.jsx
│   │   │   ├── trips/
│   │   │   │   ├── TripForm.jsx
│   │   │   │   ├── TripTable.jsx
│   │   │   │   └── DispatchModal.jsx
│   │   │   ├── maintenance/
│   │   │   │   └── MaintenanceForm.jsx
│   │   │   └── expenses/
│   │   │       ├── FuelLogForm.jsx
│   │   │       └── ExpenseForm.jsx
│   │   ├── context/
│   │   │   └── AuthContext.jsx         # stores user, token, role; persists in memory/localStorage
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   └── useFetch.js
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── VehiclesPage.jsx
│   │   │   ├── DriversPage.jsx
│   │   │   ├── TripsPage.jsx
│   │   │   ├── MaintenancePage.jsx
│   │   │   ├── ExpensesPage.jsx
│   │   │   └── ReportsPage.jsx
│   │   ├── routes/
│   │   │   └── AppRoutes.jsx
│   │   ├── utils/
│   │   │   ├── constants.js            # status enums, role enums (mirror BE enums)
│   │   │   └── formatters.js           # date/currency formatting
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css                   # tailwind directives
│   ├── .env.example                    # VITE_API_URL=http://localhost:8000
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI() instance, CORS, router includes
│   │   ├── config.py                   # settings via pydantic BaseSettings (reads .env)
│   │   ├── database.py                 # engine, SessionLocal, get_db() dependency
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── vehicle.py
│   │   │   ├── driver.py
│   │   │   ├── trip.py
│   │   │   ├── maintenance_log.py
│   │   │   ├── fuel_log.py
│   │   │   └── expense.py
│   │   ├── schemas/                    # Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── vehicle.py
│   │   │   ├── driver.py
│   │   │   ├── trip.py
│   │   │   ├── maintenance_log.py
│   │   │   ├── fuel_log.py
│   │   │   └── expense.py
│   │   ├── routers/                    # route handlers only — thin, call services
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── vehicles.py
│   │   │   ├── drivers.py
│   │   │   ├── trips.py
│   │   │   ├── maintenance.py
│   │   │   ├── fuel_logs.py
│   │   │   ├── expenses.py
│   │   │   └── dashboard.py             # KPI aggregation endpoints
│   │   ├── services/                   # business logic + validation rules live here
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py         # hashing, JWT create/verify
│   │   │   ├── trip_service.py         # dispatch/complete/cancel + all validations
│   │   │   ├── maintenance_service.py  # open/close → vehicle status cascade
│   │   │   └── report_service.py       # fuel efficiency, utilization, ROI calcs
│   │   ├── core/
│   │   │   ├── security.py             # get_current_user, role-check dependency
│   │   │   └── exceptions.py           # custom HTTPException subclasses
│   │   └── utils/
│   │       └── enums.py                # Role, VehicleStatus, DriverStatus, TripStatus
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py                      # wired to read DATABASE_URL from config
│   │   └── script.py.mako
│   ├── alembic.ini
│   ├── tests/
│   │   ├── test_trips.py
│   │   └── test_maintenance.py
│   ├── seed.py                         # populate demo data (Van-05, driver Alex, etc.)
│   ├── requirements.txt
│   ├── .env.example                    # DATABASE_URL, JWT_SECRET, JWT_EXPIRE_MIN
│   └── Dockerfile                      # optional, if you containerize instead of native Render build
│
├── db/
│   ├── README.md                       # notes: hosted on Render Postgres, connection info, backup steps
│   └── init.sql                        # optional: seed/reference SQL if you want raw-SQL seed instead of seed.py
│
├── docs/
│   └── er-diagram.png                  # export from dbdiagram.io or similar, nice for judges
│
├── .gitignore
├── render.yaml                         # infra-as-code: web service + postgres, one-click provision
└── README.md                           # setup instructions, env vars, run commands
