import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PackageTests(unittest.TestCase):
    def test_project_references(self):
        self.assertEqual(load('check').check(ROOT), [])

    def test_roundtrip_and_reproducible(self):
        module = load('package')
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            archive, checksum = module.build(ROOT, Path(a) / 'dist')
            other, _ = module.build(ROOT, Path(b) / 'dist')
            self.assertEqual(archive.read_bytes(), other.read_bytes())
            self.assertEqual(checksum.read_text().split()[0], hashlib.sha256(archive.read_bytes()).hexdigest())
            with zipfile.ZipFile(archive) as zipped:
                self.assertIsNone(zipped.testzip())
                for info in zipped.infolist():
                    relative = Path(info.filename).relative_to(Path(info.filename).parts[0])
                    self.assertEqual(zipped.read(info), (ROOT / relative).read_bytes())
                zipped.extractall(Path(a) / 'unpacked')
            extracted = next((Path(a) / 'unpacked').iterdir())
            result = subprocess.run([sys.executable, str(extracted / 'skills/skill-piano/scripts/score.py'),
                                     str(extracted / 'examples/comparison.json')], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['selected'], 'deck-b')
            with self.assertRaises(ValueError):
                module.build(ROOT, Path(a) / 'dist')

    def test_dangling_output_links_rejected(self):
        module = load('package')
        version = (ROOT / 'VERSION').read_text().strip()
        for suffix in ('.zip', '.sha256'):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as temp:
                output = Path(temp) / 'out'
                output.mkdir()
                outside = Path(temp) / 'outside'
                link = output / ('skill-orchestra-' + version + '-draft' + suffix)
                try:
                    link.symlink_to(outside)
                except OSError:
                    self.skipTest('OS does not permit creating symlinks for this test')
                with self.assertRaises(ValueError):
                    module.build(ROOT, output)
                self.assertFalse(outside.exists())
                self.assertTrue(link.is_symlink())
                self.assertEqual(list(output.iterdir()), [link])

    def test_source_filter_excludes_private_root_files(self):
        names = [p.relative_to(ROOT).parts[0] for p in load('package').sources(ROOT)]
        self.assertNotIn('dist', names)
        self.assertNotIn('archive', names)
        self.assertNotIn('.git', names)

    def test_unsafe_symlink_rejected(self):
        module = load('package')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in module.FILES:
                (root / name).write_text('0.1.0')
            for name in module.DIRECTORIES:
                (root / name).mkdir()
            try:
                (root / 'skills/link.md').symlink_to(root / 'VERSION')
            except OSError:
                self.skipTest('OS does not permit creating symlinks for this test')
            with self.assertRaises(ValueError):
                module.sources(root)


if __name__ == '__main__':
    unittest.main()
