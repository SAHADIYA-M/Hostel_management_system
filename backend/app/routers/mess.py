from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.db import get_db_connection
from app.schemas import MessCreate, MessResponse

router = APIRouter(prefix="/api/mess", tags=["Mess Subscriptions"])


@router.get("", response_model=List[MessResponse])
def get_all_mess_plans(conn=Depends(get_db_connection)):
    """Fetch all mess plans with enrolled student counts."""
    with conn.cursor() as cur:
        query = """
            SELECT 
                m.mess_id,
                m.type,
                m.cost,
                COUNT(s.student_id) AS enrolled_count
            FROM hostel.mess m
            LEFT JOIN hostel.student s ON m.mess_id = s.mess_id
            GROUP BY m.mess_id, m.type, m.cost
            ORDER BY m.mess_id;
        """
        cur.execute(query)
        return cur.fetchall()


@router.post("", response_model=MessResponse, status_code=201)
def create_mess_plan(plan: MessCreate, conn=Depends(get_db_connection)):
    """Create a new mess plan."""
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(mess_id), 0) + 1 AS next_id FROM hostel.mess;")
        next_id = cur.fetchone()["next_id"]

        cur.execute(
            """
            INSERT INTO hostel.mess (mess_id, type, cost)
            VALUES (%s, %s, %s)
            RETURNING *;
            """,
            (next_id, plan.type, plan.cost)
        )
        created = cur.fetchone()
        conn.commit()
        created["enrolled_count"] = 0
        return created
