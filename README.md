# Hostel Management System

A college DBMS project that manages essential hostel operations including room allotments, student records, mess subscriptions, fees, fines, attendance, visitors, maintenance requests, and complaints.

---

## 🏛️ Architecture

```
React (Vite) Frontend  ──[Axios / HTTP]──>  FastAPI Backend (Python 3.11+)  ──[psycopg 3 / Raw SQL]──>  PostgreSQL 16 (hostel schema)
```

- **Frontend:** Never connects directly to the database. All operations go through backend REST endpoints.
- **Backend:** Uses pure parameterized SQL queries with `psycopg 3` and connection pooling (`psycopg_pool`). No ORM, no SQLAlchemy, no Alembic.
- **Database:** Dedicated PostgreSQL schema (`hostel`) to keep tables organized and separate from `public`.

---

## 🛠️ Approved Tech Stack

| Layer | Technology | Details |
|---|---|---|
| **Database** | PostgreSQL 16 | Run locally (or plain hosted Postgres via Supabase without extra libraries) |
| **Database Tools** | pgAdmin / DBeaver | GUI for query execution, inspecting schema, and management |
| **Backend** | Python 3.11+ & FastAPI | REST API framework, Pydantic v2 for data validation, pydantic-settings |
| **Database Access** | psycopg 3 (`psycopg` + `psycopg_pool`) | Raw SQL only, strict parameterized queries (no SQL injection) |
| **Database Migrations** | Numbered `.sql` files | Executed via a simple Python runner script in `database/` |
| **Frontend** | React (Vite) + Tailwind CSS | Fast dev server, modern styling, React Router, Axios |
| **Testing** | pytest + httpx | Automated backend API testing & interactive FastAPI `/docs` |
| **UI/UX Design** | Figma | UI wireframes and screens stored in `docs/design/` |
| **Version Control** | Git & GitHub | Single repository, feature branches, pull requests |
| **Development OS** | Windows | Commands tailored for PowerShell |

---

## 📁 Repository Structure

```
hostel-management-system/
├── README.md               # Project overview, tech stack, and workflow guide
├── .gitignore              # Files ignored by Git (.venv, node_modules, .env, etc.)
├── docs/                   # Documentation ONLY (no executable code)
│   ├── project-context.md  # The agreed database design (single source of truth)
│   ├── er-diagram.png      # Conceptual ER diagram
│   └── design/             # Exported UI design screens from Figma
├── database/               # ALL SQL and database migration files
│   ├── schema.sql          # Base tables, PKs, FKs, CHECK constraints in "hostel" schema
│   ├── triggers.sql        # Database functions/triggers (capacity checks, business rules)
│   └── seed.sql            # Realistic sample dataset for testing
├── backend/                # Server code, API routes, raw SQL queries
│   └── .env.example        # Placeholder settings only (never commit actual secrets)
└── frontend/               # React client, UI pages, components, styling
```

---

## 📋 Core Project Rules

1. **Strict Folder Placement:** SQL goes strictly into `database/`, Python code into `backend/`, React code into `frontend/`, and documentation into `docs/`.
2. **Design Baseline:** `docs/project-context.md` is the final specification. Never add or remove tables, attributes, or cardinalities without explicit agreement.
3. **Database Schema:** All tables reside in a custom PostgreSQL schema (e.g., `CREATE SCHEMA IF NOT EXISTS hostel;`).
4. **Pure Raw SQL:** Only write clean, parameterized SQL. Never concatenate input strings into queries.
5. **Secret Protection:** Actual database credentials and secrets stay in a local `.env` file that is git-ignored. Only `.env.example` is committed.
6. **No Auth/Roles Yet:** Authentication/roles are on hold until confirmed and approved.

---

## 🎨 UI/UX Design & Export Guidelines

All UI screens, wireframes, and prototypes must be designed in our shared Figma project before frontend implementation begins.

- **Official Figma File:** [Hostel Management System — UI Design (Figma)](https://www.figma.com/design/OIT1nOvW1WjS5YMywyweEy/Hostel-Management-System--UI-Design?t=7D2VjWokgU2jFMMr-1)
- **Project Rule:** All team designs must be done strictly in this shared Figma project. Do not create separate personal draft files.

### Quick Export & Save Steps
1. **Frame in Figma:** Group each screen into a dedicated top-level Frame (Desktop `1440px` or `1920px`).
2. **Export:** Select the frame ➔ In the right sidebar under **Export**, click **`+`** ➔ select **PNG** at **2x** resolution (or **SVG** for icons/vectors) ➔ click **Export [Frame Name]**.
3. **Save Directory:** Save all exported image files strictly to `docs/design/`.
4. **File Naming Convention:** Use lowercase kebab-case with numerical sequence prefixes:
   - `01-dashboard.png`
   - `02-students.png`
   - `03-rooms-allotment.png`
   - `04-fees-fines.png`
   - `05-mess.png`
   - `06-attendance.png`
   - `07-visitors.png`
   - `08-maintenance-complaints.png`
5. **Commit to Git:**
   ```powershell
   git add docs/design/
   git commit -m "docs(design): export and add Figma UI screens for <screen-name>"
   git push origin <branch-name>
   ```

For the complete screen checklist and guidelines, see [`docs/design/README.md`](docs/design/README.md).

---

## 👥 Team & Links

- **Figma Design Link:** [Hostel Management System — UI Design (Figma)](https://www.figma.com/design/OIT1nOvW1WjS5YMywyweEy/Hostel-Management-System--UI-Design?t=7D2VjWokgU2jFMMr-1)
- **Team Members:** _[Add team member names here]_

