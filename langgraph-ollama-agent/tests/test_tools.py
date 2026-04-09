"""Tests for tools module"""

import pytest
from src.tools import Calculator, WebSearch


@pytest.mark.asyncio
async def test_calculator():
    """Test calculator tool."""
    calc = Calculator()
    
    assert calc.add(2, 3) == 5
    assert calc.subtract(5, 3) == 2
    assert calc.multiply(2, 3) == 6
    assert calc.divide(6, 2) == 3
    assert calc.power(2, 3) == 8


@pytest.mark.asyncio
async def test_calculator_division_by_zero():
    """Test calculator division by zero."""
    calc = Calculator()
    
    with pytest.raises(ValueError):
        calc.divide(10, 0)


@pytest.mark.asyncio
async def test_calculator_expression():
    """Test calculator expression evaluation."""
    calc = Calculator()
    result = await calc.calculate("2 + 2")
    
    assert result["success"] is True
    assert result["result"] == 4


@pytest.mark.asyncio
async def test_web_search():
    """Test web search tool."""
    search = WebSearch()
    result = await search.search("Python programming")
    
    assert "query" in result
    assert result["query"] == "Python programming"
