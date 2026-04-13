from langchain_community.tools import DuckDuckGoSearchRun
from agents import function_tool
from src.core.state import SearchConfig

search = DuckDuckGoSearchRun()

@function_tool
def web_search_tool(config: SearchConfig) -> str:
    """Searches the public web using a structured configuration.
    
    Args:
        config: The search configuration containing query, limits, and region.
    """
    try:
        # Note: DuckDuckGoSearchRun might just take a string query, 
        # so we extract it from the config, but the LLM sees the config object.
        return search.run(config.query)
    except Exception as e:
        return f"Web search error: {str(e)}"