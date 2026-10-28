"""Check tracked/exportable source names, encodings and size boundaries."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'.py', '.md', '.json', '.yml', '.txt', '.toml'}
SPECIAL = {'.gitignore', '.gitattributes', 'LICENSE'}


def audit(paths):
    failures = []
    for path in paths:
        file = ROOT / path
        if file.name not in SPECIAL and file.suffix not in ALLOWED:
            failures.append(f'{path}: unexpected file type')
            continue
        data = file.read_bytes()
        if len(data) > 200_000 or b'\0' in data:
            failures.append(f'{path}: binary or oversized content')
            continue
        try:
            data.decode('utf-8')
        except UnicodeError:
            failures.append(f'{path}: non-UTF8 data')
    return failures


def main():
    result = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True)
    if result.returncode == 0:
        paths = [p for p in result.stdout.decode().split('\0') if p]
    else:
        # Source ZIPs have no Git metadata; ignore only transient Python caches.
        paths = [str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts]
    if not paths:
        raise SystemExit('No source files selected; stage the source tree first')
    failures = audit(paths)
    if failures:
        raise SystemExit('\n'.join(failures))
    print(f'Source audit passed: {len(paths)} text files; no packaged binary assets')


if __name__ == '__main__':
    main()
