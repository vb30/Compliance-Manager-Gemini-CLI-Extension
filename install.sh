#!/bin/bash
# Simple installation script for Compliance Manager Gemini CLI Extension

set -e

echo "Installing Compliance Manager Gemini CLI Extension..."
echo ""

# Check prerequisites
if ! command -v gemini &> /dev/null; then
    echo "❌ Gemini CLI not found. Install it first:"
    echo "   npm install -g @google/gemini-cli"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11 or higher."
    exit 1
fi

echo "✓ Prerequisites found"

# Create extension directory
EXTENSION_DIR="$HOME/.gemini/extensions/compliance-manager"
mkdir -p "$EXTENSION_DIR"

# Create virtual environment (isolates dependencies from system Python)
echo "Creating virtual environment..."
python3 -m venv "$EXTENSION_DIR/.venv"

# Install dependencies using pip
echo "Installing dependencies..."
"$EXTENSION_DIR/.venv/bin/pip" install -q --upgrade pip

# Use requirements.txt if available, otherwise install directly
if [ -f "requirements.txt" ]; then
    "$EXTENSION_DIR/.venv/bin/pip" install -q -r requirements.txt
else
    "$EXTENSION_DIR/.venv/bin/pip" install -q \
        httpx>=0.28.1 \
        "mcp[cli]>=1.4.1" \
        python-dotenv>=1.0.0 \
        typing-extensions>=4.8.0 \
        aiohttp>=3.9.0 \
        google-cloud-cloudsecuritycompliance>=0.2.0
fi

# Copy files
echo "Copying extension files..."
cp compliance_manager_mcp.py "$EXTENSION_DIR/"
cp GEMINI.md "$EXTENSION_DIR/"

# Create run script
# MCP requires clean JSON on stdout - all logging goes to stderr and is suppressed
cat > "$EXTENSION_DIR/run_mcp.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

# Suppress all logging - MCP requires clean JSON on stdout
export GRPC_VERBOSITY=ERROR
export GLOG_minloglevel=3
export PYTHONUNBUFFERED=1

# Run MCP server
# Logging now goes to stderr (configured in compliance_manager_mcp.py)
# Redirect stderr to /dev/null to keep output clean for JSON-RPC
exec .venv/bin/python3 -W ignore compliance_manager_mcp.py 2> /tmp/mcpComp.log
EOF
chmod +x "$EXTENSION_DIR/run_mcp.sh"

# Create extension config
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

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Authenticate with Google Cloud:"
echo "   gcloud auth application-default login"
echo ""
echo "2. Start Gemini CLI:"
echo "   gemini"
echo ""
echo "3. Test the extension:"
echo "   List all compliance frameworks in organization YOUR_ORG_ID"
echo ""

