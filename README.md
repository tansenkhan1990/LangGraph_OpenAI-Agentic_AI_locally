# 🤖 AI Knowledge Hub (Multi-Agent System)

An industry-standard implementation of a **Local-First Knowledge Assistant** using **LangGraph** for orchestration and the **OpenAI Agent SDK** (pointing to **Ollama**) for agentic intelligence.

## 🌟 Key Features
- **Local-First Logic**: Prioritizes internal JSON data before escalating to web search.
- **Multi-Agent Handoff**: Separates the 'Librarian' (internal) from the 'Researcher' (web).
- **Dynamic Routing**: Uses LangGraph conditional edges to decide the execution path.
- **Modern Stack**: Built with `uv` for lightning-fast dependency management.

## 🏗️ Architecture
The system follows a Directed Acyclic Graph (DAG) structure:
1. **DB Lookup**: Checks `data/knowledge.json`.
2. **Conditional Path**: 
   - Found? -> **Librarian Agent** (Explains policy).
   - Missing? -> **Researcher Agent** (DuckDuckGo Search).
3. **Auditor (Future)**: Validates output quality.



## 🚀 Setup & Installation

### Prerequisites
- [Ollama](https://ollama.com/) installed and running.
- The `qwen3-vl:235b-cloud` model pulled (or a smaller alternative like `llama3`).
- [uv](https://github.com/astral-sh/uv) installed.

### Installation
1. Clone the repo.
2. Configure your `.env` (use the provided template).
3. Install dependencies:
   ```bash
   uv sync