"""
AI Boardroom — Report Models
SQLAlchemy models for final generated reports.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin


class Report(Base, UUIDMixin, TimestampMixin):
    """A final generated report from a boardroom session."""

    __tablename__ = "reports"

    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    full_content: Mapped[dict] = mapped_column(JSONB, nullable=False)  # CEO output dump
    
    pdf_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    session = relationship("Session", lazy="selectin")
    project = relationship("Project", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Report(id={self.id}, project_id={self.project_id})>"
