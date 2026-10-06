import contextlib
import io
import subprocess
import sys
import unittest

import support

build_guide = support.load_tool("build-guide")


class GuideContentTest(unittest.TestCase):
    def test_real_guide_passes_its_checks(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = build_guide.build(check_only=True)
        printed = out.getvalue()
        self.assertEqual(code, 0, printed)
        self.assertNotIn("ERROR", printed)
        self.assertIn("WARNING [check 2]", printed)  # coverage warns until phase 3

    def test_build_runs_from_the_repo_root(self):
        result = subprocess.run([sys.executable, str(support.TOOLS / "build-guide.py"), "--check"],
                                cwd=support.REPO, capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Guide checks passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
