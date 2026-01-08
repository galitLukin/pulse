"""
Simple retry helpers
"""

import asyncio
import logging
from typing import Callable, TypeVar, Optional

logger = logging.getLogger(__name__)

T = TypeVar('T')


async def retry_async(
    func: Callable[[], T],
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> T:
    """
    Retry an async function with exponential backoff
    
    Args:
        func: Async function to retry
        max_attempts: Maximum number of attempts
        delay_seconds: Initial delay between attempts
        backoff: Multiplier for delay on each retry
        exceptions: Tuple of exceptions to catch and retry on
    """
    last_exception = None
    current_delay = delay_seconds
    
    for attempt in range(1, max_attempts + 1):
        try:
            return await func()
        except exceptions as e:
            last_exception = e
            if attempt < max_attempts:
                logger.warning(
                    f"Attempt {attempt}/{max_attempts} failed: {e}. "
                    f"Retrying in {current_delay}s..."
                )
                await asyncio.sleep(current_delay)
                current_delay *= backoff
            else:
                logger.error(f"All {max_attempts} attempts failed")
    
    raise last_exception

