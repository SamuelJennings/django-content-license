# AGENTS.md — Agent Configuration for django-content-license

<!-- Thin index only — bloat here = ignored instructions. Details live in the pointed-to
     files. Scaffolded by forge-onboard; keep sections, replace placeholders. -->

`django-content-license` is a reusable Django app that stores **License** records and
attaches them to any model through a custom **LicenseField**, then renders attribution
HTML for display. It targets research/academic and creative-content projects where correct
licensing and attribution matter. See `CONTEXT.md` for the ubiquitous language.

## Stack & commands

- **Stack:** Python ≥3.10 / Django ≥3.2 (tested to 5.0), Poetry-managed. Ships to PyPI.
- **Install:** `poetry install`
- **Test:** `poetry run pytest` (or `python manage.py test`; settings module `tests.settings`)
- **Lint:** `poetry run pre-commit run --all-files` (ruff + black + pyupgrade)
- **Type-check:** `poetry run mypy licensing/`  *(currently non-blocking in CI)*
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

Required status checks the pipeline reads (exact names):
`Code Quality`, `Security Scan`, `Build Package`, and the test matrix
`Test Python 3.12, Django 4.2` (representative required combo; full matrix is 10 combos of
Python 3.10–3.12 × Django 3.2/4.1/4.2/5.0). CI is repo-native; see the org's CI audit record
in the registry.

## Engineering org

This repo is operated by the autonomous engineering org (Forge). Feature work runs
spec→plan→tasks→implement→review→PR through org-side skills — there is no Spec Kit install
here; `specs/NNN-slug/` directories are generated per feature. Constitution:
`memory/constitution.md`. Budget overrides: none.
