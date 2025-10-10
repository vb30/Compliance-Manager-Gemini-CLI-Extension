# 🚀 START HERE - Quick Setup for Your Organization

This is your personalized quick start guide for the Compliance Manager Gemini CLI Extension.

## ✅ Your Configuration

- **Organization ID**: `1035865795181`
- **Project ID**: `csc-audit-test-project`

## 📋 Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **Gemini CLI** installed
  ```bash
  npm install -g @google/gemini-cli
  ```

- [ ] **Python 3.11+** installed
  ```bash
  python3 --version
  ```

- [ ] **uv** package manager installed
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- [ ] **Google Cloud authentication** configured
  ```bash
  gcloud auth application-default login
  ```

- [ ] **IAM permissions** on your organization/project
  - Need: `roles/securitycenter.complianceManager` or `roles/securitycenter.adminViewer`

## 🎯 Installation (2 Minutes)

### Option 1: Automated Installation (Recommended)

```bash
# Run the installation script
./install.sh

# Test with your organization
./test_with_org.sh
```

### Option 2: Manual Installation

```bash
# Install dependencies
uv pip install -e .

# Create extension directory
mkdir -p ~/.gemini/extensions/compliance-manager

# Copy files
cp gemini-extension.json GEMINI.md compliance_manager_mcp.py pyproject.toml \
   ~/.gemini/extensions/compliance-manager/

# On macOS, update the uv path in gemini-extension.json
# Edit: ~/.gemini/extensions/compliance-manager/gemini-extension.json
# Change "command": "uv" to "command": "/Users/YOUR_USERNAME/.local/bin/uv"
```

## 🧪 Test It Works

```bash
# Run the test suite
python3 test_extension.py

# Run organization-specific tests
./test_with_org.sh
```

## 🎮 Your First Commands

Start Gemini CLI:
```bash
gemini
```

### Command 1: List Available Frameworks
```
> @compliance-manager-mcp list_frameworks organization_id="1035865795181"
```

Or use natural language:
```
> Show me all compliance frameworks in my organization
```

### Command 2: Check Current Deployments
```
> @compliance-manager-mcp list_framework_deployments parent="projects/csc-audit-test-project"
```

Or:
```
> What frameworks are deployed to my test project?
```

### Command 3: Explore Cloud Controls
```
> @compliance-manager-mcp list_cloud_controls organization_id="1035865795181"
```

Or:
```
> What cloud controls are available?
```

## 📚 What to Read Next

1. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed getting started guide with your config
2. **[EXAMPLE_COMMANDS.md](EXAMPLE_COMMANDS.md)** - All commands pre-configured for your org
3. **[EXAMPLES.md](EXAMPLES.md)** - Comprehensive usage examples
4. **[README.md](README.md)** - Full documentation

## 🎯 Your First Goal

Complete this simple workflow:

1. ✅ **List frameworks** - See what's available
   ```
   > Show me all frameworks in organization 1035865795181
   ```

2. ✅ **Get framework details** - Learn about one
   ```
   > Tell me about the CIS framework
   ```

3. ✅ **Check deployments** - See current state
   ```
   > What's deployed to project csc-audit-test-project?
   ```

4. ✅ **Ask questions** - Leverage Gemini's AI
   ```
   > Which framework should I use for a web application?
   ```

## 🔧 Troubleshooting

### Extension not loading?
```bash
ls -la ~/.gemini/extensions/compliance-manager/
# Should show: gemini-extension.json, GEMINI.md, compliance_manager_mcp.py, pyproject.toml
```

### Authentication issues?
```bash
gcloud auth application-default login
gcloud config set project csc-audit-test-project
```

### Permission errors?
```bash
# Check your permissions
gcloud projects get-iam-policy csc-audit-test-project \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:$(gcloud config get-value account)"
```

## 💡 Pro Tips

1. **Use natural language** - Gemini CLI understands context
   - Instead of: `@compliance-manager-mcp list_frameworks organization_id="1035865795181"`
   - Just say: `Show me all frameworks`

2. **Chain operations** - Ask for multiple steps
   ```
   > List all frameworks, then show me details of the CIS framework, 
     then check if it's deployed to my project
   ```

3. **Ask for help** - Gemini can explain and guide
   ```
   > How do I deploy a framework?
   > What's the difference between CIS and NIST?
   > Explain what cloud controls do
   ```

4. **Test safely** - Use your test project first
   - Always test in `csc-audit-test-project` before production

## 🎉 Quick Win

Try this complete workflow right now:

```bash
# 1. Start Gemini CLI
gemini

# 2. In Gemini CLI, paste this:
> I'm new to Compliance Manager. My organization is 1035865795181 and 
  my test project is csc-audit-test-project. Can you:
  1. Show me what frameworks are available
  2. Explain what the CIS framework does
  3. Check if any frameworks are deployed to my project
  4. Recommend next steps
```

Gemini will guide you through everything!

## 📞 Need Help?

- **In Gemini CLI**: Just ask! `> How do I...?`
- **Documentation**: See the files in this repository
- **Issues**: [GitHub Issues](https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension/issues)

## ✨ What's Next?

After you're comfortable with the basics:

1. **Deploy a framework** to your test project
2. **Monitor deployments** across your organization
3. **Explore cloud controls** and their configurations
4. **Generate compliance reports** using Gemini's AI

## 🚀 Ready to Start?

Run this now:

```bash
# Install the extension
./install.sh

# Test it works
./test_with_org.sh

# Start using it
gemini
```

Then in Gemini CLI:
```
> Show me all compliance frameworks in organization 1035865795181
```

**You're all set!** 🎊

---

**Quick Reference**:
- Org: `1035865795181`
- Project: `csc-audit-test-project`
- Extension: `~/.gemini/extensions/compliance-manager`

**Files to Read**:
1. This file (you are here!)
2. [GETTING_STARTED.md](GETTING_STARTED.md)
3. [EXAMPLE_COMMANDS.md](EXAMPLE_COMMANDS.md)

