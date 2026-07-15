# ADR-0001 — Licenses are a per-deployment database catalogue

- **Status:** Accepted (retroactive — recorded at onboarding 2026-07-15; confirm)
- **Context date:** observed in `licensing/models.py`, `licensing/fixtures/creativecommons.json.gz`

## Context

Licenses could be modelled three ways: (a) a hardcoded enum/choices list, (b) references
into an external registry (SPDX, the Creative Commons API) resolved at runtime, or (c) stored
database records each deployment owns.

## Decision

Licenses are stored `License` model rows. Each row carries the full license **text**, a
**description**, a **canonical URL**, and lifecycle state — the deployment owns its catalogue.
A bundled fixture (`creativecommons.json.gz`) seeds the common Creative Commons set, but
deployments are free to add, edit, and deprecate their own.

## Consequences

- Licenses are queryable, admin-editable, and translatable like any model — no network
  dependency at render time.
- The catalogue can drift from upstream (e.g. SPDX) — there is no sync mechanism. If upstream
  fidelity becomes a requirement, that is a new feature, not a change here.
- Seed data ships as a Django fixture; loading it is the deployment's choice.

## Open question

Is (c) the intended long-term design, or a stepping stone toward (b)? See CONTEXT.md open
question 3.
