"""
Connection to Pulse internal Postgres database
"""

import psycopg
from queue import Queue, Empty
import threading
from contextlib import contextmanager
from typing import Generator

from app.config import settings

logger = None  # Will be set up in utils.logging

class PulseDBPool:
    def __init__(self, connection_string: str, max_conn: int = 5):
        self.connection_string = connection_string
        self.max_conn = max_conn
        self.pool = Queue(maxsize=max_conn)
        self.lock = threading.Lock()
        self._initialized = False

    def _initialize_pool(self):
        """Lazy initialization of connection pool"""
        if not self._initialized:
            with self.lock:
                if not self._initialized:
                    if not self.connection_string:
                        raise ValueError(
                            "PULSE_DATABASE_URL is not set. "
                            "Please set it in your environment or .env file. "
                            "Example: postgresql://user:password@localhost:5432/dbname"
                        )
                    # Pre-create connections
                    for _ in range(self.max_conn):
                        self.pool.put(psycopg.connect(self.connection_string))
                    self._initialized = True

    def get_connection(self, timeout: int = 5):
        """
        Acquire a connection from the pool
        """
        self._initialize_pool()
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
        self._initialize_pool()
        self.pool.put(conn)

    @contextmanager
    def connection(self, timeout: int = 5) -> Generator[psycopg.Connection, None, None]:
        """
        Context manager for getting and releasing a connection.
        Use this instead of get_connection/release_connection manually.
        
        Example:
            with pulse_db.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
        """
        conn = self.get_connection(timeout)
        try:
            yield conn
        finally:
            self.release_connection(conn)

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
