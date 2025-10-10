# Getting Started with Your Compliance Manager Extension

Welcome! This guide will help you get started with the Compliance Manager Gemini CLI Extension using your specific GCP setup.

## Your Configuration

- **Organization ID**: `1035865795181`
- **Project ID**: `csc-audit-test-project`

## Quick Start (5 Minutes)

### Step 1: Install the Extension

```bash
# Run the automated installation script
./install.sh
```

This will:
- Install Python dependencies
- Copy extension files to `~/.gemini/extensions/compliance-manager`
- Configure the extension for your system
- Verify your Google Cloud authentication

### Step 2: Verify Installation

```bash
# Run the test script with your organization
./test_with_org.sh
```

This will verify:
- ✅ Google Cloud authentication is configured
- ✅ Extension is installed correctly
- ✅ All dependencies are available
- ✅ Provide ready-to-use commands for your setup

### Step 3: Start Gemini CLI

```bash
gemini
```

### Step 4: Try Your First Command

In Gemini CLI, try:

```
> @compliance-manager-mcp list_frameworks organization_id="1035865795181"
```

Or use natural language:

```
> Show me all compliance frameworks available in my organization
```

## What You Can Do

### 🔍 Discovery

**List all available frameworks:**
```
> Show me all compliance frameworks in organization 1035865795181
```

**Explore a specific framework:**
```
> Tell me about the CIS Google Cloud Foundation framework
```

**See available cloud controls:**
```
> What cloud controls are available in my organization?
```

### 📊 Monitoring

**Check current deployments (organization level):**
```
> @compliance-manager-mcp list_framework_deployments parent="organizations/1035865795181"
```

**Check current deployments (project level):**
```
> What frameworks are deployed to project csc-audit-test-project?
```

**View cloud control deployments:**
```
> Show me cloud control deployments in my test project
```

### 🚀 Deployment

**Deploy a framework:**
```
> I want to deploy the CIS framework to project csc-audit-test-project. Can you help me?
```

**Check deployment status:**
```
> What's the status of my framework deployment?
```

**Remove a deployment:**
```
> Remove the framework deployment from my test project
```

## Example Session

Here's what a typical first session looks like:

```bash
$ gemini

> Hi! I just installed the Compliance Manager extension. My organization is 1035865795181 and my test project is csc-audit-test-project. Can you help me get started?

[Gemini explains the extension and confirms your setup]

> Great! Can you show me what compliance frameworks are available?

[Gemini lists available frameworks using your organization ID]

> Tell me more about the CIS Google Cloud Foundation framework

[Gemini provides detailed information about CIS]

> Are there any frameworks currently deployed to my test project?

[Gemini checks deployments for csc-audit-test-project]

> I'd like to deploy the CIS framework to my test project. Can you guide me through it?

[Gemini helps you create the deployment with appropriate parameters]
```

## Ready-to-Use Commands

See [EXAMPLE_COMMANDS.md](EXAMPLE_COMMANDS.md) for a comprehensive list of commands pre-configured with your organization and project IDs.

### Quick Reference

**List frameworks:**
```
@compliance-manager-mcp list_frameworks organization_id="1035865795181"
```

**List cloud controls:**
```
@compliance-manager-mcp list_cloud_controls organization_id="1035865795181"
```

**List deployments (org):**
```
@compliance-manager-mcp list_framework_deployments parent="organizations/1035865795181"
```

**List deployments (project):**
```
@compliance-manager-mcp list_framework_deployments parent="projects/csc-audit-test-project"
```

## Common Tasks

### Task 1: Assess Current Compliance Posture

```
> I need to understand my current compliance posture. Can you:
1. Show me what frameworks are available in organization 1035865795181
2. List any frameworks deployed to project csc-audit-test-project
3. Show me cloud control deployments
4. Summarize the current state
```

### Task 2: Deploy Your First Framework

```
> I want to deploy a compliance framework to my test project. Can you:
1. Show me available frameworks
2. Recommend one for a typical web application
3. Help me deploy it to project csc-audit-test-project
4. Verify the deployment was successful
```

### Task 3: Compare Frameworks

```
> I need to choose between CIS and NIST frameworks. Can you:
1. Get details of both frameworks from organization 1035865795181
2. Compare their features and requirements
3. Recommend which one is better for my use case
```

## Troubleshooting

### Extension Not Loading?

```bash
# Check if extension is installed
ls -la ~/.gemini/extensions/compliance-manager/

# Verify configuration
cat ~/.gemini/extensions/compliance-manager/gemini-extension.json

# Restart Gemini CLI
gemini
```

### Authentication Issues?

```bash
# Re-authenticate with Google Cloud
gcloud auth application-default login

# Verify authentication works
gcloud auth application-default print-access-token

# Set your project
gcloud config set project csc-audit-test-project
```

### Permission Errors?

Ensure you have the required IAM permissions:

```bash
# Check your permissions
gcloud projects get-iam-policy csc-audit-test-project \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:YOUR_EMAIL"
```

You need one of these roles:
- `roles/securitycenter.complianceManager` (full access)
- `roles/securitycenter.adminEditor` (full access)
- `roles/securitycenter.adminViewer` (read-only)

## Next Steps

1. ✅ **Explore available frameworks** - See what's available in your organization
2. ✅ **Check current deployments** - Understand your current compliance state
3. ✅ **Test a deployment** - Deploy a framework to your test project
4. ✅ **Monitor and manage** - Use the extension to manage compliance

## Learning Resources

- **[EXAMPLE_COMMANDS.md](EXAMPLE_COMMANDS.md)** - Pre-configured commands for your setup
- **[EXAMPLES.md](EXAMPLES.md)** - Comprehensive usage examples
- **[README.md](README.md)** - Full documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide

## Getting Help

### In Gemini CLI

Just ask! Gemini understands natural language:

```
> How do I list frameworks?
> What does the CIS framework do?
> How do I deploy a framework?
> What are the best practices for compliance management?
```

### Documentation

- Check the documentation files in this repository
- See [EXAMPLE_COMMANDS.md](EXAMPLE_COMMANDS.md) for your specific setup

### Support

- **Issues**: [GitHub Issues](https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension/issues)
- **MCP Server**: [Compliance Manager MCP Server](https://github.com/vb30/Compliance-Manager-MCP-Server)

## Tips for Success

1. **Start with read-only operations** - Use `list` and `get` commands first
2. **Use natural language** - Gemini CLI is smart and understands context
3. **Test in your test project** - Use `csc-audit-test-project` for testing
4. **Ask for help** - Gemini can explain concepts and guide you
5. **Chain operations** - Ask Gemini to perform multiple steps

## Your First Goal

Try to complete this workflow:

1. ✅ List all available frameworks
2. ✅ Get details of one framework
3. ✅ Check current deployments in your project
4. ✅ Ask Gemini to explain what a framework does
5. ✅ (Optional) Deploy a framework to your test project

## Ready to Go!

You're all set! Start Gemini CLI and begin exploring:

```bash
gemini
```

Then try:
```
> Show me all compliance frameworks in organization 1035865795181
```

Happy compliance managing! 🚀

---

**Your Setup**:
- Organization: `1035865795181`
- Project: `csc-audit-test-project`
- Extension: Installed at `~/.gemini/extensions/compliance-manager`

