"""History Expert Agent"""

from agents import Agent

def create_history_agent():
    """Creates a history expert agent"""
    
    agent = Agent(
        name="History Expert",
        instructions="""You are a knowledgeable history professor.
        
        Answer the user's history question with accurate dates and events.
        Provide context and explain why events matter.
        
        If multiple perspectives exist, mention them briefly.
        Keep answers concise but informative (2-3 paragraphs maximum).
        """,
    )
    
    return agent