#!/usr/bin/env python3
"""Build a local draft ZIP from explicitly allowed source paths, not a release."""

import argparse
import hashlib
from pathlib import Path
import re
import sys
import zipfile

FILES = ('README.md', 'README.en.md', 'LICENSE', 'VERSION', 'CHANGELOG.md',
         'CONTRIBUTING.md', 'THIRD_PARTY_NOTICES.md', '.gitignore')
DIRECTORIES = ('skills', 'docs', 'tests', 'tools', 'examples', '.github')
SUFFIXES = {'.md', '.py', '.json', '.yaml', '.yml'}


def sources(root):
    root = Path(root)
    result = []
    for name in FILES:
        path = root / name
        if not path.is_file() or path.is_symlink():
            raise ValueError('Missing or unsafe source: ' + name)
        result.append(path)
    for name in DIRECTORIES:
        directory = root / name
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError('Missing or unsafe directory: ' + name)
        for path in directory.rglob('*'):
            if path.is_symlink():
                raise ValueError('Symlink not allowed: ' + str(path))
            if '__pycache__' in path.parts:
                continue
            if not path.is_file():
                continue
            if path.name != 'LICENSE' and path.suffix not in SUFFIXES:
                raise ValueError('Unexpected source file: ' + str(path))
            result.append(path)
    return sorted(result, key=lambda p: p.relative_to(root).as_posix())


def build(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    version = (root / 'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('VERSION must be a semantic version')
    entries = sources(root)
    for directory in DIRECTORIES:
        if output == root / directory or root / directory in output.parents:
            raise ValueError('Output cannot be inside packaged source directories')
    output.mkdir(parents=True, exist_ok=True)
    name = 'skill-orchestra-' + version + '-draft'
    archive = output / (name + '.zip')
    checksum = output / (name + '.sha256')
    if archive.exists() or checksum.exists():
        raise ValueError('Draft output already exists; use a new output directory')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zipped:
        for path in entries:
            info = zipfile.ZipInfo(name + '/' + path.relative_to(root).as_posix(), (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zipped.writestr(info, path.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum.write_text(digest + '  ' + archive.name + '\n', encoding='utf-8')
    return archive, checksum


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        archive, checksum = build(Path(__file__).resolve().parents[1], args.output)
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2)
    print(archive)
    print(checksum)
