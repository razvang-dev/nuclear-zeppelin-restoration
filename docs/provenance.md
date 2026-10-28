# Source provenance and public artifact boundaries

The source tree was organized from the project's original OPES/FWD tools and reconstruction work. It includes no copied emulator implementation or SIS installer code.

| Component | Origin / generation rule |
| --- | --- |
| OPES reader/builder | Original project format research; compression byte91 and native directory layout |
| FWD tools | Original project parser/serializer, extended here for native map text nodes and validation |
| MIME/SIS reader | New read-only implementation for the supported distribution's plain data fields |
| Map recipes | Original edits describing reconstruction differences relative to the user's native Chapter 1 scene; retained native nodes and action lines are source references |
| Late-room builders | Original project reconstruction functions refactored to consume an in-memory resource mapping |
| Dialogue overrides | Generated only at build time by transforming the user's surviving native scripts |
| Baseline manifest | SHA-256 identifiers and size; no recoverable original or compiled payloads |
| Tests | Newly generated synthetic fixtures; optional integration requires a user-local input |
| Technical report | Project research documentation updated through the owner-confirmed working reconstruction |

Asset paths, handler identifiers and story-state names identify the original engine interfaces that the reconstruction must address. They are references, not distributed artwork, extracted dialogue bodies or an embedded resource archive. Geometry/style fields retained from native templates are selected locally. New layout values and event-routing glue are represented as source definitions.

The public tree must not contain `.n-gage`, installed OPES or NGDAT, synthetic DR/rights records, game executables, original art/animation/dialogue files, firmware/ROMs, emulator distributions, saves, recordings, screenshots or private research archives. Generated output belongs outside Git tracking. `.gitignore` and `scripts/audit_source.py` provide mechanical checks; review new source changes for content provenance as well.

Original project source and documentation are offered under the MIT License, Copyright (c) 2026 RazvanG (https://github.com/razvang-dev). Preserve that copyright and license notice. See ../CREDITS.md for attribution. The license applies only to material its licensor can license; it grants no rights in the original game. This source audit is not a legal-clearance opinion.

This repository performs no rights-file generation, original protected-archive decryption, NGDAT repackaging or emulator modification. Existing runtime entitlement is outside the build workflow.
