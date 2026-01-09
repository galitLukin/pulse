"""
Connection to Pulse internal Postgres database
"""

import psycopg
from queue import Queue, Empty
import threading

from app.config import settings

logger = None  # Will be set up in utils.logging

class PulseDBPool:
    def __init__(self, connection_string: str, max_conn: int = 5):
        self.connection_string = connection_string
        self.max_conn = max_conn
        self.pool = Queue(maxsize=max_conn)
        self.lock = threading.Lock()

        # Pre-create connections
        for _ in range(max_conn):
            self.pool.put(psycopg.connect(connection_string))

    def get_connection(self, timeout: int = 5):
        """
        Acquire a connection from the pool
        """
        try:
            conn = self.pool.get(timeout=timeout)
            return conn
        except Empty:
            raise RuntimeError("No database connections available")

    def release_connection(self, conn):
        """
        Return a connection back to the pool
        """
        if conn.closed:
            # Re-create connection if it was closed
            conn = psycopg.connect(self.connection_string)
        self.pool.put(conn)

    def close_all(self):
        """
        Close all connections in the pool
        """
        with self.lock:
            while not self.pool.empty():
                conn = self.pool.get()
                if not conn.closed:
                    conn.close()


# Singleton
pulse_db = PulseDBPool(settings.PULSE_DATABASE_URL, max_conn=3)
