# ✅ CORRECT USAGE - Compliance Manager Extension

## 🚨 Important Discovery

Based on your error, Gemini CLI is looking for tools with the format:
```
compliance-manager-mcp:list_frameworks
```

But the MCP server is registering tools as:
```
list_frameworks
```

## ✅ Solution: Use Natural Language

**DON'T** try to call MCP tools directly with `@` syntax. Instead, use **natural language** and let Gemini CLI figure out which tool to use.

### ❌ WRONG (What you tried)
```
@compliance-manager-mcp list_frameworks
```

### ✅ CORRECT (What you should do)

#### Example 1: List Frameworks
```
I need to list all compliance frameworks in organization 1035865795181
```

or

```
Show me all compliance frameworks available in my GCP organization 1035865795181
```

#### Example 2: Get Framework Details
```
Tell me about the CIS Google Cloud Foundation framework in organization 1035865795181
```

#### Example 3: List Deployments
```
What framework deployments exist in project csc-audit-test-project?
```

#### Example 4: Create Deployment
```
I want to deploy the CIS framework to project csc-audit-test-project. 
The framework ID is cis-google-cloud-foundation-v1.3.0 and I want to call 
the deployment "cis-deployment-001"
```

## 🎯 How It Works

When you use natural language:
1. Gemini CLI reads your request
2. It looks at available MCP tools
3. It automatically calls the right tool with the right parameters
4. You get the results

## 📋 Natural Language Templates

### Discovery
```
- "List all compliance frameworks in organization 1035865795181"
- "Show me available cloud controls in my organization"
- "What compliance frameworks are available?"
```

### Inspection
```
- "Get details of framework [FRAMEWORK_ID] in organization 1035865795181"
- "Tell me about cloud control [CONTROL_ID]"
- "Show me information about the CIS framework"
```

### Deployments
```
- "List all framework deployments in project csc-audit-test-project"
- "What frameworks are deployed to my organization?"
- "Show me deployment status for [DEPLOYMENT_ID]"
```

### Actions
```
- "Deploy the CIS framework to project csc-audit-test-project"
- "Remove deployment [DEPLOYMENT_ID] from my project"
- "Create a new framework deployment"
```

## 🧪 Test It Now

Try this in Gemini CLI:

```
I need to see all compliance frameworks available in organization 1035865795181. 
Can you list them for me?
```

Gemini should:
1. Understand you want to list frameworks
2. Call the `list_frameworks` tool automatically
3. Pass `organization_id="1035865795181"`
4. Show you the results

## 💡 Why Natural Language?

The MCP (Model Context Protocol) is designed to let AI assistants use tools on your behalf. You describe what you want in plain English, and Gemini CLI:
- Figures out which tool to use
- Determines the right parameters
- Calls the tool
- Interprets the results for you

This is **much better** than trying to call tools directly!

## 🔍 Checking If It's Working

After you ask a question in natural language, watch for:

1. **Tool call indicator**: You'll see something like:
   ```
   ⚙ Calling tool: list_frameworks
   ```

2. **Results**: Gemini will show you the results and explain them

3. **Errors**: If there's an error, Gemini will explain what went wrong

## 📝 Your First Test

Copy and paste this into Gemini CLI:

```
Hi! I want to explore compliance frameworks. My GCP organization ID is 1035865795181. 
Can you show me what compliance frameworks are available?
```

Gemini should automatically:
- Recognize you want to list frameworks
- Call `list_frameworks` with `organization_id="1035865795181"`
- Show you the results in a readable format

## 🎓 Advanced Usage

Once you're comfortable, you can ask complex questions:

```
I need to understand my compliance posture. My organization is 1035865795181 
and my test project is csc-audit-test-project. Can you:
1. Show me what frameworks are available
2. Check what's currently deployed to my project
3. Recommend which framework I should deploy for a web application
```

Gemini will:
- Call `list_frameworks` for step 1
- Call `list_framework_deployments` for step 2
- Use its knowledge to recommend a framework for step 3

## ⚠️ Common Mistakes

❌ **Don't do this**:
```
@compliance-manager-mcp list_frameworks organization_id="1035865795181"
```

✅ **Do this instead**:
```
List all compliance frameworks in organization 1035865795181
```

---

❌ **Don't do this**:
```
compliance-manager-mcp:list_frameworks
```

✅ **Do this instead**:
```
Show me available compliance frameworks
```

---

❌ **Don't do this**:
```
Call the list_frameworks tool
```

✅ **Do this instead**:
```
I need to see all compliance frameworks in my organization
```

## 🚀 Ready to Try?

Start with this simple request:

```
List all compliance frameworks available in organization 1035865795181
```

Then try:

```
What cloud controls are available in my organization?
```

Then:

```
Show me any framework deployments in project csc-audit-test-project
```

## 📚 More Examples

See [EXAMPLE_COMMANDS.md](EXAMPLE_COMMANDS.md) for more natural language examples tailored to your organization and project.

---

**Remember**: Let Gemini CLI do the work! Just describe what you want in natural language. 🎯

