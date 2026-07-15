# CI Audit — django-content-license (forge-onboard, 2026-07-15)

CI is repo-native. This records the audit against the org quality floor. Base branch `main`
is **green today** (verified via check-runs API + local `manage.py test`: 95 tests pass).

## Required (must be green to complete onboarding)

| Item | Status | Evidence |
| --- | --- | --- |
| Tests run on every PR | ✅ | `tests.yml` on `pull_request` (matrix, SQLite+Postgres) |
| Lint runs on every PR | ✅ | `build.yml` → `Code Quality` job runs `pre-commit` (ruff + black) |
| Build succeeds on every PR | ✅ | `build.yml` → `Build Package` job (`poetry build`) |
| Check names recorded | ✅ | AGENTS.md → `## Agent skills > CI checks` |
| Ruleset applied on default branch | ❌ **GAP** | No branch protection/ruleset exists yet — see proposal 1 |

## Expected (gaps recorded as proposals)

| Item | Status | Note |
| --- | --- | --- |
| Type-check on PR | ⚠️ | `mypy licensing/` runs `|| true` **and mypy is not a dev dependency** → dead step. Proposal 2 |
| Coverage measured | ✅ | Codecov (`codecov/project`, `codecov/patch` green) |
| CI green on default branch today | ✅ | check-runs API + local run |
| No secret exposure in PR jobs | ✅ | Workflows use `pull_request` (not `pull_request_target`); PyPI publish is `on-release-main` only |

## Proposals (fix in the repo's own idiom, each its own PR)

1. **Apply the org ruleset** on `main`: required checks, required approval, no force-push,
   empty bypass list. Blocks onboarding completion. Needs a required-checks strategy
   (proposal 1a) and the org credential.
   - **1a. Required-checks strategy.** The test matrix produces 10 differently-named checks
     (`Test Python X, Django Y`) — brittle to require by name. Recommend adding a small
     `checks-complete` aggregate job that `needs:` all matrix jobs, then require
     `checks-complete` + `Code Quality` + `Security Scan` + `Build Package`. (Pilot repo
     django-easy-icons uses this `checks-complete` pattern.)
2. **Dead type-check/dep steps.** `mypy` and `deptry` are invoked with `|| true` but neither
   is installed → they never actually run. Either add them to the dev group and make them
   blocking (ratchet per constitution quality bar) or remove the steps. Recommend: add + fix
   + make blocking as a follow-up feature.
3. **Test-runner drift.** `pyproject.toml` configures `[tool.pytest.ini_options]` and the
   README references pytest-only test files (`test_pytest_*.py`, `test_integration.py`) that
   do not exist; the actual suite runs under `manage.py test`. Align: either adopt pytest as
   a real dev dep or drop the pytest config + README claims.
4. **`Update Dependencies` workflow failing on main** (`dependencies.yml`) — not a PR gate,
   but red. Worth a triage pass.

## Registry facts

- `verify_adapter`: `poetry` (validated — `poetry install` + `poetry run python manage.py test` → 95 pass)
- Required check names (stable): `Code Quality`, `Security Scan`, `Build Package` (+ test matrix / future `checks-complete`)
