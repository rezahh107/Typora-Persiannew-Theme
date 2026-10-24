# PersianNew — v13 structural candidate

The installable **CSS candidate** is [persiannew.css](persiannew.css). Manifest `status: ready` means the declared source file exists and passes the repository's bounded structural contract; it **does not** imply visual approval, verified Typora functionality, PDF quality or release readiness.

This is the first theme within a **multi-theme** repository. The original [v13 intake](INTAKE.md) and immutable [legacy/PersianNew2.css](legacy/PersianNew2.css) are preserved. See the [qualification and exact differences](QUALIFICATION.md) before expecting historical appearance. The purported original includes mixed-in conversation output; the working candidate uses the last coherent v13 CSS. Authentic v14 remains unavailable.

## Manual installation (candidate only)

1. In Typora, open **Preferences → Appearance → Open Theme Folder**.
2. Copy **only** `persiannew.css` into the **root** of the opened folder (not a nested `themes/persiannew/` directory). No `fonts/` directory is required by the candidate.
3. Restart Typora and choose **Persiannew** from the Themes menu.
4. Open [RTL/LTR](../../tests/fixtures/rtl-ltr.md) and [code fences](../../tests/fixtures/code-fences.md), then follow the [real-runtime checklist](../../tests/MANUAL_TYPORA.md). Record the Typora version/OS and any installed user CSS overrides.

## Typography and appearance restrictions

The original CSS referenced missing Vazir regular/bold and Amazon Ember Display regular/medium binaries. The candidate looks up these families **locally** if available and falls back to installed Vazir/Vazirmatn/Tahoma and system mono/Latin fonts otherwise. **Font substitutions can change line breaks and layout**. Amazon Ember redistribution rights are unverified: no font file is shipped or required, and users must obtain any proprietary font independently and lawfully.

The CSS retains right-to-left body/content treatment and code-specific direction rules. It has **light default and dark OS media-query styles**; do not assume this is dark-only. Broad RTL UI rules, the delayed Persian code-fence direction report, light/dark contrasts and font embedding in PDF **have not been verified in actual Typora**.

Compatibility: **NOT_PROVEN** (no validated Typora version/OS/print/PDF). Visual approval: **pending Owner**. Real Typora tests: **NOT_EXECUTED**. This CSS is a candidate, **not a release**. The safe rollback before any approved release is to remove the candidate CSS from Typora's theme folder and select a built-in theme.

Source, documentation/rights and regression boundaries: [QUALIFICATION.md](QUALIFICATION.md).
