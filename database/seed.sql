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
(1, 'North Indian Veg & Non-Veg', 4500.00),
(2, 'South Indian Pure Veg', 4000.00),
(3, 'Special Dietary & Continental', 5200.00);

-- ----------------------------------------------------------------------------
-- 6. STUDENT (12 allotted per hostel + 2 un-allotted)
-- Respects exact room capacities and gender segregation
-- ----------------------------------------------------------------------------
INSERT INTO hostel.student (student_id, fname, lname, reg_no, phone, hostel_id, room_no, allot_date, mess_id) VALUES
-- Hostel 1: Ganga Boys Hostel (12 Students)
(1001, 'Rahul', 'Sharma', 'REG2024001', '+919811122201', 1, 101, '2026-08-01', 1),
(1002, 'Aditya', 'Verma', 'REG2024002', '+919811122202', 1, 101, '2026-08-01', 1),
(1011, 'Rohan', 'Mehta', 'REG2024011', '+919811122211', 1, 102, '2026-08-01', 1),
(1012, 'Aman', 'Gupta', 'REG2024012', '+919811122212', 1, 102, '2026-08-01', 2),
(1013, 'Karthik', 'Rao', 'REG2024013', '+919811122213', 1, 103, '2026-08-02', 3),
(1014, 'Nikhil', 'Singh', 'REG2024014', '+919811122214', 1, 104, '2026-08-02', 1),
(1015, 'Vivek', 'Pandey', 'REG2024015', '+919811122215', 1, 104, '2026-08-02', 1),
(1016, 'Sanjay', 'Kumar', 'REG2024016', '+919811122216', 1, 104, '2026-08-03', 2),
(1017, 'Deepak', 'Mishra', 'REG2024017', '+919811122217', 1, 105, '2026-08-03', 1),
(1018, 'Gaurav', 'Patel', 'REG2024018', '+919811122218', 1, 105, '2026-08-03', 3),
(1019, 'Abhishek', 'Yadav', 'REG2024019', '+919811122219', 1, 106, '2026-08-04', 1),
(1020, 'Harish', 'Reddy', 'REG2024020', '+919811122220', 1, 106, '2026-08-04', 2),

-- Hostel 2: Yamuna Girls Hostel (12 Students)
(1003, 'Kavya', 'Nair', 'REG2024003', '+919811122203', 2, 201, '2026-08-01', 2),
(1021, 'Sneha', 'Roy', 'REG2024021', '+919811122221', 2, 201, '2026-08-01', 2),
(1004, 'Ananya', 'Iyer', 'REG2024004', '+919811122204', 2, 202, '2026-08-02', 2),
(1022, 'Divya', 'Pillai', 'REG2024022', '+919811122222', 2, 203, '2026-08-02', 1),
(1023, 'Megha', 'Deshmukh', 'REG2024023', '+919811122223', 2, 203, '2026-08-02', 3),
(1024, 'Ritu', 'Agarwal', 'REG2024024', '+919811122224', 2, 204, '2026-08-03', 2),
(1025, 'Swati', 'Chauhan', 'REG2024025', '+919811122225', 2, 204, '2026-08-03', 1),
(1026, 'Priyanka', 'Das', 'REG2024026', '+919811122226', 2, 205, '2026-08-03', 2),
(1027, 'Tanvi', 'Kulkarni', 'REG2024027', '+919811122227', 2, 205, '2026-08-04', 3),
(1028, 'Aishwarya', 'Bhat', 'REG2024028', '+919811122228', 2, 205, '2026-08-04', 2),
(1029, 'Neha', 'Saxena', 'REG2024029', '+919811122229', 2, 206, '2026-08-05', 1),
(1030, 'Bhavna', 'Jain', 'REG2024030', '+919811122230', 2, 206, '2026-08-05', 2),

-- Hostel 3: Kaveri Boys Hostel (12 Students)
(1007, 'Siddharth', 'Joshi', 'REG2024007', '+919811122207', 3, 301, '2026-08-05', 3),
(1031, 'Arjun', 'Kapoor', 'REG2024031', '+919811122231', 3, 301, '2026-08-01', 1),
(1032, 'Tarun', 'Khanna', 'REG2024032', '+919811122232', 3, 302, '2026-08-01', 3),
(1033, 'Pranav', 'Nambiar', 'REG2024033', '+919811122233', 3, 303, '2026-08-02', 2),
(1034, 'Varun', 'Bose', 'REG2024034', '+919811122234', 3, 303, '2026-08-02', 1),
(1035, 'Manish', 'Tiwari', 'REG2024035', '+919811122235', 3, 304, '2026-08-02', 1),
(1036, 'Mohit', 'Chopra', 'REG2024036', '+919811122236', 3, 304, '2026-08-03', 2),
(1037, 'Rajeev', 'Nath', 'REG2024037', '+919811122237', 3, 305, '2026-08-03', 1),
(1038, 'Chirag', 'Shah', 'REG2024038', '+919811122238', 3, 305, '2026-08-03', 3),
(1039, 'Devendra', 'Rawat', 'REG2024039', '+919811122239', 3, 305, '2026-08-04', 2),
(1040, 'Naveen', 'Soni', 'REG2024040', '+919811122240', 3, 306, '2026-08-04', 1),
(1041, 'Prakash', 'Hegde', 'REG2024041', '+919811122241', 3, 306, '2026-08-05', 2),

-- Un-allotted Students (2 Students)
(1005, 'Vikram', 'Rathore', 'REG2024005', '+919811122205', NULL, NULL, NULL, 1),
(1006, 'Pooja', 'Menon', 'REG2024006', '+919811122206', NULL, NULL, NULL, NULL);

-- ----------------------------------------------------------------------------
-- 7. FEE (1:N from STUDENT)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.fee (fee_id, due_date, amount, status, student_id) VALUES
-- Hostel 1
(501, '2026-10-31', 45000.00, 'Paid', 1001),
(502, '2026-10-31', 45000.00, 'Pending', 1002),
(506, '2026-10-31', 42000.00, 'Paid', 1011),
(507, '2026-10-31', 42000.00, 'Pending', 1012),
(508, '2026-10-31', 55000.00, 'Paid', 1013),
(509, '2026-10-31', 38000.00, 'Pending', 1014),
(510, '2026-10-31', 38000.00, 'Paid', 1015),
(511, '2026-10-31', 38000.00, 'Paid', 1016),
(512, '2026-10-31', 45000.00, 'Pending', 1017),
(513, '2026-10-31', 45000.00, 'Paid', 1018),
(514, '2026-10-31', 42000.00, 'Paid', 1019),
(515, '2026-10-31', 42000.00, 'Pending', 1020),
-- Hostel 2
(503, '2026-10-31', 50000.00, 'Paid', 1003),
(516, '2026-10-31', 50000.00, 'Pending', 1021),
(504, '2026-10-31', 55000.00, 'Pending', 1004),
(517, '2026-10-31', 44000.00, 'Paid', 1022),
(518, '2026-10-31', 44000.00, 'Pending', 1023),
(519, '2026-10-31', 50000.00, 'Paid', 1024),
(520, '2026-10-31', 50000.00, 'Paid', 1025),
(521, '2026-10-31', 40000.00, 'Pending', 1026),
(522, '2026-10-31', 40000.00, 'Paid', 1027),
(523, '2026-10-31', 40000.00, 'Paid', 1028),
(524, '2026-10-31', 44000.00, 'Pending', 1029),
(525, '2026-10-31', 44000.00, 'Paid', 1030),
-- Hostel 3
(505, '2026-10-31', 45000.00, 'Pending', 1007),
(526, '2026-10-31', 45000.00, 'Paid', 1031),
(527, '2026-10-31', 48000.00, 'Pending', 1032),
(528, '2026-10-31', 52000.00, 'Paid', 1033),
(529, '2026-10-31', 52000.00, 'Paid', 1034),
(530, '2026-10-31', 45000.00, 'Pending', 1035),
(531, '2026-10-31', 45000.00, 'Paid', 1036),
(532, '2026-10-31', 39000.00, 'Paid', 1037),
(533, '2026-10-31', 39000.00, 'Pending', 1038),
(534, '2026-10-31', 39000.00, 'Paid', 1039),
(535, '2026-10-31', 52000.00, 'Pending', 1040),
(536, '2026-10-31', 52000.00, 'Paid', 1041);

-- ----------------------------------------------------------------------------
-- 8. FINE (1:N from STUDENT)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.fine (fid, reason, amount, status, student_id) VALUES
(701, 'Late entry past 10:30 PM curfew', 500.00, 'Paid', 1001),
(702, 'Unauthorized electric kettle in room', 1000.00, 'Pending', 1002),
(703, 'Noise violation during quiet hours', 300.00, 'Pending', 1007),
(704, 'Damaged window mesh screen', 450.00, 'Paid', 1012),
(705, 'Missed mandatory hostel assembly', 250.00, 'Pending', 1023),
(706, 'Unapproved room guest overnight', 1200.00, 'Pending', 1035);

-- ----------------------------------------------------------------------------
-- 9. ATTENDANCE (Composite key student_id + date)
-- Realistic daily logs across all 3 hostels
-- ----------------------------------------------------------------------------
INSERT INTO hostel.attendance (student_id, date, status) VALUES
-- 2026-10-11 (Today)
-- Hostel 1
(1001, '2026-10-11', 'Present'),
(1002, '2026-10-11', 'Present'),
(1011, '2026-10-11', 'Present'),
(1012, '2026-10-11', 'Present'),
(1013, '2026-10-11', 'Present'),
(1014, '2026-10-11', 'Absent'),
(1015, '2026-10-11', 'Present'),
(1016, '2026-10-11', 'Present'),
(1017, '2026-10-11', 'Present'),
(1018, '2026-10-11', 'Present'),
(1019, '2026-10-11', 'Present'),
(1020, '2026-10-11', 'Present'),
-- Hostel 2
(1003, '2026-10-11', 'Present'),
(1021, '2026-10-11', 'Present'),
(1004, '2026-10-11', 'Present'),
(1022, '2026-10-11', 'Present'),
(1023, '2026-10-11', 'Present'),
(1024, '2026-10-11', 'Present'),
(1025, '2026-10-11', 'Absent'),
(1026, '2026-10-11', 'Present'),
(1027, '2026-10-11', 'Present'),
(1028, '2026-10-11', 'Present'),
(1029, '2026-10-11', 'Present'),
(1030, '2026-10-11', 'Present'),
-- Hostel 3
(1007, '2026-10-11', 'Present'),
(1031, '2026-10-11', 'Present'),
(1032, '2026-10-11', 'Present'),
(1033, '2026-10-11', 'Present'),
(1034, '2026-10-11', 'Absent'),
(1035, '2026-10-11', 'Present'),
(1036, '2026-10-11', 'Present'),
(1037, '2026-10-11', 'Present'),
(1038, '2026-10-11', 'Present'),
(1039, '2026-10-11', 'Present'),
(1040, '2026-10-11', 'Present'),
(1041, '2026-10-11', 'Present'),

-- 2026-10-10 (Yesterday)
(1001, '2026-10-10', 'Present'),
(1002, '2026-10-10', 'Present'),
(1003, '2026-10-10', 'Present'),
(1004, '2026-10-10', 'Absent'),
(1007, '2026-10-10', 'Present'),
(1011, '2026-10-10', 'Present'),
(1012, '2026-10-10', 'Present'),
(1021, '2026-10-10', 'Present'),
(1031, '2026-10-10', 'Present');

-- ----------------------------------------------------------------------------
-- 10. VISITOR
-- ----------------------------------------------------------------------------
INSERT INTO hostel.visitor (visitor_id, name, relation, phone) VALUES
(201, 'Ramesh Sharma', 'Father', '+919845011111'),
(202, 'Sunita Sharma', 'Mother', '+919845011112'),
(203, 'Gopinath Nair', 'Father', '+919845011113'),
(204, 'Arun Verma', 'Brother', '+919845011114'),
(205, 'Bhavin Patel', 'Guardian', '+919845011115'),
(206, 'Kavita Das', 'Mother', '+919845011116');

-- ----------------------------------------------------------------------------
-- 11. VISIT (Composite key student_id + visitor_id + visit_date)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.visit (student_id, visitor_id, visit_date) VALUES
(1001, 201, '2026-10-05'),
(1001, 202, '2026-10-05'),
(1003, 203, '2026-10-08'),
(1002, 204, '2026-10-10'),
(1018, 205, '2026-10-09'),
(1026, 206, '2026-10-10');

-- ----------------------------------------------------------------------------
-- 12. MAINTENANCE
-- Demonstrates both hostel-wide (room_no IS NULL) and room-specific requests.
-- ----------------------------------------------------------------------------
INSERT INTO hostel.maintenance (request_id, hostel_id, room_no, description, date, status) VALUES
(301, 1, 101, 'Ceiling fan speed regulator not functioning', '2026-10-08', 'Resolved'),
(302, 1, NULL, 'Main corridor water cooler filter replacement required', '2026-10-09', 'In Progress'),
(303, 2, 201, 'Bathroom door latch loose', '2026-10-09', 'Open'),
(304, 3, NULL, 'Solar water heater pressure valve inspection', '2026-10-10', 'Open'),
(305, 1, 104, 'Study table light fixture connection loose', '2026-10-11', 'Open'),
(306, 2, 205, 'Air conditioner remote control battery dead', '2026-10-10', 'Resolved'),
(307, 3, 303, 'Washbasin tap aerator leaking water', '2026-10-11', 'Open');

-- ----------------------------------------------------------------------------
-- 13. COMPLAINT (1:N from STUDENT)
-- ----------------------------------------------------------------------------
INSERT INTO hostel.complaint (complaint_id, date, description, status, student_id) VALUES
(401, '2026-10-07', 'Wi-Fi access point in 1st floor wing keeps dropping connection', 'Resolved', 1001),
(402, '2026-10-09', 'Hot water supply delayed in morning hours', 'In Progress', 1003),
(403, '2026-10-10', 'Mess breakfast timing does not align with morning lab schedule', 'Open', 1007),
(404, '2026-10-11', 'Need extra study chair in Room 104', 'Open', 1014),
(405, '2026-10-10', 'Water dispenser empty on second floor wing', 'Resolved', 1024),
(406, '2026-10-11', 'Gym equipment dumbbell rack unstable', 'Open', 1033);
