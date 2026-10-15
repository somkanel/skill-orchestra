from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/skill-piano/scripts/usage.py'
spec = importlib.util.spec_from_file_location('usage_under_test', SCRIPT)
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)


class UsageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.db = self.root / 'state/usage.sqlite3'
        self.skill = self.root / 'one/SKILL.md'
        self.skill.parent.mkdir()
        self.skill.write_text('test fixture')
        self.now = datetime(2026, 10, 14, 20, tzinfo=timezone.utc)

    def test_read_does_not_create_and_unknown_is_not_zero(self):
        result = usage.summarize([self.skill], self.db, self.now)
        self.assertEqual(result['status'], 'not_recorded')
        self.assertIsNone(result['skills'][str(self.skill)]['total'])
        self.assertFalse(self.db.parent.exists())

    def test_once_per_task_and_recent_window(self):
        usage.record(self.skill, 'old', self.db, self.now - timedelta(days=31))
        self.assertTrue(usage.record(self.skill, 'new', self.db, self.now)['recorded'])
        self.assertFalse(usage.record(self.skill, 'new', self.db, self.now)['recorded'])
        result = usage.summarize([self.skill], self.db, self.now)['skills'][str(self.skill)]
        self.assertEqual((result['total'], result['last_30_days']), (2, 1))
        self.assertEqual(result['last_used'], self.now.isoformat(timespec='microseconds'))

    def test_separate_instances_and_unseen_skill(self):
        other = self.root / 'two/SKILL.md'
        other.parent.mkdir()
        other.write_text('same displayed name, different instance')
        usage.record(self.skill, 'task', self.db, self.now)
        stats = usage.summarize([self.skill, other], self.db, self.now)['skills']
        self.assertEqual(stats[str(self.skill)]['total'], 1)
        self.assertEqual(stats[str(other)]['total'], 0)
        usage.record(other, 'task', self.db, self.now)
        self.assertEqual(usage.summarize([other], self.db, self.now)['skills'][str(other)]['total'], 1)

    def test_retry_concurrency_does_not_double_count(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(lambda _: usage.record(self.skill, 'same-task', self.db, self.now), range(8)))
        self.assertEqual(sum(r['recorded'] for r in results), 1)

    def test_symlink_alias_is_same_instance(self):
        alias = self.root / 'alias'
        try:
            alias.symlink_to(self.skill.parent, target_is_directory=True)
        except OSError:
            self.skipTest('OS does not permit creating symlinks')
        usage.record(self.skill, 'task', self.db, self.now)
        self.assertFalse(usage.record(alias / 'SKILL.md', 'task', self.db, self.now)['recorded'])

    def test_corrupt_database_not_replaced(self):
        self.db.parent.mkdir()
        self.db.write_bytes(b'not sqlite')
        result = subprocess.run([sys.executable, str(SCRIPT), '--db', str(self.db), 'record',
                                 '--skill', str(self.skill), '--task-id', 'task'], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.db.read_bytes(), b'not sqlite')

    def test_history_cannot_break_score_tie(self):
        usage.record(self.skill, 'used', self.db)
        data = json.loads((ROOT / 'examples/comparison.json').read_text())
        a, b = data['candidates']
        a['path'] = str(self.skill)
        b['path'] = str(self.root / 'unseen/SKILL.md')
        b['scores'] = a['scores']
        result = subprocess.run([sys.executable, str(ROOT / 'skills/skill-piano/scripts/score.py'),
                                 '--usage-db', str(self.db)], input=json.dumps(data), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload['state'], 'awaiting_choice')
        self.assertIsNone(payload['selected'])
        self.assertEqual(payload['candidates'][0]['usage']['total'], 1)
        self.assertEqual(payload['candidates'][1]['usage']['total'], 0)

    def test_unavailable_history_does_not_block_scoring(self):
        self.db.parent.mkdir()
        self.db.write_bytes(b'broken')
        result = subprocess.run([sys.executable, str(ROOT / 'skills/skill-piano/scripts/score.py'),
                                 str(ROOT / 'examples/comparison.json'), '--usage-db', str(self.db)],
                                text=True, capture_output=True)
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['selected'], 'deck-b')
        self.assertEqual(payload['usage_scope']['status'], 'unavailable')


if __name__ == '__main__':
    unittest.main()
