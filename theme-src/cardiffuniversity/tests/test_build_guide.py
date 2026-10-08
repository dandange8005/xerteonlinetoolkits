import contextlib
import io
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import support
import guide_fixture as fx

build_guide = support.load_tool("build-guide")


def quiet(fn, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        code = fn(*args, **kwargs)
    return code, out.getvalue()


class BuildGuideTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.guide = fx.write_guide(self.root)
        self.out = self.root / "site"

    def build(self, **kwargs):
        return quiet(build_guide.build, guide_dir=self.guide, out=self.out, last_changed=lambda p: None, **kwargs)

    def test_builds_every_page_and_the_marker(self):
        code, printed = self.build()
        self.assertEqual(code, 0, printed)
        for relative in ("index.html", "getting-started.html", "components/index.html", "components/callout.html",
                         "tasks/index.html", "tasks/draw-attention.html", build_guide.MARKER):
            self.assertTrue((self.out / relative).is_file(), relative)
        self.assertIn("Built", printed)

    def test_every_local_link_resolves(self):
        self.build()
        for page in self.out.rglob("*.html"):
            for target in re.findall(r'(?:href|src)="([^"#]+)', page.read_text(encoding="utf-8")):
                if target.startswith(("http:", "https:", "mailto:")):
                    continue
                self.assertTrue((page.parent / target).resolve().is_file(), f"{page.relative_to(self.out)} -> {target}")

    def test_font_awesome_fonts_and_bootstrap_images_are_copied(self):
        self.build()
        self.assertTrue(any((self.out / "vendor/player/fontawesome-6.6.0/webfonts").glob("fa-solid-900.*")))
        self.assertTrue((self.out / "vendor/player/img/glyphicons-halflings.png").is_file())
        self.assertTrue((self.out / "vendor/player/css/editorstyles.css").is_file())

    def test_errors_stop_the_build_and_write_nothing(self):
        bad = fx.CALLOUT.replace('<div class="cu-callout cu-callout-tip">', '<div class="cu-callout cu-calout-tip">')
        self.guide = fx.write_guide(self.root / "bad", CALLOUT=bad)
        code, printed = self.build()
        self.assertEqual(code, 1)
        self.assertIn("ERROR [check 1]", printed)
        self.assertFalse(self.out.exists())

    def test_record_errors_are_reported(self):
        self.guide = fx.write_guide(self.root / "bad", CALLOUT=fx.CALLOUT.replace('status = "current"', 'status = "draft"'))
        code, printed = self.build()
        self.assertEqual(code, 1)
        self.assertIn("status must be one of", printed)

    def test_check_only_writes_nothing(self):
        code, printed = self.build(check_only=True)
        self.assertEqual(code, 0)
        self.assertIn("Guide checks passed", printed)
        self.assertFalse(self.out.exists())

    def test_rebuild_removes_stale_pages(self):
        self.build()
        stale = self.out / "components" / "old.html"
        stale.write_text("old", encoding="utf-8")
        self.build()
        self.assertFalse(stale.exists())

    def test_a_token_group_without_a_reference_entry_stops_the_build(self):
        copy = self.guide / "reference.toml"
        text = copy.read_text(encoding="utf-8")
        copy.write_text(text[:text.index('[[groups]]\nid = "shadows"')], encoding="utf-8")
        code, printed = self.build()
        self.assertEqual(code, 1)
        self.assertIn("ERROR", printed)
        self.assertIn("no entry for token group(s): shadows", printed)
        self.assertFalse(self.out.exists())

    def test_refuses_to_delete_a_foreign_folder(self):
        self.out.mkdir()
        keep = self.out / "keep.txt"
        keep.write_text("mine", encoding="utf-8")
        code, printed = self.build()
        self.assertEqual(code, 1)
        self.assertIn("refusing to delete", printed)
        self.assertTrue(keep.exists())


    def test_failed_build_does_not_block_the_next(self):
        shutil.rmtree(self.guide / "assets")
        code, printed = self.build()
        self.assertEqual(code, 1)
        self.assertIn("ERROR", printed)
        shutil.copytree(support.GUIDE / "assets", self.guide / "assets")
        code, printed = self.build()
        self.assertEqual(code, 0, printed)

if __name__ == "__main__":
    unittest.main()
