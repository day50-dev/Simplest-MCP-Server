#!/bin/bash

set -e

echo "🧪 Testing Favorite Number MCP Server"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the test
python test_mcp.py

echo "✅ All tests passed!"
