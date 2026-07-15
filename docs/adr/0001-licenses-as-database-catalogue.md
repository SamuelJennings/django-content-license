# ADR-0001 — Licenses are a per-deployment database catalogue

- **Status:** Accepted (confirmed by Sam 2026-07-15)
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

## Resolution

Confirmed as the intended long-term design (option c), not a stepping stone toward an external
registry (Sam, 2026-07-15). The bundled `creativecommons.json.gz` is optional seed data loaded
at the deployment's choice — there is no sync. Integrating an external registry (SPDX / the
Creative Commons API) would be a future feature that supersedes this ADR, not a revision of it.
