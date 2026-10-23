# Typora Themes

A multi-theme repository and AI-assisted workflow for designing, testing, installing, maintaining, and eventually releasing independent [Typora](https://typora.io/) themes.

**Current state (2026-10-23): foundation in progress; no qualified or installable theme yet.** PersianNew's genuine v13 CSS has now been recovered and preserved byte-for-byte as an [unqualified historical input](themes/persiannew/INTAKE.md), **not** as the declared install CSS. The reported v14 source remains unverified. Source recovery does not prove Typora compatibility or authorize font redistribution.

## Start here

- **Use or develop a theme:** [themes/README.md](themes/README.md); the current [PersianNew record](themes/persiannew/README.md) explicitly marks the source as pending.
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

For a theme marked `ready`, open Typora **Preferences → Appearance → Open Theme Folder**, copy its declared CSS to the **top level** of that folder and its licensed relative assets in their referenced paths, restart Typora, and select the theme from the **Themes** menu. Refer to the theme's README for exact supported versions/platforms. There is no installable PersianNew file in this repository today.

## Authority and release

The [Owner-approved Goal Authority](https://docs.google.com/document/d/1_tY5lHTuDW4Kt8ujrU--vAcNXYj4T1rKRMLvEhKQLIw/edit) defines the **complete destination**, not just this foundation batch: independent multi-theme product, reusable official knowledge and AI workflow, meaningful real Typora testing, and owner-controlled per-theme automated releases. See [future release contract](workflows/RELEASE_DESTINATION.md). The [PPDM Repository Foundation](https://github.com/rezahh107/Personal-Preference-Decision-Model/blob/main/knowledge/current/domains/repository-foundation/INDEX.md) provides the adaptation method, not a template to copy.

Changes go through reviewable PRs. **No rename, merge, tagging, public release, or redistribution of unlicensed fonts is authorized by a passing check or PR.** License terms for future distribution require Owner decision.
