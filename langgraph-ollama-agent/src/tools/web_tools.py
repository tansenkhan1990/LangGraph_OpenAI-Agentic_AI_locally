from langchain_community.tools import DuckDuckGoSearchRun
from agents import function_tool

search = DuckDuckGoSearchRun()

@function_tool
def web_search_tool(query: str) -> str:
    """Searches the public web for current events, trends, and general information.
    
    Args:
        query: The search query to look up on DuckDuckGo.
    """
    try:
        return search.run(query)
    except Exception as e:
        return f"Web search error: {str(e)}"