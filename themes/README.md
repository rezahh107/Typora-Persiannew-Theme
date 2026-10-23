# Independent themes

Each immediate `themes/<id>/` directory represents one independent Typora theme. The slug `<id>` and install CSS basename are **lowercase alphabetic words separated by hyphens** (e.g. `paper-light`). This follows [Typora's naming rule](https://support.typora.io/About-Themes/).

Minimum files:

- `theme.json` — exact keys `id`, `css`, `status`. `css` must be `<id>.css`.
- `README.md` — purpose, install/resource instructions, compatibility evidence and limitations.
- `<id>.css` — **only when** status is `ready`.
- `assets/` — optional theme-owned, legally redistributable resources; preserve referenced relative paths.

`status` is `source-pending` when the theme has no usable source CSS, or `ready` when the declared install file exists. A pending theme must not ship its declared install CSS. A recovered historical source may be preserved separately as immutable evidence, but should **not** be called install-ready without verification and a reviewable decision.

Do not import other themes' CSS or assets. Put per-theme files and compatibility evidence next to that theme. Shared *verification and fixtures* live outside individual theme directories; shared *appearance dependencies* are deliberately not required.

Typora's install layout places CSS directly in the theme folder, not in a nested `themes/<id>` directory. Until the future packaging flow is implemented, install manually from a ready theme's README. Do not claim a package or release was generated.
