# Real Typora runtime / visual acceptance (manual, not CI)

For each **source-ready** theme, record **Typora exact version/build, OS, locale, selected theme, light/dark mode, local `base.user.css` / `<theme>.user.css` overrides, and resource/font availability**. Report per case `PASS / FAIL / NOT_EXECUTED`, include screenshot or exported-file path when available; never blanket-PASS unrun platforms.

1. Install CSS at Typora theme-folder **root**, with only its own referenced, licensed assets. Restart and confirm menu selection, fonts/fallback, and no broken URLs.
2. Open `fixtures/rtl-ltr.md`: inspect Persian paragraphs/headings, English LTR, mixed numbers/punctuation, inline code, links, lists, tables, image, cursor/edit order, and live font-size preference. Confirm whether intended direction is per-element rather than inadvertently global.
3. Open `fixtures/code-fences.md`: inspect immediately after file open **and again after CodeMirror appears/settles**; focus/blur, switch language/fences, and edit mixed Persian/English code. Compare direction, alignment, caret movement, wrapping, scrollbars, colors, syntax highlighting, `.md-fences` / `.cm-s-inner`; check source mode separately. Capture before/after evidence for the historically reported delayed RTL→LTR bug.
4. Switch between available light/dark conditions and inspect readable contrast, UI/sidebar, dialogs, task markers, tables, selection and hover. Check that another theme remains unaffected by this theme's resources/styles.
5. Print and export PDF using the **same selected theme**. Inspect pagination, colors/contrast, headings, code blocks and fonts in the saved output, with OS + Typora version recorded. Do not infer Windows/Linux dark-print behavior across old/new versions.
6. Reinstall/roll back using preserved prior CSS/assets where an actual previous version exists; report when no prior release exists.

Browser screenshots and static CSS validation are useful previews but **do not establish authentic Typora behavior**. A verified runtime should exercise both initial render and delayed CodeMirror transition. Attach evidence to the PR, not checked-in personally identifying document content.
