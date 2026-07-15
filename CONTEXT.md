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
(string or related object). Optional; absent creators render as "Unknown". Note the plural —
`creators` (attribution) is distinct from the singular `creator` read by
`get_license_creator()`. [CONFIRM] whether both are intended or the singular is legacy.

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

## Open questions (for Sam — resolve before first feature spec)

1. **README ↔ code drift.** The README documents features absent from the source: template
   tags, a package-level admin (`licensing/admin.py` does not exist), `License.get_compatibility_with()`,
   several test files, and a ReadTheDocs site. Are these a **roadmap** (keep as goals) or
   **stale docs** (prune)? This decides whether the terms enter the glossary.
2. **`creator` vs `creators`** — one intended, or is one legacy? (see **Creators**).
3. Is the stored-catalogue model (full text in DB) the intended long-term design, or a
   placeholder for pulling from an external license registry (SPDX/Creative Commons)?
