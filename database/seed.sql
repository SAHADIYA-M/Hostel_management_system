-- ============================================================================
-- Hostel Management System — Realistic Seed Dataset (PostgreSQL 16)
-- Schema: hostel
-- Baseline Specification: docs/project-context.md (Revision 2)
--
-- Insertion Order:
-- 1. hostel
-- 2. warden (1:1 with hostel)
-- 3. staff (1:N with hostel, no Name)
-- 4. room (weak entity, hostel_id + room_no)
-- 5. mess (mess plans)
-- 6. student (allotted & un-allotted students, respecting room capacity)
-- 7. fee (Pending & Paid)
-- 8. fine (Pending & Paid)
-- 9. attendance (Present & Absent)
-- 10. visitor (registered visitors)
-- 11. visit (visits log)
-- 12. maintenance (hostel-wide & room-specific)
-- 13. complaint (student complaints)
-- ============================================================================

SET search_path TO hostel, public;

-- Clear all existing data in reverse order
TRUNCATE TABLE hostel.complaint RESTART IDENTITY CASCADE;
TRUNCATE TABLE hostel.maintenance RESTART IDENTITY CASCADE;
TRUNCATE TABLE hostel.visit CASCADE;
TRUNCATE TABLE hostel.visitor RESTART IDENTITY CASCADE;
TRUNCATE TABLE hostel.attendance CASCADE;
TRUNCATE TABLE hostel.fine RESTART IDENTITY CASCADE;
TRUNCATE TABLE hostel.fee RESTART IDENTITY CASCADE;
TRUNCATE TABLE hostel.student RESTART IDENTITY CASCADE;
TRUNCATE TABLE hostel.mess RESTART IDENTITY CASCADE;
TRUNCATE TABLE hostel.room CASCADE;
TRUNCATE TABLE hostel.staff RESTART IDENTITY CASCADE;
TRUNCATE TABLE hostel.warden RESTART IDENTITY CASCADE;
TRUNCATE TABLE hostel.hostel RESTART IDENTITY CASCADE;

-- ----------------------------------------------------------------------------
-- 1. HOSTEL
-- ----------------------------------------------------------------------------
INSERT INTO hostel.hostel (hostel_id, name, address, type) VALUES
(1, 'Ganga Boys Hostel', 'North Campus, Sector 12, Academic City', 'Boys'),
(2, 'Yamuna Girls Hostel', 'South Campus, Sector 14, Academic City', 'Girls'),
(3, 'Kaveri Boys Hostel', 'East Campus, Sector 9, Academic City', 'Boys');

-- ----------------------------------------------------------------------------
-- 2. WARDEN (1:1 with HOSTEL)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.warden (warden_id, name, phone, hostel_id) VALUES
(1, 'Dr. Suresh Kumar', '+919876543210', 1),
(2, 'Prof. Meenakshi Sundaram', '+919876543211', 2),
(3, 'Dr. Rajesh Pillai', '+919876543212', 3);

-- ----------------------------------------------------------------------------
-- 3. STAFF (1:N from HOSTEL; role & phone only)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.staff (staff_id, role, phone, hostel_id) VALUES
(1, 'Head Caretaker', '+919123456780', 1),
(2, 'Senior Electrician', '+919123456781', 1),
(3, 'Night Security Guard', '+919123456782', 1),
(4, 'Hostel Matron', '+919123456783', 2),
(5, 'Housekeeping Supervisor', '+919123456784', 2),
(6, 'Day Security Guard', '+919123456785', 2),
(7, 'General Caretaker', '+919123456786', 3),
(8, 'Maintenance Plumber', '+919123456787', 3);

-- ----------------------------------------------------------------------------
-- 4. ROOM (Weak entity; identified by hostel_id + room_no)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.room (hostel_id, room_no, type, capacity) VALUES
-- Hostel 1 (Ganga Boys)
(1, 101, 'Double Sharing AC', 2),
(1, 102, 'Double Sharing Non-AC', 2),
(1, 103, 'Single Deluxe', 1),
(1, 104, 'Triple Sharing Non-AC', 3),
-- Hostel 2 (Yamuna Girls)
(2, 201, 'Double Sharing AC', 2),
(2, 202, 'Single Deluxe', 1),
(2, 203, 'Double Sharing Non-AC', 2),
-- Hostel 3 (Kaveri Boys)
(3, 301, 'Double Sharing Non-AC', 2),
(3, 302, 'Single Non-AC', 1);

-- ----------------------------------------------------------------------------
-- 5. MESS
-- ----------------------------------------------------------------------------
INSERT INTO hostel.mess (mess_id, type, cost) VALUES
(1, 'North Indian Veg & Non-Veg', 4500.00),
(2, 'South Indian Pure Veg', 4000.00),
(3, 'Special Dietary & Continental', 5200.00);

-- ----------------------------------------------------------------------------
-- 6. STUDENT
-- Note: Room 101 in Hostel 1 has capacity 2; students 1001 and 1002 fill it.
-- Students 1005 and 1006 are un-allotted (allotment fields NULL).
-- ----------------------------------------------------------------------------
INSERT INTO hostel.student (student_id, fname, lname, reg_no, phone, hostel_id, room_no, allot_date, mess_id) VALUES
(1001, 'Rahul', 'Sharma', 'REG2024001', '+919811122201', 1, 101, '2026-08-01', 1),
(1002, 'Aditya', 'Verma', 'REG2024002', '+919811122202', 1, 101, '2026-08-01', 1),
(1003, 'Kavya', 'Nair', 'REG2024003', '+919811122203', 2, 201, '2026-08-01', 2),
(1004, 'Ananya', 'Iyer', 'REG2024004', '+919811122204', 2, 202, '2026-08-02', 2),
(1005, 'Vikram', 'Rathore', 'REG2024005', '+919811122205', NULL, NULL, NULL, 1),
(1006, 'Pooja', 'Menon', 'REG2024006', '+919811122206', NULL, NULL, NULL, NULL),
(1007, 'Siddharth', 'Joshi', 'REG2024007', '+919811122207', 3, 301, '2026-08-05', 3);

-- ----------------------------------------------------------------------------
-- 7. FEE (1:N from STUDENT)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.fee (fee_id, due_date, amount, status, student_id) VALUES
(501, '2026-10-31', 45000.00, 'Paid', 1001),
(502, '2026-10-31', 45000.00, 'Pending', 1002),
(503, '2026-10-31', 50000.00, 'Paid', 1003),
(504, '2026-10-31', 55000.00, 'Pending', 1004),
(505, '2026-10-31', 45000.00, 'Pending', 1007);

-- ----------------------------------------------------------------------------
-- 8. FINE (1:N from STUDENT)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.fine (fid, reason, amount, status, student_id) VALUES
(701, 'Late entry past 10:30 PM curfew', 500.00, 'Paid', 1001),
(702, 'Unauthorized electric kettle in room', 1000.00, 'Pending', 1002),
(703, 'Noise violation during quiet hours', 300.00, 'Pending', 1007);

-- ----------------------------------------------------------------------------
-- 9. ATTENDANCE (Composite key student_id + date)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.attendance (student_id, date, status) VALUES
(1001, '2026-10-10', 'Present'),
(1002, '2026-10-10', 'Present'),
(1003, '2026-10-10', 'Present'),
(1004, '2026-10-10', 'Absent'),
(1007, '2026-10-10', 'Present'),
(1001, '2026-10-09', 'Present'),
(1002, '2026-10-09', 'Absent'),
(1003, '2026-10-09', 'Present'),
(1004, '2026-10-09', 'Present'),
(1007, '2026-10-09', 'Present');

-- ----------------------------------------------------------------------------
-- 10. VISITOR
-- ----------------------------------------------------------------------------
INSERT INTO hostel.visitor (visitor_id, name, relation, phone) VALUES
(201, 'Ramesh Sharma', 'Father', '+919845011111'),
(202, 'Sunita Sharma', 'Mother', '+919845011112'),
(203, 'Gopinath Nair', 'Father', '+919845011113'),
(204, 'Arun Verma', 'Brother', '+919845011114');

-- ----------------------------------------------------------------------------
-- 11. VISIT (Composite key student_id + visitor_id + visit_date)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.visit (student_id, visitor_id, visit_date) VALUES
(1001, 201, '2026-10-05'),
(1001, 202, '2026-10-05'),
(1003, 203, '2026-10-08'),
(1002, 204, '2026-10-10');

-- ----------------------------------------------------------------------------
-- 12. MAINTENANCE
-- Demonstrates both hostel-wide (room_no IS NULL) and room-specific requests.
-- ----------------------------------------------------------------------------
INSERT INTO hostel.maintenance (request_id, hostel_id, room_no, description, date, status) VALUES
(301, 1, 101, 'Ceiling fan speed regulator not functioning', '2026-10-08', 'Resolved'),
(302, 1, NULL, 'Main corridor water cooler filter replacement required', '2026-10-09', 'In Progress'),
(303, 2, 201, 'Bathroom door latch loose', '2026-10-09', 'Open'),
(304, 3, NULL, 'Solar water heater pressure valve inspection', '2026-10-10', 'Open');

-- ----------------------------------------------------------------------------
-- 13. COMPLAINT (1:N from STUDENT)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.complaint (complaint_id, date, description, status, student_id) VALUES
(401, '2026-10-07', 'Wi-Fi access point in 1st floor wing keeps dropping connection', 'Resolved', 1001),
(402, '2026-10-09', 'Hot water supply delayed in morning hours', 'In Progress', 1003),
(403, '2026-10-10', 'Mess breakfast timing does not align with morning lab schedule', 'Open', 1007);
