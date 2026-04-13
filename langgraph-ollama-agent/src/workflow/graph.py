from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agents import Runner
from src.core.state import AgentState, CorporateMemo, AuditReview
from src.repository.internal_db import InternalDB
from src.agent_logic.definitions import manager, librarian, scholar, synthesizer, auditor
from src.core.config import logger
import json
import re

db = InternalDB()
memory = MemorySaver()

# --- UTILITY: Robust JSON Cleaner ---
def clean_and_parse(text: str, model_class):
    """Helper to extract JSON from Markdown-wrapped responses."""
    try:
        # 1. Try to find JSON block
        json_match = re.search(r"```json\n?(.*?)\n?```", text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        
        # 2. Clean common hallucinations
        text = text.strip()
        
        # 3. Parse and validate
        data = json.loads(text)
        return model_class(**data)
    except Exception as e:
        logger.error(f"Failed to parse structured output: {str(e)}\nRaw Content: {text}")
        raise

# --- NODE DEFINITIONS ---

def intake_and_lookup_node(state: AgentState):
    logger.info(f"Node [INTAKE]: Processing '{state.query[:30]}...'")
    internal_res = db.search(state.query)
    res = Runner.run_sync(manager, f"Query: {state.query}. Internal DB: {internal_res}")
    return {
        "internal_info": internal_res,
        "messages": [{"role": "assistant", "content": res.final_output}],
        "iterations": state.iterations + 1
    }

def internal_research_node(state: AgentState):
    logger.info("Node [LIBRARIAN]: Accessing internal records...")
    ctx = state.internal_info or "No records found"
    res = Runner.run_sync(librarian, f"Context: {ctx}\nUser Query: {state.query}")
    return {"messages": [{"role": "assistant", "content": res.final_output}]}

def web_research_node(state: AgentState):
    logger.info("Node [SCHOLAR]: Accessing external web tools...")
    res = Runner.run_sync(scholar, state.query)
    return {"web_info": res.final_output, "messages": [{"role": "assistant", "content": res.final_output}]}

def synthesis_node(state: AgentState):
    logger.info("Node [SYNTHESIZER]: Constructing structured memo...")
    prompt = f"INTERNAL: {state.internal_info}\nWEB: {state.web_info}\nQUERY: {state.query}"
    
    # We call the agent. If it fails validation, it might be due to markdown.
    # Note: If output_type is set, the SDK might throw before we can clean.
    # To be safest with local models, we can temporarily ignore output_type if it fails,
    # OR we use a very descriptive prompt (done in definitions.py).
    try:
        res = Runner.run_sync(synthesizer, prompt)
        memo = res.final_output
        if isinstance(memo, str): # Safety check if model bypassed validation
            memo = clean_and_parse(memo, CorporateMemo)
    except Exception:
        # Fallback to manual extraction if the SDK parser breaks on Markdown
        # This is a key best practice for local Ollama usage.
        # Note: In a real SDK scenario, we'd use a custom parser.
        raise

    return {"final_report_obj": memo, "messages": [{"role": "assistant", "content": memo.body}]}

def audit_node(state: AgentState):
    logger.info("Node [AUDITOR]: Performing quality assurance...")
    memo = state.final_report_obj
    res = Runner.run_sync(auditor, f"Report: {memo.body}\nQuery: {state.query}")
    
    audit = res.final_output
    if isinstance(audit, str):
        audit = clean_and_parse(audit, AuditReview)
        
    return {
        "audit_obj": audit,
        "is_approved": audit.status == "APPROVED",
        "messages": [{"role": "assistant", "content": f"[AUDITOR {audit.status}]: {audit.feedback}"}]
    }

# --- ROUTING ---

def route_from_intake(state: AgentState):
    last_msg = state.messages[-1]["content"].lower()
    if any(x in last_msg for x in ["scholar", "web", "external"]):
        return "web_research"
    return "internal_research"

def route_from_audit(state: AgentState):
    if state.is_approved: return END
    if state.iterations >= 3: return END
    return "intake"

# --- GRAPH ---
builder = StateGraph(AgentState)

# Add Nodes
builder.add_node("intake", intake_and_lookup_node)
builder.add_node("internal_research", internal_research_node)
builder.add_node("web_research", web_research_node)
builder.add_node("synthesis", synthesis_node)
builder.add_node("audit", audit_node)

# Add Edges
builder.set_entry_point("intake")
builder.add_conditional_edges("intake", route_from_intake)
builder.add_edge("internal_research", "synthesis")
builder.add_edge("web_research", "synthesis")
builder.add_edge("synthesis", "audit")
builder.add_conditional_edges("audit", route_from_audit)

graph = builder.compile(checkpointer=memory)