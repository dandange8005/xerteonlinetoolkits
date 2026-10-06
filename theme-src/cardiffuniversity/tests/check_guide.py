#!/usr/bin/env python3
"""Browser checks for the built author guide (headless Chrome, standard library only).

Builds the guide into a temporary folder, opens pages at desktop and phone widths, and checks
that the theme styles the examples, nothing scrolls sideways, the guide navigation keeps its
layout under the theme's global rules, and the phone menu opens.

Usage (from the theme folder):
    python3 tests/check_guide.py
Set CHROME to another Chrome binary when needed. Exit code 1 if any check fails.
"""
import contextlib
import html
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import support

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
build_guide = support.load_tool("build-guide")

NO_SIDEWAYS_SCROLL = "document.documentElement.scrollWidth <= window.innerWidth"
CHECKS = [
    # (page, window width, check name, JavaScript expression that must be true)
    ("components/callout.html", 1280, "the theme styles the example callout",
     "getComputedStyle(document.querySelector('.g-preview .cu-callout')).borderLeftWidth === '4px'"),
    ("components/callout.html", 1280, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/callout.html", 1280, "the side menu sits left of the page",
     "document.querySelector('.g-side').getBoundingClientRect().right <= document.querySelector('.g-main').getBoundingClientRect().left + 1"),
    ("components/callout.html", 1280, "the top menu stays on one row",
     "new Set([].map.call(document.querySelectorAll('.g-top a'), function (a) { return a.offsetTop; })).size === 1"),
    ("components/callout.html", 1280, "the phone menu button is hidden on desktop",
     "document.querySelector('.g-side-toggle').hidden === true"),
    ("components/callout.html", 1280, "the on-this-page list is shown",
     "getComputedStyle(document.querySelector('.g-toc')).display !== 'none'"),
    ("components/callout.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/callout.html", 485, "the phone menu starts closed",
     "!document.querySelector('.g-side-toggle').hidden && document.querySelector('.g-side-list').hidden"),
    ("components/callout.html", 485, "the phone menu opens",
     "(document.querySelector('.g-side-toggle').click(), !document.querySelector('.g-side-list').hidden"
     " && document.querySelector('.g-side-toggle').getAttribute('aria-expanded') === 'true')"),
    ("index.html", 1280, "task tiles show their Font Awesome icon",
     "getComputedStyle(document.querySelector('.g-task i'), '::before').content !== 'none'"),
    ("index.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("getting-started.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("tasks/draw-attention.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
]

RUNNER = """<pre id="g-results" hidden></pre>
<script>
var CHECKS = %s;
window.addEventListener('load', function () {
  var out = {};
  Object.keys(CHECKS).forEach(function (name) {
    try { out[name] = String(eval(CHECKS[name])); } catch (e) { out[name] = 'ERROR ' + e.message; }
  });
  document.getElementById('g-results').textContent = JSON.stringify(out);
});
</script>
"""


def run(site, page, width, checks):
    target = site / page
    run_file = target.with_name(".check-run.html")
    page_html = target.read_text(encoding="utf-8")
    run_file.write_text(page_html.replace("</body>", RUNNER % json.dumps(checks) + "</body>"), encoding="utf-8")
    flags = ["--headless=new", "--disable-gpu", "--allow-file-access-from-files", "--virtual-time-budget=5000",
             f"--window-size={width},900", "--dump-dom"]
    if os.environ.get("CI"):
        flags.append("--no-sandbox")
    try:
        out = subprocess.run([CHROME, *flags, run_file.as_uri()], capture_output=True, text=True, timeout=90).stdout
    finally:
        run_file.unlink(missing_ok=True)
    match = re.search(r'<pre id="g-results"[^>]*>(.*?)</pre>', out, re.S)
    if not match or not match.group(1).strip():
        sys.exit(f"ERROR: {page} produced no results. Check the Chrome path ({CHROME}).")
    return json.loads(html.unescape(match.group(1)))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        site = Path(tmp) / "site"
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            code = build_guide.build(out=site)
        if code != 0:
            sys.exit("ERROR: the guide did not build:\n" + printed.getvalue())
        groups = {}
        for page, width, name, expression in CHECKS:
            groups.setdefault((page, width), {})[name] = expression
        failed = 0
        for (page, width), checks in groups.items():
            results = run(site, page, width, checks)
            for name in checks:
                actual = results.get(name, "NO RESULT")
                ok = actual == "true"
                failed += not ok
                print(f"{'PASS' if ok else 'FAIL'}  [{page} @ {width}px] {name}" + ("" if ok else f"\n      got {actual!r}"))
        print(f"\n{len(CHECKS) - failed} passed, {failed} failed")
        return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
