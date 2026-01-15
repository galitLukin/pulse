"""
Internal DB models (tables, checks)
These represent the schema of Pulse's internal database
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class MonitorType(str, Enum):
    """Types of monitors"""
    FRESHNESS = "freshness"
    VOLUME = "volume"
    SCHEMA = "schema"


class CheckStatus(str, Enum):
    """Status of a health check"""
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"
    SKIPPED = "skipped"


# These are conceptual models - actual DB schema will be in migrations
class Table:
    """A monitored table"""
    def __init__(
        self,
        id: int,
        connection_id: int,
        schema_name: str,
        table_name: str,
        monitor_types: list[MonitorType],
        time_column: Optional[str] = None,
        check_interval_minutes: int = 5,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.connection_id = connection_id
        self.schema_name = schema_name
        self.table_name = table_name
        self.monitor_types = monitor_types
        self.time_column = time_column
        self.check_interval_minutes = check_interval_minutes
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()


class Connection:
    """A database connection (customer replica)"""
    def __init__(
        self,
        id: int,
        name: str,
        connection_string: str,
        max_queries_per_minute: int = 60,
        max_concurrent_queries: int = 5,
        query_timeout_seconds: int = 2,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.connection_string = connection_string
        self.max_queries_per_minute = max_queries_per_minute
        self.max_concurrent_queries = max_concurrent_queries
        self.query_timeout_seconds = query_timeout_seconds
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()


class Check:
    """A health check execution result"""
    def __init__(
        self,
        id: int,
        table_id: int,
        monitor_type: MonitorType,
        status: CheckStatus,
        result_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        executed_at: Optional[datetime] = None
    ):
        self.id = id
        self.table_id = table_id
        self.monitor_type = monitor_type
        self.status = status
        self.result_data = result_data or {}
        self.error_message = error_message
        self.executed_at = executed_at or datetime.utcnow()

