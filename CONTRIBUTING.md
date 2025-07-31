# Contributing to DEPAAD

Thank you for your interest in contributing to DEPAAD!

## Getting Started

### Prerequisites
- Python 3.7.9+
- Access to Azure AD tenant (for testing)
- MobileIron Cloud instance (for integration testing)

### Development Setup

1. **Fork and clone**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/DEPAAD.git
   cd DEPAAD
   git remote add upstream https://github.com/vcruzcid/DEPAAD.git
   ```

2. **Setup environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your development values
   ```

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small

### Security Requirements
- **Never commit secrets** - Use environment variables
- Validate all user inputs
- Handle errors gracefully without exposing sensitive information
- Follow secure session management practices

### Testing
```bash
# Run the application locally
python app/app.py

# Test with different scenarios:
# - iOS device access with valid serial
# - Non-iOS device access (should be blocked)
# - Invalid device serial handling
# - Azure AD authentication flow
```

## Contributing Process

### Branch Strategy
- `main`: Production code
- `develop`: Integration branch
- `feature/description`: New features
- `bugfix/description`: Bug fixes

### Commit Messages
Use clear, descriptive commit messages:
```
feat: add device validation for non-iOS platforms
fix: handle MobileIron API timeout errors
docs: update configuration instructions
```

### Pull Request Process

1. **Create feature branch**:
   ```bash
   git checkout develop
   git checkout -b feature/your-feature
   ```

2. **Make changes and test**:
   - Follow coding standards
   - Test your changes thoroughly
   - Update documentation if needed

3. **Submit pull request**:
   - Target the `develop` branch
   - Include clear description of changes
   - Reference any related issues

## Issue Reporting

### Bug Reports
Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, browser)
- Error messages or screenshots

### Feature Requests
Include:
- Problem statement
- Proposed solution
- Use cases and benefits

## Security

Report security vulnerabilities privately via GitHub security advisories or email maintainers directly. Do not create public issues for security problems.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.