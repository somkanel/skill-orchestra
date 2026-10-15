import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/skill-piano/scripts/score.py'


def load_score():
    spec = importlib.util.spec_from_file_location('orchestra_score', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def candidate(identity, grades=(2, 2, 2, 2, 2), status='eligible'):
    keys = ('delivery', 'coverage', 'environment', 'constraints', 'workflow')
    return dict(id=identity, name=identity, path='/sample/' + identity + '/SKILL.md',
                eligibility=status, eligibility_evidence='Fixture: required format and tools checked.',
                checks={'Deliver the requested artifact': dict(status='supported', evidence='Synthetic capability assumed.')},
                scores={k: dict(grade=v, evidence='Fixture evidence for ' + k)
                        for k, v in zip(keys, grades)})


def request(*candidates):
    return dict(schema='skill-orchestra/score-2', task='Create an editable deck',
                stage='Create slides', requirements=['Deliver the requested artifact'], candidates=list(candidates))


class ScoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_score()

    def test_unique_winner(self):
        result = self.module.evaluate(request(candidate('A', (2, 2, 2, 1, 1)),
                                              candidate('B', (2, 1, 2, 2, 2))))
        self.assertEqual(result['state'], 'ready')
        self.assertEqual(result['selected'], 'B')
        self.assertEqual([c['total'] for c in result['candidates']], [87, 88])

    def test_top_tie_waits(self):
        result = self.module.evaluate(request(candidate('A'), candidate('B')))
        self.assertEqual(result['state'], 'awaiting_choice')
        self.assertEqual(result['options'], ['A', 'B'])
        self.assertIsNone(result['selected'])

    def test_lower_tie_does_not_block(self):
        result = self.module.evaluate(request(candidate('A'), candidate('B', (1,)*5),
                                              candidate('C', (1,)*5)))
        self.assertEqual(result['selected'], 'A')

    def test_unknown_can_tie_blocks(self):
        result = self.module.evaluate(request(candidate('A'), candidate('B', (2, 2, 2, None, 2))))
        self.assertEqual(result['state'], 'needs_evidence')
        self.assertEqual(result['candidates'][1]['range'], [84, 100])

    def test_unknown_cannot_win_does_not_block(self):
        result = self.module.evaluate(request(candidate('A'), candidate('B', (1, 1, 0, None, 0))))
        self.assertEqual(result['selected'], 'A')

    def test_unknown_eligibility_can_win_blocks(self):
        result = self.module.evaluate(request(candidate('A', (1,)*5),
                                              candidate('B', status='unknown')))
        self.assertEqual(result['state'], 'needs_evidence')

    def test_ineligible_never_wins(self):
        result = self.module.evaluate(request(candidate('A', (1,)*5),
                                              candidate('B', status='ineligible')))
        self.assertEqual(result['selected'], 'A')
        self.assertIsNone(result['candidates'][1]['total'])

    def test_no_match(self):
        result = self.module.evaluate(request(candidate('A', status='ineligible')))
        self.assertEqual(result['state'], 'no_match')

    def test_explicit_choice_is_preserved(self):
        data = request(candidate('A', (1,)*5), candidate('B'))
        data['user_choice'] = 'A'
        result = self.module.evaluate(data)
        self.assertEqual((result['state'], result['selected']), ('user_selected', 'A'))

    def test_ineligible_user_choice_is_not_overridden(self):
        data = request(candidate('A', status='ineligible'), candidate('B'))
        data['user_choice'] = 'A'
        result = self.module.evaluate(data)
        self.assertEqual(result['state'], 'choice_unavailable')
        self.assertIsNone(result['selected'])

    def test_missing_evidence_rejected(self):
        data = request(candidate('A'))
        data['candidates'][0]['scores']['delivery']['evidence'] = ''
        with self.assertRaises(ValueError):
            self.module.evaluate(data)

    def test_bad_inputs_rejected(self):
        for value in (True, 3, -1, 1.0, '2'):
            with self.subTest(value=value):
                data = request(candidate('A'))
                data['candidates'][0]['scores']['delivery']['grade'] = value
                with self.assertRaises(ValueError):
                    self.module.evaluate(data)

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            self.module.evaluate(request(candidate('A'), candidate('A')))

    def test_duplicate_paths_rejected(self):
        data = request(candidate('A'), candidate('B'))
        data['candidates'][1]['path'] = data['candidates'][0]['path']
        with self.assertRaises(ValueError):
            self.module.evaluate(data)

    def test_path_must_be_absolute(self):
        data = request(candidate('A'))
        data['candidates'][0]['path'] = 'relative/SKILL.md'
        with self.assertRaises(ValueError):
            self.module.evaluate(data)
        data['candidates'][0]['path'] = 'C:\\skills\\A\\SKILL.md'
        self.assertEqual(self.module.evaluate(data)['selected'], 'A')

    def test_unknown_explicit_choice_needs_evidence(self):
        data = request(candidate('A', status='unknown'), candidate('B'))
        data['user_choice'] = 'A'
        result = self.module.evaluate(data)
        self.assertEqual(result['state'], 'needs_evidence')
        self.assertIsNone(result['selected'])

    def test_all_unknown_needs_evidence(self):
        result = self.module.evaluate(request(candidate('A', (None,)*5)))
        self.assertEqual(result['state'], 'needs_evidence')
        self.assertEqual(result['candidates'][0]['range'], [0, 100])

    def test_wrong_schema_and_unknown_keys_rejected(self):
        for extra in ({'schema': 'old'}, {'weights': [100]}):
            data = request(candidate('A'))
            data.update(extra)
            with self.assertRaises(ValueError):
                self.module.evaluate(data)

    def test_unknown_choice_rejected(self):
        data = request(candidate('A'))
        data['user_choice'] = 'missing'
        with self.assertRaises(ValueError):
            self.module.evaluate(data)

    def test_cli_stdin_and_invalid_json(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(request(candidate('A'))),
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['selected'], 'A')
        result = subprocess.run([sys.executable, str(SCRIPT)], input='{broken', text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
