import os
from dotenv import load_dotenv
from agents import set_tracing_disabled

# Disable OpenAI automatic tracing telemetry
set_tracing_disabled(True)

# Load root .env
load_dotenv()

class Settings:
    def __init__(self):
        self.BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
        self.API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
        self.MODEL = os.getenv("LOCAL_MODEL_NAME", "qwen2.5-coder:1.5b")
        
        # Absolute path resolution relative to the root project directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.DATABASE_PATH = os.path.join(base_dir, "data", "knowledge.json")

settings = Settings()