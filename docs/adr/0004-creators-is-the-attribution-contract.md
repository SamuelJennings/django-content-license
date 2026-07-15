# ADR-0004 — `creators` (plural) is the attribution contract; the singular `creator` helper is retired

- **Status:** Accepted (Sam, 2026-07-15)
- **Context date:** observed in `licensing/utils.py`, `licensing/templates/licensing/snippet.html`

## Context

Two creator accessors coexist in the code with no clear relationship:

- **`creators`** (plural) — read by `get_license_attribution()` and by `snippet.html` to render
  the "by <creators>" clause. This is the live attribution path.
- **`creator`** (singular) — read only by `get_license_creator()`, which returns
  `getattr(instance, "creator", None)`. Nothing in `licensing/`, the templates, or the bundled
  `example/` app calls `get_license_creator()`; it is exercised only by its own unit test.

Carrying two overlapping names for "who made this" invites host models to wire the wrong one
and get silently empty attribution.

## Decision

`creators` (plural) is the single canonical attribution contract. Host models expose a
`creators` attribute (a string, or a related object with `get_absolute_url()`); attribution and
the snippet read only that. `get_license_creator()` and the singular `creator` attribute are
**legacy orphans** and will be removed (deprecate, then delete with its test in a follow-up
change). No new code should read singular `creator`.

## Consequences

- One name to document and support; the glossary (CONTEXT.md → **Creators**) pins `creators`.
- Removing `get_license_creator()` is a public-symbol removal — it ships under the deprecation
  policy (Constitution Article V): warn one minor release before deletion, CHANGELOG entry.
- Until removed, the orphan is harmless but must not be built upon.
