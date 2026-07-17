# GOALS — django-content-license

Standing directions this project steers toward, grouped by how essential they are. Directions
are headings, not tasks: you steer toward them, you don't finish them. Each has a stable id
(identity, never a rank) and, when it needs one, a status. The roadmap turns these into
shippable work that cites the id, and feature specs cite a roadmap item that cites the id, so
everything built traces back to a direction here. Progress lives in the roadmap; this file is
the standing definition of what the package is and wants to become. Scope, non-goals, and
design principles live in the README.

### Tiers (maturity, mapped to versions)
- **MVP** — the floor of a usable product. When the MVP directions are met, the package cuts **v1.0**.
- **Mature** — enhancements that make it complete and dependable, delivered across the **v1.x** line.
- **Nice-to-have** — real wants and stray ideas; never makes the package incomplete. An accepted one becomes a **v2.0+** theme.

A direction keeps its id if it changes tier.

### Statuses
Unmarked means accepted and live. Otherwise:
- **draft** — captured, not yet refined or accepted.
- **rejected** — decided against; kept with a reason, and a linked ADR when the call is a design stance.

## MVP → v1.0
- **D1 — Easy distribution.** Installable from a package index, with versioned releases.
- **D2 — One-field integration.** Licensing and attribution from a single model field and one
  template call, no bespoke code.

## Mature → v1.x
- **D3 — Flexible attribution.** Each license expresses the attribution it requires, rather
  than one fixed style.
- **D4 — Human-manageable catalogue.** A site maintainer can add, edit, and deprecate licenses
  without touching code.
- **D5 — Real internal adoption.** The projects this was extracted from rely on it instead of
  their own licensing code.

## Nice-to-have → v2.0+
- **D6 — A catalogue that doesn't rot.** `draft`. License text refreshable from an upstream
  registry (SPDX / Creative Commons) without hand-maintenance. _(2026-07-16 — the bundled set
  goes stale when upstream rewords; would supersede ADR-0001.)_

_Written 2026-07-16. Revise as the direction changes._
