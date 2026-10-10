-- ============================================================================
-- Hostel Management System — Relational Schema (PostgreSQL 16)
-- Schema: hostel
-- Baseline Specification: docs/project-context.md (Revision 2)
--
-- Rules:
-- 1. Unquoted, lowercase-friendly identifiers (no case sensitivity issues).
-- 2. Schema namespaced under "hostel".
-- 3. Composite foreign key in maintenance uses MATCH SIMPLE (default) so
--    hostel-wide requests (where room_no IS NULL) are allowed.
-- 4. Triggers (room capacity & warden check) reside in triggers.sql.
-- ============================================================================

-- Create and set schema
CREATE SCHEMA IF NOT EXISTS hostel;
SET search_path TO hostel, public;

-- Drop existing tables in reverse dependency order (safe re-run)
DROP TABLE IF EXISTS hostel.complaint CASCADE;
DROP TABLE IF EXISTS hostel.maintenance CASCADE;
DROP TABLE IF EXISTS hostel.visit CASCADE;
DROP TABLE IF EXISTS hostel.visitor CASCADE;
DROP TABLE IF EXISTS hostel.attendance CASCADE;
DROP TABLE IF EXISTS hostel.fine CASCADE;
DROP TABLE IF EXISTS hostel.fee CASCADE;
DROP TABLE IF EXISTS hostel.student CASCADE;
DROP TABLE IF EXISTS hostel.mess CASCADE;
DROP TABLE IF EXISTS hostel.room CASCADE;
DROP TABLE IF EXISTS hostel.staff CASCADE;
DROP TABLE IF EXISTS hostel.warden CASCADE;
DROP TABLE IF EXISTS hostel.hostel CASCADE;

-- ----------------------------------------------------------------------------
-- 1. HOSTEL
-- Represents each hostel building managed by the college.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.hostel (
    hostel_id       INT             PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    address         VARCHAR(255)    NOT NULL,
    type            VARCHAR(20)     NOT NULL
);

-- ----------------------------------------------------------------------------
-- 2. WARDEN
-- Represents the warden responsible for a hostel (1:1 with HOSTEL).
-- UNIQUE on hostel_id ensures no two wardens manage the same hostel.
-- Mandatory warden existence per hostel is enforced in database/triggers.sql.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.warden (
    warden_id       INT             PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    phone           VARCHAR(15)     NOT NULL,
    hostel_id       INT             NOT NULL UNIQUE,

    CONSTRAINT fk_warden_hostel
        FOREIGN KEY (hostel_id)
        REFERENCES hostel.hostel(hostel_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 3. STAFF
-- Represents staff employed by a hostel (1:N from HOSTEL).
-- Per ER diagram, STAFF has no name attribute (only role and phone).
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.staff (
    staff_id        INT             PRIMARY KEY,
    role            VARCHAR(50)     NOT NULL,
    phone           VARCHAR(15)     NOT NULL,
    hostel_id       INT             NOT NULL,

    CONSTRAINT fk_staff_hostel
        FOREIGN KEY (hostel_id)
        REFERENCES hostel.hostel(hostel_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 4. ROOM (Weak Entity)
-- Identified by composite key (hostel_id, room_no).
-- Room numbers repeat across hostels, so room_no is only unique within hostel.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.room (
    hostel_id       INT             NOT NULL,
    room_no         INT             NOT NULL,
    type            VARCHAR(30)     NOT NULL,
    capacity        INT             NOT NULL,

    CONSTRAINT pk_room
        PRIMARY KEY (hostel_id, room_no),

    CONSTRAINT fk_room_hostel
        FOREIGN KEY (hostel_id)
        REFERENCES hostel.hostel(hostel_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_room_capacity_positive
        CHECK (capacity > 0)
);

-- ----------------------------------------------------------------------------
-- 5. MESS
-- Represents mess subscription plans available to students (1:N to STUDENT).
-- Cost cannot be negative.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.mess (
    mess_id         INT             PRIMARY KEY,
    type            VARCHAR(50)     NOT NULL,
    cost            NUMERIC(10, 2)  NOT NULL,

    CONSTRAINT chk_mess_cost_non_negative
        CHECK (cost >= 0)
);

-- ----------------------------------------------------------------------------
-- 6. STUDENT
-- Registered students. Stores current room allotment and mess plan.
-- Allotment rule: hostel_id, room_no, and allot_date must either ALL be
-- populated or ALL be NULL (student not allotted a room yet).
-- Room capacity limit enforcement is handled in database/triggers.sql.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.student (
    student_id      INT             PRIMARY KEY,
    fname           VARCHAR(50)     NOT NULL,
    lname           VARCHAR(50)     NOT NULL,
    reg_no          VARCHAR(30)     NOT NULL UNIQUE,
    phone           VARCHAR(15)     NOT NULL,
    hostel_id       INT             NULL,
    room_no         INT             NULL,
    allot_date      DATE            NULL,
    mess_id         INT             NULL,

    CONSTRAINT fk_student_room
        FOREIGN KEY (hostel_id, room_no)
        REFERENCES hostel.room(hostel_id, room_no)
        MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_student_mess
        FOREIGN KEY (mess_id)
        REFERENCES hostel.mess(mess_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT chk_allotment_all_or_none
        CHECK (
            (hostel_id IS NULL AND room_no IS NULL AND allot_date IS NULL)
            OR
            (hostel_id IS NOT NULL AND room_no IS NOT NULL AND allot_date IS NOT NULL)
        )
);

-- ----------------------------------------------------------------------------
-- 7. FEE
-- Fee records incurred by students (1:N from STUDENT).
-- Status domain: Pending or Paid.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.fee (
    fee_id          INT             PRIMARY KEY,
    due_date        DATE            NOT NULL,
    amount          NUMERIC(10, 2)  NOT NULL,
    status          VARCHAR(10)     NOT NULL,
    student_id      INT             NOT NULL,

    CONSTRAINT fk_fee_student
        FOREIGN KEY (student_id)
        REFERENCES hostel.student(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_fee_amount_non_negative
        CHECK (amount >= 0),

    CONSTRAINT chk_fee_status_domain
        CHECK (status IN ('Pending', 'Paid'))
);

-- ----------------------------------------------------------------------------
-- 8. FINE
-- Fines incurred by students (1:N from STUDENT). Retained as separate entity.
-- Status domain: Pending or Paid.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.fine (
    fid             INT             PRIMARY KEY,
    reason          VARCHAR(255)    NOT NULL,
    amount          NUMERIC(10, 2)  NOT NULL,
    status          VARCHAR(10)     NOT NULL,
    student_id      INT             NOT NULL,

    CONSTRAINT fk_fine_student
        FOREIGN KEY (student_id)
        REFERENCES hostel.student(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_fine_amount_non_negative
        CHECK (amount >= 0),

    CONSTRAINT chk_fine_status_domain
        CHECK (status IN ('Pending', 'Paid'))
);

-- ----------------------------------------------------------------------------
-- 9. ATTENDANCE (Weak Entity)
-- Identified by composite key (student_id, date).
-- Enforces at most one attendance record per student per date.
-- Status domain: Present or Absent.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.attendance (
    student_id      INT             NOT NULL,
    date            DATE            NOT NULL,
    status          VARCHAR(10)     NOT NULL,

    CONSTRAINT pk_attendance
        PRIMARY KEY (student_id, date),

    CONSTRAINT fk_attendance_student
        FOREIGN KEY (student_id)
        REFERENCES hostel.student(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_attendance_status_domain
        CHECK (status IN ('Present', 'Absent'))
);

-- ----------------------------------------------------------------------------
-- 10. VISITOR
-- Independent visitor records (M:N with STUDENT via VISIT).
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.visitor (
    visitor_id      INT             PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    relation        VARCHAR(50)     NOT NULL,
    phone           VARCHAR(15)     NOT NULL
);

-- ----------------------------------------------------------------------------
-- 11. VISIT (Junction Table for M:N)
-- Associative table implementing the VISITED_BY relationship.
-- Composite primary key (student_id, visitor_id, visit_date) prevents
-- duplicate entries for the same student-visitor pair on the same date.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.visit (
    student_id      INT             NOT NULL,
    visitor_id      INT             NOT NULL,
    visit_date      DATE            NOT NULL,

    CONSTRAINT pk_visit
        PRIMARY KEY (student_id, visitor_id, visit_date),

    CONSTRAINT fk_visit_student
        FOREIGN KEY (student_id)
        REFERENCES hostel.student(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_visit_visitor
        FOREIGN KEY (visitor_id)
        REFERENCES hostel.visitor(visitor_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 12. MAINTENANCE
-- Maintenance requests concerning a hostel generally or a specific room.
-- hostel_id is mandatory. room_no is nullable (NULL = hostel-wide issue).
-- Composite FK (hostel_id, room_no) uses MATCH SIMPLE (default) so that
-- rows with room_no IS NULL are permitted without violating integrity.
-- Status domain: Open, In Progress, Resolved.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.maintenance (
    request_id      INT             PRIMARY KEY,
    hostel_id       INT             NOT NULL,
    room_no         INT             NULL,
    description     VARCHAR(500)    NOT NULL,
    date            DATE            NOT NULL,
    status          VARCHAR(15)     NOT NULL,

    CONSTRAINT fk_maintenance_hostel
        FOREIGN KEY (hostel_id)
        REFERENCES hostel.hostel(hostel_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_maintenance_room
        FOREIGN KEY (hostel_id, room_no)
        REFERENCES hostel.room(hostel_id, room_no)
        MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT chk_maintenance_status_domain
        CHECK (status IN ('Open', 'In Progress', 'Resolved'))
);

-- ----------------------------------------------------------------------------
-- 13. COMPLAINT
-- Complaints filed by students (1:N from STUDENT).
-- Status domain: Open, In Progress, Resolved.
-- ----------------------------------------------------------------------------
CREATE TABLE hostel.complaint (
    complaint_id    INT             PRIMARY KEY,
    date            DATE            NOT NULL,
    description     VARCHAR(500)    NOT NULL,
    status          VARCHAR(15)     NOT NULL,
    student_id      INT             NOT NULL,

    CONSTRAINT fk_complaint_student
        FOREIGN KEY (student_id)
        REFERENCES hostel.student(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_complaint_status_domain
        CHECK (status IN ('Open', 'In Progress', 'Resolved'))
);

-- ============================================================================
-- Helpful Indexes for Foreign Keys & Common Queries
-- ============================================================================
CREATE INDEX idx_student_room ON hostel.student(hostel_id, room_no);
CREATE INDEX idx_student_mess ON hostel.student(mess_id);
CREATE INDEX idx_fee_student ON hostel.fee(student_id);
CREATE INDEX idx_fine_student ON hostel.fine(student_id);
CREATE INDEX idx_attendance_student ON hostel.attendance(student_id);
CREATE INDEX idx_visit_student ON hostel.visit(student_id);
CREATE INDEX idx_visit_visitor ON hostel.visit(visitor_id);
CREATE INDEX idx_maintenance_hostel ON hostel.maintenance(hostel_id);
CREATE INDEX idx_complaint_student ON hostel.complaint(student_id);
