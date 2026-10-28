# Reproducible local build

## Supported input

The verified input is the original 31,237,649-byte `.n-gage` distribution with SHA-256 `34d7d73dc9d9e5b2f071eedd4768bdfa9f629de45e0cebd414c40f853814aa06`. The filename is irrelevant. No download is supplied. A repacked, modified, or different-market package is deliberately rejected; compatibility with other distributions has not been established.

Its main plaintext OPES is 32,144,179 bytes with 7,313 entries and SHA-256 `06df70afcb644f19e6521ae4471815263009b45a005873b77ce7f82114b32960`. Extraction selects the Game MIME part, walks SISData/DataUnit/FileData/Array fields and expands their plain or zlib-compressed streams. It identifies the main archive by hash. The extractor is scoped to this package, not a general SIS installer; extended SIS lengths are unsupported. No executable code is run, no archive paths are written to disk, and protected resources are not decrypted.

## Deterministic reconstruction

1. The Chapter 2 controller derives from the surviving Chapter 4 controller, changing chapter paths and image references locally.
2. Chapter 2–4 map recipes read the original Chapter 1 map tree. `from` selects a native node by child-index path; `set` changes specified fields; `children` supplies the reconstructed child sequence. Native styles and untouched branches remain local template references. New condition values, control names and coordinates are original reconstruction data. Action recipes similarly copy native line ranges and add original routing glue.
3. Chapter 5's builder starts from the surviving Chapter 6 trap scene and reconstructs interactive states and controls. Chapter 6's builder uses native layer structure, original asset identifiers and scene-specific reconstruction code.
4. Robot-route scripts are read from the user's main archive. Only targeted animation-reset transformations are applied. Full original dialogues are never embedded in this repository.
5. All 22 expanded resource SHA-256 values must match `baseline.json`. The deterministic OPES builder sorts paths, uses fixed baseline header/record bytes and zlib level9, choosing raw storage when compression is not smaller.
6. The expanded readback must equal the generated resource mapping, and the final length/SHA-256 must match the verified release. The program writes output only after these checks.

The fixed four bytes after the OPES signature and the final directory field are reproduced as baseline constants; no unproven timestamp semantics are assigned to them. This writer is for replacement script/scene archives. It is not an image-archive rewrite tool: image width/height metadata must be retained by any future general writer.

Exact payload identity is independent of the final zlib representation. Different zlib implementations can in principle produce different compressed bytes. The builder reports a container mismatch rather than silently accepting a nonmatching reference archive. `build-report.json` records Python and runtime zlib versions. The source verification report records the actually tested environment; the CI matrix tests formats, not a licensed game build on every listed platform.

## Local integration test

POSIX shell:

```sh
DIRK_GAME_PACKAGE="/absolute/path/original.n-gage" python -m unittest discover -s tests -v
```

PowerShell:

```powershell
$env:DIRK_GAME_PACKAGE = 'C:\games\original.n-gage'
python -m unittest discover -s tests -v
```

Integration builds into a temporary directory, checks the reference archive and verifies refusal to overwrite different output. Synthetic tests cover compression flags when lengths are equal, archive corruption, nested FWD/text round-trips, SIS arrays, unsupported input and output boundaries. Tests never require ROMs or emulation.

## Verify against a private baseline

If you already hold the verified reference artifact, compare it locally with the generated file using a byte comparison or SHA-256. It is not required as a build input. The checked manifest contains its checksum and each expanded payload checksum, not a compressed or encoded copy of the artifact.
