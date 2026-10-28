"""Offline command-line build and inspection."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zlib
from .opes import read_opes, build
from .package import main_archive
from .reconstruct import reconstruct, manifest


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run_build(game, output):
    reference = manifest()
    package = game.read_bytes()
    if digest(package) != reference['package_sha256']:
        raise ValueError('Unsupported game package SHA256; see docs/reproducibility.md')
    assets = read_opes(main_archive(package, reference['main_sha256']))
    resources = reconstruct(assets)
    actual = {k: digest(v) for k, v in sorted(resources.items())}
    if actual != reference['resources']:
        differences = sorted(k for k in actual.keys() | reference['resources'].keys()
                             if actual.get(k) != reference['resources'].get(k))
        raise ValueError('R12 resource mismatch: ' + ', '.join(differences))
    blob = build(resources)
    if read_opes(blob) != resources:
        raise ValueError('OPES readback mismatch')
    if len(blob) != reference['output_bytes'] or digest(blob) != reference['output_sha256']:
        raise ValueError('R12 container mismatch; check Python/zlib versions')
    output.mkdir(parents=True, exist_ok=True)
    destination = output / 'protected_general.opes'
    # Do not overwrite a user's existing file with different bytes.
    if destination.exists() and destination.read_bytes() != blob:
        raise ValueError('Output exists with different contents; choose a new directory')
    destination.write_bytes(blob)
    report = {'revision': 'R12', 'verified': True, 'entries': len(resources),
              'bytes': len(blob), 'sha256': digest(blob),
              'package_sha256': digest(package), 'resource_sha256': actual,
              'python': sys.version.split()[0], 'zlib': zlib.ZLIB_RUNTIME_VERSION}
    (output / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'R12 verified: {len(resources)} resources, {len(blob)} bytes, SHA256 {digest(blob)}')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    command = sub.add_parser('build', help='Build and verify R12 from your original .n-gage')
    command.add_argument('--game', type=Path, required=True)
    command.add_argument('--output', type=Path, default=Path('build/r12'))
    command = sub.add_parser('inspect', help='List and validate a local OPES')
    command.add_argument('archive', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'build':
            run_build(args.game, args.output)
        else:
            for name, data in sorted(read_opes(args.archive.read_bytes()).items()):
                print(f'{len(data):8d} {digest(data)} {name}')
    except (ValueError, OSError, KeyError, AssertionError, zlib.error) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
