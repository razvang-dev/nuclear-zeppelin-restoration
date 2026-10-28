# Dirk Dagger native resource restoration

Project repository: https://github.com/razvang-dev/nuclear-zeppelin-restoration

Original Python tools and reconstruction definitions for **Dirk Dagger and the Nuclear Zeppelin**, Nokia N-Gage 2.0. Build the reconstructed resource archive locally from your own original game package. The original engine, artwork and story scripts remain in use.

This repository contains source code, declarative scene recipes, documentation, hashes and synthetic tests. Original game data, compiled OPES, rights files, firmware and emulators are not included. It does not recover the original encrypted protected archive or generate entitlement files.

## What the restoration achieves

The original installation retains most of the game's artwork, animations, dialogue and story logic, but certain chapter controllers and interactive scene definitions are unavailable through its ordinary resource path. This project reconstructs those missing definitions in the formats understood by the original engine.

The restoration reconstructs missing scene definitions using the game's original assets and scripts, with placement, layering, and animation alignment checked against the original retail game's presentation in the reviewed scenes.

The reconstruction covers:

- **Chapter 2 entry and navigation:** the chapter controller, town map, first/repeat visits and native roadworker/tub event dispatch.
- **Chapter 3–4 maps:** six destinations with chapter-specific discovery gates, visit states and first-entry presentation.
- **Chapter 5 trap room:** character visibility, parallax layers, puzzle interactions, plank handling, Franklin's rescue and the onward route.
- **Chapter 6 control room:** foreground composition, character/face overlays, native instruction and quiz gates, and robot/statue animation integration.

The implementation reuses original resources supplied locally by the user. It leaves the distributed game executable and DLLs unchanged. Scene graphs (`.fwd`) define layers, visibility and interaction regions; event handlers (`.action`) connect those controls to surviving native scripts. Ten dialogue resources are transformed locally to correct specific animation-reset references and composition behavior; their original bodies are not distributed here.

## Native resource engineering

The project's OPES reader validates the native archive directory and its explicit compression flag, including compressed entries whose stored and expanded lengths happen to match. FWD tools preserve supported native scene structures, while declarative map recipes and scene builders provide reproducible reconstruction definitions.

The generated archive contains **22 resources in 12,716 bytes**. Its controller definitions, scene graphs and animation adjustments connect surviving game systems through the original engine's native interfaces. Original protected plaintext remains unrecovered; the output is a reconstructed replacement, not a decrypted historical archive.

Read the [technical restoration report](docs/technical-restoration.md) and [architecture](docs/architecture.md) for implementation details. See [provenance and distribution scope](docs/provenance.md) for the distinction between public source and locally generated game-derived output. This independent project is not affiliated with or endorsed by the game's rights holders.

## Build

Requires Python **3.10 or newer**, using only the standard library. No installation, network access, emulator or third-party Python dependency is required. Run from the repository root:

```sh
python -m dirk_restore build --game "/path/to/your/original.n-gage" --output build/restored
```

On Windows, `py -3` can replace `python`. Keep your package outside the repository.

The supported package SHA-256 is:

```text
34d7d73dc9d9e5b2f071eedd4768bdfa9f629de45e0cebd414c40f853814aa06
```

The command validates the input, reads the plain main archive from the package's Game SIS part, generates the missing native definitions, applies targeted animation-reset transformations locally, and checks every expanded resource and the final archive against the reconstruction manifest. An unrecognized package is rejected instead of producing an unverified patch.

Successful output:

- `build/restored/protected_general.opes`: **22 entries, 12,716 bytes**.
- `build/restored/build-report.json`: input/output hashes, per-resource hashes and runtime versions.

Expected final SHA-256:

```text
b586611a8a848ed109926d7c2c51b5bc3a3beb1fb9a1cfc0da251347d347b365
```

The source package is never modified. Existing differing output files are not overwritten. See [reproducibility](docs/reproducibility.md) for compatibility and verification details.

## Use the result

Close EKA2L1, back up your existing replacement, and put the generated `protected_general.opes` beside the original `opes_general.opes` in the installed game's `private/2001ad86` directory. Keep the old `protected_general.opes.ngdat` inactive under its `.ngdat.disabled` name. Preserve your working entitlement, saves, original main archive, localization, EXE and DLLs. This source build does not install or create rights files.

## Inspect an archive

```sh
python -m dirk_restore inspect build/restored/protected_general.opes
```

The inspection command reads the archive directory, expands its resources and lists their internal paths, sizes and checksums.

## Repository layout

| Path | Purpose |
| --- | --- |
| `dirk_restore/opes.py` | OPES reader and deterministic script-archive writer |
| `dirk_restore/fwd.py` | Supported native FWD node parser/serializer and construction helpers |
| `dirk_restore/package.py` | Read-only MIME/SIS plaintext-resource extraction |
| `dirk_restore/recipes/` | Chapter 2–4 map edits relative to locally supplied native templates |
| `dirk_restore/trap5.py`, `control6.py` | Original Chapter 5–6 scene/action construction and route transformations |
| `dirk_restore/baseline.json` | Reconstruction checksums; no compiled resources |
| `tests/` | Generated format fixtures and optional local integration |
| `docs/` | Technical research, architecture, provenance and reproducibility |

## Source and distribution scope

Read [provenance](docs/provenance.md) before adding files or making a release. Locally generated outputs contain game-derived resources and are not public source artifacts. Do not commit them. Original project source and documentation are available under the [MIT License](LICENSE), credited to **RazvanG**. See [credits and attribution](CREDITS.md). This license grants no rights in original game content.

For publication instructions and the final source-only review checklist, see [PUBLISHING.md](PUBLISHING.md).
