"""
AI Boardroom — Notification Service
Handles creation and retrieval of notifications.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.notifications.models import Notification


class NotificationService:
    """Service layer for in-app notifications."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_notification(
        self, user_id: str, title: str, message: str, type_: str, reference_id: str | None = None
    ) -> Notification:
        """Create a new notification for a user."""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type_,
            reference_id=reference_id,
        )
        self.session.add(notification)
        await self.session.flush()
        await self.session.refresh(notification)
        return notification

    async def list_notifications(
        self, user_id: str, page: int = 1, per_page: int = 20
    ) -> tuple[list[Notification], int, int]:
        """List user's notifications, along with total and unread counts."""
        query = select(Notification).where(Notification.user_id == user_id)

        # Total count
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.session.execute(count_query)).scalar() or 0

        # Unread count
        unread_query = select(func.count()).select_from(
            select(Notification).where(Notification.user_id == user_id, Notification.is_read == False).subquery() # noqa: E712
        )
        unread = (await self.session.execute(unread_query)).scalar() or 0

        # Paginated results
        query = query.order_by(Notification.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        notifications = list((await self.session.execute(query)).scalars().all())

        return notifications, total, unread

    async def mark_as_read(self, notification_id: str, user_id: str) -> Notification:
        """Mark a specific notification as read."""
        result = await self.session.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
        )
        notification = result.scalar_one_or_none()
        if not notification:
            raise NotFoundError("Notification", notification_id)
            
        notification.is_read = True
        await self.session.flush()
        return notification

    async def mark_all_as_read(self, user_id: str) -> int:
        """Mark all notifications as read for a user."""
        result = await self.session.execute(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read == False # noqa: E712
            )
        )
        count = 0
        for notification in result.scalars():
            notification.is_read = True
            count += 1
        await self.session.flush()
        return count
