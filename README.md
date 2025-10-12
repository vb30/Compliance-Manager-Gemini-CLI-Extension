# Compliance Manager Gemini CLI Extension

A Gemini CLI extension for Google Cloud Compliance Manager (Security Command Center Enterprise).

## What It Does

Talk to Gemini CLI in natural language to manage compliance frameworks and controls in your Google Cloud organization:
- List and inspect compliance frameworks (CIS, NIST, FedRAMP, etc.)
- View and manage cloud controls
- Deploy frameworks to organizations, folders, or projects
- Monitor compliance deployments

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
- Create a virtual environment
- Install dependencies
- Set up the extension in `~/.gemini/extensions/compliance-manager`

## Usage

Start Gemini CLI and talk to it naturally:

```bash
gemini
```

### Example Conversations

```
> List all compliance frameworks in organization 123456789012

> Show me details of the CIS framework

> Deploy the NIST framework to project my-project-id

> What frameworks are currently deployed?

> Help me understand what compliance frameworks are available
```

The extension understands natural language - just ask what you need!

## Requirements

- **IAM Permissions**: You need one of these roles on your GCP organization:
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

