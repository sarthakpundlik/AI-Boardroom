"""
AI Boardroom — WebSocket Router
Endpoints for establishing WebSocket connections.
"""

from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.logging import get_logger
from app.websocket.manager import manager

logger = get_logger(__name__)
router = APIRouter(prefix="/ws", tags=["WebSockets"])


@router.websocket("/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for a specific boardroom session.
    Clients connect here to receive real-time updates as agents converse.
    """
    # Note: In a production app, we should also authenticate the WebSocket connection.
    # Often done by passing a token in the initial request URL or headers, or first WS frame.
    
    await manager.connect(websocket, session_id)
    try:
        while True:
            # We mainly push data to the client.
            # We can listen for pings or control messages if needed.
            data = await websocket.receive_text()
            logger.debug("Received WS message", session_id=session_id, data=data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
