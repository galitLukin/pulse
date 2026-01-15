"""
Pydantic request/response models for API
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.core import MonitorType, CheckStatus


# Request Models
class ConnectionCreate(BaseModel):
    """Create a new database connection"""
    name: str = Field(..., min_length=1, max_length=255)
    connection_string: str
    max_queries_per_minute: int = Field(default=60, ge=1, le=1000)
    max_concurrent_queries: int = Field(default=5, ge=1, le=20)
    query_timeout_seconds: int = Field(default=2, ge=1, le=30)

# Response Models
class ConnectionResponse(BaseModel):
    """Database connection response"""
    id: str
    connection_name: str
    db_type: str
    host: str
    port: str
    database_name: str
    max_queries_per_minute: int
    max_concurrent_queries: int
    query_timeout_seconds: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConnectionInfo(BaseModel):
    """Connection information nested in check response"""
    id: str
    connection_name: str


class CheckResponse(BaseModel):
    """Check configuration response"""
    id: str
    check_name: str
    check_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config: dict
    connection: ConnectionInfo
    
    class Config:
        from_attributes = True

