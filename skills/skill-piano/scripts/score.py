#!/usr/bin/env python3
"""Validate evidence records and calculate task fit. Does not invoke skills."""

import argparse
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys

WEIGHTS = {'delivery': 30, 'coverage': 24, 'environment': 20,
           'constraints': 16, 'workflow': 10}


def fields(value, required, optional=()):
    if not isinstance(value, dict):
        raise ValueError('Expected an object')
    if set(value) - set(required) - set(optional) or set(required) - set(value):
        raise ValueError('Missing or unexpected fields: expected ' + ', '.join(required))


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + ' must be a non-empty string')


def evaluate(data):
    fields(data, ('schema', 'task', 'stage', 'requirements', 'candidates'), ('user_choice', 'exclusions'))
    if data['schema'] != 'skill-orchestra/score-2':
        raise ValueError('Unsupported scoring schema')
    for key in ('task', 'stage'):
        nonempty(data[key], key)
    if not isinstance(data['candidates'], list):
        raise ValueError('Candidates must be an array')
    requirements = data['requirements']
    if not isinstance(requirements, list) or not requirements:
        raise ValueError('At least one task delivery requirement is required')
    for requirement in requirements:
        nonempty(requirement, 'requirement')
    if len(set(requirements)) != len(requirements):
        raise ValueError('Task requirements must be unique')
    if 'exclusions' in data:
        if not isinstance(data['exclusions'], dict):
            raise ValueError('Exclusions must map absolute paths to reasons')
        for path, reason in data['exclusions'].items():
            nonempty(path, 'excluded path')
            nonempty(reason, 'exclusion reason')
            if not (PurePosixPath(path).is_absolute() or PureWindowsPath(path).is_absolute()):
                raise ValueError('Excluded source path must be absolute')
    records, identities, paths = [], set(), set()
    for candidate in data['candidates']:
        fields(candidate, ('id', 'name', 'path', 'eligibility', 'eligibility_evidence', 'checks', 'scores'))
        for key in ('id', 'name', 'path', 'eligibility_evidence'):
            nonempty(candidate[key], key)
        if not (PurePosixPath(candidate['path']).is_absolute()
                or PureWindowsPath(candidate['path']).is_absolute()):
            raise ValueError('Candidate path must be absolute')
        if candidate['id'] in identities or candidate['path'] in paths:
            raise ValueError('Candidate IDs and paths must be unique')
        identities.add(candidate['id'])
        paths.add(candidate['path'])
        if candidate['eligibility'] not in ('eligible', 'ineligible', 'unknown'):
            raise ValueError('Invalid eligibility')
        fields(candidate['checks'], tuple(requirements))
        effective = candidate['eligibility']
        reasons = []
        for requirement in requirements:
            check = candidate['checks'][requirement]
            fields(check, ('status', 'evidence'))
            nonempty(check['evidence'], 'requirement evidence')
            if check['status'] not in ('supported', 'missing', 'unknown'):
                raise ValueError('Invalid requirement check status')
            if check['status'] == 'missing':
                effective = 'ineligible'
                reasons.append('Missing delivery requirement: ' + requirement)
        if effective != 'ineligible' and any(c['status'] == 'unknown' for c in candidate['checks'].values()):
            effective = 'unknown'
            reasons.append('Delivery requirement evidence is incomplete')
        fields(candidate['scores'], tuple(WEIGHTS))
        lower, upper, complete, parts = 0, 0, True, {}
        for key, weight in WEIGHTS.items():
            item = candidate['scores'][key]
            fields(item, ('grade', 'evidence'))
            nonempty(item['evidence'], key + ' evidence')
            grade = item['grade']
            if grade is not None and (type(grade) is not int or grade not in (0, 1, 2)):
                raise ValueError(key + ' grade must be 0, 1, 2, or null')
            if grade is None:
                complete = False
                upper += weight
                parts[key] = None
            else:
                points = weight * grade // 2
                lower += points
                upper += points
                parts[key] = points
        # A zero in either core dimension contradicts ability to deliver this stage.
        # This is a semantic gate, not an arbitrary total-score threshold.
        if any(candidate['scores'][key]['grade'] == 0 for key in ('delivery', 'coverage')):
            effective = 'ineligible'
            reasons.append('Core delivery or task coverage is explicitly unmatched')
        excluded = effective == 'ineligible'
        records.append({**candidate, 'declared_eligibility': candidate['eligibility'],
                        'eligibility': effective, 'decision_reasons': reasons, 'points': parts,
                        'total': lower if complete and not excluded else None,
                        'range': None if excluded else [lower, upper]})

    def result(state, selected=None, options=()):
        return {'schema': 'skill-orchestra/result-2', 'task': data['task'],
                'stage': data['stage'], 'requirements': requirements, 'weights': WEIGHTS.copy(), 'state': state,
                'selected': selected, 'options': list(options), 'candidates': records,
                'exclusions': data.get('exclusions', {})}

    if 'user_choice' in data:
        nonempty(data['user_choice'], 'user_choice')
        if data['user_choice'] not in identities:
            raise ValueError('user_choice does not identify a candidate')
        chosen = next(c for c in records if c['id'] == data['user_choice'])
        selected = result('user_selected', selected=chosen['id'])
        # User choice is a routing decision, not a claim that capability is proven.
        selected['advisories'] = chosen['decision_reasons'][:]
        if chosen['eligibility'] != 'eligible':
            selected['advisories'].append(chosen['eligibility_evidence'])
        if chosen['total'] is None and chosen['eligibility'] == 'eligible':
            selected['advisories'].append('Some fit dimensions remain unassessed; explicit choice retained')
        return selected

    possible = [c for c in records if c['eligibility'] != 'ineligible']
    if not possible:
        return result('no_match')
    certain = [c for c in possible if c['eligibility'] == 'eligible' and c['total'] is not None]
    if not certain:
        return result('needs_evidence', options=[c['id'] for c in possible])
    highest = max(c['total'] for c in certain)
    unresolved = [c for c in possible if c['eligibility'] == 'unknown'
                  or (c['total'] is None and c['range'][1] >= highest)]
    if unresolved:
        return result('needs_evidence', options=[c['id'] for c in unresolved])
    top = [c['id'] for c in certain if c['total'] == highest]
    if len(top) > 1:
        return result('awaiting_choice', options=top)
    return result('ready', selected=top[0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', help='JSON input file; omitted or - reads stdin')
    parser.add_argument('--sources', type=Path, help='Verify candidates against an inspected source manifest')
    args = parser.parse_args()
    try:
        raw = Path(args.input).read_text(encoding='utf-8') if args.input and args.input != '-' else sys.stdin.read()
        data = json.loads(raw)
        result = evaluate(data)
        if args.sources:
            from inspect_skills import verify_candidates
            manifest = json.loads(args.sources.read_text(encoding='utf-8'))
            result['source_check'] = verify_candidates(data, manifest)
        else:
            result['source_check'] = {'status': 'not_checked'}
    except (ValueError, OSError, RuntimeError) as error:
        print('Scoring input rejected: ' + str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
