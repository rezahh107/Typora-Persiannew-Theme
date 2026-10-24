# Official Typora documentation coverage register

**Initial inventory, not complete coverage.** Checked 2026-10-23. Authoring-relevant links below are original official Typora pages, not copied documentation. `DOCUMENTED` = official guidance inspected and distilled in [AUTHORING_RULES.md](AUTHORING_RULES.md); **not** observed to work in a specific Typora runtime. `INDEXED / NOT_YET_CONVERTED` = known official page or topic, still requiring detailed conversion/testing. The [support index](https://support.typora.io/) and [theme guide index](https://theme.typora.io/doc/) are discovery entrypoints; future passes must reconcile added/changed pages rather than treating this list as exhaustive.

| Domain | Official reference | State / qualification boundary |
| --- | --- | --- |
| Discovery, install, names, light/dark | [About Themes](https://support.typora.io/About-Themes/) | DOCUMENTED; runtime untested |
| CSS authoring, selectors, source, print | [Write Custom Theme](https://theme.typora.io/doc/Write-Custom-Theme/) | DOCUMENTED; selector stability version-dependent |
| CSS precedence, debug, user overrides | [Add Custom CSS](https://support.typora.io/Add-Custom-CSS/) | DOCUMENTED; local settings can affect screenshots |
| CodeMirror fence lifecycle/syntax colors | [Code Block Styles](https://support.typora.io/Code-Block-Styles/) | DOCUMENTED; delayed RTL switch unverified |
| RTL limitations | [RTL](https://support.typora.io/RTL/) | DOCUMENTED as experimental; mixed-language correctness unverified |
| Typography and font sizing | [Custom Fonts](https://support.typora.io/Custom-Font/) | DOCUMENTED; font distribution permission not inferred |
| Rendering selectors, tables/lists | [Typesetting](https://support.typora.io/Typeset/) | INDEXED / NOT_YET_CONVERTED fully |
| Export/printing | [Export](https://support.typora.io/Export/), [Page Breaks](https://support.typora.io/Page-Breaks/) | INDEXED; cross-version PDF behavior needs runtime |
| PDF behavior change | [What's New 1.10](https://support.typora.io/What's-New-1.10/) | INDEXED; conflicts with older Export wording for Windows/Linux dark print |
| Code-language highlighting | [Code Fences Language Support](https://support.typora.io/Code-Fences-Language-Support/) | INDEXED / NOT_YET_CONVERTED |
| Source mode and authoring | [Write Custom Theme](https://theme.typora.io/doc/Write-Custom-Theme/) | DOCUMENTED basic classes; comprehensive coverage pending |
| Theme installation/gallery | [Install Theme](https://theme.typora.io/doc/Install-Theme/), [Submit Theme](https://theme.typora.io/doc/Submit-A-Theme/) | DOCUMENTED install; gallery submission out of current batch |
| Diagrams/Mermaid | [Diagram Options](https://support.typora.io/Diagram-Options/) | INDEXED / NOT_YET_CONVERTED |
| Tables, lists, images, links, tasks | [Typesetting](https://support.typora.io/Typeset/), [support index](https://support.typora.io/) | INDEXED; detailed selector/tests incomplete |
| OS differences and application versions | [Write Custom Theme](https://theme.typora.io/doc/Write-Custom-Theme/), [What's New 1.10](https://support.typora.io/What's-New-1.10/) | INDEXED; no supported-version matrix proved |
| Light/dark and platform modes | [About Themes](https://support.typora.io/About-Themes/), [Dark Mode](https://support.typora.io/Dark-Mode/) | DOCUMENTED basic mechanism and theme selection; runtime untested |
| Other support topics (non-theme) | [Typora support index](https://support.typora.io/) | UNCLASSIFIED; needs complete-site inventory and applicability review |

| Legacy export asset hint | [Custom Fonts](https://support.typora.io/Custom-Font/), [Export](https://support.typora.io/Export/) | Exact `@include-when-export` semantics NOT_PROVEN in official pages checked; PersianNew removed references to absent assets |

## Maintenance method

On each authoring task or when the official docs change: discover candidate pages from both official indexes; classify each page as **theme-applicable**, **related**, or **not applicable**; record its URL, review date, Typora version/platform applicability if stated, and `DOCUMENTED / RUNTIME_OBSERVED / NOT_PROVEN` status. Convert important statements into a short, cited **rule + example/fixture + verification step**, and update this table. Do not wholesale copy site content or claim whole-site coverage. Prioritize changes impacting install semantics, code fences, RTL and exports.
