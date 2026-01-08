"""
Safe, parameterized SQL queries for monitoring checks
"""

from typing import Optional, Dict, Any
from datetime import datetime
import psycopg
from psycopg import sql


class SafeQueries:
    """Collection of safe, parameterized queries for data health checks"""
    
    @staticmethod
    def check_freshness(
        cursor: psycopg.Cursor,
        schema: str,
        table: str,
        time_column: str
    ) -> Optional[datetime]:
        """
        Check table freshness using max timestamp
        Returns the max timestamp or None if no rows
        """
        query = sql.SQL("""
            SELECT MAX({time_column})
            FROM {schema}.{table}
        """).format(
            schema=sql.Identifier(schema),
            table=sql.Identifier(table),
            time_column=sql.Identifier(time_column)
        )
        
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result and result[0] else None
    
    @staticmethod
    def check_volume(cursor: psycopg.Cursor, schema: str, table: str) -> int:
        """
        Get row count for volume monitoring
        Uses count(*) - safe for indexed tables
        """
        query = sql.SQL("""
            SELECT COUNT(*)
            FROM {schema}.{table}
        """).format(
            schema=sql.Identifier(schema),
            table=sql.Identifier(table)
        )
        
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0
    
    @staticmethod
    def check_schema(
        cursor: psycopg.Cursor,
        schema: str,
        table: str
    ) -> Dict[str, Any]:
        """
        Get schema information for a table
        Returns column definitions
        """
        query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = %s
              AND table_name = %s
            ORDER BY ordinal_position
        """
        
        cursor.execute(query, (schema, table))
        columns = cursor.fetchall()
        
        return {
            "columns": [
                {
                    "name": col[0],
                    "type": col[1],
                    "nullable": col[2] == "YES",
                    "default": col[3]
                }
                for col in columns
            ]
        }
    
    @staticmethod
    def check_replica_lag(cursor: psycopg.Cursor) -> Optional[float]:
        """
        Check replica lag in seconds
        Returns None if not a replica or lag cannot be determined
        """
        # For Postgres replicas, check pg_stat_replication or replication lag
        query = """
            SELECT 
                EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp())) AS lag_seconds
            WHERE pg_is_in_recovery() = true
        """
        
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None
    
    @staticmethod
    def check_zero_rows(
        cursor: psycopg.Cursor,
        schema: str,
        table: str
    ) -> bool:
        """
        Check if table has zero rows
        Uses EXISTS for efficiency
        """
        query = sql.SQL("""
            SELECT EXISTS(
                SELECT 1
                FROM {schema}.{table}
                LIMIT 1
            )
        """).format(
            schema=sql.Identifier(schema),
            table=sql.Identifier(table)
        )
        
        cursor.execute(query)
        result = cursor.fetchone()
        return not (result[0] if result else False)

