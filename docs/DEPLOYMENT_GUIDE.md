# Hostel Management System — Final Deployment Guide

This guide walks you through deploying the entire Hostel Management System stack to production using industry-standard, free-tier-friendly cloud providers:

- **Database**: Cloud PostgreSQL on **Supabase** (Already live and configured)
- **Backend API**: Python FastAPI on **Render** (or **Railway**)
- **Frontend SPA**: React (Vite) on **Vercel** (or **Netlify**)

---

## Architecture Overview

```
[ Client Browser ]
       │
       ▼ (HTTPS)
[ Frontend (Vercel / Netlify) ]
       │
       ▼ (REST API / JSON over HTTPS)
[ Backend FastAPI (Render / Railway) ]
       │
       ▼ (psycopg 3 connection pool with SSL)
[ Supabase PostgreSQL 16 (hostel schema) ]
```

---

## 1. Database (Supabase PostgreSQL) — *Already Ready*

Your database is already initialized and active on Supabase:
- **Schema**: `hostel`
- **Tables**: 13 relational tables with triggers, composite keys, and integrity constraints.
- **Seed Data**: 12+ students per hostel across Ganga Boys Hostel, Yamuna Girls Hostel, and Kaveri Boys Hostel.

### Where to get your Database Connection String:
1. Log in to [Supabase Console](https://supabase.com).
2. Go to your Project > **Settings** (Gear icon) > **Database**.
3. Under **Connection string**, select **URI** (or Transaction Pooler mode).
4. Format:
   ```
   postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require
   ```

---

## 2. Backend Deployment (Render)

**Recommended Platform**: [Render](https://render.com) (Free web service tier, native Python support).

### Step-by-Step Instructions:

1. **Push your code to GitHub**:
   Ensure your latest code is pushed to your GitHub repository:
   ```bash
   git add .
   git commit -m "Prepare production deployment configuration"
   git push origin main
   ```

2. **Create a Web Service on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com).
   - Click **New +** > **Web Service**.
   - Connect your GitHub repository (`Hostel_management_system`).

3. **Configure Service Settings**:
   - **Name**: `hostel-management-api`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Region**: Singapore or Frankfurt (closest to your database region)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**:
   Under the **Environment Variables** section, add:
   | Key | Value | Description |
   | :--- | :--- | :--- |
   | `DATABASE_URL` | `postgresql://...` | Your Supabase connection string |
   | `DB_SCHEMA` | `hostel` | Schema name |
   | `CORS_ORIGINS` | `https://your-frontend.vercel.app` | (You can update this after deploying frontend) |

5. **Deploy**:
   - Click **Deploy Web Service**.
   - Once deployed, Render will provide your public backend URL, e.g.:
     `https://hostel-management-api.onrender.com`
   - Verify by visiting: `https://hostel-management-api.onrender.com/docs` to see the live Swagger documentation.

---

## 3. Frontend Deployment (Vercel)

**Recommended Platform**: [Vercel](https://vercel.com) (Zero configuration, lightning-fast edge CDN).

### Step-by-Step Instructions:

1. **Log in to Vercel**:
   - Go to [vercel.com](https://vercel.com) and log in with your GitHub account.

2. **Import Repository**:
   - Click **Add New...** > **Project**.
   - Select your `Hostel_management_system` repository.

3. **Configure Project Settings**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click `Edit` and select **`frontend`**.
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `dist` (default)

4. **Add Environment Variable**:
   Under **Environment Variables**, add:
   | Key | Value |
   | :--- | :--- |
   | `VITE_API_URL` | `https://hostel-management-api.onrender.com` |

   *(Replace with your actual backend URL from Step 2)*

5. **Deploy**:
   - Click **Deploy**.
   - Vercel will build and assign a production URL (e.g., `https://hostel-management-system.vercel.app`).
   - The included `frontend/vercel.json` and `frontend/public/_redirects` automatically handle single-page application routing rewrites.

---

## 4. Final Wire-Up & Verification

1. **Update Backend CORS**:
   - In Render, update the `CORS_ORIGINS` environment variable to your frontend Vercel URL:
     `https://hostel-management-system.vercel.app`
   - Trigger a quick redeploy on Render.

2. **Test End-to-End**:
   - Open your Vercel URL in your browser.
   - **Warden Login**:
     - Identifier: `1`
     - Phone: `+919876543210`
     - Verify Ganga Boys Hostel dashboard, 12 resident students, and attendance roster.
   - **Student Login**:
     - Reg No: `REG2024001`
     - Phone: `+919811122201`
     - Verify personal resident details, lodging grievances, and fee records.

---

## Alternative One-Click Platform: Railway

If you prefer deploying both Frontend and Backend on a single platform:
1. Go to [railway.app](https://railway.app).
2. Create a new project from your GitHub repo.
3. Deploy two services:
   - **Backend Service**: Set root directory to `backend`, start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
   - **Frontend Service**: Set root directory to `frontend`, run `npm run build` and `npm run preview`.
4. Add the respective environment variables (`DATABASE_URL` for backend, `VITE_API_URL` for frontend).
