"""
FastAPI Main Application Entry Point
Architecture: React Frontend -> FastAPI REST API -> psycopg 3 (Raw SQL) -> PostgreSQL 16
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.db import init_db_pool, close_db_pool, get_db_connection

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycle."""
    # Attempt pool initialization if database is configured
    try:
        init_db_pool()
        print("INFO: Database connection pool initialized successfully.")
    except Exception as e:
        print(f"WARNING: Could not connect to database on startup ({e}).")
        print("Ensure your DATABASE_URL in .env is correct.")
    yield
    # Shutdown
    close_db_pool()
    print("INFO: Database connection pool closed.")


app = FastAPI(
    title="Hostel Management System API",
    description="REST API with FastAPI, psycopg 3 (raw SQL), and PostgreSQL 16",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for React frontend (Vite default: http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def root():
    """Root welcoming endpoint with links to documentation and health status."""
    return {
        "service": "Hostel Management System API",
        "status": "online",
        "docs": "/docs",
        "health": "/api/health",
        "db_check": "/api/db-check"
    }


@app.get("/api/health", tags=["Health"])
def health_check():
    """Simple healthcheck endpoint to verify backend status."""
    return {
        "status": "healthy",
        "service": "Hostel Management System API",
        "schema": settings.db_schema,
    }


@app.get("/api/db-check", tags=["Health"])
def db_check(conn=Depends(get_db_connection)):
    """Verifies live database connectivity and current schema."""
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), current_schema(), version();")
        row = cur.fetchone()
        return {
            "status": "connected",
            "database": row["current_database"],
            "schema": row["current_schema"],
            "version": row["version"]
        }
