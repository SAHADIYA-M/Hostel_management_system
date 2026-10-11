"""
Pydantic schemas for Hostel Management System REST API.
Strictly aligned with docs/project-context.md (Revision 2) and ER diagram entities.
"""

from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


# -----------------------------------------------------------------------------
# 1. HOSTEL & WARDEN & STAFF
# -----------------------------------------------------------------------------
class HostelBase(BaseModel):
    name: str = Field(..., max_length=100)
    address: str = Field(..., max_length=255)
    type: str = Field(..., max_length=20)  # 'Boys' or 'Girls'


class HostelResponse(HostelBase):
    hostel_id: int
    warden_name: Optional[str] = None
    warden_phone: Optional[str] = None
    staff_count: Optional[int] = 0


# -----------------------------------------------------------------------------
# 2. ROOM (Weak entity: hostel_id + room_no)
# -----------------------------------------------------------------------------
class RoomCreate(BaseModel):
    hostel_id: int
    room_no: int
    type: str = Field(..., max_length=30)
    capacity: int = Field(..., gt=0)


class RoomResponse(BaseModel):
    hostel_id: int
    room_no: int
    type: str
    capacity: int
    current_occupants: int = 0
    hostel_name: Optional[str] = None


# -----------------------------------------------------------------------------
# 3. STUDENT
# -----------------------------------------------------------------------------
class StudentCreate(BaseModel):
    fname: str = Field(..., max_length=50)
    lname: str = Field(..., max_length=50)
    reg_no: str = Field(..., max_length=30)
    phone: str = Field(..., max_length=15)
    hostel_id: Optional[int] = None
    room_no: Optional[int] = None
    allot_date: Optional[date] = None
    mess_id: Optional[int] = None


class StudentAllotRequest(BaseModel):
    hostel_id: Optional[int] = None
    room_no: Optional[int] = None
    allot_date: Optional[date] = None


class StudentResponse(BaseModel):
    student_id: int
    fname: str
    lname: str
    reg_no: str
    phone: str
    hostel_id: Optional[int] = None
    room_no: Optional[int] = None
    allot_date: Optional[date] = None
    mess_id: Optional[int] = None
    hostel_name: Optional[str] = None
    room_type: Optional[str] = None
    mess_type: Optional[str] = None


# -----------------------------------------------------------------------------
# 4. FEE & FINE
# -----------------------------------------------------------------------------
class FeeCreate(BaseModel):
    due_date: date
    amount: Decimal = Field(..., ge=0)
    status: str = Field("Pending")
    student_id: int

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Pending", "Paid"):
            raise ValueError("Status must be 'Pending' or 'Paid'")
        return v


class FeeStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Pending", "Paid"):
            raise ValueError("Status must be 'Pending' or 'Paid'")
        return v


class FeeResponse(BaseModel):
    fee_id: int
    due_date: date
    amount: Decimal
    status: str
    student_id: int
    student_name: Optional[str] = None
    reg_no: Optional[str] = None


class FineCreate(BaseModel):
    reason: str = Field(..., max_length=255)
    amount: Decimal = Field(..., ge=0)
    status: str = Field("Pending")
    student_id: int

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Pending", "Paid"):
            raise ValueError("Status must be 'Pending' or 'Paid'")
        return v


class FineStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Pending", "Paid"):
            raise ValueError("Status must be 'Pending' or 'Paid'")
        return v


class FineResponse(BaseModel):
    fid: int
    reason: str
    amount: Decimal
    status: str
    student_id: int
    student_name: Optional[str] = None
    reg_no: Optional[str] = None


# -----------------------------------------------------------------------------
# 5. MESS
# -----------------------------------------------------------------------------
class MessCreate(BaseModel):
    type: str = Field(..., max_length=50)
    cost: Decimal = Field(..., ge=0)


class MessResponse(BaseModel):
    mess_id: int
    type: str
    cost: Decimal
    enrolled_count: Optional[int] = 0


# -----------------------------------------------------------------------------
# 6. ATTENDANCE (Composite key: student_id + date)
# -----------------------------------------------------------------------------
class AttendanceCreate(BaseModel):
    student_id: int
    date: date
    status: str = Field("Present")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Present", "Absent"):
            raise ValueError("Status must be 'Present' or 'Absent'")
        return v


class AttendanceBulkCreate(BaseModel):
    date: date
    hostel_id: Optional[int] = None
    status: str = Field("Present")


class AttendanceResponse(BaseModel):
    student_id: int
    date: date
    status: str
    student_name: Optional[str] = None
    reg_no: Optional[str] = None
    room_no: Optional[int] = None
    hostel_id: Optional[int] = None
    hostel_name: Optional[str] = None


# -----------------------------------------------------------------------------
# 7. VISITOR & VISIT
# -----------------------------------------------------------------------------
class VisitorCreate(BaseModel):
    name: str = Field(..., max_length=100)
    relation: str = Field(..., max_length=50)
    phone: str = Field(..., max_length=15)


class VisitorResponse(BaseModel):
    visitor_id: int
    name: str
    relation: str
    phone: str


class VisitCreate(BaseModel):
    student_id: int
    visitor_id: int
    visit_date: date


class VisitResponse(BaseModel):
    student_id: int
    visitor_id: int
    visit_date: date
    student_name: Optional[str] = None
    visitor_name: Optional[str] = None
    relation: Optional[str] = None


# -----------------------------------------------------------------------------
# 8. MAINTENANCE & COMPLAINT
# -----------------------------------------------------------------------------
class MaintenanceCreate(BaseModel):
    hostel_id: int
    room_no: Optional[int] = None
    description: str = Field(..., max_length=500)
    date: date
    status: str = Field("Open")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Open", "In Progress", "Resolved"):
            raise ValueError("Status must be 'Open', 'In Progress', or 'Resolved'")
        return v


class MaintenanceStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Open", "In Progress", "Resolved"):
            raise ValueError("Status must be 'Open', 'In Progress', or 'Resolved'")
        return v


class MaintenanceResponse(BaseModel):
    request_id: int
    hostel_id: int
    room_no: Optional[int] = None
    description: str
    date: date
    status: str
    hostel_name: Optional[str] = None


class ComplaintCreate(BaseModel):
    date: date
    description: str = Field(..., max_length=500)
    status: str = Field("Open")
    student_id: int

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Open", "In Progress", "Resolved"):
            raise ValueError("Status must be 'Open', 'In Progress', or 'Resolved'")
        return v


class ComplaintStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Open", "In Progress", "Resolved"):
            raise ValueError("Status must be 'Open', 'In Progress', or 'Resolved'")
        return v


class ComplaintResponse(BaseModel):
    complaint_id: int
    date: date
    description: str
    status: str
    student_id: int
    student_name: Optional[str] = None
    reg_no: Optional[str] = None


# -----------------------------------------------------------------------------
# 9. STUDENT SELF-SERVICE PORTAL AGGREGATED RESPONSE
# -----------------------------------------------------------------------------
class StudentPortalResponse(BaseModel):
    student_id: int
    fname: str
    lname: str
    reg_no: str
    phone: str
    allot_date: Optional[date] = None

    # Hostel & Room
    hostel_id: Optional[int] = None
    hostel_name: Optional[str] = None
    hostel_type: Optional[str] = None
    hostel_address: Optional[str] = None
    room_no: Optional[int] = None
    room_type: Optional[str] = None
    room_capacity: Optional[int] = None

    # Roommates
    roommates: List[dict] = []

    # Contacts
    warden: Optional[dict] = None
    staff_contacts: List[dict] = []

    # Mess Plan
    mess: Optional[dict] = None

    # Personal Records
    fees: List[FeeResponse] = []
    fines: List[FineResponse] = []
    attendance: List[AttendanceResponse] = []
    complaints: List[ComplaintResponse] = []
    maintenance_tickets: List[MaintenanceResponse] = []
    visitors: List[dict] = []
