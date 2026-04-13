from langchain_community.tools import DuckDuckGoSearchRun
from agents import function_tool
from src.core.state import SearchConfig
from src.core.config import logger

search = DuckDuckGoSearchRun()


@function_tool
def web_search_tool(config: SearchConfig) -> str:
    """Searches the public web using a structured SearchConfig.

    Args:
        config: The search configuration containing query, max_results, and region.
    """
    logger.info(f"🔍 Web search triggered: query='{config.query}', region='{config.region}'")

    try:
        results = search.run(config.query)
        if not results or len(results.strip()) == 0:
            logger.warning("Web search returned empty results.")
            return "No web results found for this query."
        return results
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return f"Web search error: {str(e)}"