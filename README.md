# Compliance Manager Gemini CLI Extension

A Gemini CLI extension for Google Cloud Compliance Manager (Security Command Center Enterprise).

## What It Does

Talk to Gemini CLI in natural language to manage compliance frameworks and controls in your Google Cloud organization:
- **Discover**: List and inspect built-in compliance frameworks (CIS, NIST, FedRAMP, etc.)
- **Create**: Build custom cloud controls and frameworks for your specific requirements
- **Deploy**: Apply frameworks to organizations, folders, or projects
- **Monitor**: Track compliance deployments and findings

## Installation

### Prerequisites

1. **Gemini CLI**
   ```bash
   npm install -g @google/gemini-cli
   ```

2. **Python 3.11+** (check with `python3 --version`)

3. **Google Cloud Authentication**
   ```bash
   gcloud auth application-default login
   ```

### Install

```bash
git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
cd Compliance-Manager-Gemini-CLI-Extension
chmod +x install.sh
./install.sh
```

That's it! The script will:
- Create a virtual environment with Python's built-in venv
- Install dependencies using pip (no need for uv or other tools)
- Set up the extension in `~/.gemini/extensions/compliance-manager`

### Alternative: Manual Installation with pip

If you prefer to install manually or use pip directly:

```bash
# Clone the repository
git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
cd Compliance-Manager-Gemini-CLI-Extension

# Create extension directory
mkdir -p ~/.gemini/extensions/compliance-manager

# Create virtual environment
python3 -m venv ~/.gemini/extensions/compliance-manager/.venv

# Install dependencies using requirements.txt
~/.gemini/extensions/compliance-manager/.venv/bin/pip install -r requirements.txt

# Copy files
cp compliance_manager_mcp.py ~/.gemini/extensions/compliance-manager/
cp GEMINI.md ~/.gemini/extensions/compliance-manager/

# Create run script and config (see install.sh for details)
```

## Usage

Start Gemini CLI and talk to it naturally:

```bash
gemini
```

### Example Conversations

**Discovery:**
```
> List all compliance frameworks in organization 123456789012

> Show me details of the CIS framework

> What cloud controls are available?
```

**Creating Custom Controls:**
```
> Create a custom cloud control to check for public bucket access

> I need a control to verify MFA is enabled

> Build a custom control for data residency requirements
```

**Creating Custom Frameworks:**
```
> Create a framework called "company-security-baseline" with CIS and custom controls

> Build a custom framework for EU data residency compliance

> Combine NIST and FedRAMP controls into a new framework
```

**Deployment:**
```
> Deploy the NIST framework to project my-project-id

> Apply my custom framework to the production folder

> What frameworks are currently deployed?
```

The extension understands natural language - just ask what you need!

## Requirements

### Before You Start

**Compliance Manager must be enabled** in your Google Cloud organization:

1. You need **Security Command Center Enterprise** tier
2. Enable Compliance Manager at: https://console.cloud.google.com/security/compliance-manager
3. See the [enablement guide](https://cloud.google.com/security-command-center/docs/compliance-manager-enable)

**Need help enabling?** Just ask the extension: "How do I enable Compliance Manager?"

### IAM Permissions

You need one of these roles on your GCP organization:
- `roles/securitycenter.complianceManager` (full access)
- `roles/securitycenter.adminEditor` (full access)
- `roles/securitycenter.adminViewer` (read-only)

## Troubleshooting

**Extension not loading?**
```bash
ls -la ~/.gemini/extensions/compliance-manager/
```

**Authentication issues?**
```bash
gcloud auth application-default print-access-token
```

**Need to reinstall?**
```bash
rm -rf ~/.gemini/extensions/compliance-manager
./install.sh
```

## License

Apache 2.0

## Links

- [Compliance Manager Documentation](https://cloud.google.com/security-command-center/docs/compliance-manager-overview)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [Report Issues](https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension/issues)

