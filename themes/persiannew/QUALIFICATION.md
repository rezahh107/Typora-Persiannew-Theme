# PersianNew v13 — structural candidate qualification

## Provenance and selection

- Immutable input: `legacy/PersianNew2.css` (3,024 lines; 71,144 bytes; SHA-256 `b114384a1bd9a30f1064e8405d5ce31fef66b4af26bec33d4732b8c4b8a76fb9`). **This file is unchanged.**
- The purported single legacy CSS also contains a truncated first CSS copy around line 1210, assistant conversation text beginning at line 1211, a Markdown-fenced second fragment at line 1224, and a complete standalone third v13 CSS beginning at **line 1536**. Copying all 3,024 lines verbatim would import unrelated prose/duplicates into an install theme.
- The working `persiannew.css` uses the **last complete standalone section (legacy lines 1536–3024)** as the source of its real CSS rules. It is an authentic portion of the immutable v13 artifact, **not** a byte-for-byte copy of the whole intake and **not** a reconstructed v14.
- The chosen section has seven `@font-face` rules, a light default with a `prefers-color-scheme: dark` palette, RTL editing typography, sidebar/UI rules, CodeMirror syntax colors and an `@media print` block. The preserved full legacy intake has 19 font-face rules due to concatenation.

## Bounded differences from the selected v13 section

1. Changed the inaccurate candidate header from `Production Ready` to `structural candidate`, with a short provenance comment; document colors, sizes, layout and print declarations are otherwise retained.
2. Removed four `@include-when-export url('./fonts/...')` directives because the targets are absent. Their Typora-specific behavior has not been established for current versions; no export equivalence is claimed.
3. Replaced six broken `url('./fonts/...')` face sources with **local-only** font lookups, preserving the original `font-family`, `unicode-range` and declared weights. The source's seventh face already uses `local()`. No external URLs, font downloads, bundled binaries or changes to shared resource policy.
4. The manifest becomes `ready` only in the repository's narrow meaning: install CSS is present and structural verification must pass. This is **not** a runtime/visual/PDF certification.

The initial 1,535 lines were not blindly deduplicated: they contain another incomplete version and inserted prose. Extraction rather than reinterpreting those fragments reduces design changes, but the chosen section is not guaranteed to reproduce every earlier variation. Owner visual review is necessary.

## Font dependency and redistribution matrix

| Original font file (missing) | Purpose | Candidate behavior | Rights/equivalence |
| --- | --- | --- | --- |
| `Vazir-Regular.woff2` | Persian normal text and Persian code glyphs | `local('Vazir')` / `local('Vazir Regular')` / `local('Vazirmatn')`; otherwise CSS fallbacks | Vazir/Vazirmatn upstream publishes OFL-1.1, but no binary with verified provenance is bundled here; Vazirmatn can have different metrics |
| `Vazir-Bold.woff2` | Persian bold text and code glyphs | `local('Vazir Bold')` / `local('Vazir')` / `local('Vazirmatn Bold')`; otherwise fallback | Weight/style and glyph matching are environment-dependent; a normal-face fallback for a bold declaration is not exact |
| `AmazonEmberDisplay_Rg.ttf` | Latin normal text | `local('Amazon Ember Display Regular')` / `local('Amazon Ember Display')`; otherwise fallback | **No confirmed public redistribution license**. No binary provided. Local face naming is unverified on target OS |
| `AmazonEmberDisplay_Md.ttf` | Latin “bold” (medium mapped to weight 700 in v13) | `local('Amazon Ember Display Medium')` / `local('Amazon Ember Display')`; otherwise fallback | **No confirmed redistribution license**; weight mapping preserved from v13, not exact bold design |

Users may install legitimately obtained font files through their own licensed channels. The theme works as a CSS selection without the files, but substitutes installed Vazir/Vazirmatn/Tahoma and system Latin/mono fonts where faces are unavailable. It **does not** promise identical glyphs, metrics, widths, or embedded export fonts. Do not retrieve and commit Amazon Ember from third-party mirrors or assume that an accessible CDN licenses redistribution.

Sources: [Vazir upstream](https://github.com/rastikerdar/vazir-font), [Vazirmatn upstream OFL](https://github.com/rastikerdar/vazirmatn/blob/master/OFL.txt), [Typora custom fonts](https://support.typora.io/Custom-Font/).

## Typora compatibility and CodeMirror issue

- Official [About Themes](https://support.typora.io/About-Themes/) describes root-level CSS installation and restart; [Write Custom Theme](https://theme.typora.io/doc/Write-Custom-Theme/) recommends document selectors and `@media print`. Source's broad `html/body` RTL `!important` rules can affect Windows/Linux UI; retained for v13 fidelity **without verified UI usability**.
- Official [Code Block Styles](https://support.typora.io/Code-Block-Styles/) confirms pre-initialization `.md-fences` and initialized `.cm-s-inner`. The candidate preserves styles for both. Source mode uses `.cm-s-typora-default` and is a separate surface.
- **Historical delayed code-fence direction change is NOT_PROVEN / NOT_FIXED.** The source has `unicode-bidi: plaintext` for `.md-fences` and children but also explicit LTR for descendants; CodeMirror's editable lines/caret are a separate runtime. Adding stronger CSS without reproducing the transition may harm code editing. The [code-fences fixture](../../tests/fixtures/code-fences.md) and [real Typora checklist](../../tests/MANUAL_TYPORA.md) explicitly test before and after initialization.
- Official [RTL](https://support.typora.io/RTL/) is experimental, [About Themes](https://support.typora.io/About-Themes/) supports separate light/dark theme choices and media queries; the source's actual palette defaults to white/blue and switches to dark/yellow with `prefers-color-scheme: dark`. This **differs from the historical description** of v13 as dark-only.
- Printing is declared under `@media print`; [Export](https://support.typora.io/Export/) and [Typora 1.10 changes](https://support.typora.io/What's-New-1.10/) contain version-dependent Windows/Linux dark PDF behavior. **Do not claim a supported Typora version or PDF fidelity without an observed export.**
- Theme-local CSS cascade may be modified by `base.user.css` or `persiannew.user.css`; see [Add Custom CSS](https://support.typora.io/Add-Custom-CSS/).

## Evidence and outstanding decision

- **Static/source evidence:** exact legacy blob matched on the starting main; final candidate derived from its coherent section, and a repository test guards the original SHA-256.
- **Structural/CI evidence:** recorded separately on the exact PR Head; `python3 scripts/verify.py` checks manifest, basic CSS braces/strings, local assets, fixtures and regression tests, not CSS rendering.
- **Real Typora:** `NOT_EXECUTED` when no licensed running Typora instance is available. No verified application version/OS, CodeMirror transition, font-resolution screenshot, print or PDF.
- **Owner visual decision required:** local font substitutions and the light/dark variation may deviate from the expected approved look. Do not treat structural readiness as acceptance.

Future multi-theme automated releases remain an independent **Owner-authorized** project outcome, not part of this candidate.
