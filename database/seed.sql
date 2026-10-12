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
-- 6. student (12-14 allotted students per hostel, respecting room capacity)
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
-- 2. WARDEN (1:1 with HOSTEL - Kerala Style)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.warden (warden_id, name, phone, hostel_id) VALUES
(1, 'Dr. K. Radhakrishnan', '+919876543210', 1),
(2, 'Prof. Mary Varghese', '+919876543211', 2),
(3, 'Dr. K. P. Sasidharan', '+919876543212', 3);

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
-- Hostel 1 (Ganga Boys) - Total Capacity: 12
(1, 101, 'Double Sharing AC', 2),
(1, 102, 'Double Sharing Non-AC', 2),
(1, 103, 'Single Deluxe', 1),
(1, 104, 'Triple Sharing Non-AC', 3),
(1, 105, 'Double Sharing AC', 2),
(1, 106, 'Double Sharing Non-AC', 2),
-- Hostel 2 (Yamuna Girls) - Total Capacity: 12
(2, 201, 'Double Sharing AC', 2),
(2, 202, 'Single Deluxe', 1),
(2, 203, 'Double Sharing Non-AC', 2),
(2, 204, 'Double Sharing AC', 2),
(2, 205, 'Triple Sharing Non-AC', 3),
(2, 206, 'Double Sharing Non-AC', 2),
-- Hostel 3 (Kaveri Boys) - Total Capacity: 12
(3, 301, 'Double Sharing Non-AC', 2),
(3, 302, 'Single Non-AC', 1),
(3, 303, 'Double Sharing AC', 2),
(3, 304, 'Double Sharing Non-AC', 2),
(3, 305, 'Triple Sharing Non-AC', 3),
(3, 306, 'Double Sharing AC', 2);

-- ----------------------------------------------------------------------------
-- 5. MESS
-- ----------------------------------------------------------------------------
INSERT INTO hostel.mess (mess_id, type, cost) VALUES
(1, 'Kerala Non-Veg & Veg Meals', 4500.00),
(2, 'Traditional Kerala Pure Veg', 4000.00),
(3, 'Special Dietary & Coastal Menu', 5200.00);

-- ----------------------------------------------------------------------------
-- 6. STUDENT (6 allotted students per hostel + 2 un-allotted; Kerala Style)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.student (student_id, fname, lname, reg_no, phone, hostel_id, room_no, allot_date, mess_id) VALUES
-- Hostel 1: Ganga Boys Hostel (6 Boys)
(1001, 'Ashwin', 'K.', 'REG2024001', '+919811122201', 1, 101, '2026-08-01', 1),
(1002, 'Rahul', 'Nair', 'REG2024002', '+919811122202', 1, 101, '2026-08-01', 1),
(1003, 'Vishnu', 'Prasad', 'REG2024003', '+919811122203', 1, 102, '2026-08-01', 1),
(1004, 'Gokul', 'Das', 'REG2024004', '+919811122204', 1, 102, '2026-08-01', 2),
(1005, 'Amal', 'Joseph', 'REG2024005', '+919811122205', 1, 103, '2026-08-02', 3),
(1006, 'Nithin', 'Kurup', 'REG2024006', '+919811122206', 1, 104, '2026-08-02', 1),

-- Hostel 2: Yamuna Girls Hostel (6 Girls)
(1007, 'Ananya', 'M.', 'REG2024007', '+919811122207', 2, 201, '2026-08-01', 2),
(1008, 'Kavya', 'Madhavan', 'REG2024008', '+919811122208', 2, 201, '2026-08-01', 2),
(1009, 'Malavika', 'Menon', 'REG2024009', '+919811122209', 2, 202, '2026-08-02', 2),
(1010, 'Gopika', 'V.', 'REG2024010', '+919811122210', 2, 203, '2026-08-02', 1),
(1011, 'Sneha', 'Varghese', 'REG2024011', '+919811122211', 2, 203, '2026-08-02', 3),
(1012, 'Devika', 'Pillai', 'REG2024012', '+919811122212', 2, 204, '2026-08-03', 2),

-- Hostel 3: Kaveri Boys Hostel (6 Boys)
(1013, 'Pranav', 'R.', 'REG2024013', '+919811122213', 3, 301, '2026-08-01', 3),
(1014, 'Akhil', 'Chandran', 'REG2024014', '+919811122214', 3, 301, '2026-08-01', 1),
(1015, 'Midhun', 'S.', 'REG2024015', '+919811122215', 3, 302, '2026-08-01', 3),
(1016, 'Kiran', 'Babu', 'REG2024016', '+919811122216', 3, 303, '2026-08-02', 2),
(1017, 'Bibin', 'Thomas', 'REG2024017', '+919811122217', 3, 303, '2026-08-02', 1),
(1018, 'Jishnu', 'Mohan', 'REG2024018', '+919811122218', 3, 304, '2026-08-02', 1),

-- Un-allotted Students (2 Students)
(1019, 'Sarath', 'P.', 'REG2024019', '+919811122219', NULL, NULL, NULL, 1),
(1020, 'Parvathy', 'Nair', 'REG2024020', '+919811122220', NULL, NULL, NULL, NULL);

-- ----------------------------------------------------------------------------
-- 7. FEE (1:N from STUDENT)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.fee (fee_id, due_date, amount, status, student_id) VALUES
-- Hostel 1: Ganga Boys
(501, '2026-10-31', 45000.00, 'Paid', 1001),
(502, '2026-10-31', 45000.00, 'Pending', 1002),
(503, '2026-10-31', 42000.00, 'Paid', 1003),
(504, '2026-10-31', 42000.00, 'Pending', 1004),
(505, '2026-10-31', 55000.00, 'Paid', 1005),
(506, '2026-10-31', 38000.00, 'Pending', 1006),
-- Hostel 2: Yamuna Girls
(507, '2026-10-31', 50000.00, 'Paid', 1007),
(508, '2026-10-31', 50000.00, 'Pending', 1008),
(509, '2026-10-31', 55000.00, 'Pending', 1009),
(510, '2026-10-31', 44000.00, 'Paid', 1010),
(511, '2026-10-31', 44000.00, 'Pending', 1011),
(512, '2026-10-31', 50000.00, 'Paid', 1012),
-- Hostel 3: Kaveri Boys
(513, '2026-10-31', 45000.00, 'Pending', 1013),
(514, '2026-10-31', 45000.00, 'Paid', 1014),
(515, '2026-10-31', 48000.00, 'Pending', 1015),
(516, '2026-10-31', 52000.00, 'Paid', 1016),
(517, '2026-10-31', 52000.00, 'Paid', 1017),
(518, '2026-10-31', 45000.00, 'Pending', 1018);

-- ----------------------------------------------------------------------------
-- 8. FINE (1:N from STUDENT)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.fine (fid, reason, amount, status, student_id) VALUES
(701, 'Late entry past 10:30 PM curfew', 500.00, 'Paid', 1001),
(702, 'Unauthorized electric kettle in room', 1000.00, 'Pending', 1002),
(703, 'Noise violation during quiet hours', 300.00, 'Pending', 1007),
(704, 'Damaged window mesh screen', 450.00, 'Paid', 1003),
(705, 'Missed mandatory hostel assembly', 250.00, 'Pending', 1011),
(706, 'Unapproved room guest overnight', 1200.00, 'Pending', 1014);

-- ----------------------------------------------------------------------------
-- 9. ATTENDANCE (Composite key student_id + date)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.attendance (student_id, date, status) VALUES
-- 2026-10-11 (Today)
-- Hostel 1
(1001, '2026-10-11', 'Present'),
(1002, '2026-10-11', 'Present'),
(1003, '2026-10-11', 'Present'),
(1004, '2026-10-11', 'Present'),
(1005, '2026-10-11', 'Present'),
(1006, '2026-10-11', 'Absent'),
-- Hostel 2
(1007, '2026-10-11', 'Present'),
(1008, '2026-10-11', 'Present'),
(1009, '2026-10-11', 'Present'),
(1010, '2026-10-11', 'Present'),
(1011, '2026-10-11', 'Absent'),
(1012, '2026-10-11', 'Present'),
-- Hostel 3
(1013, '2026-10-11', 'Present'),
(1014, '2026-10-11', 'Present'),
(1015, '2026-10-11', 'Present'),
(1016, '2026-10-11', 'Present'),
(1017, '2026-10-11', 'Absent'),
(1018, '2026-10-11', 'Present'),
-- 2026-10-10 (Yesterday)
(1001, '2026-10-10', 'Present'),
(1002, '2026-10-10', 'Present'),
(1007, '2026-10-10', 'Present'),
(1008, '2026-10-10', 'Absent'),
(1013, '2026-10-10', 'Present'),
(1014, '2026-10-10', 'Present');

-- ----------------------------------------------------------------------------
-- 10. VISITOR (Kerala Style Parents & Guardians)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.visitor (visitor_id, name, relation, phone) VALUES
(201, 'K. Radhakrishnan', 'Father', '+919845011111'),
(202, 'Sujatha Radhakrishnan', 'Mother', '+919845011112'),
(203, 'Madhavan Nair', 'Father', '+919845011113'),
(204, 'Gireesh Nair', 'Brother', '+919845011114'),
(205, 'Kurian Varghese', 'Guardian', '+919845011115'),
(206, 'Latha Pillai', 'Mother', '+919845011116');

-- ----------------------------------------------------------------------------
-- 11. VISIT (Composite key student_id + visitor_id + visit_date)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.visit (student_id, visitor_id, visit_date) VALUES
(1001, 201, '2026-10-05'),
(1001, 202, '2026-10-05'),
(1008, 203, '2026-10-08'),
(1002, 204, '2026-10-10'),
(1011, 205, '2026-10-09'),
(1012, 206, '2026-10-10');

-- ----------------------------------------------------------------------------
-- 12. MAINTENANCE
-- ----------------------------------------------------------------------------
INSERT INTO hostel.maintenance (request_id, hostel_id, room_no, description, date, status) VALUES
(301, 1, 101, 'Ceiling fan speed regulator not functioning', '2026-10-08', 'Resolved'),
(302, 1, NULL, 'Main corridor water cooler filter replacement required', '2026-10-09', 'In Progress'),
(303, 2, 201, 'Bathroom door latch loose', '2026-10-09', 'Open'),
(304, 3, NULL, 'Solar water heater pressure valve inspection', '2026-10-10', 'Open'),
(305, 1, 104, 'Study table light fixture connection loose', '2026-10-11', 'Open'),
(306, 2, 204, 'Air conditioner remote control battery dead', '2026-10-10', 'Resolved'),
(307, 3, 303, 'Washbasin tap aerator leaking water', '2026-10-11', 'Open');

-- ----------------------------------------------------------------------------
-- 13. COMPLAINT (1:N from STUDENT)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.complaint (complaint_id, date, description, status, student_id) VALUES
(401, '2026-10-07', 'Wi-Fi access point in 1st floor wing keeps dropping connection', 'Resolved', 1001),
(402, '2026-10-09', 'Hot water supply delayed in morning hours', 'In Progress', 1007),
(403, '2026-10-10', 'Mess breakfast timing does not align with morning lab schedule', 'Open', 1013),
(404, '2026-10-11', 'Need extra study chair in Room 104', 'Open', 1006),
(405, '2026-10-10', 'Water dispenser empty on second floor wing', 'Resolved', 1008),
(406, '2026-10-11', 'Gym equipment dumbbell rack unstable', 'Open', 1016);

