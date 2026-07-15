# Django Content License — Domain Model

<!-- Ubiquitous language for this repo. Drafted by forge-onboard from the source (not the
     README, which currently over-describes the code — see "Open questions"). Terms marked
     [CONFIRM] need Sam's ruling before they are load-bearing. -->

## Glossary

### License

A stored record describing a single content license (e.g. MIT, CC-BY-4.0). Persisted as the
`License` model, not a static enum or external registry: the project deliberately keeps the
full license **text**, a human **description**, and a **canonical URL** in the database so a
deployment owns its own license catalogue. Identified to users by **name** (unique) and by
**slug** (auto-generated, unique). Has a lifecycle (see **License Lifecycle**).

### Canonical URL

The permanent online resource describing a license (unique per `License`). It is the href
used when rendering attribution, and the stable external identity of the license — distinct
from the internal **slug**.

### License Lifecycle

A `License` is either **active** (`is_active=True`, still recommended for use) or
**deprecated** (`is_active=False`, with a required **deprecated date**). The two states are
mutually exclusive and enforced in `License.clean()`: a deprecated license *must* carry a
deprecated date; an active license *must not*. Deprecation is the retirement mechanism —
licenses are not deleted (see **Protect-on-delete**).

### Recommended License

An active license. `License.get_recommended_licenses()` returns all `is_active=True`
licenses, name-ordered — the set a project should offer for *new* content.

### LicenseField

A custom `ForeignKey` (`licensing.fields.LicenseField`) that points any model at a
`License`. Defaults: `on_delete=PROTECT`, `verbose_name="license"`, a standard help text.
Adding it to a model is the entire integration surface. Beyond the FK, it injects a
**Display Method** onto the host model.

### Display Method

The `get_<fieldname>_display()` method that `LicenseField` auto-attaches to its host model
(via `contribute_to_class`). Calling it renders the **Attribution Snippet** for that
instance. Named to mirror Django's own `get_FOO_display()` convention. (Note: it *shadows*
that convention's usual meaning — here it returns rendered HTML, not a choice label.)

### Attribution

The human-facing statement of who made a piece of content and under what license, assembled
by `get_license_attribution()`. Its parts: **title** (str of the instance), **link** (the
instance's `get_absolute_url()` if any), **creators** (the instance's `creators` attribute,
or "Unknown"), and **creators_link** (the creators' `get_absolute_url()` if any). Attribution
reads these off the host model duck-typed — the host is not required to have them.

### Attribution Snippet

The rendered HTML fragment produced by the **Display Method**, via the
`licensing/snippet.html` template. Overridable by shadowing that template path. This is the
only thing most templates call.

### Creators

The author(s) of a licensed instance, read off the host model's `creators` attribute
(string or related object). Optional; absent creators render as "Unknown". **`creators`
(plural) is the canonical attribution contract** — it is what `get_license_attribution()` and
`licensing/snippet.html` read. The singular `creator` read by `get_license_creator()` is a
legacy orphan with no production caller and is slated for removal; do not build on it.

### Slug

The URL-safe unique identifier auto-generated from a license's **name** on save, with a
numeric suffix to guarantee uniqueness. Internal identity for routing; contrast **Canonical
URL** (external identity).

### Protect-on-delete

The policy (`on_delete=PROTECT` default on `LicenseField`) that a `License` referenced by any
content cannot be deleted — retirement happens through the **License Lifecycle**
(deprecation), never deletion.

## Synonyms to avoid

- **"license" as a field name** — collides with the Python builtin and reads badly; the
  bundled example model uses `content_license`. Prefer a qualified name in host models.
- **"license type" / "license kind"** — there is no license-type concept; a `License` is a
  flat record. Don't introduce categorisation vocabulary that the model doesn't have.
- **"delete a license"** — the domain retires licenses via **deprecation**; avoid "delete".

## Resolved decisions (settled 2026-07-15)

1. **README ↔ code drift** — RESOLVED (stale docs, pruned in PR #27). The phantom features
   (template tags, package admin, `get_compatibility_with()`, ghost test files, ReadTheDocs)
   were removed from the README rather than kept as roadmap.
2. **`creator` vs `creators`** — RESOLVED: `creators` (plural) is canonical; the singular
   `creator` / `get_license_creator()` is a legacy orphan to be removed (see **Creators**).
3. **Stored-catalogue vs external registry** — RESOLVED: the per-deployment stored catalogue
   is the intended design (ADR-0001, Accepted). `creativecommons.json.gz` is optional seed
   data, not a sync. Pulling from an external registry (SPDX / Creative Commons API) would be
   a future feature superseding ADR-0001, not the current direction.
