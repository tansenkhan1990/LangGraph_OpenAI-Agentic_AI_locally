from langgraph.graph import StateGraph, END
from agents import Runner
from src.core.state import AgentState
from src.repository.internal_db import InternalDB
from src.agent_logic.definitions import librarian, researcher

db = InternalDB()

def db_lookup_node(state: AgentState):
    # Depending on how LangGraph passes the state (dict vs obj)
    query = state.query if hasattr(state, "query") else state["query"]
    result = db.search(query)
    if result:
        return {"internal_info": result, "is_resolved": True}
    return {"is_resolved": False}

def librarian_node(state: AgentState):
    query = state.query if hasattr(state, "query") else state["query"]
    internal_info = state.internal_info if hasattr(state, "internal_info") else state["internal_info"]
    
    # Use Runner as per openai-agents 0.13.6 standard
    res = Runner.run_sync(librarian, f"Context: {internal_info}\nUser: {query}")
    return {"messages": [{"role": "assistant", "content": res.final_output}]}

def web_node(state: AgentState):
    query = state.query if hasattr(state, "query") else state["query"]
    
    # Use Runner as per openai-agents 0.13.6 standard
    res = Runner.run_sync(researcher, query)
    return {"messages": [{"role": "assistant", "content": res.final_output}]}

# Build the Logic
builder = StateGraph(AgentState)
builder.add_node("db_lookup", db_lookup_node)
builder.add_node("librarian", librarian_node)
builder.add_node("web_search", web_node)

builder.set_entry_point("db_lookup")

# Dynamic Routing
builder.add_conditional_edges(
    "db_lookup",
    lambda state: "internal" if (state.is_resolved if hasattr(state, "is_resolved") else state["is_resolved"]) else "external",
    {"internal": "librarian", "external": "web_search"}
)

builder.add_edge("librarian", END)
builder.add_edge("web_search", END)

graph = builder.compile()