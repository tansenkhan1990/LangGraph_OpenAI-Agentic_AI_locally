"""
Question Classifier Agent using Ollama
This agent determines the category of a question
"""

from agents import Agent
from src.models.ollama_config import get_model_name

def create_classifier_agent():
    """
    Creates an agent that classifies questions into categories
    
    Since we're using Ollama, we need to configure the agent to use
    our local model through the OpenAI-compatible API
    """
    
    # For OpenAI Agents SDK, we need to set the model when running
    # We'll handle this in the node functions
    agent = Agent(
        name="Question Classifier",
        instructions="""You are a question classification expert.
        
        Your task: Classify questions into EXACTLY one of these categories:
        - "science" - Questions about physics, chemistry, biology, astronomy, technology
        - "history" - Questions about past events, historical figures, wars, timelines
        - "programming" - Questions about code, algorithms, programming languages, software
        
        IMPORTANT: Respond with ONLY the category name, nothing else.
        No explanations, no punctuation, just the single word.
        
        Examples:
        User: "What is photosynthesis?" → science
        User: "Who was Napoleon?" → history
        User: "How do I sort a list in Python?" → programming
        """,
        # We'll set the model dynamically when running
    )
    
    return agent