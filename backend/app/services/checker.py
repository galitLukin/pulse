"""
Runs data checks against replicas
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from app.db.replica_db import replica_db_manager
from app.db.queries import SafeQueries
from app.models.core import MonitorType, CheckStatus
from app.services.safety import SafetyGuardrails
from app.services.baselines import BaselineService

logger = logging.getLogger(__name__)


class CheckerService:
    """Service for running health checks on monitored tables"""
    
    def __init__(self):
        self.baseline_service = BaselineService()
        self.queries = SafeQueries()
    
    async def run_check(
        self,
        table_id: int,
        connection_id: int,
        schema_name: str,
        table_name: str,
        monitor_type: MonitorType,
        time_column: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run a single health check
        Returns check result with status and data
        """
        replica_conn = replica_db_manager.get_connection(connection_id)
        if not replica_conn:
            return {
                "status": CheckStatus.ERROR,
                "error_message": f"Connection {connection_id} not found",
                "result_data": {}
            }
        
        try:
            # Check safety guardrails
            if not replica_conn.guardrails.can_run_query(connection_id):
                return {
                    "status": CheckStatus.SKIPPED,
                    "error_message": "Query budget exceeded",
                    "result_data": {}
                }
            
            # Run the appropriate check
            with replica_conn.get_readonly_connection() as conn:
                with conn.cursor() as cursor:
                    result = await self._execute_check(
                        cursor,
                        monitor_type,
                        schema_name,
                        table_name,
                        time_column
                    )
                    
                    # Record query usage
                    replica_conn.guardrails.record_query(connection_id)
                    
                    return result
                    
        except Exception as e:
            logger.error(f"Error running check for table {table_id}: {e}", exc_info=True)
            return {
                "status": CheckStatus.ERROR,
                "error_message": str(e),
                "result_data": {}
            }
    
    async def _execute_check(
        self,
        cursor,
        monitor_type: MonitorType,
        schema_name: str,
        table_name: str,
        time_column: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute the actual check query"""
        
        if monitor_type == MonitorType.FRESHNESS:
            if not time_column:
                raise ValueError("time_column required for freshness check")
            
            max_timestamp = self.queries.check_freshness(
                cursor, schema_name, table_name, time_column
            )
            
            return {
                "status": CheckStatus.SUCCESS,
                "result_data": {
                    "max_timestamp": max_timestamp.isoformat() if max_timestamp else None,
                    "is_stale": max_timestamp is None or self._is_stale(max_timestamp)
                }
            }
        
        elif monitor_type == MonitorType.VOLUME:
            row_count = self.queries.check_volume(cursor, schema_name, table_name)
            has_zero_rows = row_count == 0
            
            # Check against baseline
            baseline = self.baseline_service.get_baseline(schema_name, table_name)
            is_anomaly = self.baseline_service.is_anomaly(
                schema_name, table_name, row_count
            )
            
            return {
                "status": CheckStatus.SUCCESS,
                "result_data": {
                    "row_count": row_count,
                    "has_zero_rows": has_zero_rows,
                    "baseline": baseline,
                    "is_anomaly": is_anomaly
                }
            }
        
        elif monitor_type == MonitorType.SCHEMA:
            schema_info = self.queries.check_schema(cursor, schema_name, table_name)
            
            # Compare with previous schema (stored in baseline)
            schema_changed = self.baseline_service.check_schema_change(
                schema_name, table_name, schema_info
            )
            
            return {
                "status": CheckStatus.SUCCESS,
                "result_data": {
                    "schema": schema_info,
                    "schema_changed": schema_changed
                }
            }
        
        else:
            raise ValueError(f"Unknown monitor type: {monitor_type}")
    
    def _is_stale(self, max_timestamp: datetime, threshold_minutes: int = 10) -> bool:
        """Check if timestamp is stale"""
        age_minutes = (datetime.utcnow() - max_timestamp).total_seconds() / 60
        return age_minutes > threshold_minutes


# Singleton instance
checker_service = CheckerService()

