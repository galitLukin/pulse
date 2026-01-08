"""
App startup hooks (scheduler, health checks)
"""

import logging
from app.config import settings
from app.services.scheduler import scheduler_service

logger = logging.getLogger(__name__)


async def on_startup():
    """Initialize services on startup"""
    logger.info("Starting Pulse application...")
    
    # Start the scheduler
    scheduler_service.start()
    logger.info("Scheduler started")
    
    logger.info("Pulse application started successfully")


async def on_shutdown():
    """Cleanup on shutdown"""
    logger.info("Shutting down Pulse application...")
    
    # Shutdown scheduler
    scheduler_service.shutdown()
    logger.info("Scheduler stopped")
    
    logger.info("Pulse application shut down")

