# PersianNew v13 — legacy source intake (NOT QUALIFIED)

## Preserved artifact

- File: `legacy/PersianNew2.css`
- Source: the Owner's previously uploaded `PersianNew2.css` recovered from personal file history.
- Source header: `Version: 13.0 — Mixed-Direction Code & Persian Mono Support`.
- Source size: **71,144 bytes**, **3,024 lines**.
- Original SHA-256: `b114384a1bd9a30f1064e8405d5ce31fef66b4af26bec33d4732b8c4b8a76fb9`.
- Original Git blob SHA-1: `c7b10268cb64d076a6b69a5deed66e0e3ab3509a`.
- Verified: the committed blob SHA matches the original Git blob SHA. Original CRLF line endings are preserved.

The file is a historical input, **not a release candidate or a validated theme**. Although its original heading says "Production Ready", that claim predates this repository's current acceptance procedure; do not transfer it to the current project's qualification state.

## Initial source-derived findings

1. The original CSS references four relative font assets not present in this repository: `fonts/Vazir-Regular.woff2`, `fonts/Vazir-Bold.woff2`, `fonts/AmazonEmberDisplay_Rg.ttf`, `fonts/AmazonEmberDisplay_Md.ttf`. The CSS file is preserved, **not** the missing font binaries. Distribution permission, especially for Amazon Ember Display, is unresolved.
2. The source contains 12 `@include-when-export` directives (four repeated across source sections). Their actual Typora/version-specific export behavior is **NOT_PROVEN** here; audit rather than remove or rewrite blindly.
3. It includes RTL/LTR and code-block/CodeMirror styling, CSS variables, light/dark rules and `@media print`. Correct behavior, selector compatibility and any redundancy are **NOT_EXECUTED/NOT_PROVEN** in Typora.
4. No authentic v14 CSS is part of this intake. Historical "Premium Editorial v14" descriptions are not a source file.
5. The historically reported delayed RTL-to-LTR change in Persian code fences remains a required real-runtime regression case; see `../../tests/MANUAL_TYPORA.md` and `../../tests/fixtures/code-fences.md`.

## Next qualification path

1. Do not modify `legacy/PersianNew2.css`; preserve its original checksum. Prepare an independently reviewable working copy `persiannew.css` only when ready to verify and reconcile all asset references and Typora-specific rules.
2. Distinguish justified source fixes from optional aesthetic redesign; first preserve the existing design intent. Use the official Typora docs and `../../knowledge/typora/INDEX.md`, filling **applicable** documentation gaps before claiming compliance.
3. Resolve or safely replace missing resources without silently bundling proprietary fonts. Any alteration affecting visual fidelity must be explicit and reviewed.
4. Run `python3 scripts/verify.py` against the **working** theme and examine the exact failures. The current structural verifier does **not** validate CSS files under `legacy/`, and green CI must not be reported as proof of this legacy CSS.
5. Install and exercise the candidate in real Typora (version + OS recorded), including before/after CodeMirror initialization, RTL/LTR fixtures, dark/light, menus, print/PDF, and asset loading. Until this happens, runtime is **NOT_EXECUTED**.
6. Update `theme.json` from `source-pending` to `ready` only when the declared install filename exists and the repository's structural contract passes. Even then, `ready` means source-present under the current schema; it does **not** certify real Typora rendering or publication readiness.
7. Keep future per-theme packaging and Releases a separate Owner-controlled authorization boundary; do not publish a release during intake.

## Documentation coverage boundary

Incomplete coverage of all Typora documentation does not itself prevent **legacy intake**. For qualification, every feature and affected API/selector that this particular CSS uses must have enough credible documented or real-runtime evidence to justify the intended change. Unsupported assertions remain NOT_PROVEN. Full-documentation coverage is a distinct outstanding approved project outcome.
