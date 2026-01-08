"""
Job scheduling logic using APScheduler
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from app.workers.run_checks import run_scheduled_checks

logger = logging.getLogger(__name__)


class SchedulerService:
    """Manages scheduled jobs for health checks"""
    
    def __init__(self):
        jobstores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(10)
        }
        job_defaults = {
            'coalesce': True,
            'max_instances': 1
        }
        
        self.scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults
        )
        self.is_running = False
    
    def start(self):
        """Start the scheduler"""
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped")
    
    def schedule_table_check(self, table_id: int, interval_minutes: int):
        """
        Schedule periodic checks for a table
        """
        job_id = f"check_table_{table_id}"
        
        # Remove existing job if any
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)
        
        # Add new job
        self.scheduler.add_job(
            run_scheduled_checks,
            'interval',
            minutes=interval_minutes,
            id=job_id,
            args=[table_id],
            replace_existing=True
        )
        logger.info(f"Scheduled checks for table {table_id} every {interval_minutes} minutes")
    
    def unschedule_table_check(self, table_id: int):
        """Remove scheduled checks for a table"""
        job_id = f"check_table_{table_id}"
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)
            logger.info(f"Unscheduled checks for table {table_id}")


# Singleton instance
scheduler_service = SchedulerService()

