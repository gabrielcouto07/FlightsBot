"""FastAPI application factory and startup/shutdown"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db, close_db, create_tables
from app.scheduler import get_scheduler
from app.routers import webhook, routes_api, users_api, alerts_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    Startup:
    - Initialize database
    - Create tables
    - Start APScheduler 1409
    
    Shutdown:
    - Stop scheduler
    - Close database connections
    """
    
    # Startup
    logger.info("Starting up Flight Bot...")
    
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized")
        
        # Create tables
        await create_tables()
        logger.info("Database tables created")
        
        # Start scheduler
        scheduler = get_scheduler()
        scheduler.start()
        logger.info("Scheduler started")
        
        logger.info("Flight Bot startup complete")
    
    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Flight Bot...")
    
    try:
        # Stop scheduler
        scheduler = get_scheduler()
        scheduler.stop()
        logger.info("Scheduler stopped")
        
        # Close database
        await close_db()
        logger.info("Database closed")
        
        logger.info("Flight Bot shutdown complete")
    
    except Exception as e:
        logger.error(f"Shutdown error: {e}", exc_info=True)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI app instance
    """
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="WhatsApp Flight Price Alert Bot",
        lifespan=lifespan,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(webhook.router)
    app.include_router(routes_api.router)
    app.include_router(users_api.router)
    app.include_router(alerts_api.router)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict:
        """Health check endpoint"""
        return {"status": "healthy", "app": settings.app_name}
    
    # Root endpoint
    @app.get("/")
    async def root() -> dict:
        """Root endpoint"""
        return {
            "app": settings.app_name,
            "version": settings.app_version,
            "status": "running",
        }
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
