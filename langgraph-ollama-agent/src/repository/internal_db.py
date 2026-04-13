import json
import os
from src.core.config import settings

class InternalDB:
    def search(self, query: str):
        if not os.path.exists(settings.DATABASE_PATH):
            return None
        with open(settings.DATABASE_PATH, "r") as f:
            data = json.load(f)
        for record in data.get("records", []):
            if record["topic"].lower() in query.lower():
                return record["content"]
        return None