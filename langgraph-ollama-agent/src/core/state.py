from pydantic import BaseModel, Field
from typing import List, Optional, Annotated, Literal
import operator

# --- Structured Inputs ---

class SearchConfig(BaseModel):
    query: str = Field(..., description="The search term to look up on DuckDuckGo.")
    max_results: int = Field(default=3, description="Maximum number of results to return.")
    region: str = Field(default="wt-wt", description="The region for the search (e.g., 'us-en').")

# --- Structured Outputs ---

class CorporateMemo(BaseModel):
    title: str = Field(..., description="A professional title for the memo.")
    sender: str = Field(..., description="The department or agent sending the memo.")
    body: str = Field(..., description="The main content of the memo.")
    sources_used: List[str] = Field(default_factory=list, description="List of internal and external sources used.")

class AuditReview(BaseModel):
    status: Literal["APPROVED", "REJECTED"] = Field(..., description="The final status of the report.")
    feedback: str = Field(..., description="Detailed feedback or justification for the status.")
    suggested_changes: List[str] = Field(default_factory=list, description="Specific fixes if rejected.")

# --- LangGraph State ---

class AgentState(BaseModel):
    messages: Annotated[List[dict], operator.add] = []
    query: str
    
    # Context data
    internal_info: Optional[str] = None
    web_info: Optional[str] = None
    
    # Structured tracker
    final_report_obj: Optional[CorporateMemo] = None
    audit_obj: Optional[AuditReview] = None
    
    # Flags & Tracking
    is_resolved: bool = False
    is_approved: bool = False
    iterations: int = 0
    sources: List[str] = []