#!/usr/bin/env python3

import asyncio
import subprocess
import json
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

async def test_favorite_number_server():
    """Test the favorite number MCP server"""
    
    # Start the server
    server_params = {
        "command": "python",
        "args": ["server.py"]
    }
    
    async with stdio_client(server_params) as streams:
        read_stream, write_stream = streams
        
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session
            init_result = await session.initialize()
            print(f"✓ Server initialized: {init_result.serverInfo.name}")
            
            # List available tools
            tools_result = await session.list_tools()
            print(f"✓ Available tools: {[tool.name for tool in tools_result.tools]}")
            
            # Call the tool
            result = await session.call_tool("get_users_favorite_number", {})
            print(f"✓ Tool result: {result.content[0].text}")
            
            # Verify the result
            assert result.content[0].text == "42"
            print("✓ Test passed! Favorite number is 42")

if __name__ == "__main__":
    asyncio.run(test_favorite_number_server())
