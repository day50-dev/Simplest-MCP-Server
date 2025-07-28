# Simplest MCP Ever

This repository demonstrates a minimal, working example of an MCP server and client. There's no LLM involved, this uses what's called the "stdio" method.

However, there are branches that introduce things such as LLMs. After understanding the base code, go to the various branches to see how things get stacked on top.

## Functionality

This example server exposes a single tool:

*   **`get_users_favorite_number`**: This tool, when called, simply returns the string "42" as the user's favorite number.  This is a *very* basic example illustrating the server's capability to expose tools and return results.

## Repository Contents

*   **`server.py`**: This is the core of the MCP server. It defines:
    *   The server initialization (`Server("favorite-number-server")`).
    *   The `list_tools` function, responsible for providing the list of available tools to the client.
    *   The `call_tool` function, which handles the execution of the tool based on the tool name and arguments.

*   **`test_mcp.py`**: This file contains an automated test for the MCP server. It connects to the server, lists the available tools, calls the `get_users_favorite_number` tool, and asserts that the returned value is "42".

*   **`test.sh`**: A simple shell script to execute the tests. It activates the virtual environment (if one exists) before running the test to ensure dependencies are correctly managed.


## Getting Started

Follow these steps to run the example:

3.  **Set up a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate  # On Windows
    ```

4.  **Install the `mcp` library:**

    ```bash
    python3 -m pip install mcp
    ```

5.  **Run the Tests:**

    ```bash
    ./test.sh
    ```

    This script will:
    *   Activate the virtual environment (if it exists).
    *   Execute the `test_mcp.py` file, which will start the server, connect to it, call the tool, and verify the results.

    If the test passes, you'll see the following output (or similar):

    ```
    🧪 Testing Favorite Number MCP Server
    ✓ Server initialized: favorite-number-server
    ✓ Available tools: ['get_users_favorite_number']
    ✓ Tool result: 42
    ✓ Test passed! Favorite number is 42
    ✅ All tests passed!
    ```

