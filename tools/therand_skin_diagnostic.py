#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

# Temporary diagnostic helper for the active Kodi skin branch.
FILES = [
    Path("1080i/Home.xml"),
    Path("1080i/Includes.xml"),
    Path("1080i/Includes_Home.xml"),
    Path("1080i/Includes_Widgets.xml"),
    Path("1080i/script-skinshortcuts.xml"),
    Path("1080i/Font.xml"),
    Path("1080i/SkinSettings.xml"),
    Path("shortcuts/template.xml"),
    Path("shortcuts/overrides.xml"),
]

PATTERNS = [
    r"HomeWidgetInfoWidgets",
    r"HomeVerticalMenuWidgets",
    r"InfoSub",
    r"HomeWidgetsFullscreenInfo",
    r"ListItem\.(?:Label2|Year|Date|Premiered|Plot|Title|Label)",
    r"Container\([^)]*\)\.ListItem\.(?:Label2|Year|Date|Premiered|Plot|Title|Label)",
    r"ReplayMetadata",
    r"replaymetadata",
    r"slideshowpath",
    r"Property\((?:B|b)ackground\)",
    r"type=\"multiimage\"",
    r"type=\"image\"",
    r"widget.*(?:title|font|color|bold)",
    r"(?:title|font|color|bold).*widget",
    r"Skin\.String\([^)]*(?:title|font|color|bold)",
    r"propertySettings",
    r"buttonID",
]
RX = re.compile("|".join(f"(?:{p})" for p in PATTERNS), re.IGNORECASE)


def print_context(path: Path, radius: int = 5) -> None:
    if not path.exists():
        print(f"\n### MISSING {path}")
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    hits = [i for i, line in enumerate(lines) if RX.search(line)]
    print(f"\n### {path} — {len(lines)} lines — {len(hits)} matching lines")
    emitted: set[int] = set()
    for hit in hits:
        start = max(0, hit - radius)
        end = min(len(lines), hit + radius + 1)
        if any(i in emitted for i in range(start, end)):
            continue
        print(f"\n--- {path}:{start + 1}-{end} ---")
        for i in range(start, end):
            print(f"{i + 1:05d}: {lines[i]}")
            emitted.add(i)


for file_path in FILES:
    print_context(file_path)
