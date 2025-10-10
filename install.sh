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

echo "=========================================="
echo "Compliance Manager Gemini CLI Extension"
echo "Installation Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "$1"
}

# Check if Gemini CLI is installed
echo "Checking prerequisites..."
if ! command -v gemini &> /dev/null; then
    print_error "Gemini CLI is not installed"
    print_info "Please install it first: npm install -g @google/gemini-cli"
    exit 1
fi
print_success "Gemini CLI is installed"

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "Python 3.11 or higher is required (found $PYTHON_VERSION)"
    exit 1
fi
print_success "Python $PYTHON_VERSION is installed"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    print_warning "uv is not installed"
    print_info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source the shell configuration to get uv in PATH
    if [ -f "$HOME/.bashrc" ]; then
        source "$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        source "$HOME/.zshrc"
    fi
    
    if ! command -v uv &> /dev/null; then
        print_error "Failed to install uv"
        exit 1
    fi
fi
print_success "uv is installed"

# Get the full path to uv
UV_PATH=$(which uv)
print_info "uv path: $UV_PATH"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
uv pip install --system -e .
print_success "Python dependencies installed"

# Determine installation directory
echo ""
print_info "Where would you like to install the extension?"
print_info "1) User-level (~/.gemini/extensions) [Recommended]"
print_info "2) Project-level (./.gemini/extensions)"
read -p "Enter choice [1]: " INSTALL_CHOICE
INSTALL_CHOICE=${INSTALL_CHOICE:-1}

if [ "$INSTALL_CHOICE" = "1" ]; then
    EXTENSION_DIR="$HOME/.gemini/extensions/compliance-manager"
else
    EXTENSION_DIR="./.gemini/extensions/compliance-manager"
fi

# Create extension directory
echo ""
echo "Creating extension directory..."
mkdir -p "$EXTENSION_DIR"
print_success "Extension directory created: $EXTENSION_DIR"

# Copy files
echo ""
echo "Copying extension files..."
cp gemini-extension.json "$EXTENSION_DIR/"
cp GEMINI.md "$EXTENSION_DIR/"
cp compliance_manager_mcp.py "$EXTENSION_DIR/"
cp pyproject.toml "$EXTENSION_DIR/"
cp run_mcp.sh "$EXTENSION_DIR/"
chmod +x "$EXTENSION_DIR/run_mcp.sh"
print_success "Extension files copied"

# Update gemini-extension.json with the absolute path
echo ""
echo "Updating extension configuration..."
ABSOLUTE_EXTENSION_DIR=$(cd "$EXTENSION_DIR" && pwd)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|\${extensionPath}/run_mcp.sh|$ABSOLUTE_EXTENSION_DIR/run_mcp.sh|g" "$EXTENSION_DIR/gemini-extension.json"
else
    # Linux
    sed -i "s|\${extensionPath}/run_mcp.sh|$ABSOLUTE_EXTENSION_DIR/run_mcp.sh|g" "$EXTENSION_DIR/gemini-extension.json"
fi
print_success "Extension configuration updated"

# Check Google Cloud authentication
echo ""
echo "Checking Google Cloud authentication..."
if gcloud auth application-default print-access-token &> /dev/null; then
    print_success "Google Cloud authentication is configured"
else
    print_warning "Google Cloud authentication is not configured"
    print_info "Please run: gcloud auth application-default login"
fi

# Installation complete
echo ""
echo "=========================================="
print_success "Installation complete!"
echo "=========================================="
echo ""
print_info "Extension installed to: $EXTENSION_DIR"
echo ""
print_info "Next steps:"
print_info "1. Restart Gemini CLI: gemini"
print_info "2. Test the extension with: @compliance-manager-mcp list_frameworks organization_id=\"YOUR_ORG_ID\""
echo ""
print_info "For more information, see:"
print_info "- README.md for usage examples"
print_info "- INSTALLATION.md for detailed installation guide"
print_info "- EXAMPLES.md for practical examples"
echo ""

