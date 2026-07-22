"""
AI Boardroom — File Parser
Handles structured data parsing (JSON, CSV, etc).
"""

from __future__ import annotations

import json
from io import BytesIO

import pandas as pd

from app.core.logging import get_logger

logger = get_logger(__name__)


def parse_structured_data(file_content: bytes, mime_type: str, filename: str) -> dict | list | str:
    """Parse structured data into standard dicts or lists for agent analysis."""
    try:
        if mime_type == "application/json":
            return json.loads(file_content.decode("utf-8"))
        elif mime_type == "text/csv" or filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(file_content))
            return df.to_dict(orient="records")
        elif mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(BytesIO(file_content))
            return df.to_dict(orient="records")
    except Exception as e:
        logger.error("Failed to parse structured data", filename=filename, error=str(e))
        return "Failed to parse data"
        
    return "Unstructured"
