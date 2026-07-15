# django-content-license Constitution

<!-- Authored at org onboarding (2026-07-15), mirroring the django-mvp family standard
     (see django-easy-icons/memory/constitution.md). Changes go through the constitution
     pathway (human-gated), never mid-feature. Read at the Constitution Check in /plan and
     by reviewers. DRAFT: Article VI's concrete matrix pending Sam's support-matrix ruling. -->

## Core articles (org defaults)

### Article I — Test-First
No implementation before a failing test exists for the behavior. Tests written by an
Implementer for its own tasks; pre-existing tests are never modified or deleted without an
approved decisions.md entry (tamper-check enforced).

### Article II — Simplicity
Start with the simplest design that satisfies the spec. New dependencies, new abstractions,
and new infrastructure each require a stated justification in plan.md Complexity Tracking.
YAGNI over speculation. This package is deliberately small (one model, one field, a handful
of utils) — keep it that way.

### Article III — Anti-Abstraction
No wrapper layers, base classes, or "future-proofing" indirection without a present, concrete
second use. Prefer duplication over the wrong abstraction.

### Article IV — Integration-First
Contracts and integration points are designed and tested before internals are polished.
Acceptance scenarios exercise the package the way users touch it: `INSTALLED_APPS` config,
declaring a `LicenseField` on a host model, and rendering attribution via
`obj.get_<field>_display()`.

## Project articles

### Article V — Public API stability
The public API is the `License` model, `LicenseField`, the injected `get_<field>_display()`
contract, the `licensing/snippet.html` template, and the documented helpers in
`licensing.utils`. Breaking changes to any of these require a deprecation path (warn one
minor release before removal) and a CHANGELOG entry. Semver applies (currently 0.x: minor =
may break with notice).

### Article VI — Compatibility matrix
Supported Python/Django versions are whatever the CI matrix declares — the matrix is
authoritative. Policy: track only actively-supported Django releases (family rule). Current
matrix: **Django 5.2 LTS + 6.0**, Python **3.11–3.13** (package floor `>=3.11`; CI test
matrix Python 3.12–3.13 per the shared workflow default). New code must pass the full matrix;
dropping a version is a constitution-level change recorded in CHANGELOG.

### Article VII — Attribution & data-safety contract
Rendered attribution MUST escape all interpolated values (host title, creators, license
name/URL) — attribution HTML is only ever returned through Django's template layer +
`mark_safe`, never hand-built string interpolation of model data. Licenses are retired by
deprecation, never deletion (ADR-0003); migrations follow deprecate-then-remove and keep the
bundled `creativecommons.json.gz` fixture loadable.

## Quality bar

- Coverage may not decrease (codecov tracks; the coverage matrix cell is the reference).
- Every public API change updates README + CHANGELOG in the same PR.
- `mypy licensing/` and `deptry` must be installed and pass (family standard runs both as
  local pre-commit hooks + CI). Ratchet target: blocking, once the current dead `|| true`
  steps are wired up (CI audit proposal 2).

## Non-negotiables

- One PR per feature; Sam merges; the org never merges.
- Machine verification (tests/build/lint) gates every stage exit; no LLM judgment can
  override a red gate.
