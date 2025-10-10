# Compliance Manager Gemini CLI Extension - Project Summary

## Overview

This project provides a **Gemini CLI extension** for Google Cloud Compliance Manager, enabling AI-assisted compliance management through natural language interactions.

## What This Extension Does

The extension integrates Google Cloud Compliance Manager with Gemini CLI through the Model Context Protocol (MCP), allowing users to:

- **Discover** compliance frameworks (CIS, NIST, FedRAMP, etc.) using natural language
- **Inspect** cloud controls and their configurations
- **Deploy** compliance frameworks to GCP resources
- **Monitor** framework and cloud control deployments
- **Manage** compliance posture across Google Cloud infrastructure

## Architecture

```
┌─────────────────┐
│   Gemini CLI    │
│   (User Input)  │
└────────┬────────┘
         │
         │ Natural Language
         │
┌────────▼────────────────────────────────────┐
│  Compliance Manager Extension               │
│  (gemini-extension.json + GEMINI.md)        │
└────────┬────────────────────────────────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────────────────────────────────┐
│  MCP Server (compliance_manager_mcp.py)     │
│  - FastMCP Framework                        │
│  - 11 Tools for Compliance Management       │
└────────┬────────────────────────────────────┘
         │
         │ Google Cloud API
         │
┌────────▼────────────────────────────────────┐
│  Google Cloud Compliance Manager            │
│  (Security Command Center Enterprise)       │
└─────────────────────────────────────────────┘
```

## Project Structure

```
Compliance-Manager-Gemini-CLI-Extension/
├── gemini-extension.json       # Extension manifest for Gemini CLI
├── GEMINI.md                    # Context file with extension documentation
├── compliance_manager_mcp.py    # MCP server implementation (11 tools)
├── pyproject.toml               # Python dependencies
├── setup.py                     # Python package setup
├── README.md                    # Main documentation
├── INSTALLATION.md              # Detailed installation guide
├── QUICKSTART.md                # Quick start guide
├── EXAMPLES.md                  # Practical usage examples
├── PROJECT_SUMMARY.md           # This file
├── LICENSE                      # Apache 2.0 license
├── .gitignore                   # Git ignore rules
├── install.sh                   # Automated installation script
└── test_extension.py            # Extension test suite
```

## Available Tools

The MCP server provides 11 tools organized into 4 categories:

### 1. Framework Management (2 tools)
- `list_frameworks` - List all available compliance frameworks
- `get_framework` - Get detailed framework information

### 2. Cloud Control Management (2 tools)
- `list_cloud_controls` - List all cloud controls
- `get_cloud_control` - Get detailed cloud control information

### 3. Framework Deployment (4 tools)
- `list_framework_deployments` - List framework deployments
- `get_framework_deployment` - Get deployment details
- `create_framework_deployment` - Deploy a framework
- `delete_framework_deployment` - Remove a deployment

### 4. Cloud Control Deployment (2 tools)
- `list_cloud_control_deployments` - List cloud control deployments
- `get_cloud_control_deployment` - Get cloud control deployment details

## Key Features

### 1. Natural Language Interface
Users can interact using natural language instead of complex API calls:
```
Instead of: @compliance-manager-mcp list_frameworks organization_id="123456789012"
Users can say: "Show me all compliance frameworks in my organization"
```

### 2. Context-Aware Assistance
The GEMINI.md file provides context to Gemini CLI, enabling:
- Intelligent suggestions
- Guided workflows
- Error explanation and troubleshooting
- Best practice recommendations

### 3. Comprehensive Error Handling
The MCP server handles:
- Authentication errors
- Permission issues
- Resource not found errors
- API exceptions

### 4. Long-Running Operations
Properly handles long-running operations like:
- Framework deployments
- Framework deletions

## Technology Stack

- **Language**: Python 3.11+
- **MCP Framework**: FastMCP
- **Google Cloud SDK**: google-cloud-cloudsecuritycompliance
- **Package Manager**: uv
- **Protocol**: Model Context Protocol (MCP)
- **Integration**: Gemini CLI

## Installation Methods

### Method 1: Automated Installation (Recommended)
```bash
./install.sh
```

### Method 2: Manual Installation
```bash
# Install dependencies
uv pip install -e .

# Copy to Gemini CLI extensions directory
mkdir -p ~/.gemini/extensions/compliance-manager
cp gemini-extension.json GEMINI.md compliance_manager_mcp.py pyproject.toml ~/.gemini/extensions/compliance-manager/
```

## Authentication

The extension supports multiple authentication methods:

1. **Application Default Credentials (ADC)** - Recommended
   ```bash
   gcloud auth application-default login
   ```

2. **Service Account Key**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
   ```

## Required Permissions

Users need one of these IAM roles:
- `roles/securitycenter.complianceManager` - Full access
- `roles/securitycenter.adminEditor` - Full access
- `roles/securitycenter.adminViewer` - Read-only access

## Usage Examples

### Discovery
```
> Show me all compliance frameworks available
> What cloud controls are in my organization?
> Tell me about the CIS framework
```

### Deployment
```
> Deploy the NIST framework to my project
> Show me all framework deployments
> What's the status of my CIS deployment?
```

### Monitoring
```
> What frameworks are deployed in my organization?
> Show me cloud control deployment status
> Generate a compliance report
```

## Testing

The project includes a test suite:
```bash
python3 test_extension.py
```

Tests verify:
- Python dependencies are installed
- Google Cloud clients can be initialized
- MCP server can be imported
- Authentication is configured

## Documentation

| File | Purpose |
|------|---------|
| README.md | Main documentation and overview |
| INSTALLATION.md | Detailed installation instructions |
| QUICKSTART.md | 5-minute quick start guide |
| EXAMPLES.md | Practical usage examples and workflows |
| GEMINI.md | Context for Gemini CLI (loaded automatically) |
| PROJECT_SUMMARY.md | This file - project overview |

## Related Projects

- **[Compliance Manager MCP Server](https://github.com/vb30/Compliance-Manager-MCP-Server)** - The standalone MCP server this extension is based on
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** - The official Gemini CLI repository
- **[Google Cloud Compliance Manager](https://cloud.google.com/security-command-center/docs/compliance-manager-overview)** - Official documentation

## Development

### Adding New Tools

1. Add the tool function in `compliance_manager_mcp.py` with `@mcp.tool()` decorator
2. Update `GEMINI.md` with the new tool description
3. Add examples to `EXAMPLES.md`
4. Test the tool

### Modifying the Extension

1. Edit `gemini-extension.json` for configuration changes
2. Update `GEMINI.md` for context changes
3. Modify `compliance_manager_mcp.py` for tool changes
4. Run tests with `test_extension.py`

## Troubleshooting

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| Extension not loading | Check `~/.gemini/extensions/compliance-manager/` exists |
| Authentication errors | Run `gcloud auth application-default login` |
| Permission denied | Verify IAM roles are assigned |
| Import errors | Run `uv pip install -e .` |
| MCP server not starting | Check uv path in `gemini-extension.json` |

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension/issues)
- **Documentation**: See the documentation files in this repository
- **MCP Server Issues**: [MCP Server Repository](https://github.com/vb30/Compliance-Manager-MCP-Server)

## Acknowledgments

- Built on the [Compliance Manager MCP Server](https://github.com/vb30/Compliance-Manager-MCP-Server)
- Follows [Gemini CLI extension guidelines](https://github.com/google-gemini/gemini-cli)
- Uses the [Model Context Protocol](https://modelcontextprotocol.io/)

## Version History

- **v1.0.0** (2025-10-10) - Initial release
  - 11 MCP tools for compliance management
  - Natural language interface via Gemini CLI
  - Automated installation script
  - Comprehensive documentation

## Future Enhancements

Potential future additions:
- Custom command shortcuts (e.g., `/deploy-cis`)
- Compliance reporting templates
- Multi-organization support
- Batch deployment operations
- Integration with other GCP security services
- Compliance dashboard generation

## Quick Reference

### Installation
```bash
./install.sh
```

### Testing
```bash
python3 test_extension.py
```

### Usage
```bash
gemini
> @compliance-manager-mcp list_frameworks organization_id="YOUR_ORG_ID"
```

### Uninstallation
```bash
rm -rf ~/.gemini/extensions/compliance-manager
```

---

**Project Status**: ✅ Ready for use

**Last Updated**: 2025-10-10

**Maintainer**: Varun Bhardwaj

