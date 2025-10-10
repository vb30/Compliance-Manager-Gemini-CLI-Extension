# Debug Instructions

## Current Status

✅ **MCP Server is working** - Confirmed by manual testing
✅ **Extension is installed** - Files are in `~/.gemini/extensions/compliance-manager/`
✅ **Gemini CLI detects the extension** - Shows "Using 2 GEMINI.md files and 1 MCP server"
❌ **Gemini CLI can't call the tools** - Trying to execute as shell commands instead

## The Problem

Gemini CLI is trying to execute `@compliance-manager-mcp` as a **shell command** instead of recognizing it as an MCP tool. This suggests that:

1. The MCP server might not be starting correctly when Gemini CLI launches it
2. The MCP server might be starting but not responding to the `tools/list` request
3. There might be a communication issue between Gemini CLI and the MCP server

## Next Steps

### Step 1: Check the Error Details

In Gemini CLI, press `Ctrl+O` to see the error details. This will show you what the "1 error" is.

**Please share what you see!**

### Step 2: Check MCP Server Status

In Gemini CLI, press `Ctrl+T` to view MCP servers. You should see:
- Server name: `compliance-manager-mcp`
- Status: Should show if it's connected or has errors

**Please share what you see!**

### Step 3: Try Natural Language (Without @)

Instead of using `@compliance-manager-mcp`, try this:

```
I need to list all compliance frameworks in organization 1035865795181. Can you help?
```

Gemini should:
1. Read the GEMINI.md file to understand what tools are available
2. Attempt to call the `list_frameworks` tool
3. Either succeed or show a more detailed error

### Step 4: Check Gemini CLI Logs

Gemini CLI might have logs that show what's happening. Try:

```bash
ls -la ~/.gemini/logs/ 2>/dev/null
```

If there are log files, check the most recent one:

```bash
tail -50 ~/.gemini/logs/$(ls -t ~/.gemini/logs/ | head -1)
```

## Possible Solutions

### Solution 1: Restart Gemini CLI

Sometimes Gemini CLI needs a fresh start:

```bash
# Exit Gemini CLI (Ctrl+C)
# Then restart
gemini
```

### Solution 2: Reinstall the Extension

```bash
rm -rf ~/.gemini/extensions/compliance-manager
./install.sh
```

Then restart Gemini CLI.

### Solution 3: Check Gemini CLI Version

```bash
gemini --version
```

Make sure you have version 0.10.0 or higher.

### Solution 4: Try a Different Approach

Instead of trying to call tools directly, use natural language and let Gemini figure it out:

**DON'T do this:**
```
@compliance-manager-mcp list_frameworks organization_id="1035865795181"
```

**DO this:**
```
I need to see all compliance frameworks available in organization 1035865795181
```

## What We Know

1. ✅ The MCP server works when tested manually
2. ✅ All 10 tools are properly exposed by the MCP server
3. ✅ The extension files are correctly installed
4. ✅ Gemini CLI detects the extension
5. ❌ Gemini CLI is not recognizing the tools

## Most Likely Cause

The MCP server is probably **failing to start** when Gemini CLI tries to launch it, OR it's starting but **not responding to the tools/list request** in time.

## What to Check

1. **Error details** (Ctrl+O in Gemini CLI)
2. **MCP server status** (Ctrl+T in Gemini CLI)
3. **Try natural language** instead of `@` syntax
4. **Check logs** if they exist

## Please Share

1. What does `Ctrl+O` show in Gemini CLI?
2. What does `Ctrl+T` show in Gemini CLI?
3. What happens when you try: "List all compliance frameworks in organization 1035865795181"

This information will help us diagnose the exact issue!

