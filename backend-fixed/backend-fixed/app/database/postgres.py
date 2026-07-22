"""
AI Boardroom — PostgreSQL Utilities
Database initialization, connection testing, and migration helpers.
"""

from __future__ import annotations

from sqlalchemy import text

from app.core.logging import get_logger
from app.database.session import async_session_factory

logger = get_logger(__name__)


async def check_postgres_connection() -> bool:
    """Test PostgreSQL connectivity."""
    try:
        async with async_session_factory() as session:
            result = await session.execute(text("SELECT 1"))
            row = result.scalar()
            if row == 1:
                logger.info("PostgreSQL connection verified")
                return True
    except Exception as e:
        logger.error("PostgreSQL connection failed", error=str(e))
    return False


async def get_table_count() -> dict[str, int]:
    """Get row counts for all application tables."""
    tables = [
        "users", "projects", "sessions", "documents",
        "reports", "notifications"
    ]
    counts: dict[str, int] = {}

    try:
        async with async_session_factory() as session:
            for table in tables:
                try:
                    result = await session.execute(
                        text(f"SELECT COUNT(*) FROM {table}")  # noqa: S608
                    )
                    counts[table] = result.scalar() or 0
                except Exception:
                    counts[table] = -1  # Table may not exist yet
    except Exception as e:
        logger.error("Failed to get table counts", error=str(e))

    return counts
