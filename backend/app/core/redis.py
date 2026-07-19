"""
AI Boardroom — Redis Configuration
Redis client for caching, Celery backend, and memory management.
"""

from __future__ import annotations

import redis.asyncio as redis

from app.core.config import get_settings

_redis_client = None


def get_redis_client() -> redis.Redis:
    """Get or create the Redis connection pool."""
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client
