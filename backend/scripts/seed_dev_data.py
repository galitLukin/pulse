"""
Seed development data for local testing
To run:  python -m scripts.seed_dev_data
"""

from app.db.pulse_db import pulse_db
from app.config import settings
import json
from datetime import datetime, timedelta


def clear_all_data(cur):
    """
    Clear all data from tables in the correct order (respecting foreign keys).
    Deletes in reverse dependency order.
    """
    print("Clearing all existing data...")
    
    # Delete in reverse dependency order
    cur.execute("DELETE FROM current_status;")
    cur.execute("DELETE FROM check_runs;")
    cur.execute("DELETE FROM checks;")
    cur.execute("DELETE FROM connections;")
    
    print("All data cleared.")


def seed_connections(cur):
    cur.execute(
        """
        INSERT INTO connections (
            id,
            connection_name,
            db_type,
            host,
            port,
            database_name,
            max_queries_per_minute,
            max_concurrent_queries,
            query_timeout_seconds
        )
        VALUES (
            gen_random_uuid(),
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        ON CONFLICT (id) DO NOTHING;
        """,
        (
            "Local Postgres",
            "postgres",
            "localhost",
            5432,
            "pulse",
            60,
            5,
            30
        ),
    )


def seed_checks(cur):
    # Find the connection we just seeded
    cur.execute(
        """
        SELECT id
        FROM connections
        WHERE connection_name = %s
        LIMIT 1
        """,
        ("Local Postgres",),
    )
    row = cur.fetchone()
    if not row:
        raise RuntimeError("Local Postgres connection not found")

    connection_id = row[0]

    cur.execute(
        """
        INSERT INTO checks (
            id,
            connection_id,
            check_name,
            check_type,
            config
        )
        VALUES (
            gen_random_uuid(),
            %s,
            %s,
            %s,
            %s::jsonb
        )
        ON CONFLICT (id) DO NOTHING;
        """,
        (
            connection_id,
            "Replica Lag Check < 5",
            "replica_lag",
            json.dumps({
                "max_lag_seconds": 5
            }),
        ),
    )

def seed_check_runs(cur):
    # Get the check we seeded
    cur.execute(
        """
        SELECT id
        FROM checks
        WHERE check_name = %s
        LIMIT 1
        """,
        ("Replica Lag Check < 5",),
    )
    row = cur.fetchone()
    if not row:
        raise RuntimeError("Seed check not found")

    check_id = row[0]

    # Create a few check runs with different statuses
    now = datetime.utcnow()
    
    # Successful check run (most recent)
    cur.execute(
        """
        INSERT INTO check_runs (
            id,
            check_id,
            started_at,
            finished_at,
            status,
            error_message,
            metrics
        )
        VALUES (
            gen_random_uuid(),
            %s,
            %s,
            %s,
            %s,
            %s,
            %s::jsonb
        );
        """,
        (
            check_id,
            now - timedelta(seconds=2),
            now,
            "success",
            None,
            json.dumps({
                "lag_seconds": 1.2
            }),
        ),
    )
    
    # Another successful check run (older)
    cur.execute(
        """
        INSERT INTO check_runs (
            id,
            check_id,
            started_at,
            finished_at,
            status,
            error_message,
            metrics
        )
        VALUES (
            gen_random_uuid(),
            %s,
            %s,
            %s,
            %s,
            %s,
            %s::jsonb
        );
        """,
        (
            check_id,
            now - timedelta(minutes=5, seconds=1),
            now - timedelta(minutes=5),
            "success",
            None,
            json.dumps({
                "lag_seconds": 0.8
            }),
        ),
    )
    
    # Warning check run (older)
    cur.execute(
        """
        INSERT INTO check_runs (
            id,
            check_id,
            started_at,
            finished_at,
            status,
            error_message,
            metrics
        )
        VALUES (
            gen_random_uuid(),
            %s,
            %s,
            %s,
            %s,
            %s,
            %s::jsonb
        );
        """,
        (
            check_id,
            now - timedelta(minutes=10, seconds=1),
            now - timedelta(minutes=10),
            "warning",
            "Replica lag approaching threshold",
            json.dumps({
                "lag_seconds": 4.5
            }),
        ),
    )
def seed_data():
    print("Seeding development data...")

    with pulse_db.connection() as conn:
        with conn.cursor() as cur:
            clear_all_data(cur)
            seed_connections(cur)
            seed_checks(cur)
            seed_check_runs(cur)
            conn.commit()

    print("Development data seeded successfully")


if __name__ == "__main__":
    # Allow seeding in local/dev environments
    if settings.PULSE_ENV not in ("local", "dev"):
        raise RuntimeError(f"Refusing to seed non-dev environment: {settings.PULSE_ENV}")

    # Check if database URL is set
    if not settings.PULSE_DATABASE_URL:
        raise RuntimeError(
            "PULSE_DATABASE_URL is not set. "
            "Please set it in your environment or create a .env file. "
            "Example: export PULSE_DATABASE_URL='postgresql://user:password@localhost:5432/pulse'"
        )

    seed_data()