#!/usr/bin/env python3
"""
Test script to verify Ollama is working correctly
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.ollama_config import test_ollama_connection, get_ollama_client, get_model_name

async def test_simple_chat():
    """Test a simple chat with Ollama"""
    print("\n🧪 Testing simple chat with Ollama...")
    
    client = get_ollama_client()
    model = get_model_name()
    
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Be brief."},
            {"role": "user", "content": "Say 'Hello from Ollama!'"}
        ],
        max_tokens=50,
        temperature=0.7,
    )
    
    print(f"\n📝 Response: {response.choices[0].message.content}")
    print(f"📊 Token usage: {response.usage}")

async def main():
    print("="*50)
    print("OLLAMA CONNECTION TEST")
    print("="*50)
    
    # Test connection
    if not await test_ollama_connection():
        print("\n❌ Ollama connection failed!")
        return
    
    # Test simple chat
    await test_simple_chat()
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())