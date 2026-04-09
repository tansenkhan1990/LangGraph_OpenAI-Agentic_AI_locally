"""Input Validators - Validation functions for user input and data"""

from typing import Dict, Any, Optional
import re


def validate_input(text: str, min_length: int = 1, max_length: int = 5000) -> Dict[str, Any]:
    """
    Validate user input text.
    
    Args:
        text: Input text to validate
        min_length: Minimum length required
        max_length: Maximum length allowed
        
    Returns:
        Dictionary with validation result
    """
    errors = []
    
    if not text:
        errors.append("Input cannot be empty")
    elif len(text) < min_length:
        errors.append(f"Input must be at least {min_length} characters")
    elif len(text) > max_length:
        errors.append(f"Input cannot exceed {max_length} characters")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "length": len(text),
    }


def validate_question(question: str) -> Dict[str, Any]:
    """
    Validate a question string.
    
    Args:
        question: Question to validate
        
    Returns:
        Dictionary with validation result
    """
    validation = validate_input(question, min_length=5, max_length=1000)
    
    # Additional question validation
    if validation["valid"]:
        # Check if it looks like a question
        if not any(q in question for q in ["?", "how", "what", "why", "when", "where", "who"]):
            validation["valid"] = False
            validation["errors"].append("Input does not appear to be a valid question")
    
    return validation


def validate_category(category: str) -> Dict[str, Any]:
    """
    Validate a question category.
    
    Args:
        category: Category to validate
        
    Returns:
        Dictionary with validation result
    """
    valid_categories = ["science", "history", "programming", "general"]
    
    return {
        "valid": category.lower() in valid_categories,
        "errors": [] if category.lower() in valid_categories else [f"Invalid category: {category}"],
        "category": category.lower(),
    }
