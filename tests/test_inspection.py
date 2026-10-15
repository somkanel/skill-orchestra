import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_score import candidate, request

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/skill-piano/scripts/inspect_skills.py'
spec = importlib.util.spec_from_file_location('orchestra_inspection', SCRIPT)
inspection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inspection)


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.skill = self.root / 'plain/SKILL.md'
        self.skill.parent.mkdir()
        self.skill.write_bytes('---\r\nname: plain\r\n---\r\n完整正文：支持 HTML。\r\n'.encode())

    def data(self):
        item = candidate('A')
        item['path'] = str(self.skill)
        return request(item)

    def test_complete_snapshot_and_scope_isolation(self):
        outside = self.root / 'other/SKILL.md'
        outside.parent.mkdir()
        outside.write_text('Outside allowed scope')
        result = inspection.collect(roots=[self.skill.parent])
        self.assertEqual(len(result['sources']), 1)
        self.assertEqual(result['sources'][0]['text'].encode(), self.skill.read_bytes())
        self.assertEqual(result['host_visibility'], 'not_checked')
        self.assertEqual(inspection.verify_candidates(self.data(), result)['status'], 'entrypoints_unchanged')

    def test_linked_instance_deduplicated_but_same_names_preserved(self):
        (self.root / 'alias').symlink_to(self.skill.parent, target_is_directory=True)
        other = self.root / 'other/plain/SKILL.md'
        other.parent.mkdir(parents=True)
        other.write_bytes(self.skill.read_bytes())
        result = inspection.collect(roots=[self.root])
        self.assertEqual(len(result['sources']), 2)
        record = next(s for s in result['sources'] if s['path'] == str(self.skill))
        self.assertEqual(len(record['discovered_paths']), 2)

    def test_missing_entries_report_partial_scope(self):
        result = inspection.collect([self.skill, self.root / 'missing/SKILL.md'])
        self.assertEqual(len(result['sources']), 1)
        self.assertEqual(len(result['errors']), 1)

    def test_stale_snapshot_rejected(self):
        result = inspection.collect([self.skill])
        self.skill.write_text('Changed implementation promise')
        with self.assertRaisesRegex(ValueError, 'changed'):
            inspection.verify_candidates(self.data(), result)

    def test_uninspected_candidate_rejected(self):
        with self.assertRaisesRegex(ValueError, 'no source'):
            inspection.verify_candidates(self.data(), inspection.collect())

    def test_modified_snapshot_rejected(self):
        result = inspection.collect([self.skill])
        result['sources'][0]['text'] = 'Fabricated supporting instructions'
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            inspection.verify_candidates(self.data(), result)

    def test_alias_cannot_compete_against_itself(self):
        alias = self.root / 'alias'
        alias.symlink_to(self.skill.parent, target_is_directory=True)
        data = self.data()
        item = candidate('B')
        item['path'] = str(alias / 'SKILL.md')
        data['candidates'].append(item)
        with self.assertRaisesRegex(ValueError, 'alias'):
            inspection.verify_candidates(data, inspection.collect([self.skill]))

    def test_cli_source_check_and_stale_failure(self):
        manifest = self.root / 'sources.json'
        manifest.write_text(json.dumps(inspection.collect([self.skill])))
        cmd = [sys.executable, str(SCRIPT.with_name('score.py')), '--sources', str(manifest)]
        valid = subprocess.run(cmd, input=json.dumps(self.data()), text=True, capture_output=True)
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertEqual(json.loads(valid.stdout)['source_check']['status'], 'entrypoints_unchanged')
        self.skill.write_text('Changed')
        invalid = subprocess.run(cmd, input=json.dumps(self.data()), text=True, capture_output=True)
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(invalid.stdout, '')


if __name__ == '__main__':
    unittest.main()
