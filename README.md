┌─────────────────────────────────────────────────────────────┐
│                      MAIN APPLICATION                        │
│                         (main.py)                            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    LANGGGRAPH WORKFLOW                       │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  CLASSIFIER  │───▶│   ROUTER     │───▶│   EXPERT     │  │
│  │    Node      │    │ (Conditional │    │    Node      │  │
│  │              │    │    Edge)     │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                    │          │
│         │                   │                    │          │
│         ▼                   ▼                    ▼          │
│  ┌──────────────────────────────────────────────────────┐  │

│  │              OPENAI AGENTS SDK


User Input → Classifier → Router → Expert → Answer
                ↓           ↓         ↓
            Categories   Decision   Science/History/Code




 langgraph-ollama-agent/
│
├── .env                          # Your environment variables
├── .gitignore                    # Git ignore file
├── requirements.txt              # Dependencies
├── README.md                     # Project documentation
├── docker-compose.yml            # Optional: For containerization
├── Dockerfile                    # Optional: For deployment
│
├── src/                          # Source code
│   ├── __init__.py
│   │
│   ├── agents/                   # OpenAI Agents SDK agents
│   │   ├── __init__.py
│   │   ├── classifier.py         # Question classifier agent
│   │   ├── science_expert.py     # Science expert agent
│   │   ├── history_expert.py     # History expert agent
│   │   └── code_expert.py        # Programming expert agent
│   │
│   ├── tools/                    # Custom tools for agents
│   │   ├── __init__.py
│   │   ├── calculator.py         # Math tool
│   │   └── web_search.py         # DuckDuckGo search tool
│   │
│   ├── graph/                    # LangGraph workflow
│   │   ├── __init__.py
│   │   ├── state.py              # State definitions
│   │   ├── nodes.py              # Graph nodes
│   │   ├── edges.py              # Conditional edges
│   │   └── builder.py            # Graph builder
│   │
│   ├── models/                   # Model configurations
│   │   ├── __init__.py
│   │   └── ollama_config.py      # Ollama setup
│   │
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py             # Logging setup
│   │   └── validators.py         # Input validation
│   │
│   └── main.py                   # Application entry point
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_graph.py
│   └── test_tools.py
│
├── notebooks/                    # Jupyter notebooks for experimentation
│   └── experiments.ipynb
│
├── logs/                         # Log files (gitignored)
│   └── .gitkeep
│
└── scripts/                      # Helper scripts
    ├── setup.sh                  # Setup script for Linux/Mac
    ├── setup.ps1                 # Setup script for Windows
    └── test_ollama.py            # Test Ollama connection           




# Create project directory
mkdir langgraph-ollama-agent
cd langgraph-ollama-agent

# Create directory structure
mkdir -p src/agents src/tools src/graph src/models src/utils
mkdir -p tests notebooks logs scripts

# Create empty __init__.py files
touch src/__init__.py
touch src/agents/__init__.py
touch src/tools/__init__.py
touch src/graph/__init__.py
touch src/models/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

# Create log directory placeholder
touch logs/.gitkeep    