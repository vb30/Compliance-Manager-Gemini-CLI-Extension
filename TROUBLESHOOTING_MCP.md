# Troubleshooting MCP Server Issues

## Issue: "Tool not present in registry" in Gemini CLI

### Verified Working

✅ **MCP Server is working correctly** - The test script confirms all 10 tools are exposed:
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

### Possible Causes

1. **Incorrect tool invocation syntax**
2. **MCP server not starting in Gemini CLI**
3. **Extension not loaded properly**

### Solutions

#### Solution 1: Check MCP Server Status in Gemini CLI

In Gemini CLI, press `Ctrl+T` to view MCP servers. You should see:
- `compliance-manager-mcp` listed
- Status should be "connected" or "running"

#### Solution 2: Use Correct Tool Invocation Syntax

**Option A: Direct MCP tool call (recommended)**
```
list_frameworks organization_id="1035865795181"
```

**Option B: With server prefix**
```
compliance-manager-mcp/list_frameworks organization_id="1035865795181"
```

**Option C: Natural language (let Gemini choose the tool)**
```
Show me all compliance frameworks in organization 1035865795181
```

**DON'T use** `@compliance-manager-mcp` - that's for mentioning files, not MCP tools.

#### Solution 3: Restart Gemini CLI

Sometimes Gemini CLI needs to be restarted after installing an extension:

```bash
# Exit Gemini CLI (Ctrl+C or type 'exit')
# Then restart
gemini
```

#### Solution 4: Check Extension is Loaded

When Gemini CLI starts, you should see:
```
Loading extension: compliance-manager (version: 1.0.0)
```

And at the bottom:
```
Using 2 GEMINI.md files and 1 MCP server (ctrl+t to view)
```

#### Solution 5: Verify Extension Files

```bash
ls -la ~/.gemini/extensions/compliance-manager/
```

Should show:
- gemini-extension.json
- GEMINI.md
- compliance_manager_mcp.py
- pyproject.toml

#### Solution 6: Check MCP Server Logs

If the MCP server has errors, check by running it manually:

```bash
cd ~/.gemini/extensions/compliance-manager
/opt/homebrew/bin/uv run compliance_manager_mcp.py
```

You should see:
```
INFO Successfully initialized Compliance Manager Config Client.
INFO Successfully initialized Compliance Manager Deployment Client.
INFO Starting Compliance Manager MCP server...
```

Press Ctrl+C to stop.

#### Solution 7: Test MCP Server Directly

Run the test script:

```bash
python3 test_mcp_server.py
```

Should output:
```
✓ Found 10 tools:
  - list_frameworks
  - get_framework
  ...
```

### Correct Usage Examples

Once the extension is loaded, use these commands in Gemini CLI:

#### Example 1: List Frameworks
```
list_frameworks organization_id="1035865795181"
```

#### Example 2: Get Framework Details
```
get_framework organization_id="1035865795181" framework_id="cis-google-cloud-foundation-v1.3.0"
```

#### Example 3: List Deployments
```
list_framework_deployments parent="projects/csc-audit-test-project"
```

#### Example 4: Natural Language
```
Show me all compliance frameworks available in my organization 1035865795181
```

### Common Mistakes

❌ **Wrong**: `@compliance-manager-mcp list_frameworks`
✅ **Right**: `list_frameworks organization_id="1035865795181"`

❌ **Wrong**: `@list_frameworks`
✅ **Right**: `list_frameworks organization_id="1035865795181"`

❌ **Wrong**: `compliance-manager-mcp.list_frameworks`
✅ **Right**: `list_frameworks organization_id="1035865795181"`

### Debug Checklist

- [ ] Extension shows as loaded when Gemini CLI starts
- [ ] "1 MCP server" shown at bottom of Gemini CLI
- [ ] Ctrl+T shows `compliance-manager-mcp` server
- [ ] Test script (`python3 test_mcp_server.py`) shows 10 tools
- [ ] Using correct syntax (no `@` prefix for MCP tools)
- [ ] Tried restarting Gemini CLI

### Still Not Working?

1. **Check Gemini CLI version**:
   ```bash
   gemini --version
   ```
   Should be 0.10.0 or higher.

2. **Reinstall the extension**:
   ```bash
   rm -rf ~/.gemini/extensions/compliance-manager
   ./install.sh
   ```

3. **Check for conflicting extensions**:
   ```bash
   ls ~/.gemini/extensions/
   ```

4. **View Gemini CLI errors**:
   In Gemini CLI, press `Ctrl+O` to see error details.

### Getting Help

If you're still having issues:

1. Note the exact error message
2. Check what `Ctrl+T` shows for MCP servers
3. Run `python3 test_mcp_server.py` and share output
4. Share the output of `Ctrl+O` (error details) from Gemini CLI

---

## Quick Test

Try this in Gemini CLI:

```
I need help using the Compliance Manager extension. Can you list all the tools available from the compliance-manager-mcp server?
```

Gemini should be able to see and list all 10 tools if the extension is working correctly.

