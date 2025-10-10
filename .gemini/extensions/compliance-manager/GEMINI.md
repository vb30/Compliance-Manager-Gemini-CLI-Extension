# Compliance Manager Extension for Gemini CLI

This extension provides integration with Google Cloud Compliance Manager, part of Security Command Center Enterprise.

## Purpose

The Compliance Manager extension enables you to:
- **Discover** compliance frameworks (CIS, NIST, FedRAMP, etc.)
- **Inspect** cloud controls and their configurations
- **Deploy** compliance frameworks to organizations, folders, and projects
- **Monitor** framework and cloud control deployments
- **Manage** compliance posture across your Google Cloud infrastructure

## Available Tools

### Framework Management
- `@compliance-manager-mcp list_frameworks` - List all available compliance frameworks
- `@compliance-manager-mcp get_framework` - Get detailed information about a specific framework

### Cloud Control Management
- `@compliance-manager-mcp list_cloud_controls` - List all cloud controls
- `@compliance-manager-mcp get_cloud_control` - Get detailed information about a specific cloud control

### Framework Deployment
- `@compliance-manager-mcp list_framework_deployments` - List framework deployments
- `@compliance-manager-mcp get_framework_deployment` - Get details of a specific deployment
- `@compliance-manager-mcp create_framework_deployment` - Deploy a framework to a resource
- `@compliance-manager-mcp delete_framework_deployment` - Remove a framework deployment

### Cloud Control Deployment
- `@compliance-manager-mcp list_cloud_control_deployments` - List cloud control deployments
- `@compliance-manager-mcp get_cloud_control_deployment` - Get details of a specific cloud control deployment

## Example Prompts

### Discovery
- "List all available compliance frameworks for organization 123456789012"
- "Show me details of the CIS framework"
- "What cloud controls are available in my organization?"

### Deployment
- "Deploy the NIST framework to my project"
- "Show me all framework deployments in my organization"
- "Create a deployment of the FedRAMP framework to folder 987654321"

### Monitoring
- "What frameworks are currently deployed to my project?"
- "Show me the status of all cloud control deployments"
- "Get details of the CIS framework deployment"

## Prerequisites

1. **Authentication**: Ensure you have Google Cloud credentials configured:
   - Run `gcloud auth application-default login`, OR
   - Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

2. **IAM Permissions**: You need appropriate permissions:
   - `roles/securitycenter.complianceManager` or `roles/securitycenter.adminEditor` for full access
   - `roles/securitycenter.adminViewer` for read-only operations

3. **Organization ID**: Know your Google Cloud organization ID (numeric, e.g., '123456789012')

## Resource Format

When using these tools, resources follow these formats:
- Organization: `organizations/{org_id}`
- Folder: `folders/{folder_id}`
- Project: `projects/{project_id}`

## Safety Notes

- Framework deployments are long-running operations that may take time to complete
- Deleting a framework deployment removes compliance controls from the target resource
- Always verify the target resource before creating or deleting deployments
- Use read-only operations (list/get) to explore before making changes

## More Information

For detailed documentation, see:
- [Compliance Manager Overview](https://cloud.google.com/security-command-center/docs/compliance-manager-overview)
- [MCP Server Repository](https://github.com/vb30/Compliance-Manager-MCP-Server)

