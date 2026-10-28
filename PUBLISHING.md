# Publishing this source repository

This repository is intended for **original restoration source code and technical documentation only**, not for game binaries or generated outputs.

## First publication

1. Create a new public GitHub repository under `razvang-dev` (repository name: `nuclear-zeppelin-restoration`). Do **not** select "Initialize with a README" if using the command-line instructions below.
2. From the repository root, run `python -m unittest discover -s tests -v` and `python scripts/audit_source.py`. The package-dependent integration test will be skipped without `DIRK_GAME_PACKAGE`.
3. Confirm that `git status` and `git diff --cached --name-only` show only intended source/docs; do not stage any original-game files, game-derived binaries, synthetic rights files or personal data.
4. Publish the tracked source files with Git and check the hosted CI status before making the first tagged release.

```sh
git init
git branch -M main
git add .
python scripts/audit_source.py
git diff --cached --name-only
git commit -m "Publish restoration source and documentation"
git remote add origin https://github.com/razvang-dev/nuclear-zeppelin-restoration.git
git push -u origin main
```

The remote must exist first. The above commands do **not** create it. GitHub may require account authentication. Do not commit any privately generated `build/` output.

## Before tagging a release

A build from the verified original package must still be checked in the publisher's private environment; public CI only exercises generated fixtures and does not use or distribute the proprietary game package. The last recorded complete package-to-output verification is described in [docs/verification.md](docs/verification.md). The source-only tests can be run without original data.

## Copyright and attribution

Source and documentation are licensed under the [MIT License](LICENSE). Its legal condition is preservation of the copyright and license notice in copies or substantial portions of the source. The additional request to credit RazvanG and link the repository is stated in [CREDITS.md](CREDITS.md), but is **not** a separate binding condition of MIT. Do not represent this repository as legally cleared against every third-party right. Rebuilding a game resource archive from user-owned files may raise jurisdiction-specific copyright or anti-circumvention questions; consult qualified counsel before a public launch if legal clearance is required.
