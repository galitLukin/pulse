"""
Connection to Pulse internal Postgres database
"""

import psycopg
from contextlib import contextmanager
from typing import Generator
from app.config import settings

logger = None  # Will be set up in utils.logging


class PulseDB:
    """Connection manager for Pulse internal database"""
    
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or settings.PULSE_DATABASE_URL
    
    @contextmanager
    def get_connection(self) -> Generator[psycopg.Connection, None, None]:
        """Get a database connection (context manager)"""
        conn = None
        try:
            conn = psycopg.connect(self.connection_string)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def get_cursor(self):
        """Get a cursor (for use with context manager)"""
        return self.get_connection()


# Singleton instance
pulse_db = PulseDB()

