# Typora Themes

A multi-theme repository and AI-assisted workflow for designing, testing, installing, maintaining, and eventually releasing independent [Typora](https://typora.io/) themes.

**Current state (2026-10-24): PersianNew v13 install CSS was merged into `main` in [PR #3](https://github.com/rezahh107/Typora-Persiannew-Theme/pull/3), after 38 structural checks, bounded real Typora testing on Ubuntu, and a positive comparison by the Owner in their installed Typora. The Owner reported no material difference in their tested use other than a slightly heavier font, which they prefer. This is limited acceptance of the working CSS, **not** universal font/runtime/PDF equivalence or a public release.** The [install CSS](themes/persiannew/persiannew.css) is derived from the last complete CSS section within the [immutable 3,024-line legacy intake](themes/persiannew/INTAKE.md); the historical file also contains duplicated code and conversation text. The candidate's [known differences and font restrictions](themes/persiannew/QUALIFICATION.md) matter. Authentic v14 remains unavailable.

## Start here

- **Use or develop a theme:** [themes/README.md](themes/README.md); the [PersianNew theme](themes/persiannew/README.md) explains installation, bounded runtime evidence and remaining limitations.
- **Create/edit with an AI or manually:** [workflows/CREATE_THEME.md](workflows/CREATE_THEME.md) and [AGENTS.md](AGENTS.md).
- **Author CSS from official Typora evidence:** [knowledge/typora/INDEX.md](knowledge/typora/INDEX.md) and [verified authoring rules](knowledge/typora/AUTHORING_RULES.md).
- **Run shared structural verification:** `python3 scripts/verify.py` (Python 3.10+, standard library only).
- **Validate real presentation:** [manual Typora checklist](tests/MANUAL_TYPORA.md) using [shared fixtures](tests/fixtures/). Automated checks do **not** prove Typora behavior.

## Repository layout

- `themes/<theme-id>/` — independent theme records, optional CSS and owned assets. `theme.json` declares whether the actual source exists.
- `knowledge/typora/` — cited official documentation coverage and actionable rules, including gaps.
- `workflows/` — repeatable creation and future release destination.
- `tests/` — automatic verification tests, Markdown fixtures, and manual runtime expectations.
- `scripts/verify.py` — one shared dependency-free entrypoint for humans, AI and CI.

## Install (only for a source-ready theme)

For a theme marked `ready`, open Typora **Preferences → Appearance → Open Theme Folder**, copy its declared CSS to the **top level** of that folder and its licensed relative assets in their referenced paths, restart Typora, and select the theme from the **Themes** menu. Refer to the theme's README for exact supported versions/platforms. PersianNew is merged and source-ready with bounded real Typora and Owner-desktop evidence, but has no packaged Release or guarantee of universal font/runtime equivalence. See its own README before installing.

## Authority and release

The [Owner-approved Goal Authority](https://docs.google.com/document/d/1_tY5lHTuDW4Kt8ujrU--vAcNXYj4T1rKRMLvEhKQLIw/edit) defines the **complete destination**, not just this foundation batch: independent multi-theme product, reusable official knowledge and AI workflow, meaningful real Typora testing, and owner-controlled per-theme automated releases. See [future release contract](workflows/RELEASE_DESTINATION.md). The [PPDM Repository Foundation](https://github.com/rezahh107/Personal-Preference-Decision-Model/blob/main/knowledge/current/domains/repository-foundation/INDEX.md) provides the adaptation method, not a template to copy.

Changes go through reviewable PRs. **No rename, merge, tagging, public release, or redistribution of unlicensed fonts is authorized by a passing check or PR.** License terms for future distribution require Owner decision.
