from typing import List, Dict
from app.db.pulse_db import pulse_db

def list_checks() -> List[Dict]:
    query = """
        SELECT
            c.id,
            c.check_name,
            c.check_type,
            c.is_active,
            c.created_at,
            c.updated_at,
            c.config,
            conn.id AS connection_id,
            conn.connection_name AS connection_name
        FROM checks c
        JOIN connections conn ON conn.id = c.connection_id
        ORDER BY c.created_at DESC
    """

    with pulse_db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        {
            "id": str(row[0]),
            "check_name": row[1],
            "check_type": row[2],
            "is_active": row[3],
            "created_at": row[4],
            "updated_at": row[5],
            "config": row[6],
            "connection": {
                "id": str(row[7]),
                "connection_name": row[8],
            },
        }
        for row in rows
    ]
