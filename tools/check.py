#!/usr/bin/env python3
"""Check this project's skill metadata, relative references and Python syntax."""

import ast
from pathlib import Path
import re

SKILLS = ('skill-orchestra', 'skill-piano', 'skill-violin')


def check(root):
    root = Path(root)
    errors = []
    for name in SKILLS:
        path = root / 'skills' / name / 'SKILL.md'
        if not path.is_file():
            errors.append('Missing ' + str(path))
            continue
        text = path.read_text(encoding='utf-8')
        front = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not front or not re.search(r'^name: ' + re.escape(name) + r'$', front[1], re.M):
            errors.append('Invalid skill identity: ' + name)
        if not front or not re.search(r'^description: \S.+$', front[1], re.M):
            errors.append('Missing description: ' + name)
        if not (path.parent / 'LICENSE').is_file():
            errors.append('Missing skill license: ' + name)
        if not (path.parent / 'agents/openai.yaml').is_file():
            errors.append('Missing agent metadata: ' + name)
    for path in root.rglob('*'):
        if '.git' in path.parts or 'dist' in path.parts or '__pycache__' in path.parts:
            continue
        if path.is_symlink():
            errors.append('Unexpected symlink: ' + str(path))
            continue
        if path.suffix == '.md' and path.is_file():
            for target in re.findall(r'\]\(([^)\n]+)\)', path.read_text(encoding='utf-8')):
                if target.startswith(('https:', 'http:', '#', 'mailto:')):
                    continue
                relative = target.split('#', 1)[0]
                if relative and not (path.parent / relative).is_file():
                    errors.append('Broken reference: ' + str(path) + ' -> ' + target)
        if path.suffix == '.py' and path.is_file():
            try:
                ast.parse(path.read_text(encoding='utf-8'))
            except SyntaxError as error:
                errors.append(str(error))
    return errors


if __name__ == '__main__':
    failures = check(Path(__file__).resolve().parents[1])
    for failure in failures:
        print(failure)
    if failures:
        raise SystemExit(1)
    print('Project identities, local references and Python syntax checked.')
