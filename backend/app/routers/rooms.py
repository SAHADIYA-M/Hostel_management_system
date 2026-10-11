from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.db import get_db_connection
from app.schemas import RoomCreate, RoomResponse

router = APIRouter(prefix="/api/rooms", tags=["Rooms & Allotment"])


@router.get("", response_model=List[RoomResponse])
def get_all_rooms(
    hostel_id: Optional[int] = Query(None, description="Filter by hostel ID"),
    conn=Depends(get_db_connection)
):
    """
    Fetch all rooms with dynamic current occupancy count (from student table).
    Room is a weak entity identified by (hostel_id, room_no).
    """
    with conn.cursor() as cur:
        query = """
            SELECT 
                r.hostel_id,
                r.room_no,
                r.type,
                r.capacity,
                h.name AS hostel_name,
                COUNT(s.student_id) AS current_occupants
            FROM hostel.room r
            JOIN hostel.hostel h ON r.hostel_id = h.hostel_id
            LEFT JOIN hostel.student s ON r.hostel_id = s.hostel_id AND r.room_no = s.room_no
        """
        params = []
        if hostel_id is not None:
            query += " WHERE r.hostel_id = %s"
            params.append(hostel_id)
            
        query += """
            GROUP BY r.hostel_id, r.room_no, r.type, r.capacity, h.name
            ORDER BY r.hostel_id, r.room_no;
        """
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        return rows


@router.post("", response_model=RoomResponse, status_code=201)
def create_room(room: RoomCreate, conn=Depends(get_db_connection)):
    """Create a new room under a specific hostel."""
    with conn.cursor() as cur:
        # Check if room already exists
        cur.execute(
            "SELECT 1 FROM hostel.room WHERE hostel_id = %s AND room_no = %s",
            (room.hostel_id, room.room_no)
        )
        if cur.fetchone():
            raise HTTPException(
                status_code=400,
                detail=f"Room {room.room_no} already exists in Hostel {room.hostel_id}"
            )

        cur.execute(
            """
            INSERT INTO hostel.room (hostel_id, room_no, type, capacity)
            VALUES (%s, %s, %s, %s)
            RETURNING hostel_id, room_no, type, capacity;
            """,
            (room.hostel_id, room.room_no, room.type, room.capacity)
        )
        new_room = cur.fetchone()
        conn.commit()
        new_room["current_occupants"] = 0
        return new_room
