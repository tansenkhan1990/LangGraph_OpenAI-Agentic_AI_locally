"""
Free web search tool using DuckDuckGo
No API key required!
"""

from agents import function_tool
import asyncio

@function_tool
async def web_search(query: str) -> str:
    """
    Search the web for current information
    
    Args:
        query: The search query
    
    Returns:
        Top search results as formatted text
    """
    try:
        from duckduckgo_search import DDGS
        
        print(f"🔍 Searching for: {query}")
        
        def sync_search():
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                return results
        
        results = await asyncio.to_thread(sync_search)
        
        if not results:
            return f"No results found for: {query}"
        
        formatted = []
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            body = result.get('body', 'No content')
            formatted.append(f"{i}. {title}\n   {body}\n")
        
        return "\n".join(formatted)
        
    except ImportError:
        return "Web search not available. Please install duckduckgo-search"
    except Exception as e:
        return f"Search error: {str(e)}"