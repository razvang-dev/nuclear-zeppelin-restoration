# Build architecture

The command loads a supported user package into memory, validates its identity and walks only plain SIS data containers. Native OPES resource paths are dictionary keys rather than filesystem paths. The original game package is never changed or installed.

`reconstruct.py` orchestrates the Chapter 2 controller template, three declarative map recipes and two late-room builders. Reconstruction operates on expanded resource bytes. A map recipe is a sparse scene graph relative to native nodes: `from: []` means the root, while `[0, 2]` means root child0's child2. `set` overlays fields without copying the rest of the original node. `children` replaces only the child sequence. Omitted fields are inherited. `node` creates a reconstruction-defined node when no native type template exists.

`fwd.py` emits native `fwd2DIST` nodes with big-endian strings and coordinates. Supported types are 1, 3, 5, 7, 30, 31, 40, 50, 51, 52 and 80. Type95 inspection remains partial and serialization is deliberately unsupported. Unsupported nodes fail instead of being dropped. Header/count and bounds checks precede successful readback. These tools cover this restoration's scenes, not every historic FWD variant.

`control6.py` derives each route's animations from original script calls, adds robot base clips where required and emits only the ten changed dialogue resources. No full dialogue body is shipped as source. Normalized newline handling is explicit so Windows text-mode defaults do not alter the baseline.

OPES readback and a 22-entry checksum manifest guard the final result. The public build produces an OPES and a JSON report locally, not a distributable binary patch ZIP. Public CI requires only synthetic data. Local integration additionally checks the real package-to-verified-output path.
