"""APScheduler setup and job registration"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config import get_settings
from app.jobs.scan_routes import scan_all_routes
from app.jobs.send_free_digest import send_free_digest

logger = logging.getLogger(__name__)


class SchedulerManager:
    """Manages APScheduler for background jobs"""
    
    def __init__(self):
        """Initialize scheduler"""
        self.scheduler = AsyncIOScheduler()
        self.settings = get_settings()
    
    def start(self) -> None:
        """Start the scheduler"""
        if self.scheduler.running:
            logger.warning("Scheduler already running")
            return
        
        # Register jobs
        self._register_jobs()
        
        # Start scheduler
        self.scheduler.start()
        logger.info("Scheduler started")
    
    def stop(self) -> None:
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def _register_jobs(self) -> None:
        """Register all periodic jobs"""
        
        # Scan routes job
        scan_interval = self.settings.scan_interval_minutes
        self.scheduler.add_job(
            scan_all_routes,
            trigger=IntervalTrigger(minutes=scan_interval),
            id="scan_routes",
            name="Scan all routes for deals",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(f"Registered scan_routes job every {scan_interval} minutes")
        
        # Free digest job
        digest_interval = self.settings.free_digest_interval_hours
        self.scheduler.add_job(
            send_free_digest,
            trigger=IntervalTrigger(hours=digest_interval),
            id="send_free_digest",
            name="Send free group digest",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(f"Registered send_free_digest job every {digest_interval} hours")


# Global scheduler instance
_scheduler: SchedulerManager | None = None


def get_scheduler() -> SchedulerManager:
    """Get or create the global scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = SchedulerManager()
    return _scheduler
