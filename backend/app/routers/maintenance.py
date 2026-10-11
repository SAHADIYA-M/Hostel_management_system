from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.db import get_db_connection
from app.schemas import (
    MaintenanceCreate, MaintenanceStatusUpdate, MaintenanceResponse,
    ComplaintCreate, ComplaintStatusUpdate, ComplaintResponse
)

router = APIRouter(prefix="/api", tags=["Maintenance & Complaints"])


# -----------------------------------------------------------------------------
# MAINTENANCE REQUESTS
# -----------------------------------------------------------------------------
@router.get("/maintenance", response_model=List[MaintenanceResponse])
def get_all_maintenance(
    hostel_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    conn=Depends(get_db_connection)
):
    """Fetch maintenance work orders (hostel-wide vs room-specific)."""
    with conn.cursor() as cur:
        query = """
            SELECT 
                m.request_id,
                m.hostel_id,
                m.room_no,
                m.description,
                m.date,
                m.status,
                h.name AS hostel_name
            FROM hostel.maintenance m
            JOIN hostel.hostel h ON m.hostel_id = h.hostel_id
            WHERE 1=1
        """
        params = []
        if hostel_id is not None:
            query += " AND m.hostel_id = %s"
            params.append(hostel_id)
        if status:
            query += " AND m.status = %s"
            params.append(status)

        query += " ORDER BY m.date DESC, m.request_id DESC;"
        cur.execute(query, tuple(params))
        return cur.fetchall()


@router.post("/maintenance", response_model=MaintenanceResponse, status_code=201)
def create_maintenance_request(req: MaintenanceCreate, conn=Depends(get_db_connection)):
    """Log a maintenance work order."""
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(request_id), 300) + 1 AS next_id FROM hostel.maintenance;")
        next_id = cur.fetchone()["next_id"]

        try:
            cur.execute(
                """
                INSERT INTO hostel.maintenance (request_id, hostel_id, room_no, description, date, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (next_id, req.hostel_id, req.room_no, req.description, req.date, req.status)
            )
            created = cur.fetchone()
            conn.commit()

            cur.execute("SELECT name AS hostel_name FROM hostel.hostel WHERE hostel_id = %s;", (req.hostel_id,))
            h_row = cur.fetchone() or {}
            return {**created, **h_row}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.put("/maintenance/{request_id}/status", response_model=MaintenanceResponse)
def update_maintenance_status(request_id: int, req: MaintenanceStatusUpdate, conn=Depends(get_db_connection)):
    """Update status of a maintenance ticket (Open, In Progress, Resolved)."""
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE hostel.maintenance
            SET status = %s
            WHERE request_id = %s
            RETURNING *;
            """,
            (req.status, request_id)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Maintenance ticket not found")
        conn.commit()

        cur.execute("SELECT name AS hostel_name FROM hostel.hostel WHERE hostel_id = %s;", (row["hostel_id"],))
        h_row = cur.fetchone() or {}
        return {**row, **h_row}


# -----------------------------------------------------------------------------
# STUDENT COMPLAINTS
# -----------------------------------------------------------------------------
@router.get("/complaints", response_model=List[ComplaintResponse])
def get_all_complaints(
    student_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    conn=Depends(get_db_connection)
):
    """Fetch student grievances."""
    with conn.cursor() as cur:
        query = """
            SELECT 
                c.complaint_id,
                c.date,
                c.description,
                c.status,
                c.student_id,
                CONCAT(s.fname, ' ', s.lname) AS student_name,
                s.reg_no
            FROM hostel.complaint c
            JOIN hostel.student s ON c.student_id = s.student_id
            WHERE 1=1
        """
        params = []
        if student_id is not None:
            query += " AND c.student_id = %s"
            params.append(student_id)
        if status:
            query += " AND c.status = %s"
            params.append(status)

        query += " ORDER BY c.date DESC, c.complaint_id DESC;"
        cur.execute(query, tuple(params))
        return cur.fetchall()


@router.post("/complaints", response_model=ComplaintResponse, status_code=201)
def create_complaint(req: ComplaintCreate, conn=Depends(get_db_connection)):
    """Lodge a student complaint."""
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(complaint_id), 400) + 1 AS next_id FROM hostel.complaint;")
        next_id = cur.fetchone()["next_id"]

        try:
            cur.execute(
                """
                INSERT INTO hostel.complaint (complaint_id, date, description, status, student_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (next_id, req.date, req.description, req.status, req.student_id)
            )
            created = cur.fetchone()
            conn.commit()

            cur.execute("SELECT CONCAT(fname, ' ', lname) AS student_name, reg_no FROM hostel.student WHERE student_id = %s;", (req.student_id,))
            s_row = cur.fetchone() or {}
            return {**created, **s_row}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.put("/complaints/{complaint_id}/status", response_model=ComplaintResponse)
def update_complaint_status(complaint_id: int, req: ComplaintStatusUpdate, conn=Depends(get_db_connection)):
    """Update grievance status (Open, In Progress, Resolved)."""
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE hostel.complaint
            SET status = %s
            WHERE complaint_id = %s
            RETURNING *;
            """,
            (req.status, complaint_id)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Complaint not found")
        conn.commit()

        cur.execute("SELECT CONCAT(fname, ' ', lname) AS student_name, reg_no FROM hostel.student WHERE student_id = %s;", (row["student_id"],))
        s_row = cur.fetchone() or {}
        return {**row, **s_row}
