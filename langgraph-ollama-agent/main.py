from src.workflow.graph import graph

def chat():
    print("\n" + "="*50)
    print("--- 🤖 Corporate Assistant (Ollama + LangGraph) ---")
    print("Type 'exit' to quit.")
    print("="*50 + "\n")
    
    while True:
        try:
            user_input = input("👤 Query: ")
            if user_input.lower() in ["exit", "quit"]: 
                print("👋 Goodbye!")
                break
            
            # Streaming output for a better UX
            print("\n🔍 Researching...")
            for event in graph.stream({"query": user_input}):
                for node, value in event.items():
                    # print(f"DEBUG: Executed [{node}]") # Useful for troubleshooting
                    if "messages" in value and value["messages"]:
                        print(f"\n🤖 AI ({node}):\n{value['messages'][-1]['content']}\n")
                    elif node == "db_lookup":
                        if value.get("is_resolved"):
                            print("📂 Found matching internal record.")
                        else:
                            print("🌐 No internal record found. Escalating to web search...")
            
            print("-" * 30)

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    chat()
