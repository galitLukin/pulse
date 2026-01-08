"""
Manual worker execution for testing
"""

import asyncio
import sys
from app.workers.run_checks import run_scheduled_checks


async def main():
    """Run worker manually"""
    if len(sys.argv) < 2:
        print("Usage: python run_worker.py <table_id>")
        sys.exit(1)
    
    table_id = int(sys.argv[1])
    await run_scheduled_checks(table_id)


if __name__ == "__main__":
    asyncio.run(main())

