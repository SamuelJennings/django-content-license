# Family Alignment Plan — django-content-license → django-mvp standard

> **Status: EXECUTED in PR #2 (chore/family-alignment).** Deltas 1–3 landed (shared CI,
> `fairdm-dev-tools`, modern pre-commit, matrix → Django 5.2/6.0). Delta 4 (README ↔ code
> reconciliation) remains open — tracked separately. Post-merge: add the test-matrix checks
> to the ruleset.

Recorded 2026-07-15 during forge-onboard, after studying the gold standard
(`django-mvp` + the already-onboarded `django-easy-icons`, the closest same-shape sibling).
Onboarding scaffolding (agent config, CONTEXT, ADRs, constitution) is done. This file is the
tooling/CI migration backlog — execute once Sam rules on the three open decisions.

## Open decisions (block execution)

1. **Support matrix** — narrow to family standard (Django 5.2 + 6.0, Py 3.11–3.13, drops EOL
   3.2/4.1/4.2 — breaking) · keep broad · or middle (4.2 LTS + 5.2 + 6.0). *Recommend: narrow.*
2. **CI approach** — adopt `django-mvp/shared` reusable workflows · or modernize bespoke.
   *Recommend: adopt shared.*
3. **Sequencing** — two PRs (onboard now, align next) · or one combined PR. *Recommend: two.*

## Delta 1 — CI workflows (adopt shared reusable workflows)

Replace the bespoke `tests.yml` (80-line matrix) and `build.yml` with thin callers:

```yaml
# .github/workflows/tests.yml
name: Tests
on:
  push: { branches: [main], paths: ['licensing/**','tests/**','pyproject.toml','poetry.lock','.github/workflows/tests.yml'] }
  pull_request: { types: [opened, synchronize, reopened] }   # NO paths filter — required checks must always report
  workflow_dispatch:
jobs:
  call-tests:
    uses: django-mvp/shared/.github/workflows/tests.yml@main
    with:
      coverage-package: licensing
      django-versions: '["5.2", "6.0"]'          # per decision 1
      poetry-install-args: ''                      # licensing keeps tooling in dev group, not a test group
    secrets: inherit
```
```yaml
# .github/workflows/build.yml
name: Build
on:
  push: { branches: [main], paths: ['licensing/**','pyproject.toml','poetry.lock','.pre-commit-config.yaml','.github/workflows/build.yml'] }
  pull_request: { types: [opened, synchronize, reopened] }
  workflow_dispatch:
jobs:
  call-build:
    uses: django-mvp/shared/.github/workflows/build.yml@main
    with: { source-dir: licensing }
    secrets: inherit
```
Emitted check names (for the ruleset): `Test Python <py>, Django <dj>` (per matrix combo),
`Code Quality`, `Security Scan`, `Build Package`. Also review family extras:
`auto-merge-dependabot.yml`, `changelog.yml`, `docs.yml`, `on-release-main.yml` — the repo
already has changelog/on-release/dependencies workflows; reconcile against the family versions.

## Delta 2 — Dev tooling bundle (pyproject)

Current dev group is nearly empty (pre-commit, coverage) → `pytest`/`mypy`/`deptry` not
installed. Adopt the family bundle:
```toml
[tool.poetry.group.dev.dependencies]
fairdm-dev-tools = { git = "https://github.com/FAIR-DM/dev-tools", extras = ["dev", "test"] }

[tool.poetry.group.docs.dependencies]   # if aligning docs (README claims ReadTheDocs)
fairdm-docs = { git = "https://github.com/FAIR-DM/fairdm-docs", extras = ["sphinx_book_theme"] }
```
This alone fixes the dead `mypy || true` / `deptry || true` CI steps (they were no-ops because
the tools weren't installed). Add `--cov=licensing` to pytest `addopts`. Bump `[tool.black]`
`target-version` and `[tool.ruff] target-version` off py37/py38 to py311+.

## Delta 3 — pre-commit modernization

Replace `.pre-commit-config.yaml` with the easy-icons version (swap `easy_icons` → `licensing`):
modern pinned revs (pre-commit-hooks v6.0.0, pyupgrade v3.21.2, ruff v0.14.7, black 25.11.0,
poetry 2.3.4), `poetry-lock` at manual stage, and **local `mypy` + `deptry` hooks**. CI `skip:`
list excludes the local Poetry hooks.

## Delta 4 — README ↔ code reconciliation (from CI audit + CONTEXT open questions)

Not tooling, but part of "in line": prune or build the README's phantom features (template
tags, package admin, `get_compatibility_with()`, pytest-only test files, ReadTheDocs). Decide
per CONTEXT.md open question 1. Track as its own issue/spec.

## Ruleset (onboarding completion gate — unchanged by the above)

Apply `kit/github/ruleset.json` on `main` with the emitted check names, org credential,
required approval, no force-push, empty bypass. django-easy-icons precedent: ruleset
`main-protection` (id 18769881); approval count effectively gated by the merge button under a
user-PAT identity until the GitHub App migration.
