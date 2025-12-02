"""Tests for the cat facts MCP server."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from cat_facts_mcp.server import app, call_tool, list_tools
from mcp.types import TextContent


@pytest.mark.asyncio
async def test_list_tools():
    """Test that the server lists the get_cat_fact tool."""
    tools = await list_tools()
    assert len(tools) == 1
    assert tools[0].name == "get_cat_fact"
    assert tools[0].description == "Get a random cat fact from the meowfacts API"
    assert tools[0].inputSchema["type"] == "object"
    assert tools[0].inputSchema["required"] == []


@pytest.mark.asyncio
async def test_call_tool_success():
    """Test successful API call."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": ["Cats have individual preferences for scratching surfaces and angles."]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        result = await call_tool("get_cat_fact", {})
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert result[0].type == "text"
        assert "Cats have individual preferences" in result[0].text


@pytest.mark.asyncio
async def test_call_tool_empty_data():
    """Test API call with empty data."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_response.raise_for_status = MagicMock()
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        
        result = await call_tool("get_cat_fact", {})
        
        assert len(result) == 1
        assert result[0].text == "No cat fact available"


@pytest.mark.asyncio
async def test_call_tool_http_error():
    """Test API call with HTTP error."""
    import httpx
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_get = AsyncMock(side_effect=httpx.HTTPError("Connection error"))
        mock_client.return_value.__aenter__.return_value.get = mock_get
        
        result = await call_tool("get_cat_fact", {})
        
        assert len(result) == 1
        assert "Error fetching cat fact" in result[0].text


@pytest.mark.asyncio
async def test_call_tool_unknown_tool():
    """Test calling an unknown tool."""
    with pytest.raises(ValueError, match="Unknown tool"):
        await call_tool("unknown_tool", {})
