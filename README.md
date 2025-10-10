# Compliance Manager Gemini CLI Extension

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A Gemini CLI extension for interacting with Google Cloud Compliance Manager, part of Security Command Center Enterprise.

## Overview

This extension enables Gemini CLI to interact with Google Cloud's Compliance Manager service through the Model Context Protocol (MCP). It provides tools to discover, inspect, deploy, and monitor compliance frameworks and cloud controls across your Google Cloud infrastructure.

## Features

### Framework Management
- **List Frameworks**: Discover all available compliance frameworks (CIS, NIST, FedRAMP, etc.)
- **Get Framework Details**: Inspect specific frameworks including their cloud controls and regulatory mappings

### Cloud Control Management
- **List Cloud Controls**: View all available cloud controls in your organization
- **Get Cloud Control Details**: Examine specific controls including rules, parameters, and enforcement modes

### Deployment Management
- **List Deployments**: View framework and cloud control deployments
- **Get Deployment Details**: Inspect specific deployment configurations and states
- **Create Deployments**: Apply compliance frameworks to organizations, folders, or projects
- **Delete Deployments**: Remove compliance framework deployments

## Installation

### Prerequisites

1. **Gemini CLI**: Install Gemini CLI first
   ```bash
   npm install -g @google/gemini-cli
   ```

2. **Python 3.11+**: Ensure you have Python 3.11 or higher installed

3. **uv Package Manager**: Install uv for Python package management
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. **Google Cloud Authentication**: Set up authentication
   ```bash
   gcloud auth application-default login
   ```

### Install the Extension

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
   cd Compliance-Manager-Gemini-CLI-Extension
   ```

2. **Install dependencies**:
   ```bash
   uv pip install -e .
   ```

3. **Copy the extension to Gemini CLI extensions directory**:
   ```bash
   # Create the extensions directory if it doesn't exist
   mkdir -p ~/.gemini/extensions/compliance-manager
   
   # Copy extension files
   cp gemini-extension.json ~/.gemini/extensions/compliance-manager/
   cp GEMINI.md ~/.gemini/extensions/compliance-manager/
   cp compliance_manager_mcp.py ~/.gemini/extensions/compliance-manager/
   cp pyproject.toml ~/.gemini/extensions/compliance-manager/
   ```

4. **Restart Gemini CLI** to load the extension:
   ```bash
   gemini
   ```

## Usage

Once installed, you can use the extension in Gemini CLI by referencing the MCP server:

### Example Prompts

#### Discovery
```
> @compliance-manager-mcp List all available compliance frameworks for organization 123456789012

> @compliance-manager-mcp Show me details of the CIS framework

> @compliance-manager-mcp What cloud controls are available in my organization?
```

#### Deployment
```
> @compliance-manager-mcp Deploy the NIST framework to project my-project-id

> @compliance-manager-mcp Show me all framework deployments in organization 123456789012

> @compliance-manager-mcp Create a deployment of the FedRAMP framework to folder 987654321
```

#### Monitoring
```
> @compliance-manager-mcp What frameworks are currently deployed to my project?

> @compliance-manager-mcp Show me the status of all cloud control deployments

> @compliance-manager-mcp Get details of the CIS framework deployment
```

### Natural Language Queries

Gemini CLI can understand natural language queries about compliance:

```
> Help me understand what compliance frameworks are available for my organization

> I need to deploy CIS controls to my production project, how do I do that?

> Show me the current compliance posture of my organization

> What's the difference between NIST and FedRAMP frameworks?
```

## Configuration

### Authentication

The extension uses Google Cloud's Application Default Credentials (ADC). Ensure you have one of the following configured:

1. **ADC via gcloud**:
   ```bash
   gcloud auth application-default login
   ```

2. **Service Account Key**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```

### Required IAM Permissions

You need appropriate IAM permissions on your Google Cloud organization(s):

- **Full Access**: `roles/securitycenter.complianceManager` or `roles/securitycenter.adminEditor`
- **Read-Only**: `roles/securitycenter.adminViewer`

## Extension Structure

```
compliance-manager/
├── gemini-extension.json    # Extension manifest
├── GEMINI.md                 # Context and documentation for Gemini CLI
├── compliance_manager_mcp.py # MCP server implementation
├── pyproject.toml            # Python dependencies
└── README.md                 # This file
```

## Available Tools

The extension provides the following MCP tools:

### Framework Tools
- `list_frameworks(organization_id, location="global", page_size=50)`
- `get_framework(organization_id, framework_id, location="global")`

### Cloud Control Tools
- `list_cloud_controls(organization_id, location="global", page_size=50)`
- `get_cloud_control(organization_id, cloud_control_id, location="global")`

### Framework Deployment Tools
- `list_framework_deployments(parent, location="global", page_size=50)`
- `get_framework_deployment(parent, framework_deployment_id, location="global")`
- `create_framework_deployment(parent, framework_deployment_id, framework_name, location="global", target_resource=None)`
- `delete_framework_deployment(parent, framework_deployment_id, location="global")`

### Cloud Control Deployment Tools
- `list_cloud_control_deployments(parent, location="global", page_size=50)`
- `get_cloud_control_deployment(parent, cloud_control_deployment_id, location="global")`

## Troubleshooting

### Extension Not Loading

1. **Check extension directory**:
   ```bash
   ls -la ~/.gemini/extensions/compliance-manager/
   ```

2. **Verify gemini-extension.json is valid**:
   ```bash
   cat ~/.gemini/extensions/compliance-manager/gemini-extension.json | python -m json.tool
   ```

3. **Check Gemini CLI logs** for any errors during startup

### Authentication Issues

1. **Verify ADC is configured**:
   ```bash
   gcloud auth application-default print-access-token
   ```

2. **Check IAM permissions**:
   ```bash
   gcloud projects get-iam-policy YOUR_PROJECT_ID --flatten="bindings[].members" --filter="bindings.members:user:YOUR_EMAIL"
   ```

### MCP Server Issues

1. **Test the MCP server directly**:
   ```bash
   cd ~/.gemini/extensions/compliance-manager
   uv run compliance_manager_mcp.py
   ```

2. **Check Python dependencies**:
   ```bash
   uv pip list
   ```

## About Compliance Manager

Compliance Manager in Google Cloud helps ensure that your Google Cloud infrastructure, workloads, and data meet security and regulatory requirements. It allows you to:

- Define and deploy compliant and secure configurations
- View dashboards showing alignment with compliance requirements
- Audit cloud environments and generate assessment reports
- Use software-defined controls for multiple compliance programs

For more information, see the [Compliance Manager documentation](https://cloud.google.com/security-command-center/docs/compliance-manager-overview).

## Related Projects

- **[Compliance Manager MCP Server](https://github.com/vb30/Compliance-Manager-MCP-Server)**: The standalone MCP server this extension is based on
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)**: The official Gemini CLI repository

## License

Apache 2.0

## Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension/issues)
- **Documentation**: See the [Compliance Manager documentation](https://cloud.google.com/security-command-center/docs/compliance-manager-overview)
- **MCP Server**: For MCP server-specific issues, see the [MCP Server repository](https://github.com/vb30/Compliance-Manager-MCP-Server)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This extension is built on top of the [Compliance Manager MCP Server](https://github.com/vb30/Compliance-Manager-MCP-Server) and follows the [Gemini CLI extension guidelines](https://github.com/google-gemini/gemini-cli).

