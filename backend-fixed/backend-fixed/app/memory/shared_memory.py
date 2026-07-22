"""
AI Boardroom — Shared Memory
Global/Shared memory across all agents in a session.
"""

from __future__ import annotations

import json

from app.core.redis import get_redis_client


class SharedMemory:
    """Manages state shared across all agents in a single boardroom session."""

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        self.redis = get_redis_client()
        self.key_prefix = f"shared_memory:{session_id}"

    async def set(self, key: str, value: dict | str | list) -> None:
        """Store a value in shared memory."""
        await self.redis.set(f"{self.key_prefix}:{key}", json.dumps(value))

    async def get(self, key: str) -> dict | str | list | None:
        """Retrieve a value from shared memory."""
        data = await self.redis.get(f"{self.key_prefix}:{key}")
        if data:
            return json.loads(data)
        return None

    async def clear_all(self) -> None:
        """Clear all shared memory for this session."""
        keys = await self.redis.keys(f"{self.key_prefix}:*")
        if keys:
            await self.redis.delete(*keys)
