"""
AI Boardroom — Session Model
SQLAlchemy ORM model for Boardroom Sessions.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import SessionStatus
from app.database.base import Base, TimestampMixin, UUIDMixin


class Session(Base, UUIDMixin, TimestampMixin):
    """A boardroom session where agents analyze input."""

    __tablename__ = "sessions"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default=SessionStatus.PENDING, nullable=False)
    round_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    agents_selected: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="sessions", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, project_id={self.project_id}, status={self.status})>"
