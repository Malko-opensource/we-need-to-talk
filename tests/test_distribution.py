"""Observable installation and archive guarantees, without model or network calls."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from install import install, contents, SOURCE
from package import build, PLUGIN


class DistributionTests(unittest.TestCase):
    def test_install_is_complete_and_repeatable(self):
        with tempfile.TemporaryDirectory() as directory:
            destination, backup, changed = install(SOURCE, Path(directory))
            self.assertTrue(changed)
            self.assertIsNone(backup)
            self.assertEqual(contents(destination), contents(SOURCE))
            self.assertFalse(install(SOURCE, Path(directory))[2])

    def test_customized_install_requires_backup_and_preserves_it(self):
        with tempfile.TemporaryDirectory() as directory:
            destination, _, _ = install(SOURCE, Path(directory))
            custom = destination / "my-notes.md"
            custom.write_text("local customization", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                install(SOURCE, Path(directory))
            self.assertEqual(custom.read_text(), "local customization")
            _, backup, _ = install(SOURCE, Path(directory), backup_existing=True)
            self.assertEqual((backup / "my-notes.md").read_text(), "local customization")
            self.assertEqual(contents(destination), contents(SOURCE))

    def test_failed_replacement_restores_previous_install(self):
        with tempfile.TemporaryDirectory() as directory:
            destination, _, _ = install(SOURCE, Path(directory))
            (destination / "my-notes.md").write_text("keep me", encoding="utf-8")
            rename = Path.rename
            def fail_staged_move(path, target):
                if path.parent.name.startswith(".we-need-to-talk-install-"):
                    raise OSError("simulated move failure")
                return rename(path, target)
            with patch.object(Path, "rename", fail_staged_move):
                with self.assertRaises(OSError):
                    install(SOURCE, Path(directory), backup_existing=True)
            self.assertEqual((destination / "my-notes.md").read_text(), "keep me")

    def test_source_cannot_be_used_as_install_destination(self):
        with self.assertRaises(ValueError):
            install(SOURCE, SOURCE.parent, backup_existing=True)

    def test_archive_is_reproducible_and_contains_complete_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build(Path(directory))
            first = archive.read_bytes()
            self.assertEqual(first, build(Path(directory)).read_bytes())
            with zipfile.ZipFile(archive) as bundle:
                self.assertIsNone(bundle.testzip())
                self.assertIn("we-need-to-talk/LICENSE", bundle.namelist())
                self.assertIn("we-need-to-talk/.claude-plugin/plugin.json", bundle.namelist())
                self.assertIn("we-need-to-talk/.codex-plugin/plugin.json", bundle.namelist())
                for path in SOURCE.rglob("*"):
                    if path.is_file():
                        name = "we-need-to-talk/" + path.relative_to(PLUGIN).as_posix()
                        self.assertEqual(bundle.read(name), path.read_bytes())
                self.assertFalse(any("docs/specs/" in name or "/.git/" in name for name in bundle.namelist()))


if __name__ == "__main__":
    unittest.main()
