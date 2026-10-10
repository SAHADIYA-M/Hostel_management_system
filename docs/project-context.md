# Hostel Management System — Project Context and Finalized Relational Design (Revision 2)

## 1. Purpose

This document defines the scope, conceptual entities, relationships, relational schema, and business rules of our college DBMS project: **Hostel Management System**.

The purpose is to establish a clear and consistent understanding of the database before implementation begins.

This document focuses exclusively on the project's requirements and database design. It does not define the technology stack, application architecture, or implementation workflow.

Treat the design decisions documented here as the agreed baseline. Do not independently add features, alter relationships, or introduce additional tables without a clear requirement.

**Source hierarchy.** The latest ER diagram (12 entities, including FINE) is the conceptual source of truth. This document is the relational baseline derived from it. An earlier hand-drawn relational schema also exists; where it conflicts with this document, this document wins (see Section 9 for the specific errors found in it).

## 2. Project Overview

The Hostel Management System manages the essential records and operations of a college hostel, including:

- Hostel and warden information.
- Hostel staff.
- Rooms and student room allotments.
- Student records.
- Mess subscriptions.
- Student fees and fines.
- Attendance.
- Visitors and visit records.
- Maintenance requests.
- Student complaints.

The database must represent these operations correctly, maintain referential integrity, reduce unnecessary data duplication, and enforce appropriate constraints.

The ER diagram defines the conceptual entities and relationships. The relational schema in this document maps that conceptual design into tables, primary keys, foreign keys, and constraints.

## 3. Entities and Attributes

### 3.1 HOSTEL

`HOSTEL(Hostel_ID, Name, Address, Type)`

- Hostel_ID is the primary key.
- Represents each hostel managed by the institution.

### 3.2 WARDEN

`WARDEN(Warden_ID, Name, Phone)`

- Warden_ID is the primary key.
- Represents the warden responsible for a hostel.

### 3.3 STAFF

`STAFF(Staff_ID, Role, Phone)`

- Staff_ID is the primary key.
- Represents staff members employed by a hostel.
- The current ER diagram has no Name attribute for staff (see Open Item B).

### 3.4 ROOM — Weak Entity

`ROOM(Room_No, Type, Capacity)`

- Room_No is a partial key in the conceptual ER model.
- A room is identified using its Room_No and the Hostel_ID of its parent hostel.
- A room cannot exist independently of its hostel.

### 3.5 STUDENT

`STUDENT(Student_ID, FName, LName, Reg_No, Phone)`

- Student_ID is the primary key.
- Reg_No must be unique.
- Represents students registered in the hostel management system.
- The current ER diagram has no Dept attribute; do not add one.

### 3.6 VISITOR

`VISITOR(Visitor_ID, Name, Relation, Phone)`

- Visitor_ID is the primary key.
- Stores visitor information independently of individual visit records.

### 3.7 FEE

`FEE(Fee_ID, Due_Date, Amount, Status)`

- Fee_ID is the primary key.
- Represents fee records belonging to students.

### 3.8 FINE

`FINE(FID, Reason, Amount, Status)`

- FID is the primary key.
- Represents fines incurred by students.
- This entity is retained from the original conceptual entity list and appears in the current ER diagram.

### 3.9 MESS

`MESS(Mess_ID, Type, Cost)`

- Mess_ID is the primary key.
- Represents the mess options available to students.

### 3.10 ATTENDANCE — Weak Entity

`ATTENDANCE(Date, Status)`

- Date is a partial key in the conceptual ER model.
- An attendance record is identified by the student it belongs to and its date.

### 3.11 MAINTENANCE

`MAINTENANCE(Request_ID, Room_No, Description, Date, Status)`

- Request_ID is the primary key.
- Represents maintenance requests concerning a hostel or a specific room.
- Room_No is drawn as an ordinary attribute in the ER diagram; in the relational mapping it becomes part of a composite foreign key together with Hostel_ID (see 5.12).

### 3.12 COMPLAINT

`COMPLAINT(Complaint_ID, Date, Description, Status)`

- Complaint_ID is the primary key.
- Represents complaints filed by students.

## 4. Conceptual Relationships and Cardinalities

The following relationships define the intended conceptual design.

| Relationship | Cardinality | Meaning |
|---|---|---|
| HOSTEL — WARDEN | 1:1 | Every hostel must have exactly one warden, and every warden manages exactly one hostel. |
| HOSTEL — STAFF | 1:N | A hostel can employ multiple staff members; each staff member belongs to one hostel. |
| HOSTEL — ROOM | 1:N | A hostel contains multiple rooms. ROOM is a weak entity identified through HOSTEL. |
| HOSTEL — MAINTENANCE | 1:N | A hostel can have multiple maintenance requests; each request belongs to exactly one hostel. This is drawn as the Hostel line into the existing UNDERGOES relationship, not as an additional relationship. |
| ROOM — MAINTENANCE | 1:N | A room can have multiple maintenance requests. A request may also concern the hostel generally, with no specific room. |
| ROOM — STUDENT | 1:N | A room can accommodate multiple students, subject to capacity. Each student has at most one current room allotment. The relationship has Allot_Date. |
| STUDENT — FINE | 1:N | A student can incur multiple fines; each fine belongs to one student. |
| STUDENT — FEE | 1:N | A student can have multiple fee records; each fee record belongs to one student. |
| STUDENT — VISITOR | M:N | A student can have multiple visitors, and a visitor can visit multiple students. The relationship has Visit_Date. |
| STUDENT — MESS | N:1 | Multiple students can use the same mess, while each student has at most one current mess subscription. |
| STUDENT — ATTENDANCE | 1:N | A student can have multiple attendance records, with at most one record per date. ATTENDANCE is a weak entity. |
| STUDENT — COMPLAINT | 1:N | A student can file multiple complaints; each complaint belongs to one student. |

**Mapping principle:** Foreign keys introduced during relational mapping implement these relationships. They are not additional conceptual attributes in the original ER diagram. In every 1:N relationship the foreign key sits on the "N" side.

### 4.1 Participation Constraints

Participation is derived from what the relational schema can actually enforce. The ER diagram's double lines must be made consistent with this table (see Open Item A).

| Relationship | Total participation (double line) | Partial participation (single line) |
|---|---|---|
| HOSTEL — WARDEN | Both sides | — |
| HOSTEL — STAFF | STAFF (Hostel_ID NOT NULL) | HOSTEL |
| HOSTEL — ROOM | ROOM (weak entity, always total) | HOSTEL |
| HOSTEL — MAINTENANCE | MAINTENANCE (Hostel_ID NOT NULL) | HOSTEL |
| ROOM — MAINTENANCE | — | Both sides (Room_No is nullable) |
| ROOM — STUDENT | — | Both sides (a student may have no room yet) |
| STUDENT — FEE | FEE | STUDENT |
| STUDENT — FINE | FINE | STUDENT |
| STUDENT — COMPLAINT | COMPLAINT | STUDENT |
| STUDENT — ATTENDANCE | ATTENDANCE (weak entity, always total) | STUDENT |
| STUDENT — MESS | — | Both sides (Mess_ID is nullable) |
| STUDENT — VISITOR | — | Both sides |

## 5. Finalized Relational Schema

Notation:

- PK: Primary Key
- FK: Foreign Key
- UNIQUE: Value must be unique
- NOT NULL: Value is mandatory
- NULL: Value may be absent
- CHECK: Restricts permitted values

### 5.1 HOSTEL

`HOSTEL(Hostel_ID PK, Name, Address, Type)`

- HOSTEL contains no Warden_ID and no Staff_ID. Those links are held by WARDEN.Hostel_ID and STAFF.Hostel_ID.

### 5.2 WARDEN

`WARDEN(Warden_ID PK, Name, Phone, Hostel_ID FK UNIQUE NOT NULL)`

- Hostel_ID references HOSTEL(Hostel_ID).
- Each warden belongs to exactly one hostel.
- A hostel cannot have multiple wardens.
- The requirement that every hostel has a warden must also be enforced; UNIQUE and NOT NULL alone do not guarantee it.

### 5.3 STAFF

`STAFF(Staff_ID PK, Role, Phone, Hostel_ID FK NOT NULL)`

- Hostel_ID references HOSTEL(Hostel_ID).
- Each staff member belongs to one hostel.

### 5.4 ROOM

`ROOM(Hostel_ID PK/FK, Room_No PK, Type, Capacity)`

- Composite primary key: `(Hostel_ID, Room_No)`.
- Hostel_ID references HOSTEL(Hostel_ID).
- Capacity must be greater than zero.
- Room_No is only unique within a hostel.
- This preserves the weak-entity identification of ROOM.

### 5.5 MESS

`MESS(Mess_ID PK, Type, Cost)`

- Cost must be greater than or equal to zero.
- MESS does not have a Date attribute.
- MESS contains no Student_ID; the link is held by STUDENT.Mess_ID.

### 5.6 STUDENT

`STUDENT(Student_ID PK, FName, LName, Reg_No UNIQUE, Phone, Hostel_ID NULL, Room_No NULL, Allot_Date NULL, Mess_ID FK NULL)`

Constraints and relationships:

- Mess_ID references MESS(Mess_ID).
- `(Hostel_ID, Room_No)` references ROOM(Hostel_ID, Room_No).
- Hostel_ID, Room_No, and Allot_Date must either all be populated or all be NULL.
- A student may initially be registered without a room.
- Each student has at most one current room allotment.
- The design stores only the current allotment, not a history of previous allocations.
- Multiple students may share a room, but the room capacity must not be exceeded.
- Each student has at most one current mess subscription.
- STUDENT contains no Fee_ID and no Complaint_ID; those links are held by FEE.Student_ID and COMPLAINT.Student_ID.

### 5.7 VISITOR

`VISITOR(Visitor_ID PK, Name, Relation, Phone)`

- Stores visitor details independently.
- Does not contain Student_ID because the relationship is many-to-many and is represented by VISIT.

### 5.8 FEE

`FEE(Fee_ID PK, Due_Date, Amount, Status, Student_ID FK NOT NULL)`

- Student_ID references STUDENT(Student_ID).
- Amount must be greater than or equal to zero.
- Each fee record belongs to one student.

### 5.9 FINE

`FINE(FID PK, Reason, Amount, Status, Student_ID FK NOT NULL)`

- Student_ID references STUDENT(Student_ID).
- Amount must be greater than or equal to zero.
- Each fine belongs to one student.

### 5.10 ATTENDANCE

`ATTENDANCE(Student_ID PK/FK, Date PK, Status)`

- Composite primary key: `(Student_ID, Date)`.
- Student_ID references STUDENT(Student_ID).
- Each student can have at most one attendance record per date.
- Status is restricted to Present or Absent.

### 5.11 VISIT

`VISIT(Student_ID PK/FK, Visitor_ID PK/FK, Visit_Date PK)`

- Composite primary key: `(Student_ID, Visitor_ID, Visit_Date)`.
- Student_ID references STUDENT(Student_ID).
- Visitor_ID references VISITOR(Visitor_ID).
- A student–visitor pair can have at most one record per day.
- No separate Visit_ID is required.
- This is the table for the VISITED_BY relationship in the ER diagram. The team may name the table VISIT or VISITED_BY, but must use one name consistently.

### 5.12 MAINTENANCE

`MAINTENANCE(Request_ID PK, Hostel_ID FK NOT NULL, Room_No NULL, Description, Date, Status)`

- Hostel_ID references HOSTEL(Hostel_ID).
- `(Hostel_ID, Room_No)` references ROOM(Hostel_ID, Room_No) when Room_No is provided.
- Room_No is nullable.
- A NULL Room_No means the request concerns the hostel generally.
- A populated Room_No means the request concerns that room within the specified hostel.
- The composite foreign key prevents a room from being associated with the wrong hostel.

### 5.13 COMPLAINT

`COMPLAINT(Complaint_ID PK, Date, Description, Status, Student_ID FK NOT NULL)`

- Student_ID references STUDENT(Student_ID).
- Each complaint belongs to one student.

### 5.14 Status Domains

The ER diagram does not fix the allowed Status values except for ATTENDANCE. The following domains are proposed, consistent with the sample data already used by the team, and should be treated as an assumption that can be changed with approval:

- FEE.Status and FINE.Status: Pending or Paid.
- COMPLAINT.Status and MAINTENANCE.Status: Open, In Progress, or Resolved.
- ATTENDANCE.Status: Present or Absent.

## 6. Decisions That Must Not Be Changed Silently

### Decision 1: Student–Mess

The relationship is N:1 from STUDENT to MESS.

Mess_ID belongs in STUDENT, not MESS. This allows multiple students to share a mess without duplicating mess details.

### Decision 2: Current Room Allotment

The system stores only the current room allotment.

Hostel_ID, Room_No, and Allot_Date belong in STUDENT. A separate ROOM_ALLOCATION table is not part of the current design.

### Decision 3: Composite Room Key

ROOM is identified by `(Hostel_ID, Room_No)` because room numbers may repeat across hostels.

All foreign keys referencing a room must use both columns.

### Decision 4: Maintenance Scope

The design supports both hostel-wide and room-specific maintenance.

Hostel_ID is mandatory; Room_No is optional. A room-specific request must reference a room in that same hostel.

This is achieved through the existing UNDERGOES relationship (Hostel and Room both connect to MAINTENANCE) and a foreign-key column, not through an extra relationship or table.

### Decision 5: Attendance Key

ATTENDANCE uses `(Student_ID, Date)` as its composite primary key. This prevents duplicate attendance records for a student on the same date.

### Decision 6: Visitor Relationship

VISIT is the associative table for the M:N relationship between STUDENT and VISITOR. Its composite primary key is `(Student_ID, Visitor_ID, Visit_Date)`.

### Decision 7: Warden Assignment

The conceptual requirement is exactly one warden per hostel and exactly one hostel per warden.

WARDEN.Hostel_ID is UNIQUE and NOT NULL. Additional database-level enforcement is required to guarantee that a hostel cannot exist without a warden. Do not silently weaken the conceptual requirement merely because it needs more careful enforcement.

### Decision 8: No Unnecessary Historical Tables

Do not add room-allocation history, dated mess subscriptions, or additional junction tables unless a new requirement explicitly calls for them.

### Decision 9: Foreign Key Placement

In every 1:N relationship the foreign key is stored on the "N" side only. Do not store the key on both sides, and do not store a list or single reference to the "many" side on the "one" side. In particular:

- Warden and Staff reference Hostel; Hostel does not reference them.
- Fee, Fine, and Complaint reference Student; Student does not reference them.
- Student references Mess; Mess does not reference Student.

### Decision 10: FINE Is a Separate Entity

FINE remains its own table with its own Student_ID foreign key. It is not merged into FEE.

## 7. Integrity Constraints and Business Rules

The final database design must address these rules:

1. All primary keys uniquely identify records.
2. All foreign keys reference valid parent records.
3. ROOM cannot exist without HOSTEL.
4. A student cannot be assigned to a room in a different or nonexistent hostel.
5. Room-allotment fields must be all populated or all NULL.
6. Room capacity must be positive.
7. Room occupancy must not exceed capacity.
8. Every hostel must have exactly one warden, and every warden must manage exactly one hostel.
9. Fee amounts, fine amounts, and mess costs cannot be negative.
10. Each student has at most one attendance record per date.
11. A student–visitor pair has at most one recorded visit per day.
12. Room-specific maintenance must reference a room in the same hostel.
13. Hostel-wide maintenance must reference a valid hostel.
14. Required student relationships must not contain invalid or orphaned foreign keys.
15. Status columns must accept only the domains in Section 5.14.

Some rules require more than ordinary CHECK or foreign-key constraints. Room capacity (rule 7) and mandatory warden existence (rule 8) cannot be expressed as a simple key or CHECK constraint, because they depend on other rows. Identify the appropriate enforcement mechanism when implementation is requested.

## 8. Normalization

The schema must be reviewed for First, Second, and Third Normal Forms (1NF, 2NF, and 3NF).

The explanation should address:

- Repeating groups and atomic attributes. (Storing Fee_ID or Complaint_ID inside STUDENT would break this, since a student has many of each. This is why those keys sit on the N side.)
- Partial dependencies involving composite keys. (ROOM, ATTENDANCE, and VISIT use composite keys; every non-key attribute must depend on the whole key. VISIT has no non-key attributes, since Visit_Date is part of the key.)
- Transitive dependencies. (Room details live only in ROOM, so STUDENT holds only the allotment fields that depend on the student.)
- Why the composite keys of ROOM, ATTENDANCE, and VISIT are appropriate.
- Why the chosen foreign-key placements reduce duplication.
- VISITOR.Relation: it is treated as a descriptive attribute of the visitor, as in the ER diagram. Strictly, a person's relation can differ per student; see Open Item C.

Do not decompose tables unnecessarily. Any proposed schema change must be justified by functional dependencies, integrity rules, or a specific requirement.

## 9. Corrections to the Earlier Hand-Drawn Relational Schema

The earlier hand-drawn schema contains the following errors. Do not carry them into the implementation.

1. **HOSTEL had Warden_ID and Staff_ID.** Remove both. Staff is 1:N, so a single Staff_ID in HOSTEL cannot represent many staff, and Warden_ID duplicates WARDEN.Hostel_ID and creates a circular reference.
2. **STUDENT had Fee_ID and Complaint_ID.** Remove both. Fee and complaint are 1:N from student; the key already sits in FEE and COMPLAINT.
3. **MESS had Student_ID.** Remove it. The relationship is N:1 from STUDENT to MESS and Mess_ID already sits in STUDENT. Keeping both directions is redundant.
4. **VISITOR had Student_ID.** Remove it. The relationship is M:N and is held by VISIT.
5. **STUDENT lacked Hostel_ID.** Add it. The room reference is the composite `(Hostel_ID, Room_No)` and cannot work with Room_No alone.
6. **FINE was missing.** Add the FINE table with a Student_ID foreign key.
7. **Key markings were incomplete.** ROOM's key is `(Hostel_ID, Room_No)`, ATTENDANCE's is `(Student_ID, Date)`, and VISIT's is `(Student_ID, Visitor_ID, Visit_Date)`; all columns in each must be marked as part of the key.
8. **Naming inconsistencies.** Use the full attribute names from this document (Address, Amount, FName), not the abbreviations (Addr, Amt, Fname), and use one name for the visit table.

Correct in the hand-drawn schema and retained: WARDEN.Hostel_ID, STAFF.Hostel_ID, ROOM.Hostel_ID, the nullable Room_No with Hostel_ID in MAINTENANCE, Student_ID in ATTENDANCE, FEE, and COMPLAINT, and the three-column VISITED_BY table.

## 10. Open Items for Team Decision

These are not part of the agreed baseline. Do not implement any of them without approval.

- **A. ALLOTTED participation.** The ER diagram appears to draw a double (total) line on the Student side of ALLOTTED, but this document allows a student to be registered without a room. Either change the diagram's line to single, or require every student to have a room. This document currently assumes the former.
- **B. Staff has no Name.** A staff record with only Role and Phone is thin. Adding Name would be a small, sensible change but alters the ER diagram.
- **C. Visitor details.** VISITOR.Relation may differ per student, and a returning visitor could be recorded twice unless VISITOR.Phone is UNIQUE with a lookup before insert. Decide whether to keep the current simple model or add this.
- **D. Mess–Fee link.** Judges asked why mess is not connected to FEE. This can be answered without a schema change: MESS.Cost is the charge, and billing a student's mess creates a FEE row for that student. A Fee_Type attribute is possible but not currently in the design.
- **E. Features dropped from earlier revisions.** The Outpass entity, the Complaint–Maintenance relationship, Complaint.Category, Fee_Type, and Room.Status are not in the current ER diagram and must not be reintroduced unless approved.

## 11. Scope Boundaries

The project is limited to the hostel-management entities and relationships described above.

Do not independently introduce unrelated modules such as payroll, transport, library management, inventory, payment gateways, biometric attendance, or visitor QR verification.

Do not change the agreed cardinalities, key choices, or business rules without explaining the reason and obtaining approval.
