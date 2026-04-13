import uuid
import json
from pydantic import ValidationError
from src.workflow.graph import graph
from src.core.config import logger
from src.core.state import QueryInput


def validate_input(raw: str):
    """
    Validates and sanitizes the raw user input using the QueryInput Pydantic model.
    Returns: (clean_query: str, None) on success
             (None, error_message: str) on failure
    """
    try:
        validated = QueryInput(text=raw)
        return validated.text, None
    except ValidationError as e:
        errors = e.errors()
        return None, errors[0]["msg"]


def chat():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print("\n" + "🚀" + "=" * 59)
    print("--- 🤖 PRODUCTION-READY CORPORATE INTELLIGENCE HUB ---")
    print("      ✅ Input Validated | ✅ Output Schema Enforced")
    print("=" * 61 + "\n")

    logger.info(f"New session started. Thread ID: {thread_id}")

    while True:
        try:
            raw_input = input("👤 Query: ").strip()

            # ── Exit guard ──────────────────────────────────────────────────
            if raw_input.lower() in ["exit", "quit"]:
                logger.info("Session terminated by user.")
                break

            # ── Input Validation ────────────────────────────────────────────
            query, err = validate_input(raw_input)
            if err:
                error_out = {"status": "error", "type": "INPUT_VALIDATION", "message": err}
                print(json.dumps(error_out, indent=2) + "\n")
                continue

            logger.info(f"✅ Input validated: '{query[:50]}' ({len(query)} chars)")

            # ── Execute Workflow ─────────────────────────────────────────────
            print("\n⚙️  Executing Agent Graph...")
            for _ in graph.stream({"query": query}, config=config):
                pass

            # ── Read Final State ─────────────────────────────────────────────
            state = graph.get_state(config).values

            # ── Build Validated Output Package ───────────────────────────────
            output_package = {
                "session_id": thread_id,
                "status": "success",
                "memo": None,
                "audit": None,
                "meta": {
                    "iterations": state.get("iterations"),
                    "is_approved": state.get("is_approved"),
                    "query_length": len(query),
                }
            }

            memo_obj = state.get("final_report_obj")
            audit_obj = state.get("audit_obj")

            if memo_obj:
                output_package["memo"] = memo_obj.model_dump()
            if audit_obj:
                output_package["audit"] = audit_obj.model_dump()

            print("\n" + "💎" + " FINAL JSON OUTPUT " + "=" * 41)
            print(json.dumps(output_package, indent=2))
            print("=" * 60 + "\n")

        except KeyboardInterrupt:
            logger.info("Interrupted by user.")
            break
        except Exception as e:
            logger.error(f"Unhandled error: {e}", exc_info=True)
            error_res = {
                "status": "error",
                "type": "SYSTEM_ERROR",
                "message": str(e)
            }
            print(json.dumps(error_res, indent=2))


if __name__ == "__main__":
    chat()
