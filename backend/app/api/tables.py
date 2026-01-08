"""
CRUD for monitored tables
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.api import TableCreate, TableUpdate, TableResponse, TableStatusResponse
from app.models.core import MonitorType

router = APIRouter()


@router.get("", response_model=List[TableResponse])
async def list_tables():
    """
    Get list of all monitored tables
    TODO: Fetch from database
    """
    # Placeholder - will be replaced with DB query
    return []


@router.get("/{table_id}", response_model=TableResponse)
async def get_table(table_id: int):
    """
    Get a specific table
    TODO: Fetch from database
    """
    # Placeholder
    raise HTTPException(status_code=404, detail="Table not found")


@router.post("", response_model=TableResponse, status_code=201)
async def create_table(table: TableCreate):
    """
    Create a new monitored table
    TODO: Store in database and schedule checks
    """
    # Placeholder - will create in DB and schedule checks
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{table_id}", response_model=TableResponse)
async def update_table(table_id: int, table_update: TableUpdate):
    """
    Update a monitored table
    TODO: Update in database
    """
    # Placeholder
    raise HTTPException(status_code=404, detail="Table not found")


@router.delete("/{table_id}", status_code=204)
async def delete_table(table_id: int):
    """
    Delete a monitored table
    TODO: Remove from database and unschedule checks
    """
    # Placeholder
    raise HTTPException(status_code=404, detail="Table not found")


@router.get("/{table_id}/status", response_model=TableStatusResponse)
async def get_table_status(table_id: int):
    """
    Get table status for dashboard (green/yellow/red)
    TODO: Fetch status from database
    """
    # Placeholder
    raise HTTPException(status_code=404, detail="Table not found")

