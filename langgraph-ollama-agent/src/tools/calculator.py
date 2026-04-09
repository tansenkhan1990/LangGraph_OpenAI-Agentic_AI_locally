"""
Calculator tool for the agents
This demonstrates how to add tools to OpenAI Agents SDK
"""

from agents import function_tool

@function_tool
async def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression
    
    Args:
        expression: A mathematical expression like "2 + 2" or "sqrt(16)"
    
    Returns:
        The计算结果 as a string
    """
    import math
    
    # Allowed functions for safety
    safe_dict = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sqrt': math.sqrt,
        'pow': pow,
        'pi': math.pi,
        'e': math.e,
    }
    
    try:
        # Evaluate safely
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"The result of {expression} is: {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"