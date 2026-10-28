# Source verification

Verified on 27 October 2026.

| Check | Result |
| --- | --- |
| Original package accepted by SHA-256 | Pass |
| Plain main OPES extracted from MIME/SIS | Pass |
| Expanded resource hashes | 22 / 22 match |
| Generated archive size | 12,716 bytes |
| Generated archive SHA-256 | `b586611a8a848ed109926d7c2c51b5bc3a3beb1fb9a1cfc0da251347d347b365` |
| Direct private-baseline byte comparison | Identical |
| Synthetic and local integration tests | 9 passed |
| Python | 3.12.14 |
| Runtime zlib | 1.3.2 |

The integration test covers the complete user-package-to-output path and refusal to overwrite a different existing output. The comparison used the project's private reference baseline, which is not part of the public tree.

The committed CI workflow runs synthetic tests on its declared platforms. It has not yet run on GitHub; no hosted CI result is claimed. Tests here do not execute the game or add an emulator/hardware claim. The project owner confirmed the finished restoration as working.

The repository export contains no compiled OPES, rights files, original game package, extracted proprietary resources, firmware, emulator, saves, images or recordings. Source-only auditing checks the staged/exported file set.
