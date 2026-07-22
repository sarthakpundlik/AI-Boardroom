"""
AI Boardroom — Upload Validator
Validates file sizes and MIME types.
"""

from __future__ import annotations

import magic
from fastapi import UploadFile

from app.core.constants import ALLOWED_MIME_TYPES, MAX_FILE_SIZE_BYTES
from app.core.exceptions import FileSizeExceededError, UnsupportedFileTypeError


async def validate_upload(file: UploadFile) -> str:
    """
    Validate the uploaded file size and MIME type.
    Returns the detected MIME type.
    """
    # Check size by reading to end, then seeking back
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE_BYTES:
        raise FileSizeExceededError()

    # Read first 2048 bytes for magic number detection
    header = await file.read(2048)
    await file.seek(0)
    
    mime_type = magic.from_buffer(header, mime=True)
    
    if mime_type not in ALLOWED_MIME_TYPES:
        # Some OS/python-magic versions return text/plain for CSV, so fallback
        if file.filename and file.filename.endswith(".csv"):
            mime_type = "text/csv"
        else:
            raise UnsupportedFileTypeError(mime_type)

    return mime_type
