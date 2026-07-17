# GOALS — django-content-license

Enduring goals this project pursues. Identity lives in the README; when work happens and which
release delivers it lives in the roadmap — this file names no versions. A goal is a capability
or quality you steer toward, not a task you complete: its id is stable, its importance is a tag
that can change, and whether it has been addressed enough is judged through the roadmap, specs,
and review rather than the goal itself.

**Importance** — `Essential`: not worth adopting without it · `Expected`: a complete,
dependable version is expected to have it · `Aspirational`: a genuine want whose absence never
makes the package incomplete.

**Status** — unmarked means accepted and live · `draft`: captured, not yet refined ·
`rejected`: decided against, kept with a reason and an ADR link when it's a design stance.

| ID | Goal | Importance | Status | Notes |
|----|------|------------|--------|-------|
| G1 | **Easy distribution** — installable from a package index, with versioned releases. | Essential | | |
| G2 | **One-field integration** — licensing and attribution from a single model field and one template call, no bespoke code. | Essential | | |
| G3 | **Flexible attribution** — each license expresses the attribution it requires, rather than one fixed style. | Expected | | |
| G4 | **Human-manageable catalogue** — a site maintainer can add, edit, and deprecate licenses without touching code. | Expected | | |
| G5 | **Real internal adoption** — the projects this was extracted from rely on it instead of their own licensing code. | Expected | | |
| G6 | **A catalogue that stays current** — license text can track authoritative upstream sources without manual upkeep. | Aspirational | draft | 2026-07-16 — bundled set goes stale when upstream rewords; would supersede ADR-0001. |

_Written 2026-07-16. Revise as the goals change._
