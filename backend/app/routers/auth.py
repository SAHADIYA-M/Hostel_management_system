from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.db import get_db_connection

router = APIRouter(prefix="/api/auth", tags=["Authentication & Access Gateway"])


class StudentLoginRequest(BaseModel):
    reg_no: str = Field(..., max_length=30)
    phone: str = Field(..., max_length=15)


class WardenLoginRequest(BaseModel):
    warden_id: int
    phone: str = Field(..., max_length=15)


@router.post("/student-login")
def student_login(req: StudentLoginRequest, conn=Depends(get_db_connection)):
    """
    Authenticate a resident student via Reg_No and registered Phone.
    Strictly Raw SQL.
    """
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
                h.name AS hostel_name,
                h.type AS hostel_type
            FROM hostel.student s
            LEFT JOIN hostel.hostel h ON s.hostel_id = h.hostel_id
            WHERE LOWER(TRIM(s.reg_no)) = LOWER(TRIM(%s))
              AND TRIM(s.phone) = TRIM(%s);
        """
        cur.execute(query, (req.reg_no, req.phone))
        student = cur.fetchone()

        if not student:
            # Check if reg_no exists for a clearer error message
            cur.execute("SELECT 1 FROM hostel.student WHERE LOWER(TRIM(reg_no)) = LOWER(TRIM(%s));", (req.reg_no,))
            if not cur.fetchone():
                raise HTTPException(status_code=401, detail="Registration number not found in hostel records.")
            raise HTTPException(status_code=401, detail="Invalid registered phone number for this student.")

        return {
            "role": "STUDENT",
            "student_id": student["student_id"],
            "name": f"{student['fname']} {student['lname']}",
            "reg_no": student["reg_no"],
            "hostel_id": student["hostel_id"],
            "hostel_name": student["hostel_name"],
            "hostel_type": student["hostel_type"],
            "room_no": student["room_no"],
        }


@router.post("/warden-login")
def warden_login(req: WardenLoginRequest, conn=Depends(get_db_connection)):
    """
    Authenticate a hostel warden via Warden_ID and Phone.
    Strictly Raw SQL.
    """
    with conn.cursor() as cur:
        query = """
            SELECT 
                w.warden_id,
                w.name,
                w.phone,
                w.hostel_id,
                h.name AS hostel_name,
                h.type AS hostel_type
            FROM hostel.warden w
            JOIN hostel.hostel h ON w.hostel_id = h.hostel_id
            WHERE w.warden_id = %s
              AND TRIM(w.phone) = TRIM(%s);
        """
        cur.execute(query, (req.warden_id, req.phone))
        warden = cur.fetchone()

        if not warden:
            cur.execute("SELECT 1 FROM hostel.warden WHERE warden_id = %s;", (req.warden_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=401, detail="Warden ID not found.")
            raise HTTPException(status_code=401, detail="Invalid phone number for this warden.")

        return {
            "role": "WARDEN",
            "warden_id": warden["warden_id"],
            "name": warden["name"],
            "hostel_id": warden["hostel_id"],
            "hostel_name": warden["hostel_name"],
            "hostel_type": warden["hostel_type"],
        }
