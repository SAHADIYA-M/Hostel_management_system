from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date as DateType
from app.db import get_db_connection
from app.schemas import AttendanceCreate, AttendanceBulkCreate, AttendanceResponse

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.get("", response_model=List[AttendanceResponse])
def get_attendance(
    date: Optional[DateType] = Query(None, description="Filter by date"),
    hostel_id: Optional[int] = Query(None, description="Filter by hostel"),
    student_id: Optional[int] = Query(None, description="Filter by student"),
    conn=Depends(get_db_connection)
):
    """Fetch attendance records. Composite PK (student_id, date)."""
    with conn.cursor() as cur:
        query = """
            SELECT 
                a.student_id,
                a.date,
                a.status,
                CONCAT(s.fname, ' ', s.lname) AS student_name,
                s.reg_no,
                s.room_no,
                s.hostel_id,
                h.name AS hostel_name
            FROM hostel.attendance a
            JOIN hostel.student s ON a.student_id = s.student_id
            LEFT JOIN hostel.hostel h ON s.hostel_id = h.hostel_id
            WHERE 1=1
        """
        params = []
        if date is not None:
            query += " AND a.date = %s"
            params.append(date)
        if hostel_id is not None:
            query += " AND s.hostel_id = %s"
            params.append(hostel_id)
        if student_id is not None:
            query += " AND a.student_id = %s"
            params.append(student_id)

        query += " ORDER BY a.date DESC, s.room_no, a.student_id;"
        cur.execute(query, tuple(params))
        return cur.fetchall()


@router.post("", response_model=AttendanceResponse, status_code=200)
def mark_attendance(att: AttendanceCreate, conn=Depends(get_db_connection)):
    """Mark or update attendance for a single student on a date (Upsert)."""
    with conn.cursor() as cur:
        query = """
            INSERT INTO hostel.attendance (student_id, date, status)
            VALUES (%s, %s, %s)
            ON CONFLICT (student_id, date) 
            DO UPDATE SET status = EXCLUDED.status
            RETURNING student_id, date, status;
        """
        cur.execute(query, (att.student_id, att.date, att.status))
        updated = cur.fetchone()
        conn.commit()

        # Fetch extra student details for clean response
        cur.execute(
            """
            SELECT CONCAT(s.fname, ' ', s.lname) AS student_name, s.reg_no, s.room_no, s.hostel_id, h.name AS hostel_name
            FROM hostel.student s
            LEFT JOIN hostel.hostel h ON s.hostel_id = h.hostel_id
            WHERE s.student_id = %s;
            """,
            (att.student_id,)
        )
        extra = cur.fetchone() or {}
        return {**updated, **extra}


@router.post("/bulk", status_code=200)
def mark_bulk_attendance(req: AttendanceBulkCreate, conn=Depends(get_db_connection)):
    """Mark attendance for all allotted students on a given date."""
    with conn.cursor() as cur:
        # Find all students who have room allotments
        student_query = """
            SELECT student_id 
            FROM hostel.student 
            WHERE hostel_id IS NOT NULL AND room_no IS NOT NULL
        """
        params = []
        if req.hostel_id:
            student_query += " AND hostel_id = %s"
            params.append(req.hostel_id)

        cur.execute(student_query, tuple(params))
        students = cur.fetchall()
        
        count = 0
        for s in students:
            cur.execute(
                """
                INSERT INTO hostel.attendance (student_id, date, status)
                VALUES (%s, %s, %s)
                ON CONFLICT (student_id, date)
                DO UPDATE SET status = EXCLUDED.status;
                """,
                (s["student_id"], req.date, req.status)
            )
            count += 1
        conn.commit()
        return {"message": f"Successfully updated attendance for {count} students", "date": req.date, "status": req.status}
