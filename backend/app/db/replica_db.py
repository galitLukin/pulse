"""
Read-only connections to customer replicas
"""

import psycopg
from contextlib import contextmanager
from typing import Generator, Optional, Dict
from app.config import settings
from app.services.safety import SafetyGuardrails

logger = None  # Will be set up in utils.logging


class ReplicaConnection:
    """Represents a connection to a customer's read replica"""
    
    def __init__(
        self,
        connection_string: str,
        connection_id: int,
        guardrails: Optional[SafetyGuardrails] = None
    ):
        self.connection_string = connection_string
        self.connection_id = connection_id
        self.guardrails = guardrails or SafetyGuardrails()
    
    @contextmanager
    def get_readonly_connection(self) -> Generator[psycopg.Connection, None, None]:
        """
        Get a read-only connection to the replica
        Ensures connection is read-only and respects safety guardrails
        """
        conn = None
        try:
            # Connect with read-only mode
            conn = psycopg.connect(
                self.connection_string,
                options="-c default_transaction_read_only=on"
            )
            
            # Verify read-only
            with conn.cursor() as cur:
                cur.execute("SHOW transaction_read_only")
                result = cur.fetchone()
                if result[0] != "on":
                    raise RuntimeError("Connection is not read-only")
            
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()


class ReplicaDBManager:
    """Manages connections to customer replicas"""
    
    def __init__(self):
        self._connections: Dict[int, ReplicaConnection] = {}
    
    def register_connection(
        self,
        connection_id: int,
        connection_string: str,
        guardrails: Optional[SafetyGuardrails] = None
    ) -> ReplicaConnection:
        """Register a new replica connection"""
        conn = ReplicaConnection(connection_string, connection_id, guardrails)
        self._connections[connection_id] = conn
        return conn
    
    def get_connection(self, connection_id: int) -> Optional[ReplicaConnection]:
        """Get a registered connection"""
        return self._connections.get(connection_id)
    
    def remove_connection(self, connection_id: int):
        """Remove a connection"""
        if connection_id in self._connections:
            del self._connections[connection_id]


# Singleton instance
replica_db_manager = ReplicaDBManager()

