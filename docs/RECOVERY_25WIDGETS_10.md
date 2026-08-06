# Recovery of 3.19.11+25widgets.10

This recovery was reconstructed from the verified Kodi installation archive:

- archive: `skin.arctic.zephyr.martian.25widgets-3.19.11+25widgets.10.zip`
- archive SHA-256: `4de7fd897d997624b95c5094f825b7f000a931a840acf5ed24a92722f9ff55ec`
- archive size: 54,095,471 bytes
- archive files: 2,391
- base tree: `d89ad036f909f7936d3f45c5898c94d79f440e3a`
- recovered source commit (local reference): `45c86f8e2b4b88791f302b1bf98d349c919a1166`

## Recovered delta

The working archive differs from the verified 3.19.11+25widgets.3 base by 13 files:

- 12 modified text/XML/translation files;
- one added fixed YouTube fallback image.

## Validation

The recovery script:

1. verifies SHA-256 for every base file touched by the recovery;
2. applies a binary-safe patch;
3. checks SHA-256 for all 13 recovered files;
4. parses every XML file in `1080i/` and `shortcuts/`;
5. runs `git diff --check`;
6. creates the exact recovery commit and tag `25widgets.10-working`;
7. adds this documentation in a separate commit;
8. pushes a recovery branch and opens a draft pull request.

## Rule for future work

After every successful Kodi test: commit, push, tag the working checkpoint, and update the changelog before starting the next modification.
