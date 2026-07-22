"""
AI Boardroom — Agent Memory
Private scratchpad memory for individual agents.

Redis is treated as a best-effort cache here, not a hard dependency:
if it's unreachable (e.g. not running in local dev), every method
degrades gracefully instead of crashing the boardroom run.
"""

from __future__ import annotations

from app.core.logging import get_logger
from app.core.redis import get_redis_client

logger = get_logger(__name__)


class AgentMemory:
    """Manages isolated private memory for a specific agent during a session."""

    def __init__(self, session_id: str, agent_name: str) -> None:
        self.session_id = session_id
        self.agent_name = agent_name
        self.redis = get_redis_client()
        self.key_prefix = f"agent_memory:{session_id}:{agent_name}"

    async def set_scratchpad(self, notes: str) -> None:
        """Update the agent's private scratchpad."""
        try:
            await self.redis.set(f"{self.key_prefix}:scratchpad", notes)
        except Exception as e:
            logger.warning("AgentMemory.set_scratchpad unavailable (Redis down?)", error=str(e))

    async def get_scratchpad(self) -> str | None:
        """Retrieve the agent's private scratchpad."""
        try:
            return await self.redis.get(f"{self.key_prefix}:scratchpad")
        except Exception as e:
            logger.warning("AgentMemory.get_scratchpad unavailable (Redis down?)", error=str(e))
            return None

    async def clear(self) -> None:
        """Clear the agent's memory for this session."""
        try:
            keys = await self.redis.keys(f"{self.key_prefix}:*")
            if keys:
                await self.redis.delete(*keys)
        except Exception as e:
            logger.warning("AgentMemory.clear unavailable (Redis down?)", error=str(e))
