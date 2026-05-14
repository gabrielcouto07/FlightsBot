"""SQLAlchemy database configuration and session management"""

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator

from app.config import get_settings

settings = get_settings()


async_engine: AsyncEngine | None = None
AsyncSessionLocal = None


async def init_db() -> None:
    """Initialize database engine and session factory"""
    global async_engine, AsyncSessionLocal
    
    engine_args = {
        "echo": settings.debug,
        "future": True,
    }
    
    # Use NullPool for SQLite to avoid threading issues
    if "sqlite" in settings.database_url:
        engine_args["connect_args"] = {"check_same_thread": False}
        engine_args["poolclass"] = NullPool
    
    async_engine = create_async_engine(
        settings.database_url,
        **engine_args,
    )
    
    AsyncSessionLocal = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def close_db() -> None:
    """Close database connection"""
    global async_engine
    if async_engine:
        await async_engine.dispose()
        async_engine = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session in FastAPI routes"""
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables() -> None:
    """Create all database tables"""
    import app.models  # noqa: F401
    from app.models.base import Base
    
    if async_engine is None:
        raise RuntimeError("Database engine not initialized")
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
