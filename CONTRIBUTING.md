# Contributing to DEPAAD

Thank you for your interest in contributing to DEPAAD! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Security Guidelines](#security-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [License](#license)

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful**: Treat all contributors with respect and courtesy
- **Be inclusive**: Welcome contributors of all backgrounds and skill levels
- **Be constructive**: Provide helpful feedback and suggestions
- **Be professional**: Maintain professional communication standards
- **Be secure**: Follow security best practices in all contributions

## 🚀 Getting Started

### Prerequisites

- Python 3.7.9 or higher
- Git (latest version)
- Access to Azure AD tenant (for testing)
- MobileIron Cloud instance (for integration testing)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/DEPAAD.git
   cd DEPAAD
   ```
3. Add the original repository as upstream:
   ```bash
   git remote add upstream https://github.com/vcruzcid/DEPAAD.git
   ```

## 🛠️ Development Environment

### Local Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your development values
   ```

4. **Install pre-commit hooks** (recommended):
   ```bash
   pre-commit install
   ```

### IDE Configuration

#### Visual Studio Code
Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "autopep8",
  "python.testing.pytestEnabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".venv": true,
    "flask_session": true
  }
}
```

## 🔄 Contributing Process

### Git Flow Workflow

We use Git Flow for branch management:

- **`main`**: Production-ready code
- **`develop`**: Integration branch for features
- **`feature/*`**: New features or enhancements
- **`hotfix/*`**: Critical bug fixes for production
- **`release/*`**: Release preparation

### Branch Naming Convention

- Features: `feature/issue-number-short-description`
- Bug fixes: `bugfix/issue-number-short-description`
- Hotfixes: `hotfix/issue-number-short-description`
- Documentation: `docs/short-description`

Examples:
- `feature/123-azure-ad-groups`
- `bugfix/456-session-timeout`
- `hotfix/789-security-vulnerability`

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(auth): add support for Azure AD groups
fix(api): handle MobileIron API timeout errors
docs: update deployment instructions
test(auth): add integration tests for OAuth flow
```

## 📏 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Code Quality Tools

Run these tools before submitting:

```bash
# Code formatting
black app/ tests/

# Import sorting
isort app/ tests/

# Linting
flake8 app/ tests/
pylint app/ tests/

# Type checking (if using mypy)
mypy app/

# Security scanning
bandit -r app/
safety check
```

### Documentation Standards

- Write clear, concise docstrings for all functions and classes
- Use Google-style docstrings
- Update README.md for significant changes
- Include inline comments for complex logic

Example docstring:
```python
def assign_device(userid: str, deviceid: str) -> requests.Response:
    """Assign a device to a user in MobileIron Cloud.
    
    This function makes an API call to MobileIron Cloud to associate
    a specific device with a user account.
    
    Args:
        userid (str): The MobileIron user account ID
        deviceid (str): The device ID to assign
        
    Returns:
        requests.Response: The API response object
        
    Raises:
        requests.RequestException: If the API call fails
        ValueError: If userid or deviceid is invalid
    """
```

## 🔒 Security Guidelines

### Security Requirements

- **Never commit secrets**: Use environment variables for sensitive data
- **Input validation**: Validate all user inputs
- **Output encoding**: Properly encode outputs to prevent XSS
- **Authentication**: Maintain secure session management
- **Authorization**: Implement proper access controls
- **Logging**: Log security events without exposing sensitive data

### Security Checklist

Before submitting code, ensure:

- [ ] No hardcoded secrets or credentials
- [ ] Input validation for all user data
- [ ] Proper error handling without information disclosure
- [ ] Secure session management
- [ ] HTTPS enforcement in production
- [ ] Dependencies are up to date
- [ ] Security headers are properly configured

### Vulnerability Reporting

Report security vulnerabilities privately to: security@company.com

Do not create public issues for security vulnerabilities.

## 🧪 Testing Requirements

### Test Categories

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **Security Tests**: Test security controls
4. **End-to-End Tests**: Test complete workflows

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/security/

# Run performance tests
python -m pytest tests/performance/ --benchmark-only
```

### Test Standards

- Maintain minimum 80% code coverage
- Write descriptive test names
- Use fixtures for common test data
- Mock external dependencies
- Test both success and failure scenarios

Example test structure:
```python
def test_assign_device_success():
    """Test successful device assignment."""
    # Arrange
    userid = "test-user-123"
    deviceid = "test-device-456"
    
    # Act
    result = assign_device(userid, deviceid)
    
    # Assert
    assert result.status_code == 200
    assert "success" in result.json()
```

## 📝 Pull Request Process

### Before Submitting

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout develop
   git merge upstream/develop
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**:
   ```bash
   python -m pytest
   flake8 app/ tests/
   bandit -r app/
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Template

When creating a PR, include:

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested this change manually

## Security
- [ ] I have reviewed my code for security vulnerabilities
- [ ] No sensitive information is exposed
- [ ] Input validation is implemented where needed

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and security scans
2. **Code Review**: At least one maintainer reviews the code
3. **Security Review**: Security-sensitive changes require additional review
4. **Testing**: Manual testing may be required for significant changes
5. **Approval**: PR must be approved before merging

### Merge Strategy

- Feature branches merge into `develop`
- `develop` merges into `main` for releases
- Squash commits for cleaner history
- Delete feature branches after merge

## 🐛 Issue Guidelines

### Bug Reports

Use the bug report template and include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed reproduction steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, browser, etc.
- **Screenshots**: If applicable
- **Error Messages**: Full error messages and stack traces

### Feature Requests

Use the feature request template and include:

- **Problem Statement**: What problem does this solve?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other solutions considered
- **Use Cases**: How would this be used?
- **Priority**: Business impact and urgency

### Labels

We use these labels for issue management:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `priority:high`: High priority items
- `security`: Security-related issues

## 📄 License

By contributing to DEPAAD, you agree that your contributions will be licensed under the MIT License.

## 🤔 Questions?

- Check existing issues and discussions
- Review project documentation
- Contact maintainers via GitHub issues
- Join our development chat (if available)

## 🙏 Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- Release notes for significant contributions
- Project documentation
- Annual contributor appreciation

Thank you for contributing to DEPAAD! 🚀