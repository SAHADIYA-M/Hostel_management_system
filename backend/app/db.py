"""
Database connection pool and raw SQL query utilities using psycopg 3.
Schema: hostel
ORM: None (Strictly Raw SQL with parameterization)
"""

from typing import Generator
from contextlib import contextmanager
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from app.config import get_settings

settings = get_settings()

# Initialize global connection pool
# Note: min_size=1, max_size=10, timeout=10s
pool: ConnectionPool | None = None


def init_db_pool() -> ConnectionPool:
    """Initialize the psycopg 3 connection pool."""
    global pool
    if pool is None or pool.closed:
        # Pass search_path option so all queries default to the hostel schema
        pool = ConnectionPool(
            conninfo=settings.database_url,
            min_size=1,
            max_size=10,
            timeout=10.0,
            kwargs={
                "row_factory": dict_row,
                "options": f"-c search_path={settings.db_schema},public"
            }
        )
        # Open pool synchronously
        pool.open(wait=True)
    return pool


def close_db_pool() -> None:
    """Close the psycopg 3 connection pool on shutdown."""
    global pool
    if pool is not None and not pool.closed:
        pool.close()
        pool = None


def get_db_connection():
    """
    FastAPI dependency yielding a connection from the pool.
    Usage:
        @router.get("/example")
        def route(conn = Depends(get_db_connection)):
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM hostel WHERE hostel_id = %s", (1,))
                return cur.fetchall()
    """
    global pool
    if pool is None or pool.closed:
        init_db_pool()
    with pool.connection() as conn:
        yield conn
