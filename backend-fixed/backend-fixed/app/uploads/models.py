"""
AI Boardroom — Uploads Models
SQLAlchemy model for uploaded documents.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin


class Document(Base, UUIDMixin, TimestampMixin):
    """An uploaded document belonging to a project."""

    __tablename__ = "documents"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(512), nullable=False)
    
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending, processed, failed
    error_message: Mapped[str | None] = mapped_column(String(512), nullable=True)

    project = relationship("Project", lazy="selectin")
    user = relationship("User", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, filename={self.filename}, status={self.status})>"
