# ADR-0003 — Licenses are retired by deprecation, never deleted

- **Status:** Accepted (retroactive — recorded at onboarding 2026-07-15; confirm)
- **Context date:** observed in `licensing/models.py` (`clean()`, `is_active`, `deprecated_date`), `licensing/fields.py` (`on_delete=PROTECT`)

## Context

A license referenced by published content must not silently disappear — attribution already
rendered and stored URLs must keep resolving. But licenses do fall out of recommendation
(superseded versions, withdrawn licenses).

## Decision

Two mechanisms, enforced together:

1. **Protect-on-delete.** `LicenseField` defaults to `on_delete=PROTECT`, so a referenced
   `License` cannot be deleted.
2. **Lifecycle deprecation.** A `License` is **active** (`is_active=True`, no deprecated date)
   or **deprecated** (`is_active=False`, deprecated date required). `License.clean()` enforces
   the mutual exclusion. `get_recommended_licenses()` returns only active licenses.

## Consequences

- Historical references stay valid indefinitely; retirement is a state change, not a delete.
- Callers building "choose a license" UIs should filter to `get_recommended_licenses()` /
  `is_active=True` (the bundled `LicenseField` example uses `limit_choices_to`).
- `clean()` is the enforcement point — code paths that bypass validation (bulk updates,
  direct `save()`) can still create an inconsistent state; treat `clean()` as the contract.

## Non-negotiable

Avoid the word "delete" for licenses in domain language — the operation is **deprecate**
(see CONTEXT.md synonyms-to-avoid).
