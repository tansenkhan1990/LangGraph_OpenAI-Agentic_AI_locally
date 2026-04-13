from openai import OpenAI
from agents import Agent
from src.core.config import settings
from src.core.state import CorporateMemo, AuditReview
from src.tools.web_tools import web_search_tool

# ─── OpenAI Client (pointed at local Ollama) ─────────────────────────────────
client = OpenAI(base_url=settings.BASE_URL, api_key=settings.API_KEY)


# ─── 1. Specialist Agents ────────────────────────────────────────────────────

librarian = Agent(
    name="Librarian",
    model=settings.MODEL,
    instructions=(
        "You are the Corporate Librarian. You specialize in internal company data. "
        "Use the provided context to answer accurately. Be concise."
    )
)

scholar = Agent(
    name="Scholar",
    model=settings.MODEL,
    instructions=(
        "You are the External Scholar. You specialize in public web research. "
        "Use the web_search_tool to find real-time information. Be concise."
    ),
    tools=[web_search_tool]
)


# ─── 2. Structured Output Agents ─────────────────────────────────────────────

synthesizer = Agent(
    name="Synthesizer",
    model=settings.MODEL,
    instructions=(
        "You are a raw JSON data generator. Output a CorporateMemo JSON object. "
        "MANDATORY KEYS: 'title' (str), 'sender' (str), 'body' (str), 'sources_used' (list). "
        "Do NOT use 'content' — always use 'body'. "
        "If no sources, use []. NEVER use an empty string for list fields. "
        "Return ONLY the raw JSON object. No Markdown. No extra text."
    ),
    output_type=CorporateMemo
)

auditor = Agent(
    name="Auditor",
    model=settings.MODEL,
    instructions=(
        "You are a strict quality auditor. "
        "MANDATORY KEYS: 'status' (APPROVED or REJECTED), 'feedback' (str), 'suggested_changes' (list). "
        "For 'feedback', ALWAYS write at least a short sentence explaining your decision. "
        "If no changes needed, use [] for suggested_changes. NEVER use empty strings for list fields. "
        "Return ONLY the raw JSON object. No Markdown. No extra text."
    ),
    output_type=AuditReview
)


# ─── 3. Manager (Entry Point with Handoffs) ──────────────────────────────────

manager = Agent(
    name="Manager",
    model=settings.MODEL,
    instructions=(
        "You are the Research Manager. Triage requests: "
        "If the query is about internal company data (salaries, office hours, policies), "
        "mention 'Librarian' in your response. "
        "If the query needs external/web information, mention 'Scholar' in your response."
    ),
    handoffs=[librarian, scholar]
)