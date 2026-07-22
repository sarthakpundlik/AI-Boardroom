"""
AI Boardroom — WebSocket Events
Event types for real-time communication.
"""

from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    """Types of real-time events broadcasted over WebSocket."""
    AGENT_STARTED = "agent_started"
    AGENT_FINISHED = "agent_finished"
    ROUND_ADVANCED = "round_advanced"
    CEO_STARTED = "ceo_started"
    SESSION_COMPLETED = "session_completed"
    ERROR = "error"


def format_event(event_type: EventType, payload: dict) -> dict:
    """Format an event for broadcasting."""
    return {
        "type": event_type.value,
        "payload": payload,
    }
