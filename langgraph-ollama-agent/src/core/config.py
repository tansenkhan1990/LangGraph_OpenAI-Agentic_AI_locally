import os
import logging
from pydantic import BaseModel, field_validator, AnyHttpUrl
from dotenv import load_dotenv
from agents import set_tracing_disabled

# ─── 1. Global Logging (Production-Grade) ────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("CorporateHub")

# ─── 2. Disable OpenAI Telemetry ─────────────────────────────────────────────
set_tracing_disabled(True)

# ─── 3. Load Environment Variables ───────────────────────────────────────────
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(ROOT_DIR, ".env"))


# ─── 4. Validated Settings (Pydantic BaseModel) ──────────────────────────────
class Settings(BaseModel):
    """
    Production-grade settings object.
    Validated at startup — if any critical value is misconfigured,
    the application will fail fast with a clear error message.
    """
    BASE_URL: str = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
    API_KEY: str = os.getenv("OPENAI_API_KEY", "ollama")
    MODEL: str = os.getenv("LOCAL_MODEL_NAME", "qwen3-vl:235b-cloud")
    DATABASE_PATH: str = os.path.join(ROOT_DIR, os.getenv("DATABASE_PATH", "data/knowledge.json"))

    @field_validator("BASE_URL")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError(f"OPENAI_BASE_URL must be a valid HTTP/HTTPS URL. Got: '{v}'")
        return v

    @field_validator("API_KEY")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("OPENAI_API_KEY cannot be empty.")
        return v.strip()

    @field_validator("MODEL")
    @classmethod
    def validate_model(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("LOCAL_MODEL_NAME cannot be empty.")
        return v.strip()


# ─── 5. Instantiate & Validate at Startup ────────────────────────────────────
try:
    settings = Settings()
    logger.info(f"✅ Settings validated: model={settings.MODEL}, db={settings.DATABASE_PATH}")
except Exception as e:
    logger.critical(f"❌ STARTUP FAILED: Invalid configuration — {e}")
    raise SystemExit(1)  # Fail fast in production