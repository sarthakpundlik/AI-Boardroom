"""
AI Boardroom — S3 Storage
S3 bucket storage backend.
"""

from __future__ import annotations

from io import BytesIO

from app.core.config import get_settings
from app.database.s3 import get_s3_client


class S3Storage:
    """S3 storage operations."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = get_s3_client()
        self.bucket = self.settings.S3_BUCKET_NAME

    async def save(self, content: bytes, object_name: str) -> str:
        """Save file to S3."""
        self.client.upload_fileobj(BytesIO(content), self.bucket, object_name)
        return f"s3://{self.bucket}/{object_name}"
