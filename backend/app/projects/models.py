"""
AI Boardroom — Project Model
SQLAlchemy ORM model for Projects.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import InputType, ProjectStatus
from app.database.base import Base, TimestampMixin, UUIDMixin


class Project(Base, UUIDMixin, TimestampMixin):
    """A project acts as a container for related sessions and files."""

    __tablename__ = "projects"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_type: Mapped[str] = mapped_column(String(50), default=InputType.GENERAL, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default=ProjectStatus.DRAFT, nullable=False)
    
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="projects")
    sessions = relationship("Session", back_populates="project", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, title={self.title}, status={self.status})>"
