"""
AI Boardroom — Session Memory
Short-term memory tracking current session context.

Redis is treated as a best-effort cache here, not a hard dependency:
if it's unreachable (e.g. not running in local dev), every method
degrades gracefully instead of crashing the boardroom run.
"""

from __future__ import annotations

import json

from app.core.logging import get_logger
from app.core.redis import get_redis_client

logger = get_logger(__name__)


class SessionMemory:
    """Manages short-term memory specific to the current discussion round."""

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        self.redis = get_redis_client()
        self.key_prefix = f"session_memory:{session_id}"

    async def add_message(self, agent_name: str, message: str) -> None:
        """Add a message to the session timeline."""
        try:
            entry = json.dumps({"agent": agent_name, "message": message})
            await self.redis.rpush(f"{self.key_prefix}:timeline", entry)  # type: ignore
        except Exception as e:
            logger.warning("SessionMemory.add_message unavailable (Redis down?)", error=str(e))

    async def get_timeline(self) -> list[dict[str, str]]:
        """Retrieve the ordered discussion timeline."""
        try:
            entries = await self.redis.lrange(f"{self.key_prefix}:timeline", 0, -1)  # type: ignore
            return [json.loads(e) for e in entries]
        except Exception as e:
            logger.warning("SessionMemory.get_timeline unavailable (Redis down?)", error=str(e))
            return []

    async def clear(self) -> None:
        """Clear the session timeline."""
        try:
            await self.redis.delete(f"{self.key_prefix}:timeline")  # type: ignore
        except Exception as e:
            logger.warning("SessionMemory.clear unavailable (Redis down?)", error=str(e))
