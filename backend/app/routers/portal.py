from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db_connection
from app.schemas import StudentPortalResponse

router = APIRouter(prefix="/api/portal", tags=["Student Self-Service Portal"])


@router.get("/student/{student_id}", response_model=StudentPortalResponse)
def get_student_portal_data(student_id: int, conn=Depends(get_db_connection)):
    """
    Dedicated Aggregated Endpoint for Student Self-Service Portal.
    Strictly scoped to the requested student's data:
    - Personal Profile & Allotment
    - Roommates sharing the room
    - Gender-matched Hostel Warden & Caretaker contacts
    - Personal Fee invoices and Disciplinary Fines
    - Personal Attendance History
    - Grievances & Room Maintenance status
    - Approved Visitors
    """
    with conn.cursor() as cur:
        # 1. Fetch student info and room/hostel info
        cur.execute(
            """
            SELECT 
                s.student_id, s.fname, s.lname, s.reg_no, s.phone, s.allot_date,
                s.hostel_id, s.room_no, s.mess_id,
                h.name AS hostel_name, h.type AS hostel_type, h.address AS hostel_address,
                r.type AS room_type, r.capacity AS room_capacity,
                m.type AS mess_name, m.cost AS mess_cost
            FROM hostel.student s
            LEFT JOIN hostel.hostel h ON s.hostel_id = h.hostel_id
            LEFT JOIN hostel.room r ON s.hostel_id = r.hostel_id AND s.room_no = r.room_no
            LEFT JOIN hostel.mess m ON s.mess_id = m.mess_id
            WHERE s.student_id = %s;
            """,
            (student_id,)
        )
        student = cur.fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        hostel_id = student["hostel_id"]
        room_no = student["room_no"]

        # 2. Fetch Roommates (if allotted)
        roommates = []
        if hostel_id and room_no:
            cur.execute(
                """
                SELECT student_id, fname, lname, reg_no, phone, allot_date
                FROM hostel.student
                WHERE hostel_id = %s AND room_no = %s AND student_id != %s
                ORDER BY student_id;
                """,
                (hostel_id, room_no, student_id)
            )
            roommates = cur.fetchall()

        # 3. Fetch Assigned Warden & Staff
        warden = None
        staff_contacts = []
        if hostel_id:
            cur.execute(
                """
                SELECT warden_id, name, phone
                FROM hostel.warden
                WHERE hostel_id = %s;
                """,
                (hostel_id,)
            )
            warden = cur.fetchone()

            cur.execute(
                """
                SELECT staff_id, role, phone
                FROM hostel.staff
                WHERE hostel_id = %s
                ORDER BY staff_id;
                """,
                (hostel_id,)
            )
            staff_contacts = cur.fetchall()

        # 4. Fetch Personal Fees
        cur.execute(
            """
            SELECT fee_id, due_date, amount, status, student_id
            FROM hostel.fee
            WHERE student_id = %s
            ORDER BY due_date DESC;
            """,
            (student_id,)
        )
        fees = cur.fetchall()

        # 5. Fetch Personal Fines
        cur.execute(
            """
            SELECT fid, reason, amount, status, student_id
            FROM hostel.fine
            WHERE student_id = %s
            ORDER BY fid DESC;
            """,
            (student_id,)
        )
        fines = cur.fetchall()

        # 6. Fetch Personal Attendance
        cur.execute(
            """
            SELECT student_id, date, status
            FROM hostel.attendance
            WHERE student_id = %s
            ORDER BY date DESC;
            """,
            (student_id,)
        )
        attendance = cur.fetchall()

        # 7. Fetch Complaints filed by student
        cur.execute(
            """
            SELECT complaint_id, date, description, status, student_id
            FROM hostel.complaint
            WHERE student_id = %s
            ORDER BY date DESC;
            """,
            (student_id,)
        )
        complaints = cur.fetchall()

        # 8. Fetch Maintenance for the student's room
        maintenance_tickets = []
        if hostel_id and room_no:
            cur.execute(
                """
                SELECT request_id, hostel_id, room_no, description, date, status
                FROM hostel.maintenance
                WHERE hostel_id = %s AND room_no = %s
                ORDER BY date DESC;
                """,
                (hostel_id, room_no)
            )
            maintenance_tickets = cur.fetchall()

        # 9. Fetch Visitors logged for this student
        cur.execute(
            """
            SELECT v.visitor_id, vis.name, vis.relation, vis.phone, v.visit_date
            FROM hostel.visit v
            JOIN hostel.visitor vis ON v.visitor_id = vis.visitor_id
            WHERE v.student_id = %s
            ORDER BY v.visit_date DESC;
            """,
            (student_id,)
        )
        visitors = cur.fetchall()

        mess_dict = None
        if student["mess_id"]:
            mess_dict = {
                "mess_id": student["mess_id"],
                "type": student["mess_name"],
                "cost": student["mess_cost"]
            }

        return {
            "student_id": student["student_id"],
            "fname": student["fname"],
            "lname": student["lname"],
            "reg_no": student["reg_no"],
            "phone": student["phone"],
            "allot_date": student["allot_date"],
            "hostel_id": student["hostel_id"],
            "hostel_name": student["hostel_name"],
            "hostel_type": student["hostel_type"],
            "hostel_address": student["hostel_address"],
            "room_no": student["room_no"],
            "room_type": student["room_type"],
            "room_capacity": student["room_capacity"],
            "roommates": roommates,
            "warden": warden,
            "staff_contacts": staff_contacts,
            "mess": mess_dict,
            "fees": fees,
            "fines": fines,
            "attendance": attendance,
            "complaints": complaints,
            "maintenance_tickets": maintenance_tickets,
            "visitors": visitors,
        }
