"""
AI Boardroom — Auth Models
SQLAlchemy ORM models for authentication data (e.g., Refresh Tokens).
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin


class RefreshToken(Base, UUIDMixin, TimestampMixin):
    """Stores valid refresh tokens for session management and revocation."""

    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(Text, unique=True, index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    device_info: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user = relationship("User", lazy="selectin")

    def __repr__(self) -> str:
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.is_revoked})>"
