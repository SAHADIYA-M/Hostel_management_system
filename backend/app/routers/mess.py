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


@router.delete("/{mess_id}", status_code=200)
def delete_mess_plan(mess_id: int, conn=Depends(get_db_connection)):
    """Delete a mess plan. Fails if students are still enrolled in it."""
    with conn.cursor() as cur:
        # Check if any student is still enrolled
        cur.execute(
            "SELECT COUNT(*) AS cnt FROM hostel.student WHERE mess_id = %s;",
            (mess_id,)
        )
        enrolled = cur.fetchone()["cnt"]
        if enrolled > 0:
            raise HTTPException(
                status_code=409,
                detail=f"Cannot delete: {enrolled} student(s) are still enrolled in this mess plan. Please reassign them first."
            )

        cur.execute(
            "DELETE FROM hostel.mess WHERE mess_id = %s RETURNING mess_id;",
            (mess_id,)
        )
        deleted = cur.fetchone()
        if not deleted:
            raise HTTPException(status_code=404, detail="Mess plan not found.")
        conn.commit()
        return {"message": "Mess plan deleted successfully.", "mess_id": mess_id}
