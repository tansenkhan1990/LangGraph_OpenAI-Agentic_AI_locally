# LangGraph Ollama Multi-Agent System

A sophisticated multi-agent system built with LangGraph and Ollama that classifies questions and routes them to specialized expert agents for accurate responses.

## Features

- **Multi-Agent Architecture**: Specialized agents for Science, History, and Programming
- **Question Classification**: Automatically categorizes user questions
- **LangGraph Orchestration**: Graph-based workflow management
- **Ollama Integration**: Uses local Ollama models for privacy and cost-effectiveness
- **Custom Tools**: Calculator and web search capabilities
- **Async Support**: Fully asynchronous architecture for performance
- **Comprehensive Logging**: Built-in logging and monitoring
- **Docker Support**: Ready for containerization and deployment

## Project Structure

```
langgraph-ollama-agent/
├── src/
│   ├── agents/          # Specialized expert agents
│   ├── tools/           # Custom tools for agents
│   ├── graph/           # LangGraph workflow definitions
│   ├── models/          # Model configurations
│   ├── utils/           # Utility functions
│   └── main.py          # Application entry point
├── tests/               # Unit tests
├── notebooks/           # Jupyter notebooks for experimentation
├── scripts/             # Helper scripts
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md            # This file
```

## Prerequisites

- Python 3.8+
- Ollama (for running local LLMs)
- Docker & Docker Compose (optional, for containerization)

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd langgraph-ollama-agent
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Install and run Ollama:**
Visit https://ollama.ai to download and install Ollama.
Once installed, download a model:
```bash
ollama pull mistral
```

## Usage

### Interactive Mode
```bash
python src/main.py --interactive
```

### Run a Single Query
```bash
python src/main.py
```

### Run Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

## Configuration

### Environment Variables

- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model name to use (default: mistral)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `DEBUG`: Enable debug mode (True/False)

### Supported Models

- `mistral` - Mistral 7B (recommended for balance)
- `neural-chat` - NeuralChat 7B
- `zephyr` - Zephyr 7B (better instruction following)
- `llama2` - Llama 2 70B (more capable, requires more resources)

## Docker Deployment

### Build Image
```bash
docker build -t langgraph-ollama-agent .
```

### Run with Docker Compose
```bash
docker-compose up
```

## API Usage

### Basic Example
```python
from src.graph import build_graph, GraphState

graph = build_graph()
state = GraphState(user_input="What is photosynthesis?")
result = await graph.ainvoke(state)
print(result.final_answer)
```

## Architecture

### Agent Flow

```
User Input
    ↓
[Classifier Agent] - Categorizes the question
    ↓
[Router] - Selects appropriate expert agent
    ↓
[Expert Agent] - One of:
  - Science Expert
  - History Expert
  - Code Expert
  - General Agent
    ↓
[Synthesis Node] - Formats final answer
    ↓
Final Answer
```

## Testing

The project includes comprehensive unit tests:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src
```

## Development

### Code Style
- Use Black for formatting: `black src/`
- Use isort for imports: `isort src/`
- Use flake8 for linting: `flake8 src/`
- Use mypy for type checking: `mypy src/`

### Running All Checks
```bash
./scripts/test_all.sh
```

## Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check the base URL in .env matches your Ollama setup
- Test connection: `python scripts/test_ollama.py`

### Module Import Errors
- Ensure you're in the project root directory
- Verify virtual environment is activated
- Check PYTHONPATH includes the project root

### Memory Issues
- Use a smaller model (mistral, neural-chat)
- Reduce context size in model configuration
- Consider using quantized versions of models

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Future Enhancements

- [ ] Memory/conversation history integration
- [ ] Tool calling for web search and calculations
- [ ] Multi-turn conversation support
- [ ] Response streaming
- [ ] Custom prompt templates
- [ ] RAG (Retrieval Augmented Generation) support
- [ ] Monitoring and analytics dashboard
- [ ] Performance optimization

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainers.

## Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [LangChain Documentation](https://python.langchain.com)
