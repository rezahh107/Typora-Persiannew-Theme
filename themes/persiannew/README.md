# PersianNew — v13 working CSS (merged; not released)

The merged, installable **working CSS** is [persiannew.css](persiannew.css). Manifest `status: ready` means the declared source file exists and passes the repository's bounded structural contract; it **does not by itself** imply visual approval, verified Typora functionality, PDF quality or release readiness. Separate bounded real-Typora evidence and Owner-desktop observations are documented below and in [QUALIFICATION.md](QUALIFICATION.md).

This is the first theme within a **multi-theme** repository. The original [v13 intake](INTAKE.md) and immutable [legacy/PersianNew2.css](legacy/PersianNew2.css) are preserved. See the [qualification and exact differences](QUALIFICATION.md) before expecting historical appearance. The purported original includes mixed-in conversation output; the working candidate uses the last coherent v13 CSS. Authentic v14 remains unavailable.

## Manual installation (working CSS in main; no public release)

1. In Typora, open **Preferences → Appearance → Open Theme Folder**.
2. Copy **only** `persiannew.css` into the **root** of the opened folder (not a nested `themes/persiannew/` directory). No `fonts/` directory is required by the candidate.
3. Restart Typora and choose **Persiannew** from the Themes menu.
4. Open [RTL/LTR](../../tests/fixtures/rtl-ltr.md) and [code fences](../../tests/fixtures/code-fences.md), then follow the [real-runtime checklist](../../tests/MANUAL_TYPORA.md). Record the Typora version/OS and any installed user CSS overrides.

## Typography and appearance restrictions

The original CSS referenced missing Vazir regular/bold and Amazon Ember Display regular/medium binaries. The working CSS looks up these families **locally** if available and falls back to installed Vazir/Vazirmatn/Tahoma and system mono/Latin fonts otherwise. **Font substitutions can change line breaks and layout**. Amazon Ember redistribution rights are unverified: no font file is shipped or required, and users must obtain any proprietary font independently and lawfully.

The CSS retains right-to-left body/content treatment and code-specific direction rules. It has **light default and dark OS media-query styles**; do not assume this is dark-only. Bounded real Typora tests on Ubuntu 24.04.5 / Typora 1.14.9-1 verified specific light/dark displays, code-fence edits and actual PDF exports; not all CodeMirror/caret scenarios or original licensed-font PDF behavior are proven.

Compatibility: **BOUNDED EVIDENCE** for the tested Ubuntu/Typora 1.14.9-1 scenarios; other versions, OSes and historical licensed-font equivalence remain **NOT_PROVEN**. Owner tested a byte-identical-CSS copy under a separate filename on their own Typora and reported no material observed regression, apart from slightly heavier typography which they explicitly preferred. The exact rendered font family was not identified. PR #3 was merged with Owner authorization on 2026-10-24. This **is not a public Release** or a claim of complete parity. Roll back an installed copy by selecting another theme, or removing the CSS from Typora's theme folder if appropriate.

Source, documentation/rights and regression boundaries: [QUALIFICATION.md](QUALIFICATION.md).
