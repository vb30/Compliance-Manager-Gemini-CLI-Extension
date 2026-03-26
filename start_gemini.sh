# TODO(vermaharsh): remove this file before making this public
#!/bin/bash
./install.sh
# Set Google Cloud Project
export GOOGLE_CLOUD_PROJECT="control-testing-13-473714"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Starting Gemini CLI with Audit and Compliance Manager Extension"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo ""

# Start Gemini CLI
gemini --debug --model gemini-3.1-pro-preview

