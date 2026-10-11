from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.db import get_db_connection
from app.schemas import HostelResponse

router = APIRouter(prefix="/api/hostels", tags=["Hostels & Staff"])


@router.get("", response_model=List[HostelResponse])
def get_all_hostels(conn=Depends(get_db_connection)):
    """
    Fetch all hostels along with their assigned 1:1 Warden and Staff count.
    Strictly Raw SQL.
    """
    with conn.cursor() as cur:
        query = """
            SELECT 
                h.hostel_id,
                h.name,
                h.address,
                h.type,
                w.name AS warden_name,
                w.phone AS warden_phone,
                COUNT(st.staff_id) AS staff_count
            FROM hostel.hostel h
            LEFT JOIN hostel.warden w ON h.hostel_id = w.hostel_id
            LEFT JOIN hostel.staff st ON h.hostel_id = st.hostel_id
            GROUP BY h.hostel_id, h.name, h.address, h.type, w.name, w.phone
            ORDER BY h.hostel_id;
        """
        cur.execute(query)
        rows = cur.fetchall()
        return rows


@router.get("/{hostel_id}/staff")
def get_hostel_staff(hostel_id: int, conn=Depends(get_db_connection)):
    """Fetch staff list for a specific hostel."""
    with conn.cursor() as cur:
        query = """
            SELECT staff_id, role, phone, hostel_id
            FROM hostel.staff
            WHERE hostel_id = %s
            ORDER BY staff_id;
        """
        cur.execute(query, (hostel_id,))
        return cur.fetchall()
