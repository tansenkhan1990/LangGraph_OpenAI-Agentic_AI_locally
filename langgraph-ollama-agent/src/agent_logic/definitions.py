from agents import Agent
from src.core.config import settings
from src.tools.web_tools import web_search_tool

# NOTE: The openai-agents SDK (v0.13.6) does not take 'client' in the Agent constructor.
# It uses model context and runner logic for execution.

researcher = Agent(
    name="Researcher",
    instructions="You are a helpful researcher. Use the web search tool if needed.",
    model=settings.MODEL,
    tools=[web_search_tool]
)

librarian = Agent(
    name="Librarian",
    instructions="You are the company librarian. Use the provided context to answer.",
    model=settings.MODEL
)