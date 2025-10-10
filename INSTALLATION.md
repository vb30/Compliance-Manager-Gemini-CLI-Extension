# Installation Guide

This guide provides detailed instructions for installing the Compliance Manager Gemini CLI Extension.

## Prerequisites

Before installing the extension, ensure you have the following:

### 1. Gemini CLI

Install Gemini CLI globally:

```bash
npm install -g @google/gemini-cli
```

Verify installation:

```bash
gemini --version
```

### 2. Python 3.11 or Higher

Check your Python version:

```bash
python --version
# or
python3 --version
```

If you need to install Python 3.11+:

- **macOS**: `brew install python@3.11`
- **Ubuntu/Debian**: `sudo apt install python3.11`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

### 3. uv Package Manager

Install uv for fast Python package management:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For macOS users, note the installation path (typically `~/.local/bin/uv`).

### 4. Google Cloud Authentication

Set up Google Cloud authentication using one of these methods:

#### Option A: Application Default Credentials (Recommended)

```bash
gcloud auth application-default login
```

#### Option B: Service Account Key

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

### 5. IAM Permissions

Ensure you have the required IAM permissions on your Google Cloud organization:

- **Full Access**: `roles/securitycenter.complianceManager` or `roles/securitycenter.adminEditor`
- **Read-Only**: `roles/securitycenter.adminViewer`

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
cd Compliance-Manager-Gemini-CLI-Extension
```

Or download and extract the ZIP file from GitHub.

### Step 2: Install Python Dependencies

```bash
uv pip install -e .
```

This will install all required Python packages including:
- `mcp[cli]` - Model Context Protocol
- `google-cloud-cloudsecuritycompliance` - Google Cloud Compliance Manager client
- Other dependencies

### Step 3: Install the Extension to Gemini CLI

#### Option A: User-Level Installation (Recommended)

Install the extension for your user account:

```bash
# Create the extensions directory
mkdir -p ~/.gemini/extensions/compliance-manager

# Copy extension files
cp gemini-extension.json ~/.gemini/extensions/compliance-manager/
cp GEMINI.md ~/.gemini/extensions/compliance-manager/
cp compliance_manager_mcp.py ~/.gemini/extensions/compliance-manager/
cp pyproject.toml ~/.gemini/extensions/compliance-manager/
```

#### Option B: Project-Level Installation

Install the extension for a specific project:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Create the extensions directory
mkdir -p .gemini/extensions/compliance-manager

# Copy extension files
cp /path/to/Compliance-Manager-Gemini-CLI-Extension/gemini-extension.json .gemini/extensions/compliance-manager/
cp /path/to/Compliance-Manager-Gemini-CLI-Extension/GEMINI.md .gemini/extensions/compliance-manager/
cp /path/to/Compliance-Manager-Gemini-CLI-Extension/compliance_manager_mcp.py .gemini/extensions/compliance-manager/
cp /path/to/Compliance-Manager-Gemini-CLI-Extension/pyproject.toml .gemini/extensions/compliance-manager/
```

### Step 4: Update Extension Path (macOS Users)

If you're on macOS and installed uv using the one-liner, you need to update the extension configuration to use the full path to uv:

```bash
# Edit the gemini-extension.json file
nano ~/.gemini/extensions/compliance-manager/gemini-extension.json
```

Update the `command` field to use the full path:

```json
{
  "name": "compliance-manager",
  "version": "1.0.0",
  "description": "Google Cloud Compliance Manager extension for Gemini CLI",
  "mcpServers": {
    "compliance-manager-mcp": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "--directory",
        "${extensionPath}",
        "run",
        "compliance_manager_mcp.py"
      ],
      "env": {}
    }
  },
  "contextFileName": "GEMINI.md"
}
```

Replace `YOUR_USERNAME` with your actual username, or use the full path from `which uv`.

### Step 5: Verify Installation

1. **Start Gemini CLI**:
   ```bash
   gemini
   ```

2. **Check if the extension is loaded**:
   Look for messages in the Gemini CLI startup indicating the extension was loaded.

3. **Test the extension**:
   ```
   > @compliance-manager-mcp list_frameworks organization_id="YOUR_ORG_ID"
   ```

   Replace `YOUR_ORG_ID` with your actual Google Cloud organization ID.

## Troubleshooting

### Extension Not Loading

**Problem**: The extension doesn't appear in Gemini CLI.

**Solutions**:

1. **Verify the extension directory exists**:
   ```bash
   ls -la ~/.gemini/extensions/compliance-manager/
   ```

2. **Check the gemini-extension.json is valid JSON**:
   ```bash
   cat ~/.gemini/extensions/compliance-manager/gemini-extension.json | python -m json.tool
   ```

3. **Check Gemini CLI logs** for any error messages during startup.

### Authentication Errors

**Problem**: "Permission denied" or "Authentication failed" errors.

**Solutions**:

1. **Verify ADC is configured**:
   ```bash
   gcloud auth application-default print-access-token
   ```

2. **Check your IAM permissions**:
   ```bash
   gcloud organizations get-iam-policy YOUR_ORG_ID --flatten="bindings[].members" --filter="bindings.members:user:YOUR_EMAIL"
   ```

3. **Re-authenticate**:
   ```bash
   gcloud auth application-default login
   ```

### Python Dependency Issues

**Problem**: Import errors or missing packages.

**Solutions**:

1. **Reinstall dependencies**:
   ```bash
   cd ~/.gemini/extensions/compliance-manager
   uv pip install -e .
   ```

2. **Check installed packages**:
   ```bash
   uv pip list
   ```

3. **Verify Python version**:
   ```bash
   python --version
   ```

### MCP Server Not Starting

**Problem**: The MCP server fails to start.

**Solutions**:

1. **Test the MCP server directly**:
   ```bash
   cd ~/.gemini/extensions/compliance-manager
   uv run compliance_manager_mcp.py
   ```

2. **Check for error messages** in the output.

3. **Verify the uv command path** (especially on macOS):
   ```bash
   which uv
   ```

## Uninstallation

To remove the extension:

```bash
# Remove the extension directory
rm -rf ~/.gemini/extensions/compliance-manager

# Restart Gemini CLI
gemini
```

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for usage examples
2. Review the [GEMINI.md](GEMINI.md) for available tools and prompts
3. Try the example prompts to get familiar with the extension

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the [README.md](README.md) documentation
3. Open an issue on [GitHub](https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension/issues)
4. Check the [Compliance Manager MCP Server](https://github.com/vb30/Compliance-Manager-MCP-Server) repository for MCP-specific issues

