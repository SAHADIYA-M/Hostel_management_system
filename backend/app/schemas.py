"""
Pydantic schemas for Hostel Management System REST API.
Strictly aligned with docs/project-context.md (Revision 2) and ER diagram entities.
"""

import re
from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator

# Indian Mobile Number: 10 digits starting with 6, 7, 8, 9; optional '+91' prefix
INDIAN_PHONE_REGEX = re.compile(r"^(\+91)?[6-9]\d{9}$")

# Student Register Number: exactly 10 characters, starting with 'REG' followed by 7 digits
REG_NO_REGEX = re.compile(r"^REG\d{7}$")

# Name format: letters, spaces, dots for initials
NAME_REGEX = re.compile(r"^[A-Za-z][A-Za-z\s\.]*$")


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
    room_no: int = Field(..., ge=100, le=999)
    type: str = Field(..., min_length=3, max_length=30)
    capacity: int = Field(..., ge=1, le=10)


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
    fname: str = Field(..., min_length=1, max_length=50)
    lname: str = Field(..., min_length=1, max_length=50)
    reg_no: str = Field(..., min_length=10, max_length=10)
    phone: str = Field(..., min_length=10, max_length=15)
    hostel_id: Optional[int] = None
    room_no: Optional[int] = Field(None, ge=100, le=999)
    allot_date: Optional[date] = None
    mess_id: Optional[int] = None

    @field_validator("reg_no")
    @classmethod
    def validate_reg_no(cls, v: str) -> str:
        cleaned = v.strip().upper()
        if not REG_NO_REGEX.match(cleaned):
            raise ValueError("Student registration number must be exactly 10 characters starting with 'REG' followed by 7 digits (e.g. REG2024001).")
        return cleaned

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = v.strip()
        if not INDIAN_PHONE_REGEX.match(cleaned):
            raise ValueError("Mobile number must be a valid 10-digit Indian mobile number starting with 6, 7, 8, or 9 (optional '+91' prefix, e.g. 9876543210 or +919876543210).")
        return cleaned

    @field_validator("fname", "lname")
    @classmethod
    def validate_name(cls, v: str) -> str:
        cleaned = v.strip()
        if not NAME_REGEX.match(cleaned):
            raise ValueError("Name must contain letters, spaces, or periods only.")
        return cleaned


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
    amount: Decimal = Field(..., gt=0, le=200000)
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
    reason: str = Field(..., min_length=5, max_length=255)
    amount: Decimal = Field(..., gt=0, le=50000)
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
    type: str = Field(..., min_length=3, max_length=50)
    cost: Decimal = Field(..., gt=0, le=50000)


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
    name: str = Field(..., min_length=2, max_length=100)
    relation: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., min_length=10, max_length=15)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = v.strip()
        if not INDIAN_PHONE_REGEX.match(cleaned):
            raise ValueError("Mobile number must be a valid 10-digit Indian mobile number starting with 6, 7, 8, or 9 (optional '+91' prefix, e.g. 9845011111 or +919845011111).")
        return cleaned

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        cleaned = v.strip()
        if not NAME_REGEX.match(cleaned):
            raise ValueError("Visitor name must contain letters, spaces, or periods only.")
        return cleaned


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
    room_no: Optional[int] = Field(None, ge=100, le=999)
    description: str = Field(..., min_length=5, max_length=500)
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
    description: str = Field(..., min_length=5, max_length=500)
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
