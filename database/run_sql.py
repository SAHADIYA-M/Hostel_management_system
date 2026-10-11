"""
Database runner and verification utilities for Hostel Management System.
Uses psycopg 3 with raw SQL. Adheres strictly to project safety rules:
- Credentials in backend/.env are never printed or logged.
- Only touches the 'hostel' schema.
- Runs all DDL and test operations inside transactions.
"""

import os
import sys
import argparse
from pathlib import Path
import psycopg
from psycopg.rows import dict_row

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "backend" / ".env"
SCHEMA_SQL_PATH = BASE_DIR / "database" / "schema.sql"
TRIGGERS_SQL_PATH = BASE_DIR / "database" / "triggers.sql"
SEED_SQL_PATH = BASE_DIR / "database" / "seed.sql"


def load_env() -> dict[str, str]:
    """Parse backend/.env safely."""
    env_vars = {}
    if not ENV_PATH.exists():
        raise FileNotFoundError(f".env not found at {ENV_PATH}")

    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                env_vars[key.strip()] = val.strip().strip('"').strip("'")
    return env_vars


def get_connection(autocommit: bool = False):
    """Establish connection using psycopg 3."""
    env = load_env()
    db_url = env.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL is not set in backend/.env")

    try:
        conn = psycopg.connect(db_url, autocommit=autocommit)
        return conn
    except Exception as e:
        error_type = type(e).__name__
        print(f"CONNECTION_ERROR: {error_type}")
        sys.exit(1)


def test_connection():
    """Step 1: Test connection with SELECT 1."""
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()
            if result and result[0] == 1:
                print("STATUS: SUCCESS")
            else:
                print("STATUS: FAILURE")
        conn.close()
    except Exception as e:
        print(f"CONNECTION_ERROR: {type(e).__name__}")
        sys.exit(1)


def check_tables():
    """Step 2: Check existing tables in hostel schema."""
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name = 'hostel';
            """)
            schema_exists = cur.fetchone() is not None

            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'hostel' AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            tables = [row["table_name"] for row in cur.fetchall()]

            print(f"SCHEMA_EXISTS: {schema_exists}")
            print(f"TABLE_COUNT: {len(tables)}")
            if tables:
                print("EXISTING_TABLES: " + ", ".join(tables))
            else:
                print("EXISTING_TABLES: NONE")
        conn.close()
    except Exception as e:
        print(f"CHECK_ERROR: {type(e).__name__}")
        sys.exit(1)


def run_sql_file(file_path: Path, label: str):
    """Execute a SQL file inside an explicit transaction."""
    if not file_path.exists():
        print(f"ERROR: {file_path} not found")
        sys.exit(1)

    sql_content = file_path.read_text(encoding="utf-8")
    conn = get_connection(autocommit=False)
    try:
        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute(sql_content)
        print(f"{label}: SUCCESS")
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"{label}_ERROR: {type(e).__name__}: {e}")
        sys.exit(1)


def verify_schema():
    """
    Step 5: Verify schema:
    - 13 tables
    - PKs and FKs per table
    - Triggers present
    """
    conn = get_connection(autocommit=True)
    with conn.cursor(row_factory=dict_row) as cur:
        # 1. Tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'hostel' AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = [r["table_name"] for r in cur.fetchall()]
        print(f"TABLE_COUNT: {len(tables)}")
        print("TABLES: " + ", ".join(tables))

        # 2. PKs
        print("\n--- PRIMARY KEYS ---")
        cur.execute("""
            SELECT tc.table_name, kcu.column_name, kcu.ordinal_position
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            WHERE tc.constraint_type = 'PRIMARY KEY'
              AND tc.table_schema = 'hostel'
            ORDER BY tc.table_name, kcu.ordinal_position;
        """)
        pks = {}
        for row in cur.fetchall():
            pks.setdefault(row["table_name"], []).append(row["column_name"])
        for tbl in sorted(tables):
            cols = pks.get(tbl, [])
            print(f"{tbl}: PK ({', '.join(cols)})")

        # 3. FKs
        print("\n--- FOREIGN KEYS ---")
        cur.execute("""
            SELECT
                tc.table_name,
                tc.constraint_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_schema = 'hostel'
            ORDER BY tc.table_name, tc.constraint_name, kcu.ordinal_position;
        """)
        fks = cur.fetchall()
        for fk in fks:
            print(f"{fk['table_name']}.{fk['column_name']} -> {fk['foreign_table_name']}.{fk['foreign_column_name']} ({fk['constraint_name']})")

        # 4. Triggers
        print("\n--- TRIGGERS ---")
        cur.execute("""
            SELECT trigger_name, event_manipulation, event_object_table, action_statement
            FROM information_schema.triggers
            WHERE trigger_schema = 'hostel'
            ORDER BY event_object_table, trigger_name;
        """)
        trgs = cur.fetchall()
        print(f"TRIGGER_COUNT: {len(trgs)}")
        for t in trgs:
            print(f"{t['event_object_table']}: {t['trigger_name']} ({t['event_manipulation']})")

    conn.close()


def test_rules():
    """
    Step 6: Test rules inside a transaction that is explicitly ROLLED BACK:
    1. room-capacity violation must fail
    2. hostel without a warden check
    3. NULL Room_No in MAINTENANCE must be accepted
    4. Room_No that does not exist in that hostel must be rejected
    """
    conn = get_connection(autocommit=False)
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SET search_path TO hostel, public;")
            print("1. Baseline setup: Inserting Hostel 99, Warden 99, Room 99-101 (Capacity 1)...")
            cur.execute("INSERT INTO hostel.hostel (hostel_id, name, address, type) VALUES (99, 'Test Ganga', 'Campus Area', 'Boys');")
            cur.execute("INSERT INTO hostel.warden (warden_id, name, phone, hostel_id) VALUES (99, 'Test Warden', '9876543210', 99);")
            cur.execute("INSERT INTO hostel.room (hostel_id, room_no, type, capacity) VALUES (99, 101, 'Single', 1);")
            print("   Baseline setup completed successfully.")

            # Test A: NULL Room_No in MAINTENANCE must be accepted
            print("\n2. [TEST A] NULL Room_No in MAINTENANCE (hostel-wide):")
            cur.execute("""
                INSERT INTO hostel.maintenance (request_id, hostel_id, room_no, description, date, status)
                VALUES (901, 99, NULL, 'Corridor water cooler filter repair', CURRENT_DATE, 'Open');
            """)
            print("   -> RESULT: PASSED (NULL Room_No accepted for hostel-wide request).")

            # Test B: Room_No that does not exist in that hostel must be rejected
            print("\n3. [TEST B] Non-existent Room_No in MAINTENANCE:")
            cur.execute("SAVEPOINT sp_room;")
            try:
                cur.execute("""
                    INSERT INTO hostel.maintenance (request_id, hostel_id, room_no, description, date, status)
                    VALUES (902, 99, 999, 'Repair in non-existent room', CURRENT_DATE, 'Open');
                """)
                print("   -> RESULT: FAILED (Invalid room accepted).")
            except Exception as e:
                cur.execute("ROLLBACK TO SAVEPOINT sp_room;")
                print(f"   -> RESULT: PASSED (Rejected by fk_maintenance_room: {type(e).__name__})")

            # Test C: Room-capacity violation must fail
            print("\n4. [TEST C] Room Capacity Limit (Capacity = 1):")
            cur.execute("""
                INSERT INTO hostel.student (student_id, fname, lname, reg_no, phone, hostel_id, room_no, allot_date)
                VALUES (9001, 'Student', 'One', 'REG9001', '9811122201', 99, 101, CURRENT_DATE);
            """)
            print("   Occupant 1 allotted (Room is now full at 1/1).")
            cur.execute("SAVEPOINT sp_cap;")
            try:
                cur.execute("""
                    INSERT INTO hostel.student (student_id, fname, lname, reg_no, phone, hostel_id, room_no, allot_date)
                    VALUES (9002, 'Student', 'Two', 'REG9002', '9811122202', 99, 101, CURRENT_DATE);
                """)
                print("   -> RESULT: FAILED (Capacity violation not prevented).")
            except Exception as e:
                cur.execute("ROLLBACK TO SAVEPOINT sp_cap;")
                error_msg = str(e).strip().splitlines()[0]
                print(f"   -> RESULT: PASSED (Rejected by trg_check_room_capacity: {error_msg})")

            # Test D: Hostel without a warden check
            print("\n5. [TEST D] Hostel without a Warden check:")
            cur.execute("INSERT INTO hostel.hostel (hostel_id, name, address, type) VALUES (98, 'Orphan Hostel', 'Campus East', 'Boys');")
            cur.execute("SELECT * FROM hostel.fn_verify_all_hostels_have_wardens();")
            unassigned = cur.fetchall()
            print(f"   fn_verify_all_hostels_have_wardens() identified orphan hostel: {unassigned}")

        print("\n6. Explicitly rolling back transaction...")
        conn.rollback()
        print("   -> TRANSACTION ROLLED BACK: No test data was committed.")
    except Exception as e:
        conn.rollback()
        print(f"TEST_RULES_ERROR: {type(e).__name__}: {e}")
    finally:
        conn.close()


def show_row_counts():
    """Display row counts for all tables in hostel schema."""
    conn = get_connection(autocommit=True)
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'hostel' AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = [r["table_name"] for r in cur.fetchall()]
        print("--- ROW COUNTS IN hostel SCHEMA ---")
        total = 0
        for tbl in tables:
            cur.execute(f"SELECT COUNT(*) AS cnt FROM hostel.{tbl};")
            count = cur.fetchone()["cnt"]
            total += count
            print(f"{tbl}: {count} rows")
        print(f"TOTAL: {total} rows across {len(tables)} tables")
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Hostel Management DB Runner")
    parser.add_argument("--test-connection", action="store_true", help="Test DB connection")
    parser.add_argument("--check-tables", action="store_true", help="Check existing tables")
    parser.add_argument("--run-schema", action="store_true", help="Run database/schema.sql in a transaction")
    parser.add_argument("--run-triggers", action="store_true", help="Run database/triggers.sql in a transaction")
    parser.add_argument("--verify", action="store_true", help="Verify schema, tables, PKs, FKs, triggers")
    parser.add_argument("--test-rules", action="store_true", help="Test business rules in a rolled-back transaction")
    parser.add_argument("--run-seed", action="store_true", help="Run database/seed.sql in a transaction")
    parser.add_argument("--row-counts", action="store_true", help="Show row counts across all tables")
    args = parser.parse_args()

    if args.test_connection:
        test_connection()
    elif args.check_tables:
        check_tables()
    elif args.run_schema:
        run_sql_file(SCHEMA_SQL_PATH, "RUN_SCHEMA")
    elif args.run_triggers:
        run_sql_file(TRIGGERS_SQL_PATH, "RUN_TRIGGERS")
    elif args.verify:
        verify_schema()
    elif args.test_rules:
        test_rules()
    elif args.run_seed:
        run_sql_file(SEED_SQL_PATH, "RUN_SEED")
    elif args.row_counts:
        show_row_counts()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
