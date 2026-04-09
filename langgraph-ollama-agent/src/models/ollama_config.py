"""
Ollama configuration for OpenAI Agents SDK
Since Ollama provides an OpenAI-compatible API, we can use the OpenAI client
"""

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_ollama_client():
    """
    Create an OpenAI-compatible client for Ollama
    
    Ollama runs locally and provides the same API as OpenAI,
    so we can use the OpenAI client with a custom base URL
    """
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    api_key = os.getenv("OLLAMA_API_KEY", "ollama")  # Ollama doesn't need a real key
    
    client = AsyncOpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=60.0,  # Longer timeout for local models
        max_retries=2,
    )
    
    return client

def get_model_name():
    """Get the model name from environment variables"""
    return os.getenv("LOCAL_MODEL_NAME", "qwen3-vl:235b-cloud")

# Test the connection
async def test_ollama_connection():
    """Test if Ollama is running and model is available"""
    try:
        client = get_ollama_client()
        response = await client.chat.completions.create(
            model=get_model_name(),
            messages=[{"role": "user", "content": "Say 'OK' if you can hear me"}],
            max_tokens=10,
        )
        print("✅ Ollama connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("\nPlease make sure:")
        print("1. Ollama is installed (https://ollama.ai)")
        print("2. Run: ollama pull qwen3-vl:235b-cloud")
        print("3. Run: ollama serve")
        return False