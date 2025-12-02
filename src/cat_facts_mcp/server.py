"""Cat Facts MCP Server

An MCP server that provides random cat facts from meowfacts.herokuapp.com
"""

import asyncio
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

app = Server("cat-facts-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_cat_fact",
            description="Get a random cat fact from the meowfacts API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "get_cat_fact":
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get("https://meowfacts.herokuapp.com/")
                response.raise_for_status()
                data = response.json()
                
                # Extract the fact from the data array
                if "data" in data and len(data["data"]) > 0:
                    fact = data["data"][0]
                    return [TextContent(type="text", text=fact)]
                else:
                    return [TextContent(type="text", text="No cat fact available")]
            except httpx.HTTPError as e:
                return [TextContent(type="text", text=f"Error fetching cat fact: {str(e)}")]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point for the server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
