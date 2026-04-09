"""
Conditional edges for LangGraph routing
These functions decide which node to go to next
"""

from langgraph.graph import END
from src.graph.state import AgentState

def route_after_classification(state: AgentState) -> str:
    """
    Decision function: Where to go after classification?
    
    Returns the name of the next node or END
    """
    category = state.get("category", "science")
    
    print(f"\n🚦 [ROUTER] Deciding next step based on category: {category}")
    
    # Route to the appropriate expert node
    if category == "science":
        print("   → Routing to SCIENCE expert")
        return "science_expert"
    elif category == "history":
        print("   → Routing to HISTORY expert")
        return "history_expert"
    elif category == "programming":
        print("   → Routing to PROGRAMMING expert")
        return "programming_expert"
    else:
        # Unknown category, end the workflow
        print(f"   ⚠️ Unknown category '{category}', ending workflow")
        return END

def should_retry(state: AgentState) -> str:
    """
    Check if we should retry after an error
    """
    error = state.get("error")
    retry_count = state.get("retry_count", 0)
    
    if error and retry_count < 3:
        print(f"   🔄 Retrying (attempt {retry_count + 1}/3)")
        return "retry"
    elif error:
        print(f"   ❌ Max retries reached, ending workflow")
        return END
    else:
        return "continue"