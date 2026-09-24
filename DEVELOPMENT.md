# Development Workflow

This document explains how to set up your development environment and run the project's quality checks.

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   uv run pre-commit install
   ```

   `uv run <command>` runs a command in the project environment, so there is no shell to activate.

## Development Commands

### Code Quality & Formatting

```bash
# Format code and check the lockfile
uv run invoke fmt

# Run all quality checks (what CI runs)
uv run invoke check

# Run individual tools
uv run pre-commit run --all-files    # Code style and linting
uv run mypy licensing/               # Type checking
uv run deptry .                      # Dependency analysis
```

### Testing

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run invoke test

# Run tests with tox (multiple environments)
uv run invoke test --tox
```

### Manual Pre-commit Hook Updates

The CI skips certain hooks that modify files. Run these manually when needed:

```bash
# Refresh uv.lock after editing pyproject.toml
uv lock
```

## Pre-commit Hooks

We use pre-commit hooks to maintain code quality:

- **Automatic on commit**: Basic formatting and linting (ruff, black, pyupgrade), plus local mypy + deptry
- **Lockfile**: `uv-lock` keeps `uv.lock` in step with `pyproject.toml`
- **CI checks**: All hooks except file-modifying and local-env ones

## Troubleshooting

### "uv-lock failed" or "uv sync --locked" failed in CI

This happens when your `uv.lock` file is out of sync. Run locally:
```bash
uv lock
git add uv.lock
git commit -m "Update dependency files"
```

### Pre-commit hook failures

If you see pre-commit failures in CI, run locally:
```bash
uv run pre-commit run --all-files
git add .
git commit -m "Apply pre-commit fixes"
```

## Release Process

```bash
# Bump version and create release
uv run invoke release patch   # for bug fixes
uv run invoke release minor   # for new features
uv run invoke release major   # for breaking changes
```

This will:
1. Update the version in `pyproject.toml` and `uv.lock`
2. Create a git tag
3. Push to GitHub
4. Trigger automatic PyPI publishing
