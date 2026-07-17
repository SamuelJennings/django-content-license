# GOALS — django-content-license

## Purpose

`django-content-license` is a generic Django app for associating a **License** with any
model through a single `LicenseField`, and — where a license requires it — rendering an
optional HTML **attribution** snippet on the page. It is the GitHub-style primitive: a
picked-from catalogue of licenses, plus attribution, made reusable for any Django project.
It exists because publishing content correctly needs licensing, and there was no good
generic Django app for it — so instead of baking it into a larger framework, it lives
standalone.

## Problem & users

**Problem.** Django projects that publish content — datasets, publications, creative work —
need to state a license and, for some licenses, show correct attribution. There is no clean,
generic app for this, so each project either hand-rolls it or bakes it into a larger
framework.

**Users.** Any Django developer or site maintainer who wants a repository-style license
picker plus optional attribution, with a one-field integration and no bespoke licensing code.

## Success signals

- **The projects it was built for adopt it and delete their hand-rolled licensing code** —
  the package earns its existence by replacing the thing it would otherwise be baked into.
- **One-field integration works end-to-end** — a developer adds licensing + attribution to a
  model with a single `LicenseField` and one template call, against a fresh project, with no
  custom code.

External pickup (PyPI installs, stars, third-party issues) is a welcome lagging indicator,
not a target — it follows from doing the two above well.

## Non-goals

- **Citation / metadata export** (BibTeX, DataCite, CSL) — attribution here is an optional
  HTML snippet for display, not a research-citation engine.
- **License compatibility reasoning** ("can I combine CC-BY with GPL?") — a legal-reasoning
  engine, a different product.
- **Domain-specific requirements of any single consumer** — the app stays the generic
  primitive; a project with special needs integrates them on its own side, not here.
- **A fixed, CC-only attribution format** — attribution is per-license and configurable; CC
  is only what motivated the feature (see Standing tensions).

## Desired directions (not commitments)

Wanted, not scheduled — recorded so future feature work has a target:

- **Bundled admin** — an intuitive way for site maintainers to manage the catalogue and mark
  licenses current vs. deprecated. (Supersedes today's deliberate "ships no `ModelAdmin`"
  stance; a step forward, not a contradiction.)
- **Fresher catalogue** — eventually sync from an external registry (e.g. SPDX / Creative
  Commons) so the bundled seed set doesn't go stale when upstream text is reworded, without
  manual upkeep. Would supersede ADR-0001, which remains the *current* design.

## Appetite

**Steady side-work** — actively maintained and improved as real needs pull it forward; never
a flagship with its own roadmap sprints.

## Standing tensions

- **Generic vs. any single consumer's needs → generic wins.** Real-world requirements are
  kept in mind, but when they collide with staying generic, the app stays the reusable
  primitive and the consuming project integrates its own needs on top.
- **Simplicity vs. flexibility → simplicity wins.** The whole value is the one-field, one-call
  integration surface. A feature that buys flexibility by eroding that simplicity is the wrong
  trade for this app.
- **Attribution: fixed vs. configurable → configurable.** Any license may define the
  attribution style it requires; licenses that need nothing beyond their title simply don't
  use the attribution feature. CC style is a default, not a constraint.

---

_Produced via `/forge-goals` on 2026-07-16; revise by re-running it._
