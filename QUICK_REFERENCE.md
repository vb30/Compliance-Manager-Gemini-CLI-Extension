# Quick Reference - Compliance Manager Extension

## ✅ MCP Server Status

**Verified Working**: All 10 tools are properly exposed by the MCP server.

## 🎯 Correct Usage in Gemini CLI

### ❌ WRONG Syntax
```
@compliance-manager-mcp list_frameworks organization_id="1035865795181"
```
The `@` symbol is for mentioning files, NOT for MCP tools!

### ✅ CORRECT Syntax

#### Option 1: Direct Tool Call (Recommended)
```
list_frameworks organization_id="1035865795181"
```

#### Option 2: Natural Language
```
Show me all compliance frameworks in organization 1035865795181
```

#### Option 3: With Server Prefix (if needed)
```
compliance-manager-mcp/list_frameworks organization_id="1035865795181"
```

## 📋 Available Tools

### Framework Management
```bash
# List all frameworks
list_frameworks organization_id="1035865795181"

# Get framework details
get_framework organization_id="1035865795181" framework_id="FRAMEWORK_ID"
```

### Cloud Controls
```bash
# List all cloud controls
list_cloud_controls organization_id="1035865795181"

# Get cloud control details
get_cloud_control organization_id="1035865795181" cloud_control_id="CONTROL_ID"
```

### Framework Deployments
```bash
# List deployments (organization)
list_framework_deployments parent="organizations/1035865795181"

# List deployments (project)
list_framework_deployments parent="projects/csc-audit-test-project"

# Get deployment details
get_framework_deployment parent="projects/csc-audit-test-project" framework_deployment_id="DEPLOYMENT_ID"

# Create deployment
create_framework_deployment parent="projects/csc-audit-test-project" framework_deployment_id="my-deployment" framework_name="organizations/1035865795181/locations/global/frameworks/FRAMEWORK_ID"

# Delete deployment
delete_framework_deployment parent="projects/csc-audit-test-project" framework_deployment_id="DEPLOYMENT_ID"
```

### Cloud Control Deployments
```bash
# List cloud control deployments
list_cloud_control_deployments parent="projects/csc-audit-test-project"

# Get cloud control deployment details
get_cloud_control_deployment parent="projects/csc-audit-test-project" cloud_control_deployment_id="DEPLOYMENT_ID"
```

## 🔍 Checking Extension Status

### In Gemini CLI

**Press `Ctrl+T`** to view MCP servers. You should see:
- Server name: `compliance-manager-mcp`
- Status: Connected/Running
- Tools: 10 tools available

**Press `Ctrl+O`** to view errors (if any)

### At Startup

Look for this message:
```
Loading extension: compliance-manager (version: 1.0.0)
```

And at the bottom:
```
Using 2 GEMINI.md files and 1 MCP server (ctrl+t to view)
```

## 🧪 Testing

### Test MCP Server
```bash
python3 test_mcp_server.py
```

Expected output:
```
✓ Found 10 tools:
  - list_frameworks
  - get_framework
  - list_cloud_controls
  - get_cloud_control
  - list_framework_deployments
  - get_framework_deployment
  - create_framework_deployment
  - delete_framework_deployment
  - list_cloud_control_deployments
  - get_cloud_control_deployment
```

### Test in Gemini CLI
```
I need help using the Compliance Manager extension. Can you list all available tools?
```

## 🚀 Quick Start Commands

### 1. List Available Frameworks
```
list_frameworks organization_id="1035865795181"
```

### 2. Check Current Deployments
```
list_framework_deployments parent="projects/csc-audit-test-project"
```

### 3. Natural Language Query
```
Show me all compliance frameworks available in my organization
```

## 🔧 Troubleshooting

### Extension Not Loading?
```bash
# Restart Gemini CLI
# Exit with Ctrl+C, then:
gemini
```

### Tools Not Found?
1. Check `Ctrl+T` - is `compliance-manager-mcp` listed?
2. Don't use `@` prefix for MCP tools
3. Try natural language instead

### MCP Server Not Starting?
```bash
# Test manually
cd ~/.gemini/extensions/compliance-manager
/opt/homebrew/bin/uv run compliance_manager_mcp.py
# Should show: "Successfully initialized..." messages
# Press Ctrl+C to stop
```

## 📝 Your Configuration

- **Organization ID**: `1035865795181`
- **Project ID**: `csc-audit-test-project`
- **Extension Path**: `~/.gemini/extensions/compliance-manager/`
- **MCP Server Name**: `compliance-manager-mcp`

## 💡 Pro Tips

1. **Use natural language** - Gemini CLI will automatically call the right tool
2. **No @ symbol** - That's for files, not MCP tools
3. **Check Ctrl+T** - Always verify the MCP server is connected
4. **Test first** - Use `list_frameworks` to verify everything works

## 📚 More Help

- **Detailed troubleshooting**: See [TROUBLESHOOTING_MCP.md](TROUBLESHOOTING_MCP.md)
- **Full examples**: See [EXAMPLE_COMMANDS.md](EXAMPLE_COMMANDS.md)
- **Getting started**: See [GETTING_STARTED.md](GETTING_STARTED.md)

---

**Remember**: Don't use `@compliance-manager-mcp` - just call the tool directly!

✅ **Correct**: `list_frameworks organization_id="1035865795181"`
❌ **Wrong**: `@compliance-manager-mcp list_frameworks organization_id="1035865795181"`

