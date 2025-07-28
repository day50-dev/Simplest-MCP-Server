#!/usr/bin/env python3
"""
Test client for LLM tool calling
"""

import requests
import json

class ToolHandler:
    """Handles tool execution"""
    
    @staticmethod
    def get_favorite_number(user_id):
        """Mock tool that returns user's favorite number"""
        # Mock database of favorite numbers
        favorites = {
            "user123": 42,
            "alice": 7,
            "bob": 13,
            "default": 42
        }
        return favorites.get(user_id, favorites["default"])

def call_llm(prompt, server_url="http://localhost:5000"):
    """Call the LLM server"""
    try:
        response = requests.post(
            f"{server_url}/generate",
            json={
                "prompt": prompt,
                "max_length": 200,
                "temperature": 0.7
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None

def execute_tool_call(tool_call):
    """Execute a tool call and return the result"""
    if not tool_call:
        return None
    
    tool_name = tool_call.get('name')
    parameters = tool_call.get('parameters', {})
    
    if tool_name == 'get_favorite_number':
        user_id = parameters.get('user_id', 'default')
        result = ToolHandler.get_favorite_number(user_id)
        return f"Your favorite number is {result}"
    
    return f"Unknown tool: {tool_name}"

def test_favorite_number():
    """Test the favorite number scenario"""
    print("=== Testing Favorite Number Tool Call ===")
    
    # Test prompts that should trigger tool calls
    test_prompts = [
        "What's my favorite number?",
        "Can you tell me my favorite number?",
        "I forgot my favorite number, can you help?",
        "What number do I like best?"
    ]
    
    for prompt in test_prompts:
        print(f"\n--- Testing prompt: '{prompt}' ---")
        
        # Call LLM
        result = call_llm(prompt)
        if not result:
            print("Failed to get response from LLM")
            continue
        
        print(f"LLM Response: {result['response']}")
        
        # Check for tool call
        tool_call = result.get('tool_call')
        if tool_call:
            print(f"Tool call detected: {tool_call}")
            
            # Execute tool call
            tool_result = execute_tool_call(tool_call['tool_call'] if 'tool_call' in tool_call else tool_call)
            print(f"Tool result: {tool_result}")
            
            # You could send the tool result back to the LLM for final response
            follow_up_prompt = f"The tool returned: {tool_result}. Please provide a natural response to the user."
            follow_up = call_llm(follow_up_prompt)
            if follow_up:
                print(f"Final response: {follow_up['response']}")
        else:
            print("No tool call detected")

def test_non_tool_prompt():
    """Test a prompt that shouldn't trigger tools"""
    print("\n=== Testing Non-Tool Prompt ===")
    
    prompt = "What's the weather like today?"
    print(f"Testing prompt: '{prompt}'")
    
    result = call_llm(prompt)
    if result:
        print(f"LLM Response: {result['response']}")
        print(f"Tool call: {result.get('tool_call', 'None')}")

def main():
    print("Tool Calling Test Client")
    print("Make sure the LLM server is running on localhost:5000")
    print("-" * 50)
    
    # Check if server is up
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✓ LLM server is running")
        else:
            print("✗ LLM server health check failed")
            return
    except:
        print("✗ Cannot connect to LLM server")
        print("Start the server with: python llm_server.py")
        return
    
    # Run tests
    test_favorite_number()
    test_non_tool_prompt()
    
    print("\n=== Interactive Testing ===")
    print("Type prompts to test (or 'quit' to exit):")
    
    while True:
        try:
            prompt = input("\nYou: ").strip()
            if prompt.lower() in ['quit', 'exit', 'q']:
                break
            
            if not prompt:
                continue
            
            result = call_llm(prompt)
            if result:
                print(f"LLM: {result['response']}")
                
                tool_call = result.get('tool_call')
                if tool_call:
                    print(f"[Tool call: {tool_call}]")
                    tool_result = execute_tool_call(tool_call['tool_call'] if 'tool_call' in tool_call else tool_call)
                    print(f"[Tool result: {tool_result}]")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
