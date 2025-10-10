# Quick Start Guide

Get up and running with the Compliance Manager Gemini CLI Extension in minutes!

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Gemini CLI** installed (`npm install -g @google/gemini-cli`)
- [ ] **Python 3.11+** installed
- [ ] **uv** package manager installed
- [ ] **Google Cloud** account with appropriate permissions
- [ ] **Organization ID** for your Google Cloud organization

## 5-Minute Setup

### Step 1: Install Prerequisites (if needed)

```bash
# Install Gemini CLI
npm install -g @google/gemini-cli

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Authenticate with Google Cloud
gcloud auth application-default login
```

### Step 2: Clone and Install

```bash
# Clone the repository
git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
cd Compliance-Manager-Gemini-CLI-Extension

# Run the installation script
./install.sh
```

The installation script will:
- Install Python dependencies
- Copy extension files to `~/.gemini/extensions/compliance-manager`
- Configure the extension for your system
- Verify your Google Cloud authentication

### Step 3: Verify Installation

```bash
# Test the extension
python3 test_extension.py
```

If all tests pass, you're ready to go!

### Step 4: Start Using

```bash
# Start Gemini CLI
gemini

# Try your first command
> @compliance-manager-mcp list_frameworks organization_id="YOUR_ORG_ID"
```

Replace `YOUR_ORG_ID` with your actual Google Cloud organization ID (numeric, e.g., `123456789012`).

## Your First Tasks

### 1. Discover Available Frameworks

```
> Show me all compliance frameworks available in my organization
```

### 2. Explore a Framework

```
> Tell me about the CIS Google Cloud Foundation framework
```

### 3. Check Current Deployments

```
> What frameworks are currently deployed in my organization?
```

### 4. Deploy a Framework (if you have permissions)

```
> I want to deploy the CIS framework to my test project. Can you help me?
```

## Common Commands

### List Frameworks
```
@compliance-manager-mcp list_frameworks organization_id="YOUR_ORG_ID"
```

### Get Framework Details
```
@compliance-manager-mcp get_framework organization_id="YOUR_ORG_ID" framework_id="FRAMEWORK_ID"
```

### List Cloud Controls
```
@compliance-manager-mcp list_cloud_controls organization_id="YOUR_ORG_ID"
```

### List Deployments
```
@compliance-manager-mcp list_framework_deployments parent="organizations/YOUR_ORG_ID"
```

### Create Deployment
```
@compliance-manager-mcp create_framework_deployment parent="projects/PROJECT_ID" framework_deployment_id="DEPLOYMENT_ID" framework_name="organizations/ORG_ID/locations/global/frameworks/FRAMEWORK_ID"
```

## Natural Language Examples

You don't have to use the exact command syntax! Gemini CLI understands natural language:

```
> What compliance frameworks are available?
> Show me details of the NIST framework
> Deploy CIS to my production project
> What's the status of my compliance deployments?
> Help me understand cloud controls
```

## Troubleshooting

### Extension Not Loading?

1. **Check the extension directory**:
   ```bash
   ls -la ~/.gemini/extensions/compliance-manager/
   ```

2. **Verify the configuration**:
   ```bash
   cat ~/.gemini/extensions/compliance-manager/gemini-extension.json
   ```

3. **Restart Gemini CLI**:
   ```bash
   gemini
   ```

### Authentication Issues?

```bash
# Re-authenticate
gcloud auth application-default login

# Verify authentication
gcloud auth application-default print-access-token
```

### Permission Errors?

Ensure you have the required IAM role:
- `roles/securitycenter.complianceManager` (full access)
- `roles/securitycenter.adminViewer` (read-only)

## Next Steps

Now that you're set up:

1. **Read the [README.md](README.md)** for comprehensive documentation
2. **Explore [EXAMPLES.md](EXAMPLES.md)** for practical use cases
3. **Check [INSTALLATION.md](INSTALLATION.md)** for detailed installation options
4. **Review [GEMINI.md](GEMINI.md)** for all available tools and prompts

## Getting Help

- **Documentation**: See the files in this repository
- **Issues**: [GitHub Issues](https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension/issues)
- **MCP Server**: [Compliance Manager MCP Server](https://github.com/vb30/Compliance-Manager-MCP-Server)
- **Compliance Manager**: [Official Documentation](https://cloud.google.com/security-command-center/docs/compliance-manager-overview)

## Tips for Success

1. **Start with read-only operations** (list, get) to familiarize yourself
2. **Use natural language** - Gemini CLI is smart!
3. **Test in non-production** environments first
4. **Ask for help** - Gemini CLI can explain concepts and guide you
5. **Check permissions** before attempting deployments

## Example Session

Here's what a typical first session might look like:

```
$ gemini

> Hi! I just installed the Compliance Manager extension. Can you help me get started?

[Gemini explains the extension and asks for your organization ID]

> My organization ID is 123456789012

> Great! Can you show me what compliance frameworks are available?

[Gemini lists available frameworks]

> Tell me more about the CIS framework

[Gemini provides details about CIS]

> Are there any frameworks currently deployed in my organization?

[Gemini checks deployments]

> I'd like to deploy the CIS framework to my test project "my-test-project". Can you guide me through it?

[Gemini helps you create the deployment]
```

## Ready to Go!

You're all set! Start exploring compliance management with the power of Gemini CLI.

Happy compliance managing! 🚀

