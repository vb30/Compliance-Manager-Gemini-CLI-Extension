# Troubleshooting Guide

## MCP Server Shows as "Disconnected"

If you see the MCP server as disconnected in Gemini CLI (press `Ctrl+T` to check):

```
🔴 compliance-manager-mcp - Disconnected (0 tools cached)
```

### Solution 1: Check Error Details

Press `Ctrl+O` in Gemini CLI to see error details. Common errors:

#### Error: "Connection closed"
This usually means stderr output is interfering with the MCP protocol.

**Fix**: Make sure you're using the `run_mcp.sh` wrapper script (installed automatically).

#### Error: "spawn ${extensionPath}/run_mcp.sh ENOENT"
The `${extensionPath}` variable is not being expanded.

**Fix**: The install script should replace this with an absolute path. If not, manually edit:
```bash
# For user-level installation
nano ~/.gemini/extensions/compliance-manager/gemini-extension.json

# For project-level installation
nano ./.gemini/extensions/compliance-manager/gemini-extension.json
```

Replace `${extensionPath}/run_mcp.sh` with the absolute path to `run_mcp.sh`.

### Solution 2: Verify Installation

Check that all files are in place:

```bash
# For user-level installation
ls -la ~/.gemini/extensions/compliance-manager/

# For project-level installation
ls -la ./.gemini/extensions/compliance-manager/
```

You should see:
- `gemini-extension.json`
- `GEMINI.md`
- `compliance_manager_mcp.py`
- `pyproject.toml`
- `run_mcp.sh` (executable)
- `.venv/` directory

### Solution 3: Test MCP Server Manually

```bash
# Navigate to extension directory
cd ~/.gemini/extensions/compliance-manager/
# or
cd ./.gemini/extensions/compliance-manager/

# Test the MCP server
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | ./run_mcp.sh
```

You should see a JSON response starting with:
```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05"...
```

If you see errors, check:
1. Python virtual environment: `.venv/bin/python3 --version`
2. MCP package installed: `.venv/bin/python3 -c "import mcp; print('OK')"`
3. Google Cloud package: `.venv/bin/python3 -c "from google.cloud.cloudsecuritycompliance_v1.services.config import ConfigClient; print('OK')"`

### Solution 4: Reinstall

```bash
rm -rf ~/.gemini/extensions/compliance-manager
# or
rm -rf ./.gemini/extensions/compliance-manager

./install.sh
```

Then restart Gemini CLI.

## Tools Not Found in Registry

If Gemini CLI shows the tools in the list but says "Tool not found in registry" when you try to use them:

### Cause
The MCP server is not connected (see "MCP Server Shows as Disconnected" above).

### Solution
1. Press `Ctrl+T` to check MCP server status
2. If disconnected, follow the steps above
3. Restart Gemini CLI after fixing

## Authentication Errors

### Error: "Permission denied" or "Forbidden"

**Cause**: Missing Google Cloud authentication or insufficient permissions.

**Solution**:

1. **Authenticate**:
   ```bash
   gcloud auth application-default login
   ```

2. **Verify authentication**:
   ```bash
   gcloud auth application-default print-access-token
   ```

3. **Check IAM permissions**:
   You need one of these roles:
   - `roles/securitycenter.complianceManager` (full access)
   - `roles/securitycenter.adminViewer` (read-only)

   To grant the role:
   ```bash
   gcloud organizations add-iam-policy-binding YOUR_ORG_ID \
     --member="user:YOUR_EMAIL" \
     --role="roles/securitycenter.complianceManager"
   ```

## Gemini CLI Not Recognizing Extension

### Check Extension Loading

When you start Gemini CLI, you should see:
```
Loading extension: compliance-manager (version: 1.0.0)
```

If you don't see this:

1. **Check extension directory**:
   ```bash
   ls ~/.gemini/extensions/
   # or
   ls ./.gemini/extensions/
   ```

2. **Verify gemini-extension.json**:
   ```bash
   cat ~/.gemini/extensions/compliance-manager/gemini-extension.json
   # or
   cat ./.gemini/extensions/compliance-manager/gemini-extension.json
   ```

3. **Restart Gemini CLI** after any changes

## Using the Extension

### ✅ CORRECT Usage

Use **natural language** - don't try to call tools directly:

```
List all compliance frameworks in organization 1035865795181
```

```
Show me cloud controls in my organization
```

```
What framework deployments exist in project my-project-id?
```

### ❌ WRONG Usage

Don't use `@` symbol for MCP tools:

```
@compliance-manager-mcp list_frameworks  ❌ WRONG
```

The `@` symbol is for mentioning files, not for calling MCP tools.

## Workspace vs Global Installation

Gemini CLI checks for extensions in this order:

1. **Workspace**: `./.gemini/extensions/` (current directory)
2. **Global**: `~/.gemini/extensions/` (home directory)

If you have the extension installed in both locations, the workspace version takes precedence.

To check which one is being used:
```bash
# Check workspace
ls ./.gemini/extensions/compliance-manager/ 2>/dev/null && echo "Workspace installation found"

# Check global
ls ~/.gemini/extensions/compliance-manager/ 2>/dev/null && echo "Global installation found"
```

## Getting Help

If you're still having issues:

1. **Check error details**: Press `Ctrl+O` in Gemini CLI
2. **Check MCP status**: Press `Ctrl+T` in Gemini CLI
3. **Test manually**: Run the MCP server test (see Solution 3 above)
4. **Check logs**: Look for any log files in `~/.gemini/logs/` or `~/.gemini/tmp/`

## Common Issues Summary

| Issue | Solution |
|-------|----------|
| Server disconnected | Check `Ctrl+O` for errors, verify `run_mcp.sh` exists and is executable |
| Tool not found | Server is disconnected, fix connection first |
| Permission denied | Run `gcloud auth application-default login` |
| Extension not loading | Check extension directory, verify `gemini-extension.json` |
| `${extensionPath}` not expanded | Install script should fix this, or manually replace with absolute path |

## Still Need Help?

Create an issue on GitHub with:
- Output of `Ctrl+O` (error details)
- Output of `Ctrl+T` (MCP server status)
- Output of manual MCP server test
- Your installation method (user-level or project-level)

