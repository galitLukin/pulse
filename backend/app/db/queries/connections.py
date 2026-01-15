from typing import List, Dict
from app.db.pulse_db import pulse_db

def list_connections() -> List[Dict]:
    query = """
        SELECT
            id,
            connection_name,
            db_type,
            host,
            port,
            database_name,
            max_queries_per_minute,
            max_concurrent_queries,
            query_timeout_seconds,
            is_active,
            created_at,
            updated_at
        FROM connections
        ORDER BY created_at DESC
    """
    
    with pulse_db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        {
            "id": str(row[0]),
            "connection_name": row[1],
            "db_type": row[2],
            "host": row[3],
            "port": str(row[4]),  # Convert port to string to match API model
            "database_name": row[5],
            "max_queries_per_minute": row[6],
            "max_concurrent_queries": row[7],
            "query_timeout_seconds": row[8],
            "is_active": row[9],
            "created_at": row[10],
            "updated_at": row[11]
        }
        for row in rows
    ]
