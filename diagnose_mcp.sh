#!/bin/bash
# Diagnostic script to check MCP server status

echo "=========================================="
echo "MCP Server Diagnostic"
echo "=========================================="
echo ""

# Check if extension files exist
echo "1. Checking extension files..."
if [ -d "$HOME/.gemini/extensions/compliance-manager" ]; then
    echo "✓ Extension directory exists"
    ls -la "$HOME/.gemini/extensions/compliance-manager/"
else
    echo "✗ Extension directory NOT found"
    exit 1
fi

echo ""
echo "2. Checking gemini-extension.json..."
cat "$HOME/.gemini/extensions/compliance-manager/gemini-extension.json"

echo ""
echo "3. Testing MCP server manually..."
cd "$HOME/.gemini/extensions/compliance-manager"

# Try to start the MCP server and send a test request
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | timeout 10 /opt/homebrew/bin/uv run compliance_manager_mcp.py 2>&1 | head -20

echo ""
echo "=========================================="
echo "Diagnostic complete"
echo "=========================================="

