# Deployment Guide

This guide explains how to deploy and distribute the Compliance Manager Gemini CLI Extension.

## Table of Contents

- [Local Installation](#local-installation)
- [Distribution Methods](#distribution-methods)
- [Publishing to GitHub](#publishing-to-github)
- [Version Management](#version-management)
- [User Installation](#user-installation)

## Local Installation

### For Development

```bash
# Clone the repository
git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
cd Compliance-Manager-Gemini-CLI-Extension

# Install dependencies
uv pip install -e .

# Run the installation script
./install.sh
```

### For Testing

```bash
# Test the extension
python3 test_extension.py

# Test the MCP server directly
uv run compliance_manager_mcp.py
```

## Distribution Methods

### Method 1: GitHub Repository (Recommended)

Users can install directly from GitHub:

```bash
# Clone the repository
git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
cd Compliance-Manager-Gemini-CLI-Extension

# Run the installation script
./install.sh
```

### Method 2: ZIP Archive

Create a distributable ZIP file:

```bash
# Create a release archive
git archive --format=zip --output=compliance-manager-gemini-cli-extension-v1.0.0.zip HEAD

# Users can then download and extract
unzip compliance-manager-gemini-cli-extension-v1.0.0.zip
cd compliance-manager-gemini-cli-extension
./install.sh
```

### Method 3: Direct File Copy

For manual installation:

```bash
# Create extension directory
mkdir -p ~/.gemini/extensions/compliance-manager

# Copy files
cp gemini-extension.json ~/.gemini/extensions/compliance-manager/
cp GEMINI.md ~/.gemini/extensions/compliance-manager/
cp compliance_manager_mcp.py ~/.gemini/extensions/compliance-manager/
cp pyproject.toml ~/.gemini/extensions/compliance-manager/

# Install dependencies
cd ~/.gemini/extensions/compliance-manager
uv pip install -e .
```

## Publishing to GitHub

### Initial Setup

1. **Create a new repository** on GitHub:
   - Repository name: `Compliance-Manager-Gemini-CLI-Extension`
   - Description: "Gemini CLI extension for Google Cloud Compliance Manager"
   - License: Apache 2.0
   - Add README: No (we already have one)

2. **Push the code**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Compliance Manager Gemini CLI Extension v1.0.0"
   git branch -M main
   git remote add origin https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
   git push -u origin main
   ```

### Creating a Release

1. **Tag the version**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Create a GitHub Release**:
   - Go to the repository on GitHub
   - Click "Releases" → "Create a new release"
   - Choose the tag `v1.0.0`
   - Title: "v1.0.0 - Initial Release"
   - Description: Include release notes (see below)
   - Attach the ZIP archive (optional)
   - Click "Publish release"

### Release Notes Template

```markdown
## Compliance Manager Gemini CLI Extension v1.0.0

### Features

- 🎯 11 MCP tools for comprehensive compliance management
- 🤖 Natural language interface via Gemini CLI
- 📦 Automated installation script
- 📚 Comprehensive documentation
- ✅ Test suite for verification

### Available Tools

**Framework Management**
- `list_frameworks` - List all available compliance frameworks
- `get_framework` - Get detailed framework information

**Cloud Control Management**
- `list_cloud_controls` - List all cloud controls
- `get_cloud_control` - Get detailed cloud control information

**Framework Deployment**
- `list_framework_deployments` - List framework deployments
- `get_framework_deployment` - Get deployment details
- `create_framework_deployment` - Deploy a framework
- `delete_framework_deployment` - Remove a deployment

**Cloud Control Deployment**
- `list_cloud_control_deployments` - List cloud control deployments
- `get_cloud_control_deployment` - Get cloud control deployment details

### Installation

```bash
git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
cd Compliance-Manager-Gemini-CLI-Extension
./install.sh
```

### Documentation

- [README.md](README.md) - Main documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [INSTALLATION.md](INSTALLATION.md) - Detailed installation
- [EXAMPLES.md](EXAMPLES.md) - Usage examples
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guidelines

### Requirements

- Gemini CLI
- Python 3.11+
- uv package manager
- Google Cloud account with Compliance Manager access

### Related Projects

- [Compliance Manager MCP Server](https://github.com/vb30/Compliance-Manager-MCP-Server)
```

## Version Management

### Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (1.x.x): Incompatible API changes
- **MINOR** version (x.1.x): New functionality (backwards compatible)
- **PATCH** version (x.x.1): Bug fixes (backwards compatible)

### Updating Version

When releasing a new version:

1. **Update version in files**:
   - `pyproject.toml`: `version = "1.1.0"`
   - `gemini-extension.json`: `"version": "1.1.0"`
   - `setup.py`: `version="1.1.0"`

2. **Update CHANGELOG** (create if doesn't exist):
   ```markdown
   # Changelog
   
   ## [1.1.0] - 2025-10-15
   ### Added
   - New feature X
   
   ### Fixed
   - Bug Y
   ```

3. **Commit and tag**:
   ```bash
   git add .
   git commit -m "Bump version to 1.1.0"
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin main
   git push origin v1.1.0
   ```

4. **Create GitHub Release** with release notes

## User Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
cd Compliance-Manager-Gemini-CLI-Extension
./install.sh
```

### Manual Install

```bash
# 1. Clone repository
git clone https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
cd Compliance-Manager-Gemini-CLI-Extension

# 2. Install dependencies
uv pip install -e .

# 3. Create extension directory
mkdir -p ~/.gemini/extensions/compliance-manager

# 4. Copy files
cp gemini-extension.json ~/.gemini/extensions/compliance-manager/
cp GEMINI.md ~/.gemini/extensions/compliance-manager/
cp compliance_manager_mcp.py ~/.gemini/extensions/compliance-manager/
cp pyproject.toml ~/.gemini/extensions/compliance-manager/

# 5. Update uv path (macOS)
# Edit ~/.gemini/extensions/compliance-manager/gemini-extension.json
# Change "command": "uv" to "command": "/full/path/to/uv"

# 6. Restart Gemini CLI
gemini
```

## Maintenance

### Regular Updates

1. **Monitor dependencies** for security updates
2. **Update Google Cloud SDK** when new versions are released
3. **Test with new Gemini CLI versions**
4. **Review and merge community contributions**

### Security Updates

If a security vulnerability is found:

1. **Create a patch** immediately
2. **Bump the PATCH version**
3. **Create a security advisory** on GitHub
4. **Notify users** through GitHub releases

## Support

### Documentation

Ensure all documentation is up to date:
- README.md
- INSTALLATION.md
- QUICKSTART.md
- EXAMPLES.md
- CONTRIBUTING.md

### Issue Management

- **Triage issues** regularly
- **Label issues** appropriately (bug, enhancement, documentation, etc.)
- **Respond to questions** promptly
- **Close resolved issues**

### Community Engagement

- **Welcome new contributors**
- **Review pull requests** promptly
- **Acknowledge contributions**
- **Maintain a positive community**

## Checklist for New Release

- [ ] Update version numbers in all files
- [ ] Update CHANGELOG.md
- [ ] Run all tests
- [ ] Update documentation
- [ ] Create git tag
- [ ] Push to GitHub
- [ ] Create GitHub Release
- [ ] Announce release (if applicable)
- [ ] Monitor for issues

## Rollback Procedure

If a release has critical issues:

1. **Identify the issue**
2. **Revert to previous version**:
   ```bash
   git revert <commit-hash>
   git push origin main
   ```
3. **Create a new patch release** with the fix
4. **Notify users** of the issue and fix

## Analytics and Metrics

Track these metrics to understand usage:

- GitHub stars and forks
- Download/clone statistics
- Issue and PR activity
- User feedback and questions

## Future Enhancements

Planned features for future releases:

- Custom command shortcuts
- Compliance reporting templates
- Multi-organization support
- Batch deployment operations
- Integration with other GCP security services

---

**Last Updated**: 2025-10-10

**Current Version**: 1.0.0

**Maintainer**: Varun Bhardwaj

