from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.db import get_db_connection
from app.schemas import (
    FeeCreate, FeeStatusUpdate, FeeResponse,
    FineCreate, FineStatusUpdate, FineResponse
)

router = APIRouter(prefix="/api", tags=["Fees & Fines"])


# -----------------------------------------------------------------------------
# FEES
# -----------------------------------------------------------------------------
@router.get("/fees", response_model=List[FeeResponse])
def get_all_fees(
    student_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    conn=Depends(get_db_connection)
):
    """Fetch fee records with joined student names."""
    with conn.cursor() as cur:
        query = """
            SELECT 
                f.fee_id, f.due_date, f.amount, f.status, f.student_id,
                CONCAT(s.fname, ' ', s.lname) AS student_name,
                s.reg_no
            FROM hostel.fee f
            JOIN hostel.student s ON f.student_id = s.student_id
            WHERE 1=1
        """
        params = []
        if student_id is not None:
            query += " AND f.student_id = %s"
            params.append(student_id)
        if status:
            query += " AND f.status = %s"
            params.append(status)

        query += " ORDER BY f.due_date DESC, f.fee_id DESC;"
        cur.execute(query, tuple(params))
        return cur.fetchall()


@router.post("/fees", response_model=FeeResponse, status_code=201)
def create_fee(fee: FeeCreate, conn=Depends(get_db_connection)):
    """Create a new fee record for a student."""
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(fee_id), 500) + 1 AS next_id FROM hostel.fee;")
        next_id = cur.fetchone()["next_id"]

        try:
            cur.execute(
                """
                INSERT INTO hostel.fee (fee_id, due_date, amount, status, student_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (next_id, fee.due_date, fee.amount, fee.status, fee.student_id)
            )
            created = cur.fetchone()
            conn.commit()
            return created
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.put("/fees/{fee_id}/status", response_model=FeeResponse)
def update_fee_status(fee_id: int, req: FeeStatusUpdate, conn=Depends(get_db_connection)):
    """Update fee payment status (Pending / Paid)."""
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE hostel.fee
            SET status = %s
            WHERE fee_id = %s
            RETURNING *;
            """,
            (req.status, fee_id)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Fee record not found")
        conn.commit()
        return row


# -----------------------------------------------------------------------------
# FINES (Disciplinary Fines - Separate Entity)
# -----------------------------------------------------------------------------
@router.get("/fines", response_model=List[FineResponse])
def get_all_fines(
    student_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    conn=Depends(get_db_connection)
):
    """Fetch fine records with joined student names."""
    with conn.cursor() as cur:
        query = """
            SELECT 
                fn.fid, fn.reason, fn.amount, fn.status, fn.student_id,
                CONCAT(s.fname, ' ', s.lname) AS student_name,
                s.reg_no
            FROM hostel.fine fn
            JOIN hostel.student s ON fn.student_id = s.student_id
            WHERE 1=1
        """
        params = []
        if student_id is not None:
            query += " AND fn.student_id = %s"
            params.append(student_id)
        if status:
            query += " AND fn.status = %s"
            params.append(status)

        query += " ORDER BY fn.fid DESC;"
        cur.execute(query, tuple(params))
        return cur.fetchall()


@router.post("/fines", response_model=FineResponse, status_code=201)
def create_fine(fine: FineCreate, conn=Depends(get_db_connection)):
    """Issue a new fine to a student."""
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(fid), 700) + 1 AS next_id FROM hostel.fine;")
        next_id = cur.fetchone()["next_id"]

        try:
            cur.execute(
                """
                INSERT INTO hostel.fine (fid, reason, amount, status, student_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (next_id, fine.reason, fine.amount, fine.status, fine.student_id)
            )
            created = cur.fetchone()
            conn.commit()
            return created
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.put("/fines/{fid}/status", response_model=FineResponse)
def update_fine_status(fid: int, req: FineStatusUpdate, conn=Depends(get_db_connection)):
    """Update fine payment status (Pending / Paid)."""
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE hostel.fine
            SET status = %s
            WHERE fid = %s
            RETURNING *;
            """,
            (req.status, fid)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Fine record not found")
        conn.commit()
        return row
