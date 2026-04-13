from pydantic import BaseModel
from typing import List, Optional, Annotated
import operator

class AgentState(BaseModel):
    # Annotated with operator.add allows LangGraph to append messages automatically
    messages: Annotated[List[dict], operator.add] = []
    query: str
    internal_info: Optional[str] = None
    is_resolved: bool = False