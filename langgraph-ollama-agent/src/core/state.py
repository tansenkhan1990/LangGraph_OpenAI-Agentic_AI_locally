from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Annotated, Literal
import operator


# ─── Structured Inputs ────────────────────────────────────────────────────────

class SearchConfig(BaseModel):
    """Validated input configuration for the DuckDuckGo web search tool."""
    query: str = Field(..., min_length=2, description="The search term to look up.")
    max_results: int = Field(default=3, ge=1, le=10, description="Number of results (1-10).")
    region: str = Field(default="wt-wt", description="The region for the search.")


# ─── Structured Outputs ───────────────────────────────────────────────────────

class CorporateMemo(BaseModel):
    """
    Validated structured output from the Synthesizer agent.
    Constraints are relaxed enough for local models but strict enough
    to guarantee all required fields exist.
    """
    title: str = Field(..., min_length=3, description="A professional title for the memo.")
    sender: str = Field(..., min_length=1, description="The department or agent sending the memo.")
    body: str = Field(..., min_length=10, description="The main content of the memo.")
    sources_used: List[str] = Field(default_factory=list, description="List of sources used.")


class AuditReview(BaseModel):
    """
    Validated structured output from the Auditor agent.
    Note: 'feedback' has no min_length — local models often return
    an empty string when they approve with no reservations.
    """
    status: Literal["APPROVED", "REJECTED"] = Field(..., description="Final status.")
    feedback: str = Field(default="No additional feedback.", description="Justification for the status.")
    suggested_changes: List[str] = Field(default_factory=list, description="Fixes if rejected.")


# ─── User Input Validation ────────────────────────────────────────────────────

class QueryInput(BaseModel):
    """Validated user query input — enforces length and basic content rules."""
    text: str = Field(..., min_length=3, max_length=500, description="The user's research query.")

    @field_validator("text")
    @classmethod
    def sanitize(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Query cannot be blank or whitespace-only.")
        # Basic prompt-injection guard
        forbidden = ["<script>", "DROP TABLE", "IGNORE PREVIOUS"]
        for token in forbidden:
            if token.lower() in v.lower():
                raise ValueError(f"Query contains forbidden content: '{token}'")
        return v


# ─── LangGraph State ──────────────────────────────────────────────────────────

class AgentState(BaseModel):
    """Central state object for the LangGraph DAG."""
    messages: Annotated[List[dict], operator.add] = Field(default_factory=list)
    query: str = Field(..., min_length=3, max_length=500)

    # Context data collected during research
    internal_info: Optional[str] = None
    web_info: Optional[str] = None

    # Structured output objects
    final_report_obj: Optional[CorporateMemo] = None
    audit_obj: Optional[AuditReview] = None

    # Workflow tracking
    is_resolved: bool = False
    is_approved: bool = False
    iterations: int = Field(default=0, ge=0)
    sources: List[str] = Field(default_factory=list)