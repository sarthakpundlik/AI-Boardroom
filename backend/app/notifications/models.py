"""
AI Boardroom — Notification Models
SQLAlchemy models for in-app notifications.
"""

from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class Notification(Base, UUIDMixin, TimestampMixin):
    """An in-app notification for a user."""

    __tablename__ = "notifications"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., session_complete, report_ready, mention
    reference_id: Mapped[str | None] = mapped_column(String(36), nullable=True)  # ID of related entity
    
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, user_id={self.user_id}, read={self.is_read})>"
