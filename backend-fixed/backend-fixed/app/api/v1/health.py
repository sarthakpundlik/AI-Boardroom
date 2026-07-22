"""
AI Boardroom — Health Check Endpoint
System health verification for load balancers, Kubernetes probes, and monitoring.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(settings: Settings = Depends(get_settings)):
    """
    Basic health check — always responds if the API is up.
    Used by Docker HEALTHCHECK, Kubernetes liveness probe, and load balancers.
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check — verifies all downstream services are accessible.
    Used by Kubernetes readiness probe.
    """
    checks: dict[str, str] = {}

    # Check PostgreSQL
    try:
        from app.database.session import async_session_factory
        from sqlalchemy import text

        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
        checks["postgres"] = "connected"
    except Exception as e:
        checks["postgres"] = f"error: {str(e)[:100]}"

    # Check Redis
    try:
        import redis.asyncio as aioredis

        from app.core.config import get_settings

        settings = get_settings()
        r = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        await r.ping()
        await r.aclose()
        checks["redis"] = "connected"
    except Exception as e:
        checks["redis"] = f"error: {str(e)[:100]}"

    # Check Qdrant
    try:
        from qdrant_client import QdrantClient

        settings = get_settings()
        client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        client.get_collections()
        client.close()
        checks["qdrant"] = "connected"
    except Exception as e:
        checks["qdrant"] = f"error: {str(e)[:100]}"

    all_healthy = all("error" not in v for v in checks.values())

    return {
        "status": "ready" if all_healthy else "degraded",
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
