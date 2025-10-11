#!/bin/bash
# Fix script for GCP Cloud Shell installation

set -e

echo "=========================================="
echo "Fixing Compliance Manager Extension"
echo "for GCP Cloud Shell"
echo "=========================================="
echo ""

# Check if extension directory exists
EXTENSION_DIR="$HOME/.gemini/extensions/compliance-manager"

if [ ! -d "$EXTENSION_DIR" ]; then
    echo "Error: Extension directory not found at $EXTENSION_DIR"
    echo "Please run ./install.sh first"
    exit 1
fi

echo "Extension directory found: $EXTENSION_DIR"

# Create run_mcp.sh if it doesn't exist
echo ""
echo "Creating run_mcp.sh wrapper script..."
cat > "$EXTENSION_DIR/run_mcp.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

# Suppress all Google Cloud and Python logging
export GRPC_VERBOSITY=ERROR
export GLOG_minloglevel=3
export PYTHONUNBUFFERED=1

# Run Python with stderr redirected to /dev/null
exec .venv/bin/python3 -W ignore compliance_manager_mcp.py 2>/dev/null
EOF

chmod +x "$EXTENSION_DIR/run_mcp.sh"
echo "✓ Created and made executable: $EXTENSION_DIR/run_mcp.sh"

# Update gemini-extension.json with absolute path
echo ""
echo "Updating gemini-extension.json..."
cat > "$EXTENSION_DIR/gemini-extension.json" << EOF
{
  "name": "compliance-manager",
  "version": "1.0.0",
  "description": "Google Cloud Compliance Manager extension for Gemini CLI",
  "mcpServers": {
    "compliance-manager-mcp": {
      "command": "$EXTENSION_DIR/run_mcp.sh",
      "args": [],
      "env": {}
    }
  },
  "contextFileName": "GEMINI.md"
}
EOF

echo "✓ Updated gemini-extension.json with absolute path"

# Verify files exist
echo ""
echo "Verifying installation..."
if [ -f "$EXTENSION_DIR/run_mcp.sh" ]; then
    echo "✓ run_mcp.sh exists"
else
    echo "✗ run_mcp.sh missing"
    exit 1
fi

if [ -x "$EXTENSION_DIR/run_mcp.sh" ]; then
    echo "✓ run_mcp.sh is executable"
else
    echo "✗ run_mcp.sh is not executable"
    exit 1
fi

if [ -f "$EXTENSION_DIR/compliance_manager_mcp.py" ]; then
    echo "✓ compliance_manager_mcp.py exists"
else
    echo "✗ compliance_manager_mcp.py missing"
    exit 1
fi

if [ -d "$EXTENSION_DIR/.venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "✗ Virtual environment missing"
    exit 1
fi

# Test the MCP server
echo ""
echo "Testing MCP server..."
if echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | "$EXTENSION_DIR/run_mcp.sh" | grep -q "jsonrpc"; then
    echo "✓ MCP server responds correctly"
else
    echo "✗ MCP server test failed"
    echo ""
    echo "Trying to run MCP server to see errors..."
    echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | "$EXTENSION_DIR/run_mcp.sh"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Fix completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Restart Gemini CLI (exit and run 'gemini' again)"
echo "2. Press Ctrl+T to verify the server is connected"
echo "3. Try: 'List all compliance frameworks in organization 1035865795181'"
echo ""

