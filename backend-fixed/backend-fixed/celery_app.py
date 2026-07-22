"""
AI Boardroom — Celery Application
Configuration for background workers.
"""

from __future__ import annotations

from celery import Celery

from app.core.config import get_settings

settings = get_settings()

# We use Redis for both broker and result backend
celery_app = Celery(
    "aiboardroom_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    # In production, discover tasks from your modules
    imports=["app.uploads.service", "app.orchestrator.graph"],
)

# Optional: Periodic task routing
celery_app.conf.beat_schedule = {
    # Example: cleanup old tokens every night
    # 'cleanup-tokens': {
    #     'task': 'app.auth.tasks.cleanup_expired_tokens',
    #     'schedule': crontab(hour=3, minute=0),
    # },
}
