import contextlib
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import support
from html_tree import parse

build_guide = support.load_tool("build-guide")


class GuideContentTest(unittest.TestCase):
    def test_real_guide_passes_its_checks(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = build_guide.build(check_only=True)
        printed = out.getvalue()
        self.assertEqual(code, 0, printed)
        self.assertNotIn("ERROR", printed)
        self.assertIn("WARNING [check 2]", printed)  # coverage warns until phase 3

    def test_check_2_counts_only_what_records_must_still_cover(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            build_guide.build(check_only=True)
        match = re.search(r"(\d+) author-facing classes are not covered yet", out.getvalue())
        self.assertIsNotNone(match, out.getvalue())
        # 355 author-facing classes, 259 shown in the utility tables, so at most 96 are left for records.
        self.assertLessEqual(int(match.group(1)), 96)

    def test_built_reference_pages_list_every_token(self):
        tokens = json.loads((support.THEME / "tokens" / "tokens.json").read_text(encoding="utf-8"))
        expected = {name for group, members in tokens.items() if not group.startswith("$")
                    for name in members if not name.startswith("$")}
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "site"
            with contextlib.redirect_stdout(io.StringIO()) as printed:
                code = build_guide.build(out=out)
            self.assertEqual(code, 0, printed.getvalue())
            shown = set()
            for name in ("colours", "tokens"):
                tree = parse((out / "reference" / f"{name}.html").read_text(encoding="utf-8"))
                shown |= {c.text()[2:] for c in tree.find_all("code") if c.text().startswith("--cu-")}
            utilities = parse((out / "reference" / "utilities.html").read_text(encoding="utf-8"))
        self.assertEqual(shown, expected)
        self.assertIn("mt-4", {c.text()[1:] for c in utilities.find_all("code")})

    def test_build_runs_from_the_repo_root(self):
        result = subprocess.run([sys.executable, str(support.TOOLS / "build-guide.py"), "--check"],
                                cwd=support.REPO, capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Guide checks passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
