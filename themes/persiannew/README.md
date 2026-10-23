# PersianNew — source pending

**NOT INSTALLABLE / NOT QUALIFIED.** This is the first intended theme in the collection. The authentic v13 CSS is now preserved without edits as [legacy/PersianNew2.css](legacy/PersianNew2.css), with byte identity and intake findings recorded in [INTAKE.md](INTAKE.md). The declared install CSS `persiannew.css` is still absent, `theme.json` remains `source-pending`, and no redistributable font assets or verified v14 source exist in the repository.

The original file header identifies **v13.0**. It contains Persian/English typography, Vazir and Amazon Ember Display references, RTL/LTR handling, code-block styling and print CSS, but those implementation details have **not** passed this repository's qualification process. A light "Premium Editorial" v14 was discussed historically; **its authentic CSS remains missing and must not be fabricated.**

Before standardization: use the preserved [v13 intake](INTAKE.md) as the immutable reference; inspect licenses for every asset (especially Amazon Ember), the four referenced but missing font files, and relevant official Typora behavior. Create a separately reviewable working install CSS without silently redesigning or declaring v14. Switch `theme.json` to `ready` only when the declared install CSS exists and structural checks pass; real Typora testing and publication remain separate gates.

Mandatory regression scenario when source becomes available: a Persian code fence may initially render RTL, then change direction after CodeMirror initialization. Exercise the before/after transition and mixed LTR code using [the code-fence fixture](../../tests/fixtures/code-fences.md) and [runtime checklist](../../tests/MANUAL_TYPORA.md). This issue is **reported, not reproduced** in this repository.

Compatibility: **NOT_PROVEN** (Typora version, OS, real visual behavior and export). Font redistribution permissions: **NOT_PROVEN**. Installation instructions: unavailable until a real, reviewable source exists.
