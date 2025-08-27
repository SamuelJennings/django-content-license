# Development Workflow

This document explains how to set up your development environment and run the project's quality checks.

## Setup

1. **Install dependencies:**
   ```bash
   poetry install
   poetry run pre-commit install
   ```

2. **Activate the shell:**
   ```bash
   poetry shell
   ```

## Development Commands

### Code Quality & Formatting

```bash
# Format code and update dependency files
poetry run invoke fmt

# Run all quality checks (what CI runs)
poetry run invoke check

# Run individual tools
poetry run pre-commit run --all-files    # Code style and linting
poetry run mypy licensing/               # Type checking
poetry run deptry .                      # Dependency analysis
```

### Testing

```bash
# Run tests
python manage.py test

# Run tests with coverage
poetry run invoke test

# Run tests with tox (multiple environments)
poetry run invoke test --tox
```

### Manual Pre-commit Hook Updates

The CI skips certain hooks that modify files. Run these manually when needed:

```bash
# Update poetry.lock and requirements.txt
poetry run pre-commit run --hook-stage manual --all-files

# Or use the convenience command
poetry run invoke fmt
```

## Pre-commit Hooks

We use pre-commit hooks to maintain code quality:

- **Automatic on commit**: Basic formatting and linting
- **Manual (run with `invoke fmt`)**: Poetry lock file and requirements.txt updates
- **CI checks**: All hooks except file-modifying ones

## Troubleshooting

### "poetry-lock failed" in CI

This happens when your `poetry.lock` file is out of sync. Run locally:
```bash
poetry run invoke fmt
git add poetry.lock requirements.txt
git commit -m "Update dependency files"
```

### Pre-commit hook failures

If you see pre-commit failures in CI, run locally:
```bash
poetry run pre-commit run --all-files
git add .
git commit -m "Apply pre-commit fixes"
```

## Release Process

```bash
# Bump version and create release
poetry run invoke release patch   # for bug fixes
poetry run invoke release minor   # for new features
poetry run invoke release major   # for breaking changes
```

This will:
1. Update the version in `pyproject.toml`
2. Create a git tag
3. Push to GitHub
4. Trigger automatic PyPI publishing
