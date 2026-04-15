# Contributing to BudgetCLI

Thank you for your interest in contributing to BudgetCLI! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- Familiarity with CLI applications and Python

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/BudgetCLI.git
cd BudgetCLI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Follow PEP 8 style guide
- Keep commits focused and descriptive
- Add tests for new functionality
- Update documentation as needed

### 3. Code Quality Checks

```bash
# Format with black
black budgetcli

# Lint with ruff
ruff check budgetcli --fix

# Type check with mypy
mypy budgetcli

# Run tests
pytest

# Run tests with coverage
pytest --cov=budgetcli
```

### 4. Commit Your Changes

```bash
git commit -m "feat: add new feature" -m "Detailed description of changes"
```

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `test:` for tests
- `refactor:` for refactoring

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Architecture Guidelines

### Clean Architecture Principles

1. **CLI Layer** (`budgetcli/cli/`):
   - Only orchestrate services
   - No business logic
   - Handle user input/output with Rich

2. **Business Logic** (`budgetcli/core/`):
   - All calculations and logic
   - Services for domain operations
   - Centralized validation

3. **Data Access** (`budgetcli/database/`):
   - SQLite connection management
   - Schema and models
   - Database operations only

4. **Utilities** (`budgetcli/utils/`):
   - Export functionality
   - Chart generation
   - Helper functions

### File Organization

- One service class per file
- Clear, descriptive module names
- Comprehensive docstrings
- Type hints on all functions

## Testing Requirements

- Minimum 80% code coverage
- Unit tests for all service methods
- Validation tests for all validators
- Test edge cases and error conditions

### Writing Tests

```python
# budgetcli/tests/test_feature.py
import pytest
from budgetcli.core.services import SomeService

@pytest.fixture
def temp_db():
    """Setup temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        init_db(str(Path(tmpdir) / "test.db"))
        yield str(Path(tmpdir) / "test.db")

def test_feature_success(temp_db):
    """Test successful operation."""
    service = SomeService(temp_db)
    result = service.do_something()
    assert result is not None

def test_feature_error():
    """Test error handling."""
    with pytest.raises(ValidationError):
        service.do_something_invalid()
```

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def add_transaction(
    transaction_type: str,
    category: str,
    amount: float,
    date: str,
    note: str = "",
) -> Transaction:
    """
    Add a new transaction.

    Args:
        transaction_type: Type of transaction (income/expense).
        category: Category name.
        amount: Transaction amount.
        date: Date in ISO format (YYYY-MM-DD).
        note: Optional transaction note.

    Returns:
        Created transaction object.

    Raises:
        ValidationError: If validation fails.
        RepositoryException: If database operation fails.
    """
```

### Update README

If adding features, update:
- Feature list
- Usage examples
- Architecture diagram (if applicable)

## Common Issues

### Database Errors

```bash
# Reset database during development
python -c "from budgetcli.database import reset_db; reset_db()"
```

### Import Errors

```bash
# Reinstall in development mode
pip install -e "."
```

### Test Failures

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
pytest --cache-clear
```

## Performance Considerations

- Minimize database queries
- Use indices for frequently filtered columns
- Cache calculations when appropriate
- Profile slow operations

## Security

- Validate all user input
- Use parameterized queries (done via SQLite adapters)
- Don't store sensitive data in plain text
- Keep dependencies updated

## Release Checklist

- [ ] All tests passing
- [ ] Code coverage ≥ 80%
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped (semantic versioning)
- [ ] Tag created: `git tag v1.0.0`

## Questions?

- Check existing issues and discussions
- Create a new discussion for questions
- Review existing code for patterns

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md
- GitHub contributors page
- Release notes

Thank you for contributing! 🎉
