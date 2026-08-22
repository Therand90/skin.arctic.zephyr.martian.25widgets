# Validated skin baseline — 3.19.11+25widgets.89.5-develop

Validated on 2026-08-22 as the skin component of the stable Therand inline-trailer stack.

## Canonical artifact

```text
skin.arctic.zephyr.martian.25widgets-3.19.11+25widgets.89.5-pagination-stop.zip
SHA256 86e58b12dc6e0603e2d0434e9a4a46958ce7dd885c946ef46fe2c643df507a62
```

## Relevant history

- `.89.2` introduced the validated root→inline handoff and is the clean architectural base.
- `.89.3` and `.89.4` were experiments intended to reduce dynamic provider refreshes during preview lifecycle. They did **not** solve the Kodi `CDirectoryProvider` refresh storm and should not be treated as successful fixes.
- `.89.5` retains those harmless visibility changes but adds the validated pagination identity fallback: when `ListItem.Title` is empty (for example JackTook `Next (N)` cards), `ListItem.Label` is published as `TherandInset.SelectedTitle`. This makes leaving the last poster a real selection change so AutoTrailer stops the owned trailer immediately.
- `.89.6` attempted a JackTook player-refresh/sort guard. It failed: refresh bursts remained and page-2 pagination stopped populating. `.89.6` is rejected.

The exact source delta from the validated `.89.2` artifact to `.89.5` is archived in `baseline/89.2-to-89.5.patch` and touches only:

- `addon.xml`
- `1080i/Includes_Animations.xml`
- `1080i/Includes_Widgets.xml`

## Companion validated versions

- AutoTrailer `0.27.2`
- YouTube `7.4.4+therand.1.0.4`
- JackTook `1.18.0.4` with local runtime compatibility patch

This branch is a restoration/reference snapshot. Future experiments should not be developed directly on it.
