"""
LangGraph Workflow Builder
This assembles all the nodes and edges into a complete workflow
"""

from langgraph.graph import StateGraph, END
from src.graph.state import AgentState
from src.graph.nodes import (
    classify_question_node,
    answer_science_node,
    answer_history_node,
    answer_programming_node,
)
from src.graph.edges import route_after_classification

def build_workflow() -> StateGraph:
    """
    Build and compile the complete LangGraph workflow
    
    Workflow structure:
    START → classifier → [route] → science/history/programming → END
    """
    
    # 1. Create a new graph with our state type
    workflow = StateGraph(AgentState)
    
    # 2. Add all our nodes (the workers)
    workflow.add_node("classifier", classify_question_node)
    workflow.add_node("science_expert", answer_science_node)
    workflow.add_node("history_expert", answer_history_node)
    workflow.add_node("programming_expert", answer_programming_node)
    
    # 3. Set the entry point (where the workflow starts)
    workflow.set_entry_point("classifier")
    
    # 4. Add conditional routing after classification
    #    This is the MAGIC of LangGraph - decision points!
    workflow.add_conditional_edges(
        "classifier",               # From this node
        route_after_classification, # Use this function to decide where to go
        {
            "science_expert": "science_expert",
            "history_expert": "history_expert", 
            "programming_expert": "programming_expert",
            END: END,
        }
    )
    
    # 5. Add edges from experts to END
    #    After an expert answers, the workflow ends
    workflow.add_edge("science_expert", END)
    workflow.add_edge("history_expert", END)
    workflow.add_edge("programming_expert", END)
    
    # 6. Compile the graph (makes it executable)
    app = workflow.compile()
    
    print("\n✅ LangGraph workflow compiled successfully!")
    print("   Workflow structure: classifier → [router] → expert → END")
    
    return app