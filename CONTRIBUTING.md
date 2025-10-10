# Contributing to Compliance Manager Gemini CLI Extension

Thank you for your interest in contributing to the Compliance Manager Gemini CLI Extension! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project follows a code of conduct that we expect all contributors to adhere to:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Compliance-Manager-Gemini-CLI-Extension.git
   cd Compliance-Manager-Gemini-CLI-Extension
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/vb30/Compliance-Manager-Gemini-CLI-Extension.git
   ```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- uv package manager
- Gemini CLI
- Google Cloud account with Compliance Manager access

### Setup Development Environment

1. **Install dependencies**:
   ```bash
   uv pip install -e .
   ```

2. **Set up authentication**:
   ```bash
   gcloud auth application-default login
   ```

3. **Install the extension locally**:
   ```bash
   ./install.sh
   ```

4. **Run tests**:
   ```bash
   python3 test_extension.py
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Fixes** - Fix issues in the code
2. **New Features** - Add new MCP tools or capabilities
3. **Documentation** - Improve or add documentation
4. **Examples** - Add usage examples
5. **Tests** - Add or improve tests
6. **Performance** - Optimize code performance

### Contribution Workflow

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Test your changes**:
   ```bash
   python3 test_extension.py
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Example Function

```python
@mcp.tool()
async def example_tool(
    organization_id: str,
    optional_param: str = "default",
) -> Dict[str, Any]:
    """Name: example_tool

    Description: Brief description of what the tool does.
    
    Parameters:
    organization_id (required): The Google Cloud organization ID.
    optional_param (optional): Description of optional parameter. Defaults to 'default'.
    """
    if not client:
        return {"error": "Client not initialized."}
    
    try:
        # Implementation
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return {"error": "An error occurred", "details": str(e)}
```

### Documentation Standards

- Use clear, concise language
- Include code examples
- Update all relevant documentation files
- Add comments for complex logic

### File Organization

When adding new files:
- Python code: Root directory
- Documentation: Root directory (*.md files)
- Tests: Root directory (test_*.py files)
- Configuration: Root directory

## Testing

### Running Tests

```bash
# Run the test suite
python3 test_extension.py

# Test the MCP server directly
uv run compliance_manager_mcp.py
```

### Writing Tests

When adding new features, include tests that verify:
- The feature works as expected
- Error cases are handled properly
- Edge cases are covered

### Manual Testing

1. Install the extension locally
2. Start Gemini CLI
3. Test your changes with real commands
4. Verify error handling

## Submitting Changes

### Pull Request Guidelines

1. **Title**: Use a clear, descriptive title
   - Good: "Add support for custom framework parameters"
   - Bad: "Update code"

2. **Description**: Include:
   - What changes were made
   - Why the changes were needed
   - How to test the changes
   - Any breaking changes

3. **Checklist**:
   - [ ] Code follows the style guidelines
   - [ ] Tests pass
   - [ ] Documentation updated
   - [ ] Commit messages are clear
   - [ ] No merge conflicts

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example**:
```
feat: Add support for framework filtering

- Add filter parameter to list_frameworks tool
- Update documentation with filtering examples
- Add tests for filtering functionality

Closes #123
```

## Reporting Bugs

### Before Reporting

1. Check if the bug has already been reported
2. Verify it's not a configuration issue
3. Test with the latest version

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- OS: [e.g., macOS 14.0]
- Python version: [e.g., 3.11.5]
- Gemini CLI version: [e.g., 0.10.0]
- Extension version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.

**Logs**
```
Paste relevant logs here
```
```

## Suggesting Enhancements

### Enhancement Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other relevant information.

**Example usage**
How the feature would be used:
```
> Example command or interaction
```
```

## Adding New MCP Tools

When adding a new tool to the MCP server:

1. **Add the tool function** in `compliance_manager_mcp.py`:
   ```python
   @mcp.tool()
   async def new_tool(param: str) -> Dict[str, Any]:
       """Tool description"""
       # Implementation
   ```

2. **Update GEMINI.md** with:
   - Tool name and description
   - Parameters
   - Example usage

3. **Add examples** to EXAMPLES.md

4. **Update README.md** if needed

5. **Test the tool** thoroughly

## Documentation Contributions

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add more examples
- Improve installation instructions
- Add troubleshooting tips
- Translate documentation

## Review Process

1. **Automated checks** run on all PRs
2. **Maintainer review** - A maintainer will review your PR
3. **Feedback** - Address any requested changes
4. **Approval** - Once approved, your PR will be merged

## Getting Help

If you need help:

- **Questions**: Open a GitHub Discussion
- **Issues**: Open a GitHub Issue
- **Chat**: Contact the maintainers

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Thank You!

Thank you for contributing to the Compliance Manager Gemini CLI Extension! Your contributions help make compliance management more accessible and efficient for everyone.

