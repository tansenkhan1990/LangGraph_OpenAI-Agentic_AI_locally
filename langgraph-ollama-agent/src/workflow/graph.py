from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agents import Agent, Runner
from src.core.state import AgentState, CorporateMemo, AuditReview
from src.repository.internal_db import InternalDB
from src.agent_logic.definitions import manager, librarian, scholar, synthesizer, auditor
from src.core.config import logger
from pydantic import BaseModel
from typing import Type
import json
import re

db = InternalDB()
memory = MemorySaver()

MAX_RETRIES = 2  # Per-node retry limit for structured output failures


# ─── Utility: Robust JSON Cleaner ────────────────────────────────────────────

def clean_and_parse(text: str, model_class: Type[BaseModel]) -> BaseModel:
    """
    Extracts valid JSON from raw LLM output that may be wrapped in
    Markdown fences or contain trailing text. Validates against a
    Pydantic model.
    """
    # 1. Strip markdown fences if present
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if json_match:
        text = json_match.group(1)

    # 2. Try to find a JSON object in the text
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        text = brace_match.group(0)

    text = text.strip()

    # 3. Parse and validate
    data = json.loads(text)
    return model_class(**data)


def run_structured_agent(
    agent: Agent,
    prompt: str,
    model_class: Type[BaseModel],
    retries: int = MAX_RETRIES
) -> BaseModel:
    """
    Runs an agent with output_type and handles common local-model failures:
    - Markdown-wrapped JSON
    - Missing/wrong field names
    - Retries on validation error
    """
    last_error = None
    for attempt in range(retries + 1):
        try:
            res = Runner.run_sync(agent, prompt)
            output = res.final_output

            # If SDK already parsed it into the model, great
            if isinstance(output, model_class):
                return output

            # If it came back as a string, try manual parsing
            if isinstance(output, str):
                return clean_and_parse(output, model_class)

            # If it's a dict (shouldn't happen, but defensive)
            if isinstance(output, dict):
                return model_class(**output)

            raise TypeError(
                f"Unsupported output type from agent '{agent.name}': {type(output).__name__}"
            )

        except Exception as e:
            last_error = e
            if attempt < retries:
                logger.warning(
                    f"Structured output attempt {attempt + 1}/{retries + 1} failed: {e}. Retrying..."
                )
                # Add a hint to the prompt for the retry
                prompt += "\n\nIMPORTANT: Return ONLY valid JSON. No markdown."
            else:
                logger.error(f"All {retries + 1} attempts failed for {model_class.__name__}: {e}")
                raise last_error


# ─── Node Definitions ────────────────────────────────────────────────────────

def intake_and_lookup_node(state: AgentState):
    """Checks internal DB and runs the Manager for triage."""
    logger.info(f"Node [INTAKE]: Processing '{state.query[:40]}'")
    internal_res = db.search(state.query)
    res = Runner.run_sync(manager, f"Query: {state.query}. Internal DB: {internal_res}")
    return {
        "internal_info": internal_res,
        "messages": [{"role": "assistant", "content": res.final_output}],
        "iterations": state.iterations + 1,
    }


def internal_research_node(state: AgentState):
    """Runs the Librarian specialist on internal data."""
    logger.info("Node [LIBRARIAN]: Accessing internal records...")
    ctx = state.internal_info or "No records found"
    res = Runner.run_sync(librarian, f"Context: {ctx}\nUser Query: {state.query}")
    return {"messages": [{"role": "assistant", "content": res.final_output}]}


def web_research_node(state: AgentState):
    """Runs the Scholar specialist with web tools."""
    logger.info("Node [SCHOLAR]: Accessing external web tools...")
    res = Runner.run_sync(scholar, state.query)
    return {
        "web_info": res.final_output,
        "messages": [{"role": "assistant", "content": res.final_output}],
    }


def synthesis_node(state: AgentState):
    """Runs the Synthesizer to produce a structured CorporateMemo."""
    logger.info("Node [SYNTHESIZER]: Constructing structured memo...")
    prompt = (
        f"INTERNAL DATA: {state.internal_info or 'None'}\n"
        f"WEB DATA: {state.web_info or 'None'}\n"
        f"QUERY: {state.query}"
    )
    memo = run_structured_agent(synthesizer, prompt, CorporateMemo)
    logger.info(f"Memo created: '{memo.title}'")
    return {
        "final_report_obj": memo,
        "messages": [{"role": "assistant", "content": memo.body}],
    }


def audit_node(state: AgentState):
    """Runs the Auditor to validate the memo with structured output."""
    logger.info("Node [AUDITOR]: Performing quality assurance...")
    memo = state.final_report_obj
    prompt = f"Report Title: {memo.title}\nReport Body: {memo.body}\nOriginal Query: {state.query}"
    audit = run_structured_agent(auditor, prompt, AuditReview)
    logger.info(f"Audit result: {audit.status}")
    return {
        "audit_obj": audit,
        "is_approved": audit.status == "APPROVED",
        "messages": [{"role": "assistant", "content": f"[AUDITOR {audit.status}]: {audit.feedback}"}],
    }


# ─── Routing Logic ───────────────────────────────────────────────────────────

def route_from_intake(state: AgentState):
    """Routes to Scholar (web) or Librarian (internal) based on Manager response."""
    if not state.messages:
        return "internal_research"
    last_msg = state.messages[-1]["content"].lower()
    if any(keyword in last_msg for keyword in ["scholar", "web", "external", "search", "online"]):
        return "web_research"
    return "internal_research"


def route_from_audit(state: AgentState):
    """Self-correction loop: retry if rejected, stop if approved or max iterations."""
    if state.is_approved:
        logger.info("✅ Audit APPROVED. Workflow complete.")
        return END
    if state.iterations >= 3:
        logger.warning("⚠️ Max iterations reached. Exiting with last result.")
        return END
    logger.info("🔄 Audit REJECTED. Re-entering intake for correction...")
    return "intake"


# ─── Build the Graph ──────────────────────────────────────────────────────────

builder = StateGraph(AgentState)

builder.add_node("intake", intake_and_lookup_node)
builder.add_node("internal_research", internal_research_node)
builder.add_node("web_research", web_research_node)
builder.add_node("synthesis", synthesis_node)
builder.add_node("audit", audit_node)

builder.set_entry_point("intake")
builder.add_conditional_edges("intake", route_from_intake)
builder.add_edge("internal_research", "synthesis")
builder.add_edge("web_research", "synthesis")
builder.add_edge("synthesis", "audit")
builder.add_conditional_edges("audit", route_from_audit)

graph = builder.compile(checkpointer=memory)