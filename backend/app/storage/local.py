"""
AI Boardroom — Local Storage
Local file system storage backend.
"""

from __future__ import annotations

import os

from app.core.config import get_settings


class LocalStorage:
    """Local file system operations."""

    def __init__(self) -> None:
        self.upload_dir = get_settings().UPLOAD_DIR

    async def save(self, content: bytes, filename: str) -> str:
        """Save file locally."""
        full_path = os.path.join(self.upload_dir, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(content)
        return full_path
