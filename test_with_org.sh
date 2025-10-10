#!/bin/bash
# Copyright 2025 Varun Bhardwaj
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Your GCP configuration
ORG_ID="1035865795181"
PROJECT_ID="csc-audit-test-project"

echo "=========================================="
echo "Testing Compliance Manager Extension"
echo "=========================================="
echo ""
echo "Organization ID: $ORG_ID"
echo "Project ID: $PROJECT_ID"
echo ""

# Check authentication
echo "Checking Google Cloud authentication..."
if gcloud auth application-default print-access-token &> /dev/null; then
    echo -e "${GREEN}✓ Authentication configured${NC}"
else
    echo -e "${RED}✗ Authentication not configured${NC}"
    echo "Please run: gcloud auth application-default login"
    exit 1
fi

# Check if extension is installed
echo ""
echo "Checking extension installation..."
if [ -d "$HOME/.gemini/extensions/compliance-manager" ]; then
    echo -e "${GREEN}✓ Extension is installed${NC}"
else
    echo -e "${YELLOW}⚠ Extension not found${NC}"
    echo "Run ./install.sh to install the extension"
    exit 1
fi

# Test Python imports
echo ""
echo "Testing Python dependencies..."
python3 test_extension.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All dependencies are installed${NC}"
else
    echo -e "${RED}✗ Some dependencies are missing${NC}"
    exit 1
fi

# Provide test commands
echo ""
echo "=========================================="
echo "Extension is ready to use!"
echo "=========================================="
echo ""
echo "Try these commands in Gemini CLI:"
echo ""
echo -e "${GREEN}1. List all frameworks:${NC}"
echo "   > @compliance-manager-mcp list_frameworks organization_id=\"$ORG_ID\""
echo ""
echo -e "${GREEN}2. List cloud controls:${NC}"
echo "   > @compliance-manager-mcp list_cloud_controls organization_id=\"$ORG_ID\""
echo ""
echo -e "${GREEN}3. List framework deployments (organization):${NC}"
echo "   > @compliance-manager-mcp list_framework_deployments parent=\"organizations/$ORG_ID\""
echo ""
echo -e "${GREEN}4. List framework deployments (project):${NC}"
echo "   > @compliance-manager-mcp list_framework_deployments parent=\"projects/$PROJECT_ID\""
echo ""
echo -e "${GREEN}5. Natural language query:${NC}"
echo "   > Show me all compliance frameworks available in organization $ORG_ID"
echo ""
echo -e "${YELLOW}To start Gemini CLI, run:${NC}"
echo "   gemini"
echo ""

