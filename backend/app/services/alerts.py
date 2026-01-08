"""
Alert creation & suppression logic
"""

import logging
from datetime import datetime
from typing import Optional, List
from app.models.core import MonitorType, CheckStatus, AlertStatus
from app.db.pulse_db import pulse_db

logger = logging.getLogger(__name__)


class AlertService:
    """Service for managing alerts"""
    
    def __init__(self):
        # Track consecutive failures per table+monitor
        self._failure_counts: dict = {}  # {f"{table_id}_{monitor_type}": count}
        self._active_alerts: dict = {}  # {f"{table_id}_{monitor_type}": alert_id}
    
    def should_alert(
        self,
        table_id: int,
        monitor_type: MonitorType,
        check_status: CheckStatus,
        threshold: int = 2
    ) -> bool:
        """
        Determine if an alert should be created
        Requires threshold consecutive failures
        """
        key = f"{table_id}_{monitor_type}"
        
        if check_status == CheckStatus.SUCCESS:
            # Reset failure count on success
            self._failure_counts[key] = 0
            return False
        
        # Increment failure count
        self._failure_counts[key] = self._failure_counts.get(key, 0) + 1
        
        # Alert if we've hit the threshold
        return self._failure_counts[key] >= threshold
    
    def create_alert(
        self,
        table_id: int,
        monitor_type: MonitorType,
        message: str
    ) -> int:
        """
        Create a new alert
        Returns alert ID
        TODO: Store in database
        """
        key = f"{table_id}_{monitor_type}"
        
        # Check if alert already exists
        if key in self._active_alerts:
            logger.info(f"Alert already exists for {key}, not creating duplicate")
            return self._active_alerts[key]
        
        # Create new alert
        alert_id = len(self._active_alerts) + 1  # TODO: Use DB sequence
        self._active_alerts[key] = alert_id
        
        logger.warning(f"Alert created: {alert_id} - {message}")
        
        # TODO: Store in database
        # TODO: Send email notification
        
        return alert_id
    
    def resolve_alert(
        self,
        table_id: int,
        monitor_type: MonitorType
    ):
        """Resolve an active alert"""
        key = f"{table_id}_{monitor_type}"
        
        if key in self._active_alerts:
            alert_id = self._active_alerts[key]
            del self._active_alerts[key]
            logger.info(f"Alert {alert_id} resolved for {key}")
            
            # TODO: Update in database
    
    def get_active_alerts(self, table_id: Optional[int] = None) -> List[dict]:
        """
        Get active alerts
        TODO: Fetch from database
        """
        # Placeholder - will be replaced with DB query
        return []
    
    def suppress_alerts(self, table_id: int, reason: str):
        """Suppress alerts for a table (e.g., during replica instability)"""
        logger.info(f"Alerts suppressed for table {table_id}: {reason}")
        # TODO: Implement suppression logic


# Singleton instance
alert_service = AlertService()

