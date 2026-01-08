"""
Seed development data for local testing
"""

import asyncio
from app.db.pulse_db import pulse_db


async def seed_data():
    """Seed development database with test data"""
    # TODO: Implement seeding logic
    print("Seeding development data...")
    
    with pulse_db.get_connection() as conn:
        with conn.cursor() as cur:
            # Example: Insert test workspace, connection, table
            # cur.execute("INSERT INTO workspaces (name) VALUES (%s) RETURNING id", ("Test Workspace",))
            pass
    
    print("Development data seeded successfully")


if __name__ == "__main__":
    asyncio.run(seed_data())

