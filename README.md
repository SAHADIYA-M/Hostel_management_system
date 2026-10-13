# Hostel Management System

A full-stack college DBMS project for managing hostel operations — room allotments, student records, mess subscriptions, fees, fines, daily attendance, visitor logs, maintenance requests, and complaints.

Built with **React + Vite** on the frontend, **FastAPI + Python** on the backend, and **PostgreSQL 16** (hosted on Supabase) as the database — all communicating over a clean REST API with no ORM.

---

## Architecture

```
Browser (React + Vite)
     │
     │  HTTP/JSON  (Axios)
     ▼
FastAPI (Python 3.11+) — Uvicorn ASGI Server
     │
     │  psycopg 3  (Raw SQL — No ORM)
     ▼
PostgreSQL 16  →  hostel schema  →  13 relational tables
(Supabase managed instance)
```

- The **frontend** never touches the database directly. Every operation goes through a backend REST endpoint.
- The **backend** uses strictly parameterized raw SQL queries — no SQLAlchemy, no Alembic, no ORM.
- The **database** lives in a dedicated `hostel` schema inside the PostgreSQL instance.

---

## Tech Stack

| Layer | Technology | Details |
|---|---|---|
| Frontend Framework | React 19 + Vite | Component-based SPA, fast HMR dev server |
| Styling | TailwindCSS v3 | Utility-first CSS, ships only used classes |
| Routing | React Router DOM v7 | Client-side navigation without page reloads |
| Icons | Lucide React | Tree-shakeable SVG icon library |
| HTTP Client | Axios | REST calls with interceptors and timeout handling |
| Backend Framework | FastAPI | Auto-generated `/docs`, dependency injection, Pydantic validation |
| ASGI Server | Uvicorn | Runs FastAPI, async-ready |
| Data Validation | Pydantic v2 | Validates every request body before it reaches SQL |
| Config Management | pydantic-settings | Reads `.env` file with type coercion |
| Database Driver | psycopg 3 (binary + pool) | Official PostgreSQL adapter, connection pooling (1–10 connections) |
| Database | PostgreSQL 16 | Hosted on Supabase, custom `hostel` schema |
| Testing | pytest + httpx | Backend API tests via FastAPI's TestClient |

---

## Repository Structure

```
Hostel_management_system/
│
├── README.md                        ← You are here
├── .gitignore                       ← Ignores .venv, node_modules, .env files
├── .env                             ← Root-level env (git-ignored, never commit)
│
├── database/                        ← ALL SQL and database tooling
│   ├── schema.sql                   ← Creates the hostel schema + all 13 tables
│   ├── triggers.sql                 ← PL/pgSQL triggers: room capacity, warden audit
│   ├── seed.sql                     ← Realistic sample data for all 13 tables
│   ├── add_constraints.sql          ← Migration: patches CHECK constraints on live DB
│   └── run_sql.py                   ← Python CLI to run/verify/test all SQL files
│
├── backend/                         ← FastAPI REST API
│   ├── .env                         ← Database URL and config (git-ignored)
│   ├── .env.example                 ← Safe placeholder — committed to Git
│   ├── Procfile                     ← Deployment start command (Railway)
│   ├── requirements.txt             ← Python dependencies
│   └── app/
│       ├── main.py                  ← FastAPI app, CORS middleware, lifespan, routers
│       ├── config.py                ← pydantic-settings config loader (lru_cache)
│       ├── db.py                    ← psycopg3 connection pool (min=1, max=10)
│       ├── schemas.py               ← All Pydantic request/response models
│       └── routers/
│           ├── auth.py              ← POST /api/auth/student-login, /warden-login
│           ├── hostels.py           ← GET /api/hostels
│           ├── rooms.py             ← GET/POST /api/rooms
│           ├── students.py          ← CRUD /api/students + /allot
│           ├── fees.py              ← /api/fees + /api/fines (status updates)
│           ├── mess.py              ← GET /api/mess
│           ├── attendance.py        ← GET/POST /api/attendance (bulk mark)
│           ├── visitors.py          ← /api/visitors + /api/visits
│           ├── maintenance.py       ← /api/maintenance + /api/complaints
│           └── portal.py            ← GET /api/portal/{student_id} (aggregated view)
│
├── frontend/                        ← React + Vite SPA
│   ├── index.html                   ← Single HTML entry point
│   ├── package.json                 ← npm dependencies and scripts
│   ├── vite.config.js               ← Vite dev server + /api proxy to :8000
│   ├── tailwind.config.js           ← Custom brand colour palette (indigo)
│   ├── postcss.config.js            ← PostCSS + Autoprefixer
│   ├── eslint.config.js             ← ESLint with react-hooks and react-refresh rules
│   ├── vercel.json                  ← SPA rewrite rule for React Router on Vercel
│   └── src/
│       ├── main.jsx                 ← createRoot, mounts <App /> into index.html
│       ├── App.jsx                  ← All page views/logic (warden & student portal)
│       ├── index.css                ← Tailwind directives + base resets
│       ├── api/
│       │   ├── client.js            ← Axios instance (base URL, interceptors, timeout)
│       │   └── services/            ← One service file per API resource:
│       │       ├── authService.js
│       │       ├── studentService.js
│       │       ├── hostelService.js
│       │       ├── roomService.js
│       │       ├── feeService.js
│       │       ├── messService.js
│       │       ├── attendanceService.js
│       │       ├── visitorService.js
│       │       ├── maintenanceService.js
│       │       └── portalService.js
│       └── components/
│           ├── LoginPage.jsx        ← Dual-role login (Warden / Student)
│           ├── StudentPortal.jsx    ← Student self-service view
│           └── StatusBadge.jsx      ← Reusable Paid/Pending/Open badge
│
└── docs/                            ← Documentation only (no executable code)
    ├── project-context.md           ← Finalized relational schema + business rules
    └── design/                      ← Exported UI mockups from Figma
        ├── 00-login-page.png
        ├── 00-ui-kit.png
        ├── 01-dashboard.png
        ├── 02-students.png
        ├── 03-rooms-allotment.png
        ├── 04-fees-fines.png
        ├── 05-mess.png
        ├── 06-attendance.png
        ├── 07-visitors.png
        ├── 08-maintenance-complaints.png
        └── 09-student-portal.png
```

---

## Database Schema (13 Tables)

All tables reside in the `hostel` schema inside PostgreSQL.

| Table | Type | Primary Key | Description |
|---|---|---|---|
| `hostel` | Regular | `hostel_id` | Hostel buildings (Boys/Girls) |
| `warden` | Regular | `warden_id` | 1:1 with hostel, enforced unique FK |
| `staff` | Regular | `staff_id` | 1:N from hostel (role + phone only) |
| `room` | **Weak entity** | `(hostel_id, room_no)` | Room numbers repeat across hostels |
| `mess` | Regular | `mess_id` | Meal plans with cost |
| `student` | Regular | `student_id` | Stores current room allotment + mess |
| `fee` | Regular | `fee_id` | Hostel fee records per student |
| `fine` | Regular | `fid` | Disciplinary fines per student |
| `attendance` | **Weak entity** | `(student_id, date)` | One record per student per day |
| `visitor` | Regular | `visitor_id` | Visitor registry |
| `visit` | Junction (M:N) | `(student_id, visitor_id, visit_date)` | Student↔Visitor visit log |
| `maintenance` | Regular | `request_id` | Room-specific or hostel-wide repairs |
| `complaint` | Regular | `complaint_id` | Student-filed complaints |

**Key database rules enforced:**
- Room capacity checked by a `BEFORE INSERT/UPDATE` PL/pgSQL trigger (`trg_check_room_capacity`)
- Room allotment fields are all-or-none: `hostel_id`, `room_no`, `allot_date` must all be set or all be NULL
- Phone numbers validated by regex: `^(\+91)?[6-9][0-9]{9}$`
- Registration numbers validated by regex: `^REG[0-9]{7}$`
- Status columns use domain constraints: `Pending/Paid`, `Open/In Progress/Resolved`, `Present/Absent`

---

## API Overview

The backend exposes a REST API at `/api/`. Interactive docs are auto-generated at `/docs`.

| Resource | Endpoints | Methods |
|---|---|---|
| Auth | `/api/auth/student-login`, `/warden-login`, `/logout` | POST |
| Hostels | `/api/hostels` | GET |
| Rooms | `/api/rooms` | GET, POST |
| Students | `/api/students`, `/api/students/{id}`, `/api/students/{id}/allot` | GET, POST, PUT |
| Fees | `/api/fees`, `/api/fees/{id}/status` | GET, POST, PUT |
| Fines | `/api/fines`, `/api/fines/{id}/status` | GET, POST, PUT |
| Mess | `/api/mess` | GET |
| Attendance | `/api/attendance` | GET, POST (bulk mark) |
| Visitors | `/api/visitors`, `/api/visits` | GET, POST |
| Maintenance | `/api/maintenance`, `/api/maintenance/{id}/status` | GET, POST, PUT |
| Complaints | `/api/complaints`, `/api/complaints/{id}/status` | GET, POST, PUT |
| Student Portal | `/api/portal/{student_id}` | GET (aggregated single-student view) |
| Health | `/api/health`, `/api/db-check` | GET |

---

## Local Development Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- A PostgreSQL 16 database (Supabase or local)

### 1. Clone and configure environment

```powershell
git clone https://github.com/your-org/Hostel_management_system.git
cd Hostel_management_system
```

Create `backend/.env` from the example:
```powershell
Copy-Item backend\.env.example backend\.env
```
Then open `backend/.env` and fill in your `DATABASE_URL`:
```
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require
DB_SCHEMA=hostel
CORS_ORIGINS=http://localhost:5173
```

### 2. Set up the database

```powershell
cd database
python run_sql.py --test-connection   # Verify DB is reachable
python run_sql.py --run-schema        # Create all 13 tables
python run_sql.py --run-triggers      # Add capacity trigger + warden audit function
python run_sql.py --verify            # Confirm structure (PKs, FKs, triggers)
python run_sql.py --run-seed          # Load sample data
python run_sql.py --row-counts        # Confirm data inserted
python run_sql.py --test-rules        # Verify all business rules fire correctly
cd ..
```

### 3. Run the backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API is now live at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### 4. Run the frontend

Open a new terminal:
```powershell
cd frontend
npm install
npm run dev
```

App is now live at `http://localhost:5173`.  
The Vite dev server proxies all `/api` requests to `http://localhost:8000`.

---

## Test Credentials (from seed data)

| Role | Login Field | Value |
|---|---|---|
| **Warden** (Ganga Boys) | Warden ID | `1` |
| | Phone | `+919876543210` |
| **Warden** (Yamuna Girls) | Warden ID | `2` |
| | Phone | `+919876543211` |
| **Student** | Reg No | `REG2024007` |
| | Phone | `+919811122207` |

---

## UI Modules (Warden Portal)

| # | Module | What it shows |
|---|---|---|
| 1 | Dashboard | Live stats: students, room occupancy, pending fees/fines, open requests |
| 2 | Students | Full student roster, room allotment, mess plan, search & filter |
| 3 | Rooms | Room registry with capacity vs occupancy, allot/vacate students |
| 4 | Fees & Fines | Fee and fine records, toggle Paid/Pending status |
| 5 | Mess | Mess plans and enrolled student counts |
| 6 | Attendance | Mark all students Present/Absent by date or individually |
| 7 | Visitors | Visitor registry and visit log |
| 8 | Maintenance & Complaints | Maintenance tickets (room-specific or hostel-wide) and student complaints |

The **Student Self-Service Portal** (`09-student-portal.png`) shows each logged-in student only their own data: room, roommates, fee invoices, fines, attendance, complaints, and visitors.

---

## Project Rules

1. **Folder discipline**: SQL → `database/`, Python → `backend/`, React → `frontend/`, documentation → `docs/`. No exceptions.
2. **Raw SQL only**: All database queries use `psycopg 3` with `%s` parameterized queries. No string concatenation, no ORM.
3. **Schema baseline**: `docs/project-context.md` is the agreed relational design. Do not add/remove tables or change cardinalities without team approval.
4. **Secrets**: Credentials stay in `.env` files. Only `.env.example` is committed to Git.
5. **No CORS workarounds**: In production the backend's `CORS_ORIGINS` env var must list the exact frontend domain.

---

## Design Assets

UI mockups exported from Figma are stored in `docs/design/`. All design work is done in the shared Figma file:

🎨 **[Hostel Management System — UI Design (Figma)](https://www.figma.com/design/OIT1nOvW1WjS5YMywyweEy/Hostel-Management-System--UI-Design?t=7D2VjWokgU2jFMMr-1)**

Export convention: lowercase kebab-case with a two-digit sequence prefix (e.g., `01-dashboard.png`).

---

## Team

| Name | Role |
|---|---|
| Sahadiya M | Developer |
| Rose Sharlin | Developer |
| Adithyan VT | Developer |
| Bharath P | Developer |
| Srividya K | Developer |
| Anagha ES | Developer |
| Anagha P | Developer |
| Ayfa P | Developer |
| Neeraja T | Developer |
