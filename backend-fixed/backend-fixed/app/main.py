"""
AI Boardroom — Main Application Entry Point
Wires up all routers, middleware, and startup events.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import health, metrics
from app.auth import router as auth_router
from app.core.config import get_settings
from app.core.exceptions import setup_exception_handlers
from app.core.logging import setup_logging
from app.database.session import init_db
from app.database.qdrant import init_qdrant_collections
from app.database.seed import run_seeds
from app.notifications import router as notifications_router
from app.projects import router as projects_router
from app.reports import router as reports_router
from app.sessions import router as sessions_router
from app.uploads import router as uploads_router
from app.users import router as users_router
from app.websocket import router as ws_router

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for startup and shutdown."""
    setup_logging()
    logger.info("Starting AI Boardroom Application...")
    
    # Init DB
    await init_db()
    await run_seeds()
    
    # Init Vector DB (optional — skip if Qdrant is unavailable)
    try:
        await init_qdrant_collections()
    except Exception as e:
        logger.warning("Qdrant initialization skipped (service unavailable): %s", e)

    if not get_settings().OPENAI_API_KEY:
        logger.warning(
            "OPENAI_API_KEY is not set in backend/.env — every boardroom "
            "session will fail as soon as an agent tries to call the LLM. "
            "Add a real key and restart the server before creating a session."
        )

    yield
    
    logger.info("Shutting down AI Boardroom Application...")


def create_app() -> FastAPI:
    """Factory to create the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handlers
    setup_exception_handlers(app)

    # Serve locally-stored files (report PDFs, uploads) when not using S3.
    # Without this, StorageManager's local file paths (e.g. report.pdf_url)
    # are unreachable from the browser.
    if not (settings.AWS_ACCESS_KEY_ID and settings.S3_BUCKET_NAME):
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        app.mount("/media", StaticFiles(directory=settings.UPLOAD_DIR), name="media")

    # Register Routers
    
    app.include_router(health.router, prefix="/api/v1")
    app.include_router(metrics.router, prefix="/api/v1")
    
    app.include_router(auth_router.router, prefix="/api/v1")
    app.include_router(users_router.router, prefix="/api/v1")
    app.include_router(projects_router.router, prefix="/api/v1")
    app.include_router(uploads_router.router, prefix="/api/v1")
    app.include_router(sessions_router.router, prefix="/api/v1")
    app.include_router(reports_router.router, prefix="/api/v1")
    app.include_router(notifications_router.router, prefix="/api/v1")
    
    # WebSockets attached at root for cleaner connection strings
    app.include_router(ws_router.router)

    return app


app = create_app()
