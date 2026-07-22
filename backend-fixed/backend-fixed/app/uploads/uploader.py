"""
AI Boardroom — Uploader Coordination
Coordinates validation, storage, and database tracking for uploads.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from fastapi import UploadFile

from app.storage.manager import StorageManager
from app.uploads.validator import validate_upload


class Uploader:
    """Coordinates the upload process."""

    def __init__(self) -> None:
        self.storage_manager = StorageManager()

    async def handle_upload(self, file: UploadFile, project_id: str) -> tuple[str, str, int, bytes]:
        """
        Validates the file, saves it to storage, and returns metadata.
        Returns: (storage_path, mime_type, file_size, file_content)
        """
        # Validate and get MIME type
        mime_type = await validate_upload(file)
        
        # Read content
        await file.seek(0)
        content = await file.read()
        file_size = len(content)
        
        # Generate unique storage path
        timestamp = datetime.now().strftime("%Y%m%d")
        unique_id = str(uuid.uuid4())[:8]
        safe_filename = file.filename.replace(" ", "_") if file.filename else "unnamed_file"
        destination_path = f"projects/{project_id}/{timestamp}_{unique_id}_{safe_filename}"
        
        # Save file to storage
        storage_path = await self.storage_manager.save_file(content, destination_path)
        
        return storage_path, mime_type, file_size, content
