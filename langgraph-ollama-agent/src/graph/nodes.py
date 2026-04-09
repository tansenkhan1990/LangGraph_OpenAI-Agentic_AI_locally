"""
LangGraph Nodes
Each node is a step in our workflow
"""

import os
from agents import Runner
from src.graph.state import AgentState
from src.models.ollama_config import get_ollama_client, get_model_name
from src.agents.classifier import create_classifier_agent
from src.agents.science_expert import create_science_agent
from src.agents.history_expert import create_history_agent
from src.agents.code_expert import create_code_agent

# Get Ollama configuration
ollama_client = get_ollama_client()
model_name = get_model_name()

async def classify_question_node(state: AgentState) -> dict:
    """
    NODE 1: Classify the question category
    
    This node takes the user's question and determines
    which expert should answer it.
    """
    print("\n🤔 [CLASSIFIER NODE] Analyzing question...")
    print(f"   Question: {state['question']}")
    
    try:
        # Create the classifier agent
        classifier = create_classifier_agent()
        
        # Run the agent with our Ollama model
        # Note: We need to pass the custom client to use Ollama
        result = await Runner.run(
            classifier, 
            state['question'],
            # For Ollama, we need to use the OpenAI-compatible client
            # The Agents SDK uses the OPENAI_API_KEY env var by default
            # We'll set it in the environment before running
        )
        
        category = result.final_output.strip().lower()
        
        # Validate category
        valid_categories = ["science", "history", "programming"]
        if category not in valid_categories:
            print(f"   ⚠️ Invalid category '{category}', defaulting to 'science'")
            category = "science"
        
        print(f"   ✅ Category determined: {category}")
        
        return {
            "category": category,
            "error": None
        }
        
    except Exception as e:
        print(f"   ❌ Classification error: {e}")
        return {
            "category": "science",  # Default
            "error": str(e),
            "retry_count": state.get("retry_count", 0) + 1
        }

async def answer_science_node(state: AgentState) -> dict:
    """
    NODE 2A: Answer science questions
    """
    print("\n🔬 [SCIENCE EXPERT NODE] Generating answer...")
    print(f"   Question: {state['question']}")
    
    try:
        science_agent = create_science_agent()
        
        result = await Runner.run(
            science_agent,
            state['question']
        )
        
        answer = result.final_output
        print(f"   ✅ Answer generated ({len(answer)} characters)")
        
        return {
            "answer": answer,
            "messages": [{"role": "assistant", "content": answer}]
        }
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        print(f"   ❌ Error: {e}")
        return {
            "answer": error_msg,
            "error": str(e)
        }

async def answer_history_node(state: AgentState) -> dict:
    """
    NODE 2B: Answer history questions
    """
    print("\n📜 [HISTORY EXPERT NODE] Generating answer...")
    print(f"   Question: {state['question']}")
    
    try:
        history_agent = create_history_agent()
        
        result = await Runner.run(
            history_agent,
            state['question']
        )
        
        answer = result.final_output
        print(f"   ✅ Answer generated ({len(answer)} characters)")
        
        return {
            "answer": answer,
            "messages": [{"role": "assistant", "content": answer}]
        }
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        print(f"   ❌ Error: {e}")
        return {
            "answer": error_msg,
            "error": str(e)
        }

async def answer_programming_node(state: AgentState) -> dict:
    """
    NODE 2C: Answer programming questions
    """
    print("\n💻 [CODE EXPERT NODE] Generating answer...")
    print(f"   Question: {state['question']}")
    
    try:
        code_agent = create_code_agent()
        
        result = await Runner.run(
            code_agent,
            state['question']
        )
        
        answer = result.final_output
        print(f"   ✅ Answer generated ({len(answer)} characters)")
        
        return {
            "answer": answer,
            "messages": [{"role": "assistant", "content": answer}]
        }
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        print(f"   ❌ Error: {e}")
        return {
            "answer": error_msg,
            "error": str(e)
        }