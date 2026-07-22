"""
AI Boardroom — Agent Tools
Custom tools provided to agents (e.g., Web Search).
"""

from __future__ import annotations

from langchain_core.tools import tool

from app.core.logging import get_logger

logger = get_logger(__name__)


@tool
def search_internal_database(query: str) -> str:
    """Search the company's internal database for relevant metrics or history."""
    logger.info("Tool called: search_internal_database", query=query)
    # Placeholder for actual DB search if needed beyond RAG
    return f"Results for '{query}': No additional historical data found."


def get_agent_tools() -> list:
    """Return the list of tools available to agents."""
    return [search_internal_database]
