"""
Timeouts, query budgets, guardrails
"""

import logging
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict
from app.config import settings

logger = logging.getLogger(__name__)


class SafetyGuardrails:
    """Enforces safety guardrails per connection"""
    
    def __init__(
        self,
        max_queries_per_minute: int = None,
        max_concurrent_queries: int = None,
        query_timeout_seconds: int = None
    ):
        self.max_queries_per_minute = max_queries_per_minute or settings.MAX_QUERIES_PER_MINUTE
        self.max_concurrent_queries = max_concurrent_queries or settings.MAX_CONCURRENT_QUERIES
        self.query_timeout_seconds = query_timeout_seconds or settings.QUERY_TIMEOUT_SECONDS
        
        # Track query counts per connection
        self._query_timestamps: Dict[int, list] = defaultdict(list)
        self._concurrent_queries: Dict[int, int] = defaultdict(int)
    
    def can_run_query(self, connection_id: int) -> bool:
        """Check if a query can be run (respects rate limits)"""
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        
        # Clean old timestamps
        timestamps = self._query_timestamps[connection_id]
        self._query_timestamps[connection_id] = [
            ts for ts in timestamps if ts > minute_ago
        ]
        
        # Check rate limit
        if len(self._query_timestamps[connection_id]) >= self.max_queries_per_minute:
            logger.warning(
                f"Rate limit exceeded for connection {connection_id}: "
                f"{len(self._query_timestamps[connection_id])}/{self.max_queries_per_minute}"
            )
            return False
        
        # Check concurrent queries
        if self._concurrent_queries[connection_id] >= self.max_concurrent_queries:
            logger.warning(
                f"Concurrent query limit exceeded for connection {connection_id}: "
                f"{self._concurrent_queries[connection_id]}/{self.max_concurrent_queries}"
            )
            return False
        
        return True
    
    def record_query(self, connection_id: int):
        """Record that a query was executed"""
        now = datetime.utcnow()
        self._query_timestamps[connection_id].append(now)
        self._concurrent_queries[connection_id] += 1
    
    def release_query(self, connection_id: int):
        """Release a concurrent query slot"""
        if self._concurrent_queries[connection_id] > 0:
            self._concurrent_queries[connection_id] -= 1


class ReplicaSafety:
    """System-level replica safety checks"""
    
    @staticmethod
    def check_replica_lag(lag_seconds: Optional[float]) -> bool:
        """
        Check if replica lag is acceptable
        Returns True if lag is acceptable, False if too high
        """
        if lag_seconds is None:
            return True  # Can't determine lag, assume OK
        
        threshold = settings.REPLICA_LAG_THRESHOLD_SECONDS
        return lag_seconds < threshold
    
    @staticmethod
    def should_suppress_checks(lag_seconds: Optional[float]) -> bool:
        """Determine if checks should be suppressed due to replica instability"""
        if not settings.BACKPRESSURE_ENABLED:
            return False
        
        if lag_seconds is None:
            return False
        
        # Suppress if lag is very high (2x threshold)
        return lag_seconds > (settings.REPLICA_LAG_THRESHOLD_SECONDS * 2)

