# GOALS — django-content-license

## Purpose

`django-content-license` lets any Django model carry a content license, and where a license
needs it, renders a small HTML attribution snippet for the page. Think of the license picker
GitHub puts on a new repository, plus the attribution part that some licenses (like Creative
Commons) ask you to show. It exists because a lot of projects need this and there was no good
generic app for it, so instead of building it into a larger framework it lives on its own.

## Problem & users

Projects that publish content need to say what license it's under, and some licenses want a
visible attribution line to go with it. Today you either write that yourself or inherit it
from whatever framework you're on. This app is the small piece that just does it.

It's for any Django developer or site maintainer who wants a license picker and optional
attribution by adding one field to a model, without writing licensing code of their own.

## Success signals

The projects it was built for switch to it and delete the licensing code they were carrying.
That's the honest test of whether it was worth pulling out.

Adding it to a model takes one `LicenseField` and one template call, on a fresh project, with
nothing hand-written. If that stops being true, the app has drifted from the point.

PyPI installs, stars, and issues from people I don't know are nice to see, but I'm not
building for them and won't chase them.

## Non-goals

It doesn't export citations or metadata (BibTeX, DataCite, CSL). Attribution here is a bit of
HTML to display, not a research-citation system.

It doesn't reason about license compatibility (whether you can combine CC-BY with GPL, say).
That's a legal engine and a different project.

It doesn't grow to fit one particular consumer. If a project has a special need, it wires that
in on its own side and this app stays generic.

And attribution isn't locked to the Creative Commons style. CC is what prompted the feature,
but each license defines whatever attribution it requires.

## Desired directions

Things I want, not things that are scheduled. They're written down so future work has a target
to aim at.

A bundled admin, so a site maintainer can manage the catalogue and mark which licenses are
current and which are deprecated. Today the app ships no `ModelAdmin` on purpose; this would
move that forward.

A way to keep the catalogue fresh by syncing from an external registry like SPDX or Creative
Commons, so the bundled seed set doesn't go stale when upstream text changes and I don't have
to hand-update it. That would replace the current design recorded in ADR-0001.

## Appetite

Steady side-work. I'll maintain it and improve it as real needs come up, but it isn't a
flagship and won't get its own roadmap sprints.

## Standing tensions

When staying generic pulls against one consumer's specific need, generic wins. I keep those
needs in mind, but the consuming project integrates them on its side, not in here.

When more flexibility would cost the one-field, one-call simplicity, simplicity wins. That
simple integration is most of the value.

Attribution stays configurable rather than fixed. A license defines the attribution it needs,
and a license that only wants its title shown just doesn't use the feature. The CC style is a
default, not a rule.

---

_Produced via `/forge-goals` on 2026-07-16; revise by re-running it._
