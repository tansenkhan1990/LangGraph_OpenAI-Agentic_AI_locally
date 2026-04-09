"""
Main Application Entry Point
Run this to start the LangGraph + Ollama agent system
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.graph.builder import build_workflow
from src.graph.state import AgentState
from src.utils.logger import app_logger
from src.models.ollama_config import test_ollama_connection

# Load environment variables
load_dotenv()

async def run_single_question(workflow, question: str):
    """
    Run a single question through the workflow
    """
    # Create initial state
    initial_state: AgentState = {
        "question": question,
        "category": None,
        "answer": None,
        "messages": [],
        "error": None,
        "retry_count": 0,
    }
    
    print("\n" + "="*60)
    print(f"❓ QUESTION: {question}")
    print("="*60)
    
    # Run the workflow
    final_state = await workflow.ainvoke(initial_state)
    
    # Display the answer
    print("\n" + "="*60)
    print("📝 FINAL ANSWER:")
    print("="*60)
    print(final_state.get("answer", "No answer generated"))
    print("="*60)
    
    return final_state

async def interactive_mode():
    """
    Run the workflow in interactive mode (chat loop)
    """
    print("\n" + "🎓" * 30)
    print("   LANGRAPH + OLLAMA SMART ASSISTANT")
    print("   Using model: " + os.getenv("LOCAL_MODEL_NAME", "qwen3-vl:235b-cloud"))
    print("🎓" * 30)
    
    print("\n📋 Available experts:")
    print("   🔬 Science Expert - answers science questions")
    print("   📜 History Expert - answers history questions")
    print("   💻 Code Expert - answers programming questions")
    
    print("\n💡 Try asking:")
    print("   • 'What is quantum entanglement?' → Science")
    print("   • 'Who was Alexander the Great?' → History")
    print("   • 'How do I create a list in Python?' → Programming")
    
    print("\n⚠️  Commands:")
    print("   • 'quit' or 'exit' - End the conversation")
    print("   • 'status' - Show system status")
    
    # Build the workflow
    workflow = build_workflow()
    
    while True:
        try:
            # Get user input
            question = input("\n" + "🤔 " + "You: ").strip()
            
            if question.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye! Have a great day!")
                break
            
            if question.lower() == 'status':
                print("\n📊 System Status:")
                print(f"   Model: {os.getenv('LOCAL_MODEL_NAME')}")
                print(f"   Ollama URL: {os.getenv('OLLAMA_BASE_URL')}")
                print(f"   Log Level: {os.getenv('LOG_LEVEL')}")
                continue
            
            if not question:
                print("   Please enter a question.")
                continue
            
            # Run the workflow
            await run_single_question(workflow, question)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            app_logger.error(f"Error in interactive mode: {e}")
            print(f"\n❌ An error occurred: {e}")

async def batch_mode(questions_file: str = None):
    """
    Run multiple questions from a file
    """
    if not questions_file:
        questions_file = input("Enter path to questions file: ").strip()
    
    if not os.path.exists(questions_file):
        print(f"❌ File not found: {questions_file}")
        return
    
    with open(questions_file, 'r') as f:
        questions = [line.strip() for line in f if line.strip()]
    
    print(f"\n📚 Running batch of {len(questions)} questions...")
    
    workflow = build_workflow()
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] Processing...")
        try:
            result = await run_single_question(workflow, question)
            results.append({
                "question": question,
                "answer": result.get("answer"),
                "category": result.get("category")
            })
        except Exception as e:
            app_logger.error(f"Failed on question {i}: {e}")
            results.append({
                "question": question,
                "answer": f"Error: {e}",
                "category": None
            })
    
    # Save results
    output_file = "batch_results.txt"
    with open(output_file, 'w') as f:
        for r in results:
            f.write(f"Q: {r['question']}\n")
            f.write(f"Category: {r['category']}\n")
            f.write(f"A: {r['answer']}\n")
            f.write("-"*50 + "\n")
    
    print(f"\n✅ Batch complete! Results saved to {output_file}")

async def main():
    """
    Main entry point
    """
    # First, test Ollama connection
    print("\n🔌 Testing Ollama connection...")
    if not await test_ollama_connection():
        print("\n❌ Cannot connect to Ollama. Please make sure:")
        print("   1. Ollama is installed: https://ollama.ai")
        print("   2. The model is pulled: ollama pull qwen3-vl:235b-cloud")
        print("   3. Ollama is running: ollama serve")
        print("\n   After fixing, run this script again.")
        return
    
    print("\n✅ Ollama is ready!")
    
    # Choose mode
    print("\n📌 Select mode:")
    print("   1. Interactive mode (chat with the AI)")
    print("   2. Single question mode")
    print("   3. Batch mode (process questions from file)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        await interactive_mode()
    elif choice == "2":
        workflow = build_workflow()
        question = input("Enter your question: ").strip()
        await run_single_question(workflow, question)
    elif choice == "3":
        await batch_mode()
    else:
        print("Invalid choice. Running interactive mode by default.")
        await interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())