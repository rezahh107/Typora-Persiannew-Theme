# Instructions for AI theme contributors

Read [README.md](README.md), then the relevant [theme README](themes/README.md), [creation workflow](workflows/CREATE_THEME.md) and [Typora knowledge index](knowledge/typora/INDEX.md) before editing.

Authority: current Owner task and the [complete adopted goal](https://docs.google.com/document/d/1_tY5lHTuDW4Kt8ujrU--vAcNXYj4T1rKRMLvEhKQLIw/edit) > repository-owned operational instructions > official Typora behavior for platform claims > cited engineering references. Retrieve [PPDM DEF-REPO-01](https://github.com/rezahh107/Personal-Preference-Decision-Model/blob/main/knowledge/current/defaults/DEF-REPO-01.md) for foundation work; apply **Inspect → Applicability → Smallest Sufficient Delta → Validate**, not a copied file tree.

Each theme owns its CSS/assets, installation notes and independently verifiable behavior. For PersianNew's current source status and limitations, consult [theme.json](themes/persiannew/theme.json) and the [theme README](themes/persiannew/README.md); `ready` indicates structural source availability, **not** Typora runtime or visual approval. Do not invent v13/v14 CSS, silently replace a legacy file, or bundle fonts without known distribution rights. A new non-Persian theme is allowed.

Run `python3 scripts/verify.py` on changes and report **what it actually checks**. For visual changes, follow `tests/MANUAL_TYPORA.md`, recording actual Typora version/OS, screenshots and observations; if unavailable, report `NOT_EXECUTED`. Official documentation claims belong in `knowledge/typora/` with source and version/date boundaries, not guesses.

Work on a branch and propose a reviewable PR. **Do not merge or rename the repository without Owner authorization; public releases require a separate explicit authorization.** `AGENTS.md` is guidance, not a guarantee that an AI host has GitHub access or that runtime checks passed.
