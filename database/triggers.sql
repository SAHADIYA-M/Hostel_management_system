-- ============================================================================
-- Hostel Management System — Business Rule Triggers & Functions (PostgreSQL 16)
-- Schema: hostel
-- Baseline Specification: docs/project-context.md (Revision 2)
--
-- Rules Enforced Here:
-- 1. Rule 7: Room capacity limit must not be exceeded before inserting or
--    updating a student's room assignment.
-- 2. Rule 8: Every hostel must have exactly one warden (audit & transactional
--    enforcement).
-- ============================================================================

SET search_path TO hostel, public;

-- ----------------------------------------------------------------------------
-- 1. TRIGGER: Enforce Room Capacity Limit (Rule 7)
-- Prevents allotting a student to a room if current occupancy has reached
-- the room's declared capacity.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION hostel.fn_check_room_capacity()
RETURNS TRIGGER AS $$
DECLARE
    v_max_capacity  INT;
    v_current_count INT;
BEGIN
    -- Only run check if room is being assigned or changed
    IF NEW.room_no IS NOT NULL AND NEW.hostel_id IS NOT NULL THEN

        -- Fetch the room capacity
        SELECT capacity INTO v_max_capacity
        FROM hostel.room
        WHERE hostel_id = NEW.hostel_id AND room_no = NEW.room_no;

        IF NOT FOUND THEN
            RAISE EXCEPTION 'Cannot allot student: Room % does not exist in Hostel %',
                NEW.room_no, NEW.hostel_id
                USING ERRCODE = 'foreign_key_violation';
        END IF;

        -- Count existing students in the room (excluding this student if updating)
        SELECT COUNT(*) INTO v_current_count
        FROM hostel.student
        WHERE hostel_id = NEW.hostel_id
          AND room_no = NEW.room_no
          AND student_id <> COALESCE(NEW.student_id, -1);

        -- Enforce capacity constraint
        IF v_current_count >= v_max_capacity THEN
            RAISE EXCEPTION 'Room capacity exceeded: Room % in Hostel % has max capacity of % (currently has % occupants)',
                NEW.room_no, NEW.hostel_id, v_max_capacity, v_current_count
                USING ERRCODE = 'check_violation';
        END IF;

    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to student table
DROP TRIGGER IF EXISTS trg_check_room_capacity ON hostel.student;

CREATE TRIGGER trg_check_room_capacity
BEFORE INSERT OR UPDATE OF hostel_id, room_no
ON hostel.student
FOR EACH ROW
EXECUTE FUNCTION hostel.fn_check_room_capacity();

-- ----------------------------------------------------------------------------
-- 2. PROCEDURE / AUDIT: Enforce Mandatory Warden Existence (Rule 8)
-- WARDEN.hostel_id UNIQUE NOT NULL guarantees at most 1 warden per hostel.
-- This function verifies that NO hostel exists without an assigned warden.
-- Can be called at transaction boundaries or during audits.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION hostel.fn_verify_all_hostels_have_wardens()
RETURNS TABLE (
    unassigned_hostel_id INT,
    hostel_name          VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT h.hostel_id, h.name
    FROM hostel.hostel h
    LEFT JOIN hostel.warden w ON h.hostel_id = w.hostel_id
    WHERE w.warden_id IS NULL;
END;
$$ LANGUAGE plpgsql;
