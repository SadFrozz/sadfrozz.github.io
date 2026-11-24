# SadFrozz project portal

Bilingual public documentation for six SadFrozz projects, published at https://sadfrozz.github.io/ through GitHub Pages.

## Build

Python 3.9+; no third-party packages, package manager or network calls are required.

```sh
python scripts/build.py
python scripts/check.py
python -m http.server 8765 --directory docs
```

GitHub Pages publishes the tracked `docs/` directory from `main`. Generated HTML works without JavaScript. JavaScript only enables catalogue search and category filtering. No external fonts, analytics, project runtime data or credentials are used.

## Update documentation

1. Inspect the public repositories, current branches, published releases and actual source behavior.
2. Update both languages in `content/projects.json` and source/release pins in `content/snapshot.json`.
3. Keep release functionality separate from unreleased branch changes and distinguish source review from hardware testing.
4. Run the build and checks, preview desktop/mobile and commit the generated `docs/` with content changes.

Never copy local REAPER projects, subtitles.json, settings.json, role maps, EFI configurations, network dumps, passwords or keys into this repository.

The portal links to original release assets; it does not redistribute project binaries. Project and dependency licensing remains defined in the original repositories. The documentation snapshot is dated 2026-11-24.
