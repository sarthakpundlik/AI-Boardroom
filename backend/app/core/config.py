"""
AI Boardroom — Core Configuration
Centralized settings management using pydantic-settings.
All environment variables are loaded and validated here.
"""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    APP_NAME: str = "AI Boardroom"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    LOG_LEVEL: str = "info"

    # --- PostgreSQL ---
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "ai_boardroom"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "ai_boardroom"
    DATABASE_URL: str = "postgresql+asyncpg://ai_boardroom:password@localhost:5432/ai_boardroom"

    # --- Redis ---
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- Qdrant ---
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "ai_boardroom_docs"

    # --- JWT ---
    JWT_SECRET_KEY: str = "change-this-to-a-secure-random-string-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- OAuth 2.0 ---
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_CLIENT_SECRET: str = ""
    MICROSOFT_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/microsoft/callback"

    # --- AI Providers ---
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_PRIMARY: str = "gpt-4o"
    OPENAI_MODEL_ECONOMY: str = "gpt-4o-mini"
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # --- AWS S3 ---
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "ai-boardroom-uploads"
    S3_ENDPOINT_URL: str = ""

    # --- Email ---
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@aiboardroom.com"
    SMTP_FROM_NAME: str = "AI Boardroom"

    # --- Celery ---
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # --- File Upload ---
    MAX_FILE_SIZE_MB: int = 50
    MAX_SESSION_SIZE_MB: int = 200
    UPLOAD_DIR: str = "./uploads"

    # --- Rate Limiting ---
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.strip("[]").split(",")]
        return v

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def sync_database_url(self) -> str:
        """Synchronous database URL for Alembic migrations."""
        return self.DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance — loaded once per process."""
    return Settings()
