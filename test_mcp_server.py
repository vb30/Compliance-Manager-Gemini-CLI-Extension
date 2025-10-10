#!/usr/bin/env python3
"""Test script to verify MCP server is exposing tools correctly."""

import subprocess
import json
import sys

def test_mcp_server():
    """Test the MCP server by sending a tools/list request."""
    
    # MCP initialize request
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    # MCP tools/list request
    tools_list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    try:
        # Start the MCP server
        process = subprocess.Popen(
            ["/opt/homebrew/bin/uv", "--directory", 
             "/Users/varunbhardwaj/.gemini/extensions/compliance-manager",
             "run", "compliance_manager_mcp.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send initialize request
        process.stdin.write(json.dumps(initialize_request) + "\n")
        process.stdin.flush()

        # Read initialize response
        init_response = process.stdout.readline()
        print("Initialize response:", init_response)

        # Send initialized notification (required by MCP protocol)
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        process.stdin.write(json.dumps(initialized_notification) + "\n")
        process.stdin.flush()

        # Send tools/list request
        process.stdin.write(json.dumps(tools_list_request) + "\n")
        process.stdin.flush()

        # Read tools/list response
        tools_response = process.stdout.readline()
        print("\nTools list response:", tools_response)
        
        if tools_response:
            try:
                tools_data = json.loads(tools_response)
                if "result" in tools_data and "tools" in tools_data["result"]:
                    tools = tools_data["result"]["tools"]
                    print(f"\n✓ Found {len(tools)} tools:")
                    for tool in tools:
                        print(f"  - {tool.get('name', 'unknown')}")
                else:
                    print("\n✗ No tools found in response")
                    print("Response structure:", json.dumps(tools_data, indent=2))
            except json.JSONDecodeError as e:
                print(f"\n✗ Failed to parse response: {e}")
        
        # Terminate the process
        process.terminate()
        process.wait(timeout=5)
        
    except Exception as e:
        print(f"\n✗ Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mcp_server()

