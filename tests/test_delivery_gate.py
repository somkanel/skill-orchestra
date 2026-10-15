import itertools
import unittest
from test_score import candidate, request, load_score

REQUIREMENT = 'Deliver the requested artifact'


class DeliveryGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.score = load_score()

    def check(self, item, status):
        item['checks'][REQUIREMENT] = dict(status=status, evidence='Explicit test capability finding.')
        return item

    def test_zero_fit_no_longer_selected(self):
        result = self.score.evaluate(request(candidate('A', (0,)*5)))
        self.assertEqual(result['state'], 'no_match')
        self.assertIsNone(result['selected'])

    def test_no_candidates_is_no_match(self):
        self.assertEqual(self.score.evaluate(request())['state'], 'no_match')

    def test_high_score_cannot_override_missing_deliverable(self):
        good = candidate('A', (1,)*5)
        bad = self.check(candidate('B'), 'missing')
        result = self.score.evaluate(request(good, bad))
        self.assertEqual(result['selected'], 'A')
        self.assertEqual(result['candidates'][1]['eligibility'], 'ineligible')

    def test_unknown_capability_does_not_become_no_match(self):
        result = self.score.evaluate(request(self.check(candidate('A'), 'unknown')))
        self.assertEqual(result['state'], 'needs_evidence')

    def test_low_unknown_capability_still_needs_clarification(self):
        result = self.score.evaluate(request(candidate('A'), self.check(candidate('B', (1,)*5), 'unknown')))
        self.assertEqual(result['state'], 'needs_evidence')

    def test_user_choice_cannot_override_missing_capability(self):
        data = request(self.check(candidate('A'), 'missing'), candidate('B'))
        data['user_choice'] = 'A'
        result = self.score.evaluate(data)
        self.assertEqual(result['state'], 'choice_unavailable')
        self.assertIsNone(result['selected'])

    def test_user_choice_unknown_capability_waits(self):
        data = request(self.check(candidate('A'), 'unknown'))
        data['user_choice'] = 'A'
        self.assertEqual(self.score.evaluate(data)['state'], 'needs_evidence')

    def test_user_choice_zero_core_is_unavailable(self):
        data = request(candidate('A', (0,)*5))
        data['user_choice'] = 'A'
        self.assertEqual(self.score.evaluate(data)['state'], 'choice_unavailable')

    def test_every_requirement_must_be_addressed(self):
        data = request(candidate('A'))
        data['requirements'].append('Include editable source')
        with self.assertRaises(ValueError):
            self.score.evaluate(data)
        data['candidates'][0]['checks']['Include editable source'] = dict(status='missing', evidence='Only flattened image output.')
        self.assertEqual(self.score.evaluate(data)['state'], 'no_match')

    def test_unstated_or_duplicate_requirements_rejected(self):
        for requirements in ([], [''], [REQUIREMENT, REQUIREMENT]):
            data = request(candidate('A'))
            data['requirements'] = requirements
            with self.assertRaises(ValueError):
                self.score.evaluate(data)

    def test_legacy_record_cannot_skip_gate(self):
        data = request(candidate('A'))
        data['schema'] = 'skill-orchestra/score-1'
        with self.assertRaises(ValueError):
            self.score.evaluate(data)

    def test_all_1024_grade_combinations_respect_core_gate(self):
        for values in itertools.product((0, 1, 2, None), repeat=5):
            result = self.score.evaluate(request(candidate('A', values)))
            if 0 in values[:2]:
                self.assertEqual(result['state'], 'no_match')
            elif None in values:
                self.assertEqual(result['state'], 'needs_evidence')
            else:
                self.assertEqual(result['state'], 'ready')

    def test_input_order_does_not_change_winner_or_tie_members(self):
        for items in ((candidate('A'), candidate('B', (1,)*5)), (candidate('A'), candidate('B'))):
            forward = self.score.evaluate(request(*items))
            reverse = self.score.evaluate(request(*reversed(items)))
            self.assertEqual(forward['state'], reverse['state'])
            self.assertEqual(forward['selected'], reverse['selected'])
            self.assertEqual(set(forward['options']), set(reverse['options']))


if __name__ == '__main__':
    unittest.main()
