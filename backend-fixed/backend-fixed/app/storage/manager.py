"""
AI Boardroom — Storage Manager
Facade for local or S3 storage backends.
"""

from __future__ import annotations

import os
from io import BytesIO

from app.core.config import get_settings
from app.core.logging import get_logger
from app.database.s3 import get_s3_client

logger = get_logger(__name__)


class StorageManager:
    """Manages file storage, abstracting local vs S3."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.use_s3 = bool(self.settings.AWS_ACCESS_KEY_ID and self.settings.S3_BUCKET_NAME)
        
        if not self.use_s3:
            os.makedirs(self.settings.UPLOAD_DIR, exist_ok=True)

    async def save_file(self, file_content: bytes, destination_path: str) -> str:
        """Save a file to the active storage backend. Returns the access URI/path."""
        if self.use_s3:
            return await self._save_s3(file_content, destination_path)
        return await self._save_local(file_content, destination_path)

    async def _save_local(self, file_content: bytes, destination_path: str) -> str:
        full_path = os.path.join(self.settings.UPLOAD_DIR, destination_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Use simple sync write here (could be async with aiofiles if needed)
        with open(full_path, "wb") as f:
            f.write(file_content)
            
        logger.info("File saved locally", path=full_path)
        # Web-accessible path — served by the StaticFiles mount registered in
        # main.py (`/media` -> UPLOAD_DIR). A bare filesystem path or a
        # local:// URI isn't something a browser can ever fetch.
        return f"/media/{destination_path}"

    async def _save_s3(self, file_content: bytes, destination_path: str) -> str:
        client = get_s3_client()
        bucket = self.settings.S3_BUCKET_NAME
        
        # S3 client is synchronous, so in a high-load app this would be wrapped in run_in_threadpool
        client.upload_fileobj(
            BytesIO(file_content),
            bucket,
            destination_path
        )
        
        logger.info("File saved to S3", bucket=bucket, key=destination_path)
        return f"s3://{bucket}/{destination_path}"
