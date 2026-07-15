# ADR-0002 — Attribution rendered via an injected display method + overridable template

- **Status:** Accepted (retroactive — recorded at onboarding 2026-07-15; confirm)
- **Context date:** observed in `licensing/fields.py`, `licensing/utils.py`, `licensing/templates/licensing/snippet.html`

## Context

Host models need to render a licensing/attribution statement. Options: a standalone template
tag/filter (`{% license_attribution obj %}`), a mixin the host inherits, or behaviour attached
by the field itself.

## Decision

`LicenseField.contribute_to_class` injects a `get_<fieldname>_display()` method onto the host
model. Calling it renders `licensing/snippet.html` with the instance and its license. The
template branches on which attribution parts are present (`get_absolute_url`, `creators`,
`creators.get_absolute_url`) and is overridable by shadowing the template path. Host models
opt in purely by declaring the field — no mixin, no template-tag import.

## Consequences

- Zero-ceremony integration: add the field, call `obj.get_<field>_display()` in a template.
- The method name mirrors Django's `get_FOO_display()` but returns rendered **HTML**, not a
  choice label — a deliberate convention echo that can surprise. Documented in CONTEXT.md.
- Attribution reads `creators` / `get_absolute_url` duck-typed off the host; hosts are not
  required to provide them, and missing parts degrade gracefully ("Unknown", no link).
- The README references "template tags" that do not exist — this ADR is the actual mechanism.

## Alternatives rejected

- **Template tag library:** requires a `{% load %}` and passing the object explicitly; more
  ceremony, and no natural place for per-field defaults.
- **Model mixin:** forces inheritance and conflicts with hosts that already have a base class.
