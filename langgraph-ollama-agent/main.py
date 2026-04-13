import uuid
import json
from src.workflow.graph import graph
from src.core.config import logger

def chat():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print("\n" + "🚀" + "="*59)
    print("--- 🤖 JSON-NATIVE CORPORATE INTELLIGENCE HUB ---")
    print("      Input: JSON | Output: JSON")
    print("="*61 + "\n")
    
    while True:
        try:
            # 1. Natural Language Input
            user_input = input("👤 Query: ")
            if user_input.lower() in ["exit", "quit"]: 
                break
            
            if not user_input.strip():
                continue

            # 2. Execute Workflow
            config = {"configurable": {"thread_id": thread_id}}
            print("\n⚙️  Executing Agent Graph...")
            
            # Streaming to keep the session alive
            for _ in graph.stream({"query": user_input}, config=config):
                pass

            # 3. Handle JSON Output
            state = graph.get_state(config).values
            
            output_package = {
                "session_id": thread_id,
                "status": "success",
                "memo": None,
                "audit": None,
                "meta": {
                    "iterations": state.get("iterations"),
                    "is_approved": state.get("is_approved")
                }
            }
            
            if state.get("final_report_obj"):
                output_package["memo"] = state["final_report_obj"].model_dump()
            
            if state.get("audit_obj"):
                output_package["audit"] = state["audit_obj"].model_dump()

            print("\n" + "💎" + " FINAL JSON OUTPUT " + "="*41)
            print(json.dumps(output_package, indent=2))
            print("="*60 + "\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            error_res = {"status": "error", "message": str(e)}
            print(json.dumps(error_res, indent=2))

if __name__ == "__main__":
    chat()
