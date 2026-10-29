from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date
from psycopg.errors import CheckViolation, ForeignKeyViolation
from app.db import get_db_connection
from app.schemas import StudentCreate, StudentAllotRequest, StudentResponse, MessPlanUpdate

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("", response_model=List[StudentResponse])
def get_all_students(
    hostel_id: Optional[int] = Query(None, description="Filter by hostel ID"),
    unallotted: Optional[bool] = Query(None, description="Filter unallotted students"),
    search: Optional[str] = Query(None, description="Search by name or reg_no"),
    conn=Depends(get_db_connection)
):
    """Fetch students with joined room, hostel, and mess plan details."""
    with conn.cursor() as cur:
        query = """
            SELECT 
                s.student_id,
                s.fname,
                s.lname,
                s.reg_no,
                s.phone,
                s.hostel_id,
                s.room_no,
                s.allot_date,
                s.mess_id,
                h.name AS hostel_name,
                r.type AS room_type,
                m.type AS mess_type
            FROM hostel.student s
            LEFT JOIN hostel.hostel h ON s.hostel_id = h.hostel_id
            LEFT JOIN hostel.room r ON s.hostel_id = r.hostel_id AND s.room_no = r.room_no
            LEFT JOIN hostel.mess m ON s.mess_id = m.mess_id
            WHERE 1=1
        """
        params = []
        if hostel_id is not None:
            query += " AND s.hostel_id = %s"
            params.append(hostel_id)
        if unallotted is True:
            query += " AND (s.hostel_id IS NULL OR s.room_no IS NULL)"
        if search:
            query += " AND (s.fname ILIKE %s OR s.lname ILIKE %s OR s.reg_no ILIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])

        query += " ORDER BY s.student_id;"
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        return rows


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, conn=Depends(get_db_connection)):
    """Fetch a single student by ID."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                s.student_id, s.fname, s.lname, s.reg_no, s.phone,
                s.hostel_id, s.room_no, s.allot_date, s.mess_id,
                h.name AS hostel_name, r.type AS room_type, m.type AS mess_type
            FROM hostel.student s
            LEFT JOIN hostel.hostel h ON s.hostel_id = h.hostel_id
            LEFT JOIN hostel.room r ON s.hostel_id = r.hostel_id AND s.room_no = r.room_no
            LEFT JOIN hostel.mess m ON s.mess_id = m.mess_id
            WHERE s.student_id = %s;
            """,
            (student_id,)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Student not found")
        return row


@router.post("", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, conn=Depends(get_db_connection)):
    """Register a new student."""
    with conn.cursor() as cur:
        # Check unique reg_no
        cur.execute("SELECT 1 FROM hostel.student WHERE LOWER(reg_no) = LOWER(%s);", (student.reg_no,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail=f"Registration number '{student.reg_no}' is already registered")

        # Get next student_id
        cur.execute("SELECT COALESCE(MAX(student_id), 1000) + 1 AS next_id FROM hostel.student;")
        next_id = cur.fetchone()["next_id"]

        try:
            cur.execute(
                """
                INSERT INTO hostel.student (student_id, fname, lname, reg_no, phone, hostel_id, room_no, allot_date, mess_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (
                    next_id, student.fname, student.lname, student.reg_no, student.phone,
                    student.hostel_id, student.room_no, student.allot_date, student.mess_id
                )
            )
            created = cur.fetchone()
            conn.commit()
            return created
        except (CheckViolation, ForeignKeyViolation) as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.put("/{student_id}/allot", response_model=StudentResponse)
def allot_student_room(student_id: int, req: StudentAllotRequest, conn=Depends(get_db_connection)):
    """
    Allot or vacate a student's room.
    Enforces Rule 5 (allotment fields all populated or all NULL) and
    Trigger Rule 7 (room capacity limit).
    """
    allot_date = req.allot_date or (date.today() if req.hostel_id and req.room_no else None)
    
    if (req.hostel_id is None or req.room_no is None) and req.hostel_id != req.room_no:
        raise HTTPException(
            status_code=400,
            detail="Both hostel_id and room_no must be provided, or both must be null to vacate room."
        )

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
                UPDATE hostel.student
                SET hostel_id = %s, room_no = %s, allot_date = %s
                WHERE student_id = %s
                RETURNING *;
                """,
                (req.hostel_id, req.room_no, allot_date, student_id)
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Student not found")
            conn.commit()
            return row
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{student_id}/mess", response_model=StudentResponse)
def update_student_mess_plan(student_id: int, req: MessPlanUpdate, conn=Depends(get_db_connection)):
    """Assign a new mess plan or unenroll (mess_id=null) for a student."""
    with conn.cursor() as cur:
        try:
            cur.execute(
                """
                UPDATE hostel.student
                SET mess_id = %s
                WHERE student_id = %s
                RETURNING *;
                """,
                (req.mess_id, student_id)
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Student not found")
            conn.commit()
            return row
        except HTTPException:
            raise
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.delete("/students/{student_id}", status_code=200)
def delete_student(student_id: int, conn=Depends(get_db_connection)):
    """Delete a student record."""
    with conn.cursor() as cur:
        try:
            cur.execute("DELETE FROM hostel.student WHERE student_id = %s RETURNING student_id;", (student_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Student not found")
            conn.commit()
            return {"message": "Student record deleted successfully", "student_id": student_id}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))
