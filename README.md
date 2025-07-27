# Simplest MCP Ever

This repository demonstrates a minimal, working example of a [Modular Code Platform (MCP)](https://modcode.org/) server.  It's designed to be a starting point for developers looking to understand and build their own MCP-compatible tools and applications.

## What is MCP?

MCP enables a modular, tool-centric approach to software development.  An MCP server exposes a set of tools that client applications can discover and invoke.  This fosters interoperability and composability across different systems.

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

## Understanding the Code

*   **`server.py`**: Pay close attention to the `@app.list_tools()` and `@app.call_tool()` decorators. These link functions to particular MCP functionalities.  The `list_tools` has to provide a *list* of `Tool` types, and the `call_tool` can call different functions depending on the tool `name`.

*   **`test_mcp.py`**:  This illustrates how MCP clients connect to servers and call tools. It showcases the initialization process, tool discovery, and tool invocation. Using `StdioServerParameters` as the server paramater for client is critical to allowing the client to communicate correctly with the server.

## Expanding the Example

This example serves as a foundation. You can extend it by:

*   **Adding more tools:** Define new functions decorated with `@app.call_tool()` to expose more functionality. Don't forget to add their definitions to the `list_tools` call.
*   **Accepting arguments:** Modify the tool's input schema and the `call_tool` function to accept arguments from the client.
*   **Connecting to external systems:** Integrate the tools with databases, APIs, or other services to perform real-world tasks.
*   **Using more sophisticated return values:** Using the `TextContent` to return results helps standardise output.

## Resources

*   **[Modular Code Platform (MCP) Specification](https://modcode.org/)**: The official documentation for the MCP standard. Be sure to read up on this when creating tools with more functionality.

This simple example should provide a solid entry point for exploring the world of MCP and building your own interoperable applications!
```
