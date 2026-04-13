import os
import logging
from dotenv import load_dotenv
from agents import set_tracing_disabled

# 1. Global Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("CorporateHub")

# 2. Disable OpenAI automatic tracing telemetry
set_tracing_disabled(True)

# 3. Load Environment Variables
# Using absolute path to find .env in project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

class Settings:
    BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
    API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
    MODEL = os.getenv("LOCAL_MODEL_NAME", "qwen3-vl:235b-cloud")
    DATABASE_PATH = os.path.join(ROOT_DIR, os.getenv("DATABASE_PATH", "data/knowledge.json"))

settings = Settings()