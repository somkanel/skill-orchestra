#!/usr/bin/env python3
"""Read explicitly scoped skill entrypoints. Never execute discovered content."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

SKIP = {'.git', '__pycache__', 'node_modules', 'dist'}


def collect(paths=(), roots=()):
    discovered = [Path(p).expanduser().absolute() for p in paths]
    errors = []
    for value in roots:
        root = Path(value).expanduser().absolute()
        if not root.is_dir():
            errors.append({'path': str(root), 'error': 'Skill root is not a readable directory'})
            continue

        def failed(error):
            errors.append({'path': str(error.filename), 'error': str(error)})

        for directory, dirs, files in os.walk(root, followlinks=False, onerror=failed):
            dirs[:] = sorted(d for d in dirs if d not in SKIP)
            parent = Path(directory)
            if 'SKILL.md' in files:
                discovered.append(parent / 'SKILL.md')
            # Inspect linked skill entrypoints without recursively following linked trees.
            for name in dirs:
                linked = parent / name
                if linked.is_symlink() and (linked / 'SKILL.md').is_file():
                    discovered.append(linked / 'SKILL.md')
    records = {}
    for path in sorted(set(discovered), key=str):
        if path.is_dir():
            path = path / 'SKILL.md'
        try:
            real = path.resolve(strict=True)
            if real.name != 'SKILL.md' or not real.is_file():
                raise ValueError('Expected a SKILL.md entrypoint')
            if str(real) in records:
                records[str(real)]['discovered_paths'].append(str(path))
                continue
            raw = real.read_bytes()
            text = raw.decode('utf-8')
            records[str(real)] = {'path': str(real), 'discovered_paths': [str(path)],
                                  'sha256': hashlib.sha256(raw).hexdigest(),
                                  'text': text, 'lines': len(text.splitlines())}
        except (OSError, ValueError, RuntimeError) as error:
            errors.append({'path': str(path), 'error': str(error)})
    return {'schema': 'skill-orchestra/sources-1',
            'scope': {'paths': [str(p) for p in paths], 'roots': [str(p) for p in roots]},
            'host_visibility': 'not_checked', 'sources': list(records.values()), 'errors': errors}


def verify_candidates(data, manifest):
    """Bind each score candidate to an unchanged local entrypoint snapshot."""
    if not isinstance(manifest, dict) or manifest.get('schema') != 'skill-orchestra/sources-1':
        raise ValueError('Unsupported sources manifest')
    records = {}
    for item in manifest.get('sources', []):
        if not isinstance(item, dict):
            raise ValueError('Invalid source record')
        path, text, digest = item.get('path'), item.get('text'), item.get('sha256')
        if not isinstance(path, str) or not Path(path).is_absolute() or not isinstance(text, str):
            raise ValueError('Invalid source snapshot')
        if hashlib.sha256(text.encode('utf-8')).hexdigest() != digest:
            raise ValueError('Source snapshot digest mismatch: ' + path)
        if path in records:
            raise ValueError('Duplicate source identity: ' + path)
        records[path] = item
    checked = set()
    for candidate in data['candidates']:
        path = Path(candidate['path']).resolve(strict=True)
        key = str(path)
        if key in checked:
            raise ValueError('Candidates alias the same skill: ' + key)
        if key not in records:
            raise ValueError('Candidate has no source snapshot: ' + key)
        if hashlib.sha256(path.read_bytes()).hexdigest() != records[key]['sha256']:
            raise ValueError('Skill changed after inspection; inspect and reassess: ' + key)
        checked.add(key)
    return {'status': 'entrypoints_unchanged', 'candidate_count': len(checked),
            'limits': 'Checks source snapshots only, not evidence semantics, references, quality or host visibility.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', type=Path, help='Explicit skill directories or SKILL.md files')
    parser.add_argument('--root', action='append', default=[], type=Path, help='Only scan this skill root; repeatable')
    args = parser.parse_args()
    if not args.paths and not args.root:
        parser.error('Provide skill paths or an explicit --root')
    result = collect(args.paths, args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result['errors'] else 0


if __name__ == '__main__':
    sys.exit(main())
