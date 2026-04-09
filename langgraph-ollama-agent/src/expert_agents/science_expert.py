"""Science Expert Agent"""

from agents import Agent

def create_science_agent():
    """Creates a science expert agent"""
    
    agent = Agent(
        name="Science Expert",
        instructions="""You are a knowledgeable science professor.
        
        Answer the user's science question clearly and accurately.
        Use simple language and provide examples when helpful.
        
        If you're unsure about something, admit it rather than guessing.
        Keep answers concise but informative (2-3 paragraphs maximum).
        """,
    )
    
    return agent