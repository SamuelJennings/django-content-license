"""Invoke tasks for testing, building docs and releasing."""

from invoke import task


@task
def test(c):
    """Run the test suite with coverage.

    Args:
        c: The invoke context.
    """
    print("🚀 Testing code: Running pytest")
    c.run("uv run pytest --cov --cov-config=pyproject.toml --cov-report=html")


@task
def docs(c):
    """Build the documentation.

    Args:
        c: The invoke context.
    """
    c.run("sphinx-apidoc -M -T -o docs/ licensing **/migrations/* -e --force -d 2")
    c.run("sphinx-build -E -b html docs docs/_build")


@task
def prerelease(c):
    """Run the pre-commit hooks, the lockfile check and the test suite before a release.

    Args:
        c: The invoke context.
    """
    print("🚀 Starting comprehensive pre-release checks...")
    print("=" * 60)

    print(
        "\n🧹 Step 1: Running comprehensive linting, type checking, and dependency analysis"
    )
    print("🚀 Running pre-commit hooks (includes mypy and deptry)")
    c.run("uv run pre-commit run -a")

    print("\n🔍 Step 2: Checking lock file consistency")
    print("🚀 Checking uv.lock is consistent with 'pyproject.toml'")
    c.run("uv lock --check")

    print("\n🧪 Step 3: Running comprehensive test suite")
    print("🚀 Running pytest with coverage")
    c.run(
        "uv run pytest --cov --cov-config=pyproject.toml --cov-report=html --cov-report=term --tb=no -qq"
    )

    print("\n" + "=" * 60)
    print("✅ Pre-release checks completed successfully!")
    print(
        "🎉 Repository is ready for release. You can now run 'invoke release' with the appropriate rule."
    )
    print("   Example: invoke release --rule=patch")


@task
def release(c, rule="") -> None:
    """Bump the version, commit, tag and push, which publishes the package to PyPI.

    Args:
        c: The invoke context.
        rule: A `uv version --bump` rule: major, minor, patch, alpha, beta, rc or
            stable. Empty releases the current version unchanged.
    """
    unstaged_result = c.run("git diff --name-only", hide=True, warn=True)
    if unstaged_result.stdout.strip():
        print("⚠️  WARNING: You have unstaged changes:")
        print(unstaged_result.stdout)
        response = input("Continue with release? (y/N): ").strip().lower()
        if response not in ("y", "yes"):
            print("❌ Release cancelled.")
            return

    if rule:
        c.run(f"uv version --bump {rule}")

    version_short = c.run("uv version --short", hide=True).stdout.strip()
    version = c.run("uv version", hide=True).stdout.strip()

    staged_result = c.run("git diff --cached --name-only", hide=True, warn=True)
    if staged_result.stdout.strip():
        print(f"🚀 Committing staged changes and version bump for v{version_short}")
        c.run(
            f'git add pyproject.toml uv.lock && git commit -m "Release v{version_short}"'
        )
    else:
        print(f"🚀 Committing version bump for v{version_short}")
        c.run(f'git commit pyproject.toml uv.lock -m "Release v{version_short}"')

    c.run(f'git tag -a v{version_short} -m "{version}"')

    print(f"📤 Pushing v{version_short} to remote repository...")
    c.run("git push origin main --follow-tags")


@task
def live_docs(c):
    """Serve the documentation with live reload on port 9000.

    Args:
        c: The invoke context.
    """
    c.run(
        "sphinx-autobuild -b html --host 0.0.0.0 --port 9000 --watch . -c . . _build/html"
    )
