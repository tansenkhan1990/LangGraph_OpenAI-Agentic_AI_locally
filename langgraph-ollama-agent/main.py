"""
SIMPLE LANGRAPH + OLLAMA PROJECT
Run this file directly - no complex structure needed!
"""

import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

# Load environment variables
load_dotenv()

# Disable agents tracing to remove "OPENAI_API_KEY is not set" messages
set_tracing_disabled(True)

MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "qwen3-vl:235b-cloud")

# ============================================
# SETUP OLLAMA CLIENT
# ============================================

def get_ollama_client():
    """Create OpenAI-compatible client for Ollama"""
    return AsyncOpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        timeout=60.0,
    )

# ============================================
# DEFINE OUR STATE (What the workflow remembers)
# ============================================

class WorkflowState(TypedDict):
    """The memory of our workflow"""
    question: str           # User's question
    category: str           # science, history, or programming
    answer: str             # Final answer
    error: str              # Any error messages

# ============================================
# CREATE OUR AGENTS (Using OpenAI Agents SDK)
# ============================================

# Agent 1: Figures out what type of question
classifier_agent = Agent(
    name="Classifier",
    model=MODEL_NAME,
    instructions="""You classify questions into ONE of these categories:
    - 'science' for questions about physics, chemistry, biology, space
    - 'history' for questions about past events, people, wars
    - 'programming' for questions about code, computers, software
    
    Respond with ONLY the category name. Nothing else.
    Example: 'science' or 'history' or 'programming'
    """
)

# Agent 2: Science expert
science_agent = Agent(
    name="Science Expert",
    model=MODEL_NAME,
    instructions="""You are a science professor. Answer the question clearly.
    Use simple language. Keep answers to 2-3 paragraphs.
    """
)

# Agent 3: History expert
history_agent = Agent(
    name="History Expert", 
    model=MODEL_NAME,
    instructions="""You are a history professor. Include important dates.
    Explain why events matter. Keep answers to 2-3 paragraphs.
    """
)

# Agent 4: Programming expert
programming_agent = Agent(
    name="Programming Expert",
    model=MODEL_NAME,
    instructions="""You are a software engineer. Include code examples.
    Explain concepts step by step. Be practical.
    """
)

# ============================================
# LANGRAPH NODES (The steps in our workflow)
# ============================================

async def classify_question(state: WorkflowState):
    """Step 1: Figure out the question category"""
    print("\n📋 [1/3] CLASSIFYING your question...")
    
    # Run the classifier agent
    result = await Runner.run(classifier_agent, state["question"])
    category = result.final_output.strip().lower()
    
    # Validate category
    if category not in ["science", "history", "programming"]:
        category = "science"  # Default
    
    print(f"   ✅ Question type: {category.upper()}")
    return {"category": category}

async def answer_question(state: WorkflowState):
    """Step 2: Get answer from the right expert"""
    category = state["category"]
    
    print(f"\n🎯 [2/3] Getting answer from {category.upper()} expert...")
    
    # Pick the right agent
    if category == "science":
        agent = science_agent
        icon = "🔬"
    elif category == "history":
        agent = history_agent
        icon = "📜"
    else:
        agent = programming_agent
        icon = "💻"
    
    print(f"   {icon} Consulting {category} expert...")
    
    # Run the expert agent
    result = await Runner.run(agent, state["question"])
    
    print(f"   ✅ Answer ready!")
    return {"answer": result.final_output}

# ============================================
# BUILD THE LANGRAPH WORKFLOW
# ============================================

def create_workflow():
    """Create the decision graph"""
    
    # Create empty graph
    workflow = StateGraph(WorkflowState)
    
    # Add our steps (nodes)
    workflow.add_node("classifier", classify_question)
    workflow.add_node("answer_expert", answer_question)
    
    # Set start point
    workflow.set_entry_point("classifier")
    
    # Connect nodes
    workflow.add_edge("classifier", "answer_expert")
    workflow.add_edge("answer_expert", END)
    
    # Compile the graph
    return workflow.compile()

# ============================================
# MAIN APPLICATION
# ============================================

async def test_ollama():
    """Test if Ollama is working"""
    print("\n🔌 Testing Ollama connection...")
    
    try:
        client = get_ollama_client()
        response = await client.chat.completions.create(
            model=os.getenv("LOCAL_MODEL_NAME", "qwen2.5:7b"),
            messages=[{"role": "user", "content": "Say 'OK'"}],
            max_tokens=10,
        )
        print("   ✅ Ollama is working!\n")
        return True
    except Exception as e:
        print(f"   ❌ Ollama error: {e}")
        print("\n   Please make sure:")
        print("   1. Ollama is installed: https://ollama.ai")
        print(f"   2. Run: ollama pull {os.getenv('LOCAL_MODEL_NAME', 'qwen2.5:7b')}")
        print("   3. Run: ollama serve")
        return False

async def main():
    """Main program"""
    
    print("="*60)
    print("🤖 LANGRAPH + OLLAMA SMART ASSISTANT")
    print("="*60)
    
    # Test Ollama first
    if not await test_ollama():
        return
    
    # Create the workflow
    print("📊 Building LangGraph workflow...")
    app = create_workflow()
    print("   ✅ Workflow ready!\n")
    
    print("💡 Try asking questions like:")
    print("   • 'What is black hole?' → Science")
    print("   • 'Who was Cleopatra?' → History")
    print("   • 'How to sort a list in Python?' → Programming")
    print("\n   Type 'quit' to exit")
    print("="*60)
    
    # Interactive loop
    while True:
        # Get user input
        user_input = input("\n❓ You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            print("   Please enter a question.")
            continue
        
        # Create initial state
        initial_state = {
            "question": user_input,
            "category": "",
            "answer": "",
            "error": "",
        }
        
        print("\n" + "🔄" * 30)
        print("PROCESSING YOUR QUESTION")
        print("🔄" * 30)
        
        try:
            # Run the LangGraph workflow
            final_state = await app.ainvoke(initial_state)
            
            # Display the answer
            print("\n" + "="*60)
            print("📝 ANSWER:")
            print("="*60)
            print(final_state["answer"])
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("   Please try again.")

if __name__ == "__main__":
    asyncio.run(main())