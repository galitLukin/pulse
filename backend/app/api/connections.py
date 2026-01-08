"""
DB connection setup endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.models.api import ConnectionCreate, ConnectionResponse
from app.db.replica_db import replica_db_manager
from app.services.safety import SafetyGuardrails

router = APIRouter()


@router.get("", response_model=List[ConnectionResponse])
async def list_connections():
    """
    Get list of all database connections
    TODO: Fetch from database
    """
    # Placeholder - will be replaced with DB query
    return []


@router.get("/{connection_id}", response_model=ConnectionResponse)
async def get_connection(connection_id: int):
    """
    Get a specific connection
    TODO: Fetch from database
    """
    # Placeholder
    raise HTTPException(status_code=404, detail="Connection not found")


@router.post("", response_model=ConnectionResponse, status_code=201)
async def create_connection(connection: ConnectionCreate):
    """
    Create a new database connection
    Registers the connection with the replica manager
    """
    # TODO: Store in database
    # TODO: Validate connection string by testing connection
    
    # Create guardrails
    guardrails = SafetyGuardrails(
        max_queries_per_minute=connection.max_queries_per_minute,
        max_concurrent_queries=connection.max_concurrent_queries,
        query_timeout_seconds=connection.query_timeout_seconds
    )
    
    # Register with replica manager (temporary - will use DB ID)
    connection_id = 1  # TODO: Get from DB insert
    replica_db_manager.register_connection(
        connection_id,
        connection.connection_string,
        guardrails
    )
    
    # Placeholder response
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{connection_id}", status_code=204)
async def delete_connection(connection_id: int):
    """
    Delete a database connection
    TODO: Remove from database and replica manager
    """
    replica_db_manager.remove_connection(connection_id)
    # Placeholder
    raise HTTPException(status_code=404, detail="Connection not found")

