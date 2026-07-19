"""
AI Boardroom — Async Database Session Factory
Provides SQLAlchemy async engine and session for PostgreSQL.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

# Async engine with connection pool
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG and not settings.is_production,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Create all tables. Use Alembic for production migrations."""
    from app.database.base import Base

    # Import all models so they register with Base.metadata
    import app.auth.models  # noqa: F401
    import app.users.models  # noqa: F401
    import app.projects.models  # noqa: F401
    import app.sessions.models  # noqa: F401
    import app.uploads.models  # noqa: F401
    import app.reports.models  # noqa: F401
    import app.notifications.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Dispose the engine and close all connections."""
    await engine.dispose()
