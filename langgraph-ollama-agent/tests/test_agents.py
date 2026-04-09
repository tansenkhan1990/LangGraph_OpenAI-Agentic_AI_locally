"""Tests for agents module"""

import pytest
from src.agents import QuestionClassifier, ScienceExpert, HistoryExpert, CodeExpert


@pytest.mark.asyncio
async def test_classifier():
    """Test question classifier."""
    classifier = QuestionClassifier()
    result = await classifier.classify("What is photosynthesis?")
    
    assert "category" in result
    assert result["question"] == "What is photosynthesis?"


@pytest.mark.asyncio
async def test_science_expert():
    """Test science expert agent."""
    expert = ScienceExpert()
    result = await expert.answer("What is photosynthesis?")
    
    assert "answer" in result
    assert result["question"] == "What is photosynthesis?"


@pytest.mark.asyncio
async def test_history_expert():
    """Test history expert agent."""
    expert = HistoryExpert()
    result = await expert.answer("What year did World War 2 end?")
    
    assert "answer" in result
    assert result["question"] == "What year did World War 2 end?"


@pytest.mark.asyncio
async def test_code_expert():
    """Test code expert agent."""
    expert = CodeExpert()
    result = await expert.answer("How do I create a list in Python?")
    
    assert "answer" in result
    assert result["question"] == "How do I create a list in Python?"
