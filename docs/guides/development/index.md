# Development Guide

[VERIFIED via source - 2026-01-03]

Guide for developers contributing to the dotfiles-config project.

## Contents

- [Setup](setup.md) - Setting up development environment
- [Testing](testing.md) - Writing and running tests
- [Adding Commands](adding-commands.md) - How to add new CLI commands
- [Code Style](code-style.md) - Code style and conventions

## Quick Development Setup

```bash
# Clone repository
git clone <repository-url>
cd dotfiles/config

# Install with development dependencies
make install-dev

# Activate virtual environment
make shell

# Run tests
make test-cov
```

[VERIFIED via source - 2026-01-03]

## Development Workflow

### 1. Make Changes

Edit source files in `src/` directory.

### 2. Run Tests

```bash
make test-cov
```

[VERIFIED via tests - 2026-01-03]

Ensure all tests pass and coverage remains high.

### 3. Test Manually

```bash
config <your-command>
```

Test your changes with actual CLI usage.

### 4. Update Documentation

Update relevant documentation in `docs/` if needed.

## Project Standards

### Code Quality

- **Type hints:** All functions must have type annotations
- **Docstrings:** All public functions must have docstrings
- **Tests:** New features must include tests
- **Coverage:** Aim for high test coverage (>80%)

[VERIFIED via tests - 2026-01-03]

### Testing

- **Unit tests:** Test individual components in isolation
- **Integration tests:** Test CLI commands end-to-end
- **Fixtures:** Use shared fixtures from `conftest.py`
- **Assertions:** Clear, specific assertions

[VERIFIED via tests - 2026-01-03]

### Documentation

- **Docstrings:** Google style docstrings
- **Comments:** Explain why, not what
- **Markdown:** Use proper formatting
- **Examples:** Include working examples

## Tools and Technologies

**Core:**
- Python 3.12+
- Typer - CLI framework
- uv - Package manager

**Testing:**
- pytest - Test framework
- pytest-cov - Coverage reporting

**Build:**
- Hatchling - Build backend
- Make - Task automation

[VERIFIED via source - 2026-01-03]

## See Also

- [Setup Guide](setup.md) - Detailed setup instructions
- [Testing Guide](testing.md) - Testing best practices
- [Adding Commands](adding-commands.md) - How to add new commands
- [Architecture](../../architecture/index.md) - System design
