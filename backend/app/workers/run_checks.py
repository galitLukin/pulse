"""
Entry point for scheduled checks
"""

import logging
import time

from app.services.checker import checker_service
from app.models.core import MonitorType, CheckStatus
from app.db.pulse_db import pulse_db  # uses the manual pool

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def run_scheduled_checks(table_id: int):
    """
    Run scheduled health checks for a table
    Called by the scheduler
    """
    logger.info(f"Running scheduled checks for table {table_id}")
    
    # TODO: Fetch table configuration from database
    # Example check flow:
    # 1. Get table config (connection_id, schema, table, monitor_types)
    # 2. For each monitor_type:
    #    - Run check
    #    - Store result

    logger.info(f"Completed checks for table {table_id}")


def run_once():
    logger.info("Running checks...")
    with pulse_db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()
            logger.info(f"Test query result: {result}")


if __name__ == "__main__":
    while True:
        run_once()
        time.sleep(60)
