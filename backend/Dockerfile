# ============================================================
# AI Boardroom — Dockerfile
# Multi-stage build for production
# ============================================================

FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# --- Dependencies Stage ---
FROM base as dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Production Stage ---
FROM base as production

COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

COPY . .

RUN adduser --disabled-password --gecos "" appuser && \
    mkdir -p /app/uploads /app/logs && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/api/v1/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
