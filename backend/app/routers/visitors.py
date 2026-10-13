from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date as DateType
from app.db import get_db_connection
from app.schemas import VisitorCreate, VisitorResponse, VisitCreate, VisitResponse

router = APIRouter(prefix="/api", tags=["Visitors & Visits"])


@router.get("/visitors", response_model=List[VisitorResponse])
def get_all_visitors(conn=Depends(get_db_connection)):
    """Fetch visitor directory."""
    with conn.cursor() as cur:
        cur.execute("SELECT visitor_id, name, relation, phone FROM hostel.visitor ORDER BY visitor_id;")
        return cur.fetchall()


@router.post("/visitors", response_model=VisitorResponse, status_code=201)
def create_visitor(visitor: VisitorCreate, conn=Depends(get_db_connection)):
    """Register a new visitor."""
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(visitor_id), 200) + 1 AS next_id FROM hostel.visitor;")
        next_id = cur.fetchone()["next_id"]

        cur.execute(
            """
            INSERT INTO hostel.visitor (visitor_id, name, relation, phone)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
            """,
            (next_id, visitor.name, visitor.relation, visitor.phone)
        )
        created = cur.fetchone()
        conn.commit()
        return created


@router.get("/visits", response_model=List[VisitResponse])
def get_all_visits(
    student_id: Optional[int] = Query(None),
    visit_date: Optional[DateType] = Query(None),
    conn=Depends(get_db_connection)
):
    """Fetch visit logs with joined student and visitor details."""
    with conn.cursor() as cur:
        query = """
            SELECT 
                v.student_id,
                v.visitor_id,
                v.visit_date,
                CONCAT(s.fname, ' ', s.lname) AS student_name,
                vis.name AS visitor_name,
                vis.relation
            FROM hostel.visit v
            JOIN hostel.student s ON v.student_id = s.student_id
            JOIN hostel.visitor vis ON v.visitor_id = vis.visitor_id
            WHERE 1=1
        """
        params = []
        if student_id is not None:
            query += " AND v.student_id = %s"
            params.append(student_id)
        if visit_date is not None:
            query += " AND v.visit_date = %s"
            params.append(visit_date)

        query += " ORDER BY v.visit_date DESC;"
        cur.execute(query, tuple(params))
        return cur.fetchall()


@router.post("/visits", response_model=VisitResponse, status_code=201)
def create_visit(visit: VisitCreate, conn=Depends(get_db_connection)):
    """Log a student visit (Rule 11: 1 visit per student-visitor pair per day)."""
    with conn.cursor() as cur:
        try:
            cur.execute(
                """
                INSERT INTO hostel.visit (student_id, visitor_id, visit_date)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (visit.student_id, visit.visitor_id, visit.visit_date)
            )
            created = cur.fetchone()
            conn.commit()

            cur.execute("SELECT CONCAT(fname, ' ', lname) AS student_name FROM hostel.student WHERE student_id = %s;", (visit.student_id,))
            s_row = cur.fetchone() or {}

            cur.execute("SELECT name AS visitor_name, relation FROM hostel.visitor WHERE visitor_id = %s;", (visit.visitor_id,))
            v_row = cur.fetchone() or {}

            return {**created, **s_row, **v_row}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.delete("/visitors/{visitor_id}", status_code=200)
def delete_visitor(visitor_id: int, conn=Depends(get_db_connection)):
    """Delete a visitor record."""
    with conn.cursor() as cur:
        try:
            cur.execute("DELETE FROM hostel.visitor WHERE visitor_id = %s RETURNING visitor_id;", (visitor_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Visitor not found")
            conn.commit()
            return {"message": "Visitor deleted successfully", "visitor_id": visitor_id}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))
