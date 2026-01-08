"""
Rolling averages / baselines for anomaly detection
"""

import logging
from typing import Dict, Optional, List
from collections import deque
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class BaselineService:
    """Manages rolling baselines for anomaly detection"""
    
    def __init__(self, window_size: int = 10):
        """
        window_size: Number of recent values to keep for baseline
        """
        self.window_size = window_size
        # Store recent values per table: {f"{schema}.{table}": deque([values])}
        self._volume_baselines: Dict[str, deque] = {}
        # Store schema snapshots: {f"{schema}.{table}": schema_dict}
        self._schema_snapshots: Dict[str, dict] = {}
    
    def record_volume(self, schema: str, table: str, row_count: int):
        """Record a volume measurement"""
        key = f"{schema}.{table}"
        if key not in self._volume_baselines:
            self._volume_baselines[key] = deque(maxlen=self.window_size)
        
        self._volume_baselines[key].append({
            "row_count": row_count,
            "timestamp": datetime.utcnow()
        })
    
    def get_baseline(self, schema: str, table: str) -> Optional[Dict]:
        """Get baseline statistics for a table"""
        key = f"{schema}.{table}"
        if key not in self._volume_baselines or len(self._volume_baselines[key]) == 0:
            return None
        
        values = list(self._volume_baselines[key])
        row_counts = [v["row_count"] for v in values]
        
        if not row_counts:
            return None
        
        avg = sum(row_counts) / len(row_counts)
        min_val = min(row_counts)
        max_val = max(row_counts)
        
        return {
            "average": avg,
            "min": min_val,
            "max": max_val,
            "count": len(row_counts)
        }
    
    def is_anomaly(
        self,
        schema: str,
        table: str,
        current_value: int,
        threshold_percent: float = 0.3
    ) -> bool:
        """
        Check if current value is an anomaly
        threshold_percent: 0.3 = 30% deviation triggers anomaly
        """
        baseline = self.get_baseline(schema, table)
        if not baseline:
            # No baseline yet, not an anomaly
            return False
        
        avg = baseline["average"]
        if avg == 0:
            return current_value != 0
        
        deviation = abs(current_value - avg) / avg
        return deviation > threshold_percent
    
    def check_schema_change(
        self,
        schema: str,
        table: str,
        current_schema: dict
    ) -> bool:
        """Check if schema has changed"""
        key = f"{schema}.{table}"
        
        if key not in self._schema_snapshots:
            # First time seeing this schema, store it
            self._schema_snapshots[key] = current_schema
            return False
        
        previous_schema = self._schema_snapshots[key]
        
        # Compare schemas
        prev_columns = {col["name"]: col for col in previous_schema.get("columns", [])}
        curr_columns = {col["name"]: col for col in current_schema.get("columns", [])}
        
        # Check for added/removed columns
        if set(prev_columns.keys()) != set(curr_columns.keys()):
            self._schema_snapshots[key] = current_schema
            return True
        
        # Check for type changes
        for col_name, prev_col in prev_columns.items():
            curr_col = curr_columns[col_name]
            if prev_col["type"] != curr_col["type"]:
                self._schema_snapshots[key] = current_schema
                return True
            if prev_col["nullable"] != curr_col["nullable"]:
                self._schema_snapshots[key] = current_schema
                return True
        
        return False


# Singleton instance
baseline_service = BaselineService()

