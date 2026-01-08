"""
Time helpers
"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Get current UTC datetime"""
    return datetime.now(timezone.utc)


def is_stale(timestamp: datetime, threshold_minutes: int) -> bool:
    """Check if a timestamp is stale"""
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    
    age_minutes = (utc_now() - timestamp).total_seconds() / 60
    return age_minutes > threshold_minutes

