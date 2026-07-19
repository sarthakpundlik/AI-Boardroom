"""
AI Boardroom — S3 Storage Client
Manages AWS S3 (or S3-compatible) object storage for file uploads and reports.
"""

from __future__ import annotations

import boto3
from botocore.config import Config as BotoConfig

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_s3_client = None


def get_s3_client():
    """Get or create the S3 client singleton."""
    global _s3_client
    if _s3_client is None:
        settings = get_settings()
        config = BotoConfig(
            region_name=settings.AWS_REGION,
            retries={"max_attempts": 3, "mode": "adaptive"},
        )
        kwargs = {
            "service_name": "s3",
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID or None,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY or None,
            "config": config,
        }
        if settings.S3_ENDPOINT_URL:
            kwargs["endpoint_url"] = settings.S3_ENDPOINT_URL

        _s3_client = boto3.client(**kwargs)
        logger.info("S3 client initialized", region=settings.AWS_REGION)
    return _s3_client


def generate_presigned_url(
    key: str,
    expiration: int = 3600,
    bucket: str | None = None,
) -> str:
    """Generate a presigned URL for secure file access."""
    settings = get_settings()
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": bucket or settings.S3_BUCKET_NAME,
            "Key": key,
        },
        ExpiresIn=expiration,
    )
