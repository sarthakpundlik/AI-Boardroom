"""
AI Boardroom — WebSocket Router
Endpoints for establishing WebSocket connections.
"""

from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from app.auth.jwt_handler import decode_access_token
from app.core.logging import get_logger
from app.database.session import async_session_factory
from app.sessions.repository import SessionRepository
from app.websocket.manager import manager

logger = get_logger(__name__)
router = APIRouter(prefix="/ws", tags=["WebSockets"])


@router.websocket("/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, token: str | None = None):
    """
    WebSocket endpoint for a specific boardroom session.
    Clients connect here to receive real-time updates as agents converse.

    Auth: the frontend appends the access token as a query param
    (?token=...), since browsers can't set custom headers on the
    WebSocket handshake. The token must decode to a user who owns the
    project the session belongs to.
    """
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing auth token")
        return

    payload = decode_access_token(token)
    if not payload or not payload.get("sub"):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or expired token")
        return

    user_id = payload["sub"]

    async with async_session_factory() as db:
        session_obj = await SessionRepository(db).get_by_id(session_id)

    if not session_obj:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Session not found")
        return

    if session_obj.project.user_id != user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Not authorized for this session")
        return

    await manager.connect(websocket, session_id)
    try:
        while True:
            # We mainly push data to the client.
            # We can listen for pings or control messages if needed.
            data = await websocket.receive_text()
            logger.debug("Received WS message", session_id=session_id, data=data)

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
