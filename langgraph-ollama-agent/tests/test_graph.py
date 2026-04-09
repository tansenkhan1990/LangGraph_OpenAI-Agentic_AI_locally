"""Tests for graph module"""

import pytest
from src.graph import GraphState, build_graph


def test_graph_state_initialization():
    """Test GraphState initialization."""
    state = GraphState(user_input="Test question")
    
    assert state.user_input == "Test question"
    assert state.question_category == ""
    assert state.final_answer == ""
    assert state.error == ""


def test_graph_state_to_dict():
    """Test GraphState to_dict method."""
    state = GraphState(
        user_input="Test",
        question_category="science",
        final_answer="Test answer"
    )
    
    result = state.to_dict()
    
    assert result["user_input"] == "Test"
    assert result["question_category"] == "science"
    assert result["final_answer"] == "Test answer"


def test_build_graph():
    """Test graph building."""
    graph = build_graph()
    
    assert graph is not None
