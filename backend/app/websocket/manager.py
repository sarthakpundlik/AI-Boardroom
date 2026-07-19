"""
AI Boardroom — WebSocket Manager
Manages active WebSocket connections for real-time updates.
"""

from __future__ import annotations

import json

from fastapi import WebSocket

from app.core.logging import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    """Manages active WebSocket connections and broadcasts."""

    def __init__(self) -> None:
        # Map of session_id -> list of active WebSockets
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str) -> None:
        """Accept a new connection and track it by session_id."""
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
        logger.info("WebSocket connected", session_id=session_id)

    def disconnect(self, websocket: WebSocket, session_id: str) -> None:
        """Remove a disconnected websocket."""
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
        logger.info("WebSocket disconnected", session_id=session_id)

    async def broadcast_to_session(self, session_id: str, message: dict) -> None:
        """Send a JSON message to all clients connected to a specific session."""
        if session_id in self.active_connections:
            text_data = json.dumps(message)
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_text(text_data)
                except Exception as e:
                    logger.error("Failed to send WebSocket message", error=str(e))


manager = ConnectionManager()
