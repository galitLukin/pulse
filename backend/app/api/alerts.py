"""
Fetch alerts for UI
"""

from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.api import AlertResponse
from app.services.alerts import alert_service

router = APIRouter()


@router.get("", response_model=List[AlertResponse])
async def list_alerts(
    table_id: Optional[int] = Query(None, description="Filter by table ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Get list of alerts
    TODO: Fetch from database with filters
    """
    alerts = alert_service.get_active_alerts(table_id)
    # Placeholder - will be replaced with DB query
    return []


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int):
    """
    Get a specific alert
    TODO: Fetch from database
    """
    # Placeholder
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Alert not found")

