"""
AI Boardroom — Metrics
Exposes internal monitoring metrics (Prometheus ready).
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

# For a production app, we would use prometheus_client to track actual counters/gauges.
# For now, we expose a dummy /metrics endpoint that tools like Prometheus can scrape.

router = APIRouter(prefix="/metrics", tags=["Monitoring"])


@router.get("", response_class=PlainTextResponse)
async def get_metrics():
    """Return application metrics in Prometheus text format."""
    # Example placeholder metrics
    metrics_data = [
        "# HELP aiboardroom_requests_total Total number of HTTP requests.",
        "# TYPE aiboardroom_requests_total counter",
        "aiboardroom_requests_total 100",
        "",
        "# HELP aiboardroom_active_sessions Active boardroom sessions.",
        "# TYPE aiboardroom_active_sessions gauge",
        "aiboardroom_active_sessions 5",
        "",
        "# HELP aiboardroom_documents_processed Total documents successfully processed.",
        "# TYPE aiboardroom_documents_processed counter",
        "aiboardroom_documents_processed 42",
    ]
    
    return "\n".join(metrics_data)
