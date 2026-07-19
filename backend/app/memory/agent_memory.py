"""
AI Boardroom — Agent Memory
Private scratchpad memory for individual agents.
"""

from __future__ import annotations

from app.core.redis import get_redis_client


class AgentMemory:
    """Manages isolated private memory for a specific agent during a session."""

    def __init__(self, session_id: str, agent_name: str) -> None:
        self.session_id = session_id
        self.agent_name = agent_name
        self.redis = get_redis_client()
        self.key_prefix = f"agent_memory:{session_id}:{agent_name}"

    async def set_scratchpad(self, notes: str) -> None:
        """Update the agent's private scratchpad."""
        await self.redis.set(f"{self.key_prefix}:scratchpad", notes)

    async def get_scratchpad(self) -> str | None:
        """Retrieve the agent's private scratchpad."""
        return await self.redis.get(f"{self.key_prefix}:scratchpad")

    async def clear(self) -> None:
        """Clear the agent's memory for this session."""
        keys = await self.redis.keys(f"{self.key_prefix}:*")
        if keys:
            await self.redis.delete(*keys)
