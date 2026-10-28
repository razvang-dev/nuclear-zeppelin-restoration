"""Optional local integration. Never attach original packages to public CI."""
import os
from pathlib import Path
import tempfile
import unittest
from dirk_restore.__main__ import run_build

class LocalBuild(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('DIRK_GAME_PACKAGE'), 'Set DIRK_GAME_PACKAGE locally')
    def test_full_build_and_output_protection(self):
        with tempfile.TemporaryDirectory() as directory:
            report = run_build(Path(os.environ['DIRK_GAME_PACKAGE']), Path(directory))
            self.assertTrue(report['verified']); self.assertEqual(report['entries'], 22)
            (Path(directory) / 'protected_general.opes').write_bytes(b'not expected')
            with self.assertRaisesRegex(ValueError, 'different contents'):
                run_build(Path(os.environ['DIRK_GAME_PACKAGE']), Path(directory))

    def test_unknown_input_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'fake.n-gage'; source.write_bytes(b'fixture')
            output = Path(directory) / 'out'
            with self.assertRaisesRegex(ValueError, 'Unsupported game package'):
                run_build(source, output)
            self.assertFalse(output.exists())
