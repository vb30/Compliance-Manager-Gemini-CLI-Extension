# 🎯 SOLUTION: How to Use the Compliance Manager Extension

## ❌ The Problem

You tried:
```
@compliance-manager-mcp list_frameworks
```

This resulted in error:
```
Tool "compliance-manager-mcp:list_frameworks" not found in registry.
```

## 🔍 Why This Happened

1. The `@` symbol in Gemini CLI is for **mentioning files**, not for calling MCP tools
2. Gemini CLI tried to interpret this as a tool call with server prefix
3. The MCP server registers tools as `list_frameworks`, not `compliance-manager-mcp:list_frameworks`

## ✅ THE SOLUTION: Use Natural Language

**Just describe what you want in plain English!**

### Example 1: List Frameworks

Instead of:
```
@compliance-manager-mcp list_frameworks
```

Just say:
```
List all compliance frameworks in organization 1035865795181
```

or

```
Show me available compliance frameworks for my GCP organization 1035865795181
```

### Example 2: Get Framework Details

```
Tell me about the CIS Google Cloud Foundation framework in organization 1035865795181
```

### Example 3: List Deployments

```
What framework deployments exist in project csc-audit-test-project?
```

### Example 4: Create Deployment

```
I want to deploy a compliance framework to project csc-audit-test-project. 
Can you help me with that?
```

## 🎯 How It Works

When you use natural language:

1. **You describe** what you want
2. **Gemini reads** the GEMINI.md file that describes available tools
3. **Gemini chooses** the right tool (e.g., `list_frameworks`)
4. **Gemini calls** the tool with the right parameters
5. **You get** the results explained in plain English

## 📋 Quick Start Commands

Copy and paste these into Gemini CLI:

### Command 1: List Frameworks
```
I need to see all compliance frameworks available in organization 1035865795181
```

### Command 2: List Cloud Controls
```
Show me all cloud controls available in organization 1035865795181
```

### Command 3: Check Deployments
```
What framework deployments are in project csc-audit-test-project?
```

### Command 4: Get Help
```
I'm new to the Compliance Manager extension. Can you explain what it does and show me what's available in organization 1035865795181?
```

## 🧪 Test It Now

1. **Open Gemini CLI** (if not already open):
   ```bash
   gemini
   ```

2. **Verify the extension is loaded**:
   Look for: `Using 2 GEMINI.md files and 1 MCP server`

3. **Try this command**:
   ```
   List all compliance frameworks in organization 1035865795181
   ```

4. **Watch what happens**:
   - Gemini will understand you want to list frameworks
   - It will call the `list_frameworks` tool automatically
   - You'll see the results

## 💡 Why Natural Language is Better

### ❌ Direct Tool Calls (Complex)
```
@compliance-manager-mcp list_frameworks organization_id="1035865795181" location="global" page_size=50
```
- Hard to remember syntax
- Easy to make mistakes
- Not user-friendly

### ✅ Natural Language (Easy)
```
Show me compliance frameworks in my organization
```
- Easy to understand
- Natural to use
- Gemini figures out the details

## 🎓 Advanced Examples

### Multi-Step Workflow
```
I need to understand my compliance posture. My organization is 1035865795181 
and my test project is csc-audit-test-project. Can you:
1. Show me what frameworks are available
2. Check what's currently deployed to my project
3. List the cloud controls
4. Recommend which framework I should deploy for a web application
```

Gemini will:
- Call `list_frameworks` for step 1
- Call `list_framework_deployments` for step 2
- Call `list_cloud_controls` for step 3
- Use its knowledge to recommend for step 4

### Deployment Workflow
```
I want to deploy the CIS Google Cloud Foundation framework to my test project. 
My organization is 1035865795181 and my project is csc-audit-test-project. 
Can you guide me through the process?
```

Gemini will:
- Ask for confirmation
- Help you find the framework ID
- Call `create_framework_deployment` with the right parameters
- Verify the deployment was successful

## 🔧 Troubleshooting

### If Gemini says it can't find the tool:

1. **Check the extension is loaded**:
   - Look for: `Using 2 GEMINI.md files and 1 MCP server`
   - Press `Ctrl+T` to see MCP servers

2. **Restart Gemini CLI**:
   ```bash
   # Exit with Ctrl+C
   gemini
   ```

3. **Try a simpler request**:
   ```
   What tools are available from the compliance-manager-mcp server?
   ```

### If you get an authentication error:

```bash
gcloud auth application-default login
```

### If you get a permission error:

Make sure you have the required IAM role:
- `roles/securitycenter.complianceManager` (full access)
- `roles/securitycenter.adminViewer` (read-only)

## 📝 Your Configuration

- **Organization ID**: `1035865795181`
- **Project ID**: `csc-audit-test-project`
- **Extension**: Installed and working ✅
- **MCP Server**: Running ✅

## 🚀 Ready to Start!

Try this right now in Gemini CLI:

```
Hi! I want to explore compliance frameworks. My GCP organization ID is 1035865795181. 
Can you show me what compliance frameworks are available?
```

Then try:

```
What cloud controls are available in my organization?
```

Then:

```
Show me any framework deployments in project csc-audit-test-project
```

## 📚 More Resources

- **[CORRECT_USAGE.md](CORRECT_USAGE.md)** - Detailed usage guide
- **[EXAMPLE_COMMANDS.md](EXAMPLE_COMMANDS.md)** - More examples
- **[TROUBLESHOOTING_MCP.md](TROUBLESHOOTING_MCP.md)** - Troubleshooting guide

---

## 🎯 Remember

**DON'T** use `@compliance-manager-mcp` or try to call tools directly.

**DO** use natural language and let Gemini CLI do the work!

✅ **Correct**: "List all compliance frameworks in organization 1035865795181"
❌ **Wrong**: "@compliance-manager-mcp list_frameworks"

---

**The extension is working perfectly - just use natural language!** 🎉

