-- ============================================================================
-- Migration: Add Strict Mobile Number & Pattern Validation Constraints
-- Schema: hostel
-- ============================================================================

SET search_path TO hostel, public;

-- 1. Warden Constraints
ALTER TABLE hostel.warden DROP CONSTRAINT IF EXISTS chk_warden_phone_format;
ALTER TABLE hostel.warden ADD CONSTRAINT chk_warden_phone_format
    CHECK (phone ~ '^(\+91)?[6-9][0-9]{9}$');

ALTER TABLE hostel.warden DROP CONSTRAINT IF EXISTS chk_warden_name_format;
ALTER TABLE hostel.warden ADD CONSTRAINT chk_warden_name_format
    CHECK (name ~ '^[A-Za-z][A-Za-z\s\.]*$');

-- 2. Staff Constraints
ALTER TABLE hostel.staff DROP CONSTRAINT IF EXISTS chk_staff_phone_format;
ALTER TABLE hostel.staff ADD CONSTRAINT chk_staff_phone_format
    CHECK (phone ~ '^(\+91)?[6-9][0-9]{9}$');

-- 3. Room Constraints
ALTER TABLE hostel.room DROP CONSTRAINT IF EXISTS chk_room_no_range;
ALTER TABLE hostel.room ADD CONSTRAINT chk_room_no_range
    CHECK (room_no BETWEEN 100 AND 999);

ALTER TABLE hostel.room DROP CONSTRAINT IF EXISTS chk_room_capacity_range;
ALTER TABLE hostel.room ADD CONSTRAINT chk_room_capacity_range
    CHECK (capacity BETWEEN 1 AND 10);

-- 4. Mess Cost Constraint
ALTER TABLE hostel.mess DROP CONSTRAINT IF EXISTS chk_mess_cost_positive;
ALTER TABLE hostel.mess DROP CONSTRAINT IF EXISTS chk_mess_cost_non_negative;
ALTER TABLE hostel.mess ADD CONSTRAINT chk_mess_cost_positive
    CHECK (cost > 0);

-- 5. Student Constraints
ALTER TABLE hostel.student DROP CONSTRAINT IF EXISTS chk_student_phone_format;
ALTER TABLE hostel.student ADD CONSTRAINT chk_student_phone_format
    CHECK (phone ~ '^(\+91)?[6-9][0-9]{9}$');

ALTER TABLE hostel.student DROP CONSTRAINT IF EXISTS chk_student_reg_no_format;
ALTER TABLE hostel.student ADD CONSTRAINT chk_student_reg_no_format
    CHECK (reg_no ~ '^REG[0-9]{7}$');

ALTER TABLE hostel.student DROP CONSTRAINT IF EXISTS chk_student_fname_format;
ALTER TABLE hostel.student ADD CONSTRAINT chk_student_fname_format
    CHECK (fname ~ '^[A-Za-z][A-Za-z\s\.]*$');

ALTER TABLE hostel.student DROP CONSTRAINT IF EXISTS chk_student_lname_format;
ALTER TABLE hostel.student ADD CONSTRAINT chk_student_lname_format
    CHECK (lname ~ '^[A-Za-z][A-Za-z\s\.]*$');

-- 6. Fee Amount Constraint
ALTER TABLE hostel.fee DROP CONSTRAINT IF EXISTS chk_fee_amount_positive;
ALTER TABLE hostel.fee DROP CONSTRAINT IF EXISTS chk_fee_amount_non_negative;
ALTER TABLE hostel.fee ADD CONSTRAINT chk_fee_amount_positive
    CHECK (amount > 0);

-- 7. Fine Amount Constraint
ALTER TABLE hostel.fine DROP CONSTRAINT IF EXISTS chk_fine_amount_positive;
ALTER TABLE hostel.fine DROP CONSTRAINT IF EXISTS chk_fine_amount_non_negative;
ALTER TABLE hostel.fine ADD CONSTRAINT chk_fine_amount_positive
    CHECK (amount > 0);

-- 8. Visitor Constraints
ALTER TABLE hostel.visitor DROP CONSTRAINT IF EXISTS chk_visitor_phone_format;
ALTER TABLE hostel.visitor ADD CONSTRAINT chk_visitor_phone_format
    CHECK (phone ~ '^(\+91)?[6-9][0-9]{9}$');

ALTER TABLE hostel.visitor DROP CONSTRAINT IF EXISTS chk_visitor_name_format;
ALTER TABLE hostel.visitor ADD CONSTRAINT chk_visitor_name_format
    CHECK (name ~ '^[A-Za-z][A-Za-z\s\.]*$');
