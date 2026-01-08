"""
Pydantic request/response models for API
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.core import MonitorType, CheckStatus, AlertStatus


# Request Models
class ConnectionCreate(BaseModel):
    """Create a new database connection"""
    name: str = Field(..., min_length=1, max_length=255)
    connection_string: str
    max_queries_per_minute: int = Field(default=60, ge=1, le=1000)
    max_concurrent_queries: int = Field(default=5, ge=1, le=20)
    query_timeout_seconds: int = Field(default=2, ge=1, le=30)


class TableCreate(BaseModel):
    """Create a new monitored table"""
    connection_id: int
    schema_name: str = Field(..., min_length=1)
    table_name: str = Field(..., min_length=1)
    monitor_types: List[MonitorType]
    time_column: Optional[str] = None
    check_interval_minutes: int = Field(default=5, ge=1, le=60)


class TableUpdate(BaseModel):
    """Update a monitored table"""
    monitor_types: Optional[List[MonitorType]] = None
    time_column: Optional[str] = None
    check_interval_minutes: Optional[int] = Field(None, ge=1, le=60)


# Response Models
class ConnectionResponse(BaseModel):
    """Database connection response"""
    id: int
    name: str
    is_active: bool
    max_queries_per_minute: int
    max_concurrent_queries: int
    query_timeout_seconds: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TableResponse(BaseModel):
    """Monitored table response"""
    id: int
    connection_id: int
    schema_name: str
    table_name: str
    monitor_types: List[MonitorType]
    time_column: Optional[str]
    check_interval_minutes: int
    last_check_at: Optional[datetime] = None
    status: str = "unknown"  # green, yellow, red
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CheckResponse(BaseModel):
    """Health check result response"""
    id: int
    table_id: int
    monitor_type: MonitorType
    status: CheckStatus
    result_data: dict
    error_message: Optional[str]
    executed_at: datetime
    
    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    """Alert response"""
    id: int
    table_id: int
    monitor_type: MonitorType
    message: str
    status: AlertStatus
    created_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TableStatusResponse(BaseModel):
    """Table status summary for dashboard"""
    id: int
    schema_name: str
    table_name: str
    status: str  # green, yellow, red
    last_check_at: Optional[datetime]
    recent_alerts: List[AlertResponse]
    
    class Config:
        from_attributes = True

