# Contributing to Mergington High School Activities Management System

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences
- Accept responsibility and apologize for mistakes

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Basic knowledge of Python and JavaScript

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code.git
   cd Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code
   ```

3. **Add the upstream repository:**
   ```bash
   git remote add upstream https://github.com/FabianGonzalezLenceDataX/Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code.git
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   cd src
   python app.py
   ```

6. **Run tests to verify setup:**
   ```bash
   pytest
   ```

## Development Process

### Branch Strategy

- `main` - Stable production code
- `develop` - Development branch (if applicable)
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `docs/*` - Documentation updates

### Creating a Feature Branch

```bash
# Update your local main branch
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes in your feature branch
2. Write or update tests for your changes
3. Update documentation if needed
4. Ensure all tests pass
5. Commit your changes with clear messages

### Syncing with Upstream

Keep your fork up to date with the upstream repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Coding Standards

### Python (Backend)

Follow **PEP 8** style guidelines:

```python
# Good
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an extracurricular activity.
    
    Args:
        activity_name (str): The name of the activity
        email (str): Student's email address
    
    Returns:
        dict: Success message
    """
    pass

# Bad - missing docstring and type hints
def signup(name, email):
    pass
```

**Key Points:**
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter)
- Add docstrings to all functions, classes, and modules
- Use type hints for function parameters and returns
- Import order: standard library, third-party, local

**Tools:**
```bash
# Format code with Black
pip install black
black src/

# Check style with flake8
pip install flake8
flake8 src/

# Type checking with mypy
pip install mypy
mypy src/
```

### JavaScript (Frontend)

Follow **ES6+** standards:

```javascript
// Good
/**
 * Fetches all activities from the API.
 * @returns {Promise<void>}
 */
async function fetchActivities() {
  const response = await fetch('/activities');
  const data = await response.json();
  return data;
}

// Bad - no documentation, old syntax
function fetchActivities() {
  return fetch('/activities').then(function(response) {
    return response.json();
  });
}
```

**Key Points:**
- Use 2 spaces for indentation
- Use `const` and `let`, avoid `var`
- Use arrow functions where appropriate
- Add JSDoc comments to all functions
- Use async/await over promise chains
- Use template literals for string interpolation

**Recommended Tool:**
```bash
# Install ESLint
npm install -g eslint
eslint src/static/app.js
```

### HTML

```html
<!-- Good - semantic HTML with proper indentation -->
<section id="activities-container">
  <h3>Available Activities</h3>
  <div id="activities-list">
    <!-- Content -->
  </div>
</section>

<!-- Bad - non-semantic and poor structure -->
<div id="activities">
<div><b>Activities</b></div>
<div id="list"></div>
</div>
```

### CSS

```css
/* Good - BEM-like naming, organized */
.activity-card {
  padding: 1rem;
  margin: 1rem 0;
}

.activity-card__title {
  font-size: 1.5rem;
  font-weight: bold;
}

/* Bad - unclear naming */
.card {
  padding: 1rem;
}
```

## Testing Guidelines

### Writing Tests

All new features should include tests. Tests should be:

- **Independent**: Each test should run independently
- **Repeatable**: Tests should produce same results every time
- **Self-validating**: Tests should have clear pass/fail criteria
- **Timely**: Write tests alongside or before code

### Test Structure

```python
def test_feature_name():
    """Test description explaining what is being tested."""
    # Arrange - Set up test data
    test_data = {"key": "value"}
    
    # Act - Perform the action
    result = function_to_test(test_data)
    
    # Assert - Verify the result
    assert result == expected_value
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v
```

### Test Coverage

Aim for at least 80% code coverage for new features:

```bash
pytest --cov=src --cov-report=term-missing
```

## Documentation Guidelines

### Code Documentation

All code must be properly documented:

#### Python Files

Add a header to each new Python file:

```python
"""
University of La Laguna
School of Engineering and Technology
Degree in Computer Engineering
External Internships (PE)

@author Your Name <your.email@example.com>
@since YYYY-MM-DD
@file filename.py
@desc Brief description of the file's purpose
@see {@link https://github.com/FabianGonzalezLenceDataX/Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code}
"""
```

Add docstrings to all functions:

```python
def function_name(param1: str, param2: int) -> dict:
    """Brief description of what the function does.
    
    More detailed explanation if needed.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
    
    Returns:
        dict: Description of return value
    
    Raises:
        HTTPException: When and why this exception is raised
    
    Example:
        >>> result = function_name("test", 123)
        >>> # Returns: {"key": "value"}
    """
    pass
```

#### JavaScript Files

Add a header to each new JavaScript file:

```javascript
/**
 * University of La Laguna
 * School of Engineering and Technology
 * Degree in Computer Engineering
 * External Internships (PE)
 *
 * @author Your Name <your.email@example.com>
 * @since YYYY-MM-DD
 * @file filename.js
 * @desc Brief description of the file's purpose
 * @see {@link https://github.com/FabianGonzalezLenceDataX/Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code}
 */
```

Add JSDoc comments to all functions:

```javascript
/**
 * Description of what the function does.
 * 
 * @async
 * @function functionName
 * @param {string} param1 - Description of param1
 * @param {number} param2 - Description of param2
 * @returns {Promise<Object>} Description of return value
 * @throws {Error} When and why error is thrown
 * 
 * @example
 * const result = await functionName("test", 123);
 * // Returns: {key: "value"}
 */
async function functionName(param1, param2) {
  // Implementation
}
```

### Documentation Files

Update relevant documentation when making changes:

- **README.md** - Update if adding new features or changing setup
- **docs/API.md** - Update if modifying API endpoints
- **docs/ARCHITECTURE.md** - Update if changing system design
- **CHANGELOG.md** - Add entry for your changes

## Pull Request Process

### Before Submitting

1. ✅ All tests pass (`pytest`)
2. ✅ Code follows style guidelines
3. ✅ Documentation is updated
4. ✅ Commits have clear messages
5. ✅ Branch is up to date with main

### Creating a Pull Request

1. **Push your changes:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub:**
   - Go to your fork on GitHub
   - Click "Pull Request"
   - Select your feature branch
   - Fill out the PR template

3. **PR Description should include:**
   - What changes were made
   - Why the changes were made
   - How to test the changes
   - Screenshots (if UI changes)
   - Related issues (e.g., "Fixes #123")

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How to test these changes:
1. Step one
2. Step two

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] Self-review completed
```

### Review Process

- PRs require at least one approval
- Address all review comments
- Keep discussion professional and constructive
- Be patient - reviews may take a few days

## Reporting Issues

### Bug Reports

Use the issue tracker to report bugs. Include:

- **Title**: Clear, concise description
- **Description**: Detailed explanation of the bug
- **Steps to Reproduce**: Numbered steps to reproduce
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, browser, etc.
- **Screenshots**: If applicable

**Bug Report Template:**

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., Windows 11]
- Python: [e.g., 3.10]
- Browser: [e.g., Chrome 120]

## Screenshots
If applicable, add screenshots
```

### Feature Requests

Use the issue tracker for feature requests. Include:

- **Title**: Clear feature name
- **Problem**: What problem does this solve?
- **Solution**: Proposed solution
- **Alternatives**: Alternative solutions considered
- **Additional Context**: Any other relevant information

## Questions?

If you have questions:

1. Check the [README.md](README.md)
2. Review the [docs/](docs/) folder
3. Search existing issues
4. Create a new issue with the "question" label

## Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Project documentation

Thank you for contributing to the Mergington High School Activities Management System!

---

**Last Updated:** February 5, 2026  
**Maintained by:** Fabián González Lence
