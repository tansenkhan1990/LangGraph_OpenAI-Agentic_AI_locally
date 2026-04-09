"""
LangGraph State Definition
This defines what information flows through our graph
"""

from typing import TypedDict, Optional, List, Any
from langgraph.graph import add_messages
from typing_extensions import Annotated

class AgentState(TypedDict):
    """
    The state of our LangGraph workflow.
    
    This is like a shared memory that all nodes can access and modify.
    LangGraph passes this between nodes automatically.
    """
    
    # The original user question
    question: str
    
    # The category determined by classifier (science, history, programming)
    category: Optional[str]
    
    # The final answer
    answer: Optional[str]
    
    # Conversation history (uses special add_messages reducer)
    messages: Annotated[List[Any], add_messages]
    
    # Error tracking
    error: Optional[str]
    
    # Retry count for error handling
    retry_count: int