from invoke import task


@task
def test(c):
    """
    Run the test suite
    """
    print("🚀 Testing code: Running pytest")
    c.run("uv run pytest --cov --cov-config=pyproject.toml --cov-report=html")


@task
def docs(c):
    """
    Build the documentation and open it in the browser
    """
    c.run("sphinx-apidoc -M -T -o docs/ licensing **/migrations/* -e --force -d 2")
    c.run("sphinx-build -E -b html docs docs/_build")


@task
def prerelease(c):
    """
    Run comprehensive pre-release checks and update all required files.

    This task performs all necessary steps to prepare the repository for release:
    1. Run linting, formatting, type checking, and dependency checks via pre-commit hooks
    2. Run quality checks and tests

    Use this before running the release task to ensure everything is ready.

    Pre-commit hooks include:
    - Code formatting (Black, Ruff)
    - Type checking (mypy)
    - Dependency analysis (deptry)
    - Lockfile consistency
    """
    print("🚀 Starting comprehensive pre-release checks...")
    print("=" * 60)

    # Step 1: Run comprehensive linting, type checking, and dependency analysis
    print(
        "\n🧹 Step 1: Running comprehensive linting, type checking, and dependency analysis"
    )
    print("🚀 Running pre-commit hooks (includes mypy and deptry)")
    c.run("uv run pre-commit run -a")

    # Step 2: Check lock file consistency
    print("\n🔍 Step 2: Checking lock file consistency")
    print("🚀 Checking uv.lock is consistent with 'pyproject.toml'")
    c.run("uv lock --check")

    # Step 3: Run comprehensive test suite
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
def release(c, rule=""):
    """
    Create a new git tag and push it to the remote repository.

    .. note::
        This will create a new tag and push it to the remote repository, which will trigger a new build and deployment of the package to PyPI.

    Args:
        rule: Version bump rule (major, minor, patch, etc.)

    RULE	    BEFORE	AFTER
    major	    1.3.0	2.0.0
    minor	    2.1.4	2.2.0
    patch	    4.1.1	4.1.2
    alpha	    1.0.2	1.0.3a1
    alpha	    1.0.3a1	1.0.3a2
    beta	    1.0.3a2	1.0.3b1
    rc	        1.0.3b1	1.0.3rc1
    stable	    1.0.3rc1	1.0.3
    """
    # Check for unstaged changes
    unstaged_result = c.run("git diff --name-only", hide=True, warn=True)
    if unstaged_result.stdout.strip():
        print("⚠️  WARNING: You have unstaged changes:")
        print(unstaged_result.stdout)
        response = input("Continue with release? (y/N): ").strip().lower()
        if response not in ("y", "yes"):
            print("❌ Release cancelled.")
            return

    if rule:
        # bump the current version using the specified rule
        c.run(f"uv version --bump {rule}")

    # 1. Get the current version number as a variable
    version_short = c.run("uv version --short", hide=True).stdout.strip()
    version = c.run("uv version", hide=True).stdout.strip()

    # 2. Commit the version bump and any staged changes
    # Check if there are any staged changes
    staged_result = c.run("git diff --cached --name-only", hide=True, warn=True)
    if staged_result.stdout.strip():
        print(f"🚀 Committing staged changes and version bump for v{version_short}")
        c.run(
            f'git add pyproject.toml uv.lock && git commit -m "Release v{version_short}"'
        )
    else:
        print(f"🚀 Committing version bump for v{version_short}")
        c.run(f'git commit pyproject.toml uv.lock -m "Release v{version_short}"')

    # 3. Create a tag
    c.run(f'git tag -a v{version_short} -m "{version}"')

    # 4. Push commits and tags together
    print(f"📤 Pushing v{version_short} to remote repository...")
    c.run("git push origin main --follow-tags")


@task
def live_docs(c):
    """
    Build the documentation and open it in a live browser
    """
    c.run(
        "sphinx-autobuild -b html --host 0.0.0.0 --port 9000 --watch . -c . . _build/html"
    )
