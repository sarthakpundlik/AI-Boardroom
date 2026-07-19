"""
AI Boardroom — Main Application Entry Point
Wires up all routers, middleware, and startup events.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health, metrics
from app.auth import router as auth_router
from app.core.config import get_settings
from app.core.exceptions import setup_exception_handlers
from app.core.logging import setup_logging
from app.database.postgres import create_tables
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
    await create_tables()
    await run_seeds()
    
    # Init Vector DB
    init_qdrant_collections()
    
    yield
    
    logger.info("Shutting down AI Boardroom Application...")


def create_app() -> FastAPI:
    """Factory to create the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
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
