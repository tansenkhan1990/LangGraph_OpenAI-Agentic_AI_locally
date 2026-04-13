import json
import os
from typing import Optional
from pydantic import BaseModel, Field
from src.core.config import settings, logger


class KnowledgeRecord(BaseModel):
    """Typed representation of a single internal knowledge record."""
    topic: str = Field(..., description="The topic keyword for this record.")
    content: str = Field(..., min_length=5, description="The actual information stored.")


class InternalDB:
    """
    Typed, validated access layer for the local JSON knowledge base.
    - Validates file existence at query time.
    - Deserializes records into typed KnowledgeRecord objects.
    - Returns Optional[str] — None if no match found.
    """

    def search(self, query: str) -> Optional[str]:
        if not os.path.exists(settings.DATABASE_PATH):
            logger.warning(f"Knowledge base not found at: {settings.DATABASE_PATH}")
            return None

        try:
            with open(settings.DATABASE_PATH, "r") as f:
                raw = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in knowledge base: {e}")
            return None

        records = raw.get("records", [])
        for item in records:
            try:
                record = KnowledgeRecord(**item)  # Validate each record at read time
                if record.topic.lower() in query.lower():
                    logger.info(f"DB hit on topic: '{record.topic}'")
                    return record.content
            except Exception as e:
                logger.warning(f"Skipping malformed record {item}: {e}")
                continue

        return None