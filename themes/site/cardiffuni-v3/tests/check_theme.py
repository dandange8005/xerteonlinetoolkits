#!/usr/bin/env python3
"""Computed-style checks for the cardiffuni-v3 theme (headless Chrome, standard library only).

Usage (from the theme folder):
    python3 tests/check_theme.py              run every group
    python3 tests/check_theme.py tokens roles run the named groups only
Exit code 1 if any selected check fails.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixture.html"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# (group, name, JavaScript expression evaluated in the fixture, expected string)
CHECKS = [
    ("smoke", "theme loaded: body copy is 18px", "cs('body','fontSize')", "18px"),
    ("tokens", "--cu-action is dark Cardiff red", "v('var(--cu-action)')", "rgb(194, 31, 22)"),
    ("tokens", "--cu-callout-tip is Cadet", "v('var(--cu-callout-tip)')", "rgb(94, 185, 155)"),
    ("tokens", "--cu-space-6 is 24px", "v('var(--cu-space-6)','paddingTop')", "24px"),
    ("roles", "action unchanged: #C21F16", "v('var(--color-action)')", "rgb(194, 31, 22)"),
    ("roles", "action hover unchanged: #A11A12", "v('var(--color-action-hover)')", "rgb(161, 26, 18)"),
    ("roles", "error is #A11A12", "v('var(--color-status-error)')", "rgb(161, 26, 18)"),
    ("roles", "focus is black", "v('var(--color-focus)')", "rgb(18, 18, 18)"),
    ("roles", "draft label text is black", "v('var(--color-warning)')", "rgb(18, 18, 18)"),
    ("roles", "draft label background is Yellow", "v('var(--color-warning-bg)','backgroundColor')", "rgb(255, 179, 0)"),
    ("roles", "tertiary text is grey-70", "v('var(--color-text-tertiary)')", "rgb(102, 102, 102)"),
    ("roles", "link blue unchanged", "v('var(--color-link-default)')", "rgb(4, 91, 198)"),
    ("roles", "brand red unchanged", "v('var(--color-brand-primary)')", "rgb(228, 37, 27)"),
    ("roles", "heading font is the Franklin Gothic stack", "cs('#pageTitle','fontFamily').split(',')[0].trim()", '"Franklin Gothic Heavy"'),
    ("roles", "primary button still dark red", "cs('.button.button-primary','backgroundColor')", "rgb(194, 31, 22)"),
    ("rules", "rule is 1px", "cs('#rule','borderTopWidth')", "1px"),
    ("rules", "rule is neutral grey-30", "cs('#rule','borderTopColor')", "rgb(204, 204, 204)"),
    ("rules", "strong rule is 2px", "cs('#rule-strong','borderTopWidth')", "2px"),
    ("rules", "strong rule is ink", "cs('#rule-strong','borderTopColor')", "rgb(18, 18, 18)"),
    ("rules", "rule has 32px space above", "cs('#rule','marginTop')", "32px"),
]


def evaluate(checks):
    exprs = {f"{g}::{n}": js for g, n, js, _ in checks}
    page = FIXTURE.read_text(encoding="utf-8").replace("/*@CHECKS@*/", "const CHECKS = " + json.dumps(exprs) + ";")
    run_file = HERE / ".fixture-run.html"
    run_file.write_text(page, encoding="utf-8")
    try:
        out = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
             "--virtual-time-budget=3000", "--window-size=1280,900", "--dump-dom", run_file.as_uri()],
            capture_output=True, text=True, timeout=90,
        ).stdout
    finally:
        run_file.unlink(missing_ok=True)
    match = re.search(r'<pre id="results">(.*?)</pre>', out, re.S)
    if not match:
        sys.exit("ERROR: the fixture produced no results. Check the Chrome path and the fixture's script.")
    return json.loads(html.unescape(match.group(1)))


def main():
    groups = set(sys.argv[1:])
    selected = [c for c in CHECKS if not groups or c[0] in groups]
    if not selected:
        sys.exit(f"ERROR: no checks in groups {sorted(groups)}. Known: {sorted({c[0] for c in CHECKS})}")
    results = evaluate(selected)
    failed = 0
    for group, name, _, expected in selected:
        actual = results.get(f"{group}::{name}", "NO RESULT")
        ok = actual == expected
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  [{group}] {name}" + ("" if ok else f"\n      expected {expected!r}, got {actual!r}"))
    print(f"\n{len(selected) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
