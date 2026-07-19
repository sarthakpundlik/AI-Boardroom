"""
AI Boardroom — Database Seeder
Seeds initial data for development and testing.
"""

from __future__ import annotations

from app.core.constants import UserRole
from app.core.logging import get_logger
from app.core.security import hash_password
from app.database.session import async_session_factory
from app.users.models import User

logger = get_logger(__name__)


async def seed_admin_user() -> None:
    """Create a default admin user if none exists."""
    from sqlalchemy import select

    async with async_session_factory() as session:
        result = await session.execute(
            select(User).where(User.role == UserRole.ADMIN).limit(1)
        )
        existing = result.scalar_one_or_none()

        if existing is None:
            admin = User(
                email="admin@aiboardroom.com",
                name="Admin",
                hashed_password=hash_password("Admin@123!"),
                role=UserRole.ADMIN,
                is_active=True,
                oauth_provider="email",
            )
            session.add(admin)
            await session.commit()
            logger.info("Default admin user created", email=admin.email)
        else:
            logger.info("Admin user already exists, skipping seed")


async def run_seeds() -> None:
    """Run all database seeds."""
    logger.info("Running database seeds...")
    await seed_admin_user()
    logger.info("Database seeding complete")
