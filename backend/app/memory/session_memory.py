"""
AI Boardroom — Session Memory
Short-term memory tracking current session context.
"""

from __future__ import annotations

import json

from app.core.redis import get_redis_client


class SessionMemory:
    """Manages short-term memory specific to the current discussion round."""

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        self.redis = get_redis_client()
        self.key_prefix = f"session_memory:{session_id}"

    async def add_message(self, agent_name: str, message: str) -> None:
        """Add a message to the session timeline."""
        entry = json.dumps({"agent": agent_name, "message": message})
        await self.redis.rpush(f"{self.key_prefix}:timeline", entry)

    async def get_timeline(self) -> list[dict]:
        """Retrieve the ordered discussion timeline."""
        entries = await self.redis.lrange(f"{self.key_prefix}:timeline", 0, -1)
        return [json.loads(e) for e in entries]

    async def clear(self) -> None:
        """Clear the session timeline."""
        await self.redis.delete(f"{self.key_prefix}:timeline")
