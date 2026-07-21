# AGENTS.md — Agent Configuration for django-content-license

<!-- Thin index only — bloat here = ignored instructions. Details live in the pointed-to
     files. Scaffolded by forge-onboard; keep sections, replace placeholders. -->

`django-content-license` is a reusable Django app that stores **License** records and
attaches them to any model through a custom **LicenseField**, then renders attribution
HTML for display. It targets research/academic and creative-content projects where correct
licensing and attribution matter. See `CONTEXT.md` for the ubiquitous language.

## Stack & commands

- **Stack:** Python ≥3.11 / Django 5.2 LTS + 6.0 (family standard — supported releases only),
  Poetry-managed. Dev toolchain via the `mvp-shared` bundle. Ships to PyPI.
- **Install:** `poetry install`
- **Test:** `poetry run pytest` (pytest-django; settings module `tests.settings`)
- **Lint/format:** `poetry run pre-commit run --all-files` (ruff lint + ruff-format; local mypy + deptry hooks)
- **Type-check:** `poetry run mypy licensing/`
- **Build:** `poetry build`
- **All checks (as CI runs):** `poetry run invoke check`

## Agent skills

### Issue tracker

Issues tracked in GitHub Issues via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix).
See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — `CONTEXT.md` glossary at root, `docs/adr/` for standing decisions.
See `docs/agents/domain.md`.

### CI checks

CI delegates to the `django-mvp/shared` reusable workflows (`tests.yml`, `build.yml`).
Required status checks (exact names): `Code Quality`, `Security Scan`, `Build Package`, plus
the test matrix `Test Python <py>, Django <dj>` (Python 3.12–3.13 × Django 5.2/6.0). See the
org's CI audit record in the registry.

## Engineering org

This repo is operated by the autonomous engineering org (Forge). Feature work runs
spec→plan→tasks→implement→review→PR through org-side skills — there is no Spec Kit install
here; `specs/NNN-slug/` directories are generated per feature. Constitution:
`memory/constitution.md`. Budget overrides: none.
