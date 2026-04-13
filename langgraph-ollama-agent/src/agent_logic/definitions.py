from openai import OpenAI
from agents import Agent
from src.core.config import settings
from src.core.state import CorporateMemo, AuditReview
from src.tools.web_tools import web_search_tool

# Initialize OpenAI client 
client = OpenAI(base_url=settings.BASE_URL, api_key=settings.API_KEY)

# 1. Specialists
librarian = Agent(
    name="Librarian",
    model=settings.MODEL,
    instructions=(
        "You are the Corporate Librarian. You specialize in internal company data. "
        "Use the provided context to answer accurately."
    )
)

scholar = Agent(
    name="Scholar",
    model=settings.MODEL,
    instructions=(
        "You are the External Scholar. You specialize in public web trends. "
        "Use the web_search_tool via the SearchConfig object."
    ),
    tools=[web_search_tool]
)

# 2. Support agents
synthesizer = Agent(
    name="Synthesizer",
    model=settings.MODEL,
    instructions=(
        "You are a raw JSON data generator. Your task is to output a CorporateMemo object. "
        "MANDATORY: You must use these EXACT JSON keys: 'title', 'sender', 'body', 'sources_used'. "
        "Do NOT use 'content'—use 'body'. "
        "IMPORTANT: If there are no sources, use an empty list [] - NEVER use an empty string. "
        "Return ONLY the raw JSON object without any Markdown formatting or extra text."
    ),
    output_type=CorporateMemo
)

auditor = Agent(
    name="Auditor",
    model=settings.MODEL,
    instructions=(
        "You are a strict data validation agent. "
        "MANDATORY: You must use these EXACT JSON keys: 'status', 'feedback', 'suggested_changes'. "
        "IMPORTANT: If there are no changes, use an empty list [] - NEVER use an empty string. "
        "Return ONLY the raw JSON object. Set status to 'APPROVED' only if the memo is accurate."
    ),
    output_type=AuditReview
)

# 3. The Manager
manager = Agent(
    name="Manager",
    model=settings.MODEL,
    instructions=(
        "You are the Research Manager responsible for triaging requests. "
        "Decide if we need Internal Data (Librarian) or External Data (Scholar)."
    ),
    handoffs=[librarian, scholar]
)