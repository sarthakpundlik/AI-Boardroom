"""
AI Boardroom — Project Memory
Long-term memory persisting across multiple sessions within a project.
"""

from __future__ import annotations


from app.core.redis import get_redis_client


class ProjectMemory:
    """Manages long-term context that persists across sessions."""

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id
        self.redis = get_redis_client()
        self.key_prefix = f"project_memory:{project_id}"

    async def store_insight(self, key: str, insight: str) -> None:
        """Store a high-level insight derived during a session."""
        await self.redis.hset(f"{self.key_prefix}:insights", key, insight)

    async def get_insights(self) -> dict:
        """Retrieve all stored insights for the project."""
        return await self.redis.hgetall(f"{self.key_prefix}:insights")

    async def add_decision(self, decision: str) -> None:
        """Log a major decision made in the project."""
        await self.redis.rpush(f"{self.key_prefix}:decisions", decision)

    async def get_decisions(self) -> list[str]:
        """Get the history of decisions."""
        return await self.redis.lrange(f"{self.key_prefix}:decisions", 0, -1)
