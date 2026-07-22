"""
AI Boardroom — Orchestrator Runner
Kicks off a full boardroom session as a background task: builds the
LangGraph workflow, runs it to completion, persists the final report,
and keeps the session row + WebSocket clients in sync throughout.

This is invoked from app/sessions/router.py via FastAPI BackgroundTasks
right after a session row is created, so the HTTP response returns
immediately while the (potentially multi-minute) LLM-driven discussion
runs in the background.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.core.config import get_settings
from app.core.constants import AGENT_SELECTION_MATRIX, MAX_DISCUSSION_ROUNDS, InputType, SessionStatus
from app.core.logging import get_logger
from app.database.session import async_session_factory
from app.notifications.service import NotificationService
from app.orchestrator.graph import build_boardroom_graph
from app.projects.repository import ProjectRepository
from app.reports.service import ReportService
from app.sessions.repository import SessionRepository
from app.websocket.events import EventType, format_event
from app.websocket.manager import manager

logger = get_logger(__name__)


def _friendly_error_message(exc: Exception) -> str:
    """Translate common failure modes into a message a non-engineer can act
    on; otherwise fall back to the raw exception text (still useful, just
    less polished)."""
    text = str(exc)
    lowered = text.lower()

    if "api_key" in lowered or "api key" in lowered or "authentication" in lowered:
        return (
            "The Gemini API key on the server is missing or invalid. Add a "
            "valid GEMINI_API_KEY to backend/.env, restart the backend, and "
            "start a new session."
        )
    if "rate limit" in lowered or "429" in text:
        return "The Gemini account hit a rate limit or ran out of quota. Check your Gemini billing/usage and try again."
    if "timeout" in lowered or "timed out" in lowered:
        return "The AI model took too long to respond. This is usually temporary — try starting a new session."
    if "connection" in lowered or "connect" in lowered:
        return "Couldn't reach the Gemini API from the server. Check the server's internet connection and try again."

    # Truncate defensively — raw provider errors can be very long.
    return text[:300] if text else "An unexpected error occurred while the board was deliberating."


async def _build_rag_context(project_id: str, query: str) -> str:
    """Best-effort retrieval of project context. Never blocks the run."""
    try:
        from app.rag.context import build_agent_context
        from app.rag.retriever import Retriever

        retriever = Retriever()
        docs = await retriever.retrieve_for_project(query=query, project_id=project_id)
        if not docs:
            return "No supporting documents were uploaded for this project."
        return build_agent_context(docs)
    except Exception as e:
        logger.warning("RAG retrieval unavailable, continuing without it", error=str(e))
        return "No supporting documents were uploaded for this project."


async def run_boardroom_session(session_id: str, project_id: str, user_id: str) -> None:
    """
    Runs the full boardroom workflow for a session:
    select agents -> parallel analysis rounds -> CEO synthesis -> report.
    Owns its own DB session since it runs outside the HTTP request lifecycle.
    """
    async with async_session_factory() as db:
        session_repo = SessionRepository(db)
        project_repo = ProjectRepository(db)

        session_obj = await session_repo.get_by_id(session_id)
        project = await project_repo.get_by_id(project_id)

        if not session_obj or not project:
            logger.error("Session or project vanished before orchestration could start", session_id=session_id)
            return

        try:
            input_type = InputType(project.input_type)
        except ValueError:
            input_type = InputType.GENERAL

        selected_agents = [a.value for a in AGENT_SELECTION_MATRIX.get(input_type, AGENT_SELECTION_MATRIX[InputType.GENERAL])]

        # Persist the selection and mark the session as started.
        session_obj.agents_selected = selected_agents
        session_obj.status = SessionStatus.ROUND_1
        session_obj.started_at = datetime.now(timezone.utc)
        await session_repo.update(session_obj)
        await db.commit()

        try:
            settings = get_settings()
            if not settings.GEMINI_API_KEY:
                raise RuntimeError(
                    "No Gemini API key is configured on the server. Add a real "
                    "GEMINI_API_KEY to backend/.env and restart the backend, "
                    "then start a new session."
                )

            rag_context = await _build_rag_context(project_id, project.description or project.title)

            graph = build_boardroom_graph(selected_agents)
            initial_state = {
                "session_id": session_id,
                "project_id": project_id,
                "project_description": project.description or project.title,
                "rag_context": rag_context,
                "timeline": [],
                "agent_findings": [],
                "current_round": 1,
                "max_rounds": MAX_DISCUSSION_ROUNDS,
                "selected_agents": selected_agents,
                "final_report": None,
            }

            final_state = await graph.ainvoke(initial_state)

            final_report = final_state.get("final_report")
            if not final_report:
                raise RuntimeError("The board did not produce a final report.")

            full_content = {
                **final_report,
                "agent_findings": list(final_state.get("agent_findings", [])),
            }

            report_service = ReportService(db)
            report = await report_service.create_report(
                session_id=session_id, project_id=project_id, user_id=user_id, ceo_output=full_content
            )

            session_obj.status = SessionStatus.COMPLETED
            session_obj.round_count = MAX_DISCUSSION_ROUNDS
            session_obj.completed_at = datetime.now(timezone.utc)
            await session_repo.update(session_obj)

            notification_service = NotificationService(db)
            await notification_service.create_notification(
                user_id=user_id,
                title="Boardroom session complete",
                message=f"The board has reached a decision on '{project.title}'.",
                type_="session_completed",
                reference_id=report.id,
            )

            await db.commit()

            await manager.broadcast_to_session(
                session_id,
                format_event(EventType.SESSION_COMPLETED, {"report_id": report.id, "session_id": session_id}),
            )

        except Exception as e:
            error_message = _friendly_error_message(e)
            logger.error("Boardroom session failed", session_id=session_id, error=str(e))
            await db.rollback()

            async with async_session_factory() as fail_db:
                fail_session_repo = SessionRepository(fail_db)
                fail_session_obj = await fail_session_repo.get_by_id(session_id)
                if fail_session_obj:
                    fail_session_obj.status = SessionStatus.FAILED
                    await fail_session_repo.update(fail_session_obj)

                notification_service = NotificationService(fail_db)
                await notification_service.create_notification(
                    user_id=user_id,
                    title="Boardroom session failed",
                    message=f"'{project.title}' couldn't complete: {error_message}",
                    type_="session_failed",
                    reference_id=session_id,
                )
                await fail_db.commit()

            await manager.broadcast_to_session(
                session_id,
                format_event(EventType.ERROR, {"message": error_message}),
            )
