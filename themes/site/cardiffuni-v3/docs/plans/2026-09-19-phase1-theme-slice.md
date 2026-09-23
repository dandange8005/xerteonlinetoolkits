# cardiffuni-v3 Phase 1 (Theme Slice) Implementation Plan

> **Historical implementation plan.** Phase 1 was implemented on 19–21 September 2026. Unchecked steps below are retained as original instructions, not an outstanding task list. The test round superseded the white-navbar/unchanged-red constraints with an approved charcoal navbar and red-rule sidebar selection. Current status and next work are in [the follow-up checklist](2026-09-21-follow-up.md).

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the `cardiffuni-v3` Xerte theme up to the Cardiff Resource Design System v1.3 far enough to build the first Assessment Menu pages: generated tokens, corrected colour roles, rules, the seven callouts, and a white header, navbar and sidebar.

**Architecture:** The design system's `v1/tokens.css` stays the single source of truth. A generator (`sync-theme.py`, beside `sync-guide.py` in the design system folder) writes its declarations into the theme as `scss/_cu-tokens.scss` at `:root`. The theme's existing semantic custom properties (`--color-*`, `--font-*`) are pointed at those `--cu-*` tokens, so existing components change without being rewritten. New theme CSS (rules, callouts, header, navbar, sidebar) uses `--cu-*` tokens directly. A headless-Chrome check script reads computed styles from a test page that loads CSS in the same order as the Xerte site player.

**Tech Stack:** Dart Sass 1.x via `npx -y sass@1` (no global install), Python 3 standard library, Google Chrome headless (macOS), Xerte Online Toolkits 3.14 Bootstrap site template (Bootstrap 2.3.0, Font Awesome 6.6.0 loaded by the player), Docker Xerte at `http://localhost:8080`.

**Spec:**
- `10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/design-system/cardiffuni-v3 Mapping.md` (vault): tasks T1–T4, T6, T8, T10
- `10 Projects 📋/11 Work Projects/2-lane Assessment/Drafts/Assessment Menu - Xerte Build Plan.md` (vault): Phase 1
- `10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/design-system/DESIGN.md` (vault): spec v1.3

Vault root: `/Users/nanzhang/obsidian-vault`. Design system folder (called `$DS` below): `/Users/nanzhang/obsidian-vault/10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/design-system`. Theme folder (called `$THEME` below): `/Users/nanzhang/Projects/xerteonlinetoolkits/themes/site/cardiffuni-v3`.

**Shell setup (run in every new terminal before a task):**

```bash
export THEME="/Users/nanzhang/Projects/xerteonlinetoolkits/themes/site/cardiffuni-v3"
export DS="/Users/nanzhang/obsidian-vault/10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/design-system"
```

Docker Xerte must be running for Task 8 only (`docker ps` shows `xerteonlinetoolkits-web-1`).

## Global Constraints

- Change nothing outside `$THEME` in the Xerte repo (and nothing in `cardiffuni-v2`). New files for the design system go only in `$DS`.
- Work on branch `feature/cardiffuni-v3-ds-v1.3`, created from `develop`. Never commit to `develop`.
- Tokens are generated from `$DS/v1/tokens.css`, never hand-copied. No raw hex colours in new theme CSS; use `--cu-*` tokens.
- Red usage is Nan's separate decision (`$DS/Red Usage Decisions.md`). **Do not change any existing red use in the theme** (navbar hover/active colour, sidebar active background, feedback tab, back-to-top, form focus borders, alerts, labels, progress bars, utilities). The only colour-role changes in this plan are: focus → black, draft label → black on Yellow, tertiary text → grey-70, and pointing action/hover/error at the tokens (same values as now).
- Header: white, thin brand-red top edge, official red logo top left. No gradient, overlay or shadow.
- Components stay flat: no box-shadow on page content; shadow scale is for overlays only.
- Headings use `'Franklin Gothic Heavy','Franklin Gothic',system-ui,sans-serif`. No web font is loaded.
- Font Awesome: the player already loads 6.6.0. Do not add Font Awesome to the theme.
- Compile the theme with `npx -y sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map`, run from `$THEME`. Commit both `.css` and `.css.map`. (The previous commit was also autoprefixed; the lost prefixes are obsolete, so plain Sass output is accepted.)
- End commit messages with: `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

---

## File map

| File | Responsibility | Task |
| --- | --- | --- |
| `$THEME/tests/check_theme.py` | Runs the fixture in headless Chrome and compares computed styles with expected values, by named group | 1 (grows in 2–7) |
| `$THEME/tests/fixture.html` | Test page: loads Bootstrap, the base `custom.css`, Font Awesome and the theme in player order; holds header, navbar, sidebar, button, rules and callout markup | 1 (grows in 4–7) |
| `$DS/sync-theme.py` | Generator: `v1/tokens.css` → `$THEME/scss/_cu-tokens.scss`, with `--check` | 2 |
| `$DS/test_sync_theme.py` | Tests for the generator | 2 |
| `$THEME/scss/_cu-tokens.scss` | Generated design system tokens at `:root` (never edit) | 2 |
| `$THEME/cardiffuni-v3.scss` | Entry point; loads `_cu-tokens` first | 2 |
| `$THEME/scss/_allvariables.scss` | Theme semantic tokens, pointed at `--cu-*` | 3 |
| `$THEME/scss/_tokens.scss` | Theme primitives, with the duplicated colour and font primitives removed | 3 |
| `$THEME/scss/components/_rules.scss` | `.cu-rule`, `.cu-rule-strong` | 4 |
| `$THEME/scss/components/_callout.scss` | Seven `.cu-callout-*` types, replacing the v2 set | 5 |
| `$THEME/scss/_custom-components.scss` | Forwards the new component files | 4 |
| `$THEME/demos/components.html` | Callout demo updated to the seven types | 5 |
| `$THEME/logo_left.svg` | Official red Cardiff logo; the player uses it as the theme's left header logo | 6 |
| `$THEME/scss/_layouts.scss` | Header, navbar and sidebar | 6, 7 |
| `$THEME/MIGRATION.md`, `$THEME/cardiffuni-v3.info` | Paths and version text | 1, 8 |

---

### Task 1: Branch, housekeeping and the test harness

**Files:**
- Modify: `$THEME/MIGRATION.md` (source paths), `$THEME/cardiffuni-v3.info` (description), `$THEME/cardiffuni-v3.scss:1-4` (entry comment)
- Create: `$THEME/tests/check_theme.py`, `$THEME/tests/fixture.html`
- Commit: this plan file

**Interfaces:**
- Produces: `python3 tests/check_theme.py [group ...]` (run from `$THEME`), exit 0 when all selected checks pass, 1 otherwise. Checks are tuples `(group, name, js_expression, expected)` in the `CHECKS` list. In expressions, three helpers are available:
  - `cs(selector, property)` returns `getComputedStyle(element)[property]`, or `'MISSING'` if no element matches.
  - `v(value, property='color')` resolves a CSS value (e.g. `'var(--color-focus)'`) through a probe element and returns the computed result.
  - `ps(selector, pseudo, property)` reads a pseudo-element's computed style.
- Produces: `fixture.html` containing the placeholder comment `/*@CHECKS@*/`, which the runner replaces with the checks.

- [ ] **Step 1: Create the branch**

```bash
cd /Users/nanzhang/Projects/xerteonlinetoolkits
git status --short          # expect: only the untracked plan file under themes/site/cardiffuni-v3/docs/
git switch -c feature/cardiffuni-v3-ds-v1.3
```

- [ ] **Step 2: Write the test runner**

Create `$THEME/tests/check_theme.py`:

```python
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
```

- [ ] **Step 3: Write the fixture**

Create `$THEME/tests/fixture.html`. Stylesheets load in the player's order (`modules/site/player_html5/rloObject.htm`: Bootstrap, responsive, `custom.css`, Font Awesome), then the theme, which the player inserts last. The markup copies the player's page frame.

```html
<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>cardiffuni-v3 checks</title>
<link rel="stylesheet" href="../../../../modules/site/parent_templates/site/common/css/bootstrap.css">
<link rel="stylesheet" href="../../../../modules/site/parent_templates/site/common/css/bootstrap-responsive.css">
<link rel="stylesheet" href="../../../../modules/site/parent_templates/site/common/css/custom.css">
<link rel="stylesheet" href="../../../../modules/site/parent_templates/site/common/fontawesome-6.6.0/css/all.min.css">
<link rel="stylesheet" href="../cardiffuni-v3.css">
</head>
<body>
<div class="navbar navbar-inverse" id="topnav" role="navigation"><div class="navbar-inner"><div class="container"><div class="nav-collapse collapse">
  <ul class="nav" id="nav"><li class="activePage"><a href="#">Home</a></li><li><a href="#">Exams</a></li></ul>
</div></div></div></div>

<header class="jumbotron logoL" id="overview"><div class="container">
  <div class="logoL"><img class="logo logoL themeLogo" src="../logo_left.svg" alt="Cardiff University / Prifysgol Caerdydd"></div>
  <div class="titles"><h1 id="pageTitle">Assessment Menu</h1><p id="pageSubTitle">Designing meaningful, inclusive and future-focused assessment</p></div>
</div></header>

<div class="container"><div class="row-fluid">
  <div class="span3 bs-docs-sidebar" id="contentTable" role="navigation">
    <ul class="nav nav-list bs-docs-sidenav" id="toc">
      <li class="active"><a href="#">About this category</a></li><li><a href="#">Essay</a></li><li><a href="#">Report</a></li>
    </ul>
  </div>
  <div class="span9" id="mainContent" role="main">
    <p>Reading copy.</p>
    <button class="button button-primary" type="button">Primary</button>
    <!--@MARKUP@-->
  </div>
</div></div>

<pre id="results"></pre>
<script>
/*@CHECKS@*/
function cs(selector, property) {
  var el = document.querySelector(selector);
  return el ? getComputedStyle(el)[property] : 'MISSING';
}
function v(value, property) {
  property = property || 'color';
  var probe = document.createElement('div');
  document.body.appendChild(probe);
  probe.style[property] = value;
  var out = getComputedStyle(probe)[property];
  probe.remove();
  return out;
}
function ps(selector, pseudo, property) {
  var el = document.querySelector(selector);
  return el ? getComputedStyle(el, pseudo)[property] : 'MISSING';
}
window.addEventListener('load', function () {
  var results = {};
  Object.keys(CHECKS).forEach(function (key) {
    try { results[key] = String(new Function('cs', 'v', 'ps', 'return ' + CHECKS[key])(cs, v, ps)); }
    catch (e) { results[key] = 'ERROR: ' + e.message; }
  });
  document.getElementById('results').textContent = JSON.stringify(results);
});
</script>
</body>
</html>
```

(`<!--@MARKUP@-->` marks where later tasks add their test markup. The logo image is missing until Task 6; that doesn't affect earlier checks.)

- [ ] **Step 4: Run the smoke check**

Run: `cd "$THEME" && python3 tests/check_theme.py smoke`
Expected: `PASS  [smoke] theme loaded: body copy is 18px` and `1 passed, 0 failed`. If it says the fixture produced no results, check the Chrome path in `CHROME`.

- [ ] **Step 5: Fix stale paths and version text**

In `$THEME/MIGRATION.md`, the **Sources** table and the vault path line point at a `codex/` folder that no longer exists. Replace the table and the line under it with:

```markdown
| What | Where |
|---|---|
| Specification | `design-system/DESIGN.md` (spec v1.3) in the Cardiff University Design System vault project |
| Tokens and component CSS | `design-system/v1/tokens.css`, `components.css` |
| Implementation and host notes | `design-system/Implementation.md` |
| Visual reference | `design-system/cardiff-resource-design-guide.html` |
| Theme audit and task list | `design-system/cardiffuni-v3 Mapping.md` |
| Phase 1 plan | `docs/plans/2026-09-19-phase1-theme-slice.md` (this repo) |

Vault path: `10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/design-system/`
```

In `MIGRATION.md`'s **Goal** paragraph, change `Cardiff Resource Design System v1.1` to `Cardiff Resource Design System v1.3`.

In `$THEME/cardiffuni-v3.info`, replace the `description:` line with:

```
description: Cardiff University theme v3, aligned with the Cardiff Resource Design System v1.3 (flat, dark Cardiff red primary action, 18px reading copy)
```

In `$THEME/cardiffuni-v3.scss`, change line 3 ` * Aligned with Cardiff Resource Design System v1.1` to ` * Aligned with Cardiff Resource Design System v1.3`, and change the last line's comment to:

```scss
/* v3: no web font - Design System v1.3 uses the Franklin Gothic stack with system fallbacks */
```

- [ ] **Step 6: Compile, re-run the smoke check, commit**

```bash
cd "$THEME"
npx -y sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map
python3 tests/check_theme.py smoke        # expect 1 passed
cd /Users/nanzhang/Projects/xerteonlinetoolkits
git add themes/site/cardiffuni-v3/tests themes/site/cardiffuni-v3/docs themes/site/cardiffuni-v3/MIGRATION.md \
        themes/site/cardiffuni-v3/cardiffuni-v3.info themes/site/cardiffuni-v3/cardiffuni-v3.scss \
        themes/site/cardiffuni-v3/cardiffuni-v3.css themes/site/cardiffuni-v3/cardiffuni-v3.css.map
git commit -m "chore(cardiffuni-v3): add computed-style checks, fix design system paths, target spec v1.3

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: Token generator and generated tokens (T2)

**Files:**
- Create: `$DS/sync-theme.py`, `$DS/test_sync_theme.py`
- Create (generated): `$THEME/scss/_cu-tokens.scss`
- Modify: `$THEME/cardiffuni-v3.scss` (load the tokens first)
- Modify: `$THEME/tests/check_theme.py` (group `tokens`)

**Interfaces:**
- Consumes: `check_theme.py` from Task 1.
- Produces: `python3 "$DS/sync-theme.py" [--check] [--theme PATH]`. It writes `PATH/scss/_cu-tokens.scss` (default `PATH` = `$THEME`). `--check` exits 1 if the file is missing or different. Every `--cu-*` custom property from `v1/tokens.css` is defined at `:root` in the compiled theme (e.g. `--cu-action`, `--cu-focus`, `--cu-callout-tip`, `--cu-space-4`, `--cu-weight-bold`).

- [ ] **Step 1: Write the generator's failing tests**

Create `$DS/test_sync_theme.py`:

```python
"""Tests for sync-theme.py. Run: python3 test_sync_theme.py (from the design-system folder)."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "sync-theme.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class SyncThemeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.theme = Path(self.tmp.name)
        (self.theme / "scss").mkdir()
        self.target = self.theme / "scss" / "_cu-tokens.scss"

    def tearDown(self):
        self.tmp.cleanup()

    def test_check_fails_when_partial_missing(self):
        result = run("--check", "--theme", str(self.theme))
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing", result.stdout)

    def test_write_then_check_passes(self):
        self.assertEqual(run("--theme", str(self.theme)).returncode, 0)
        self.assertEqual(run("--check", "--theme", str(self.theme)).returncode, 0)

    def test_output_is_root_block_with_tokens_and_header(self):
        run("--theme", str(self.theme))
        text = self.target.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("// GENERATED by sync-theme.py"))
        self.assertIn(":root {", text)
        self.assertNotIn(".cu-resource", text)
        self.assertIn("--cu-action:var(--cu-brand-red-dark)", text.replace(" ", ""))

    def test_check_fails_after_manual_edit(self):
        run("--theme", str(self.theme))
        self.target.write_text(self.target.read_text(encoding="utf-8") + "\n/* edited */\n", encoding="utf-8")
        result = run("--check", "--theme", str(self.theme))
        self.assertEqual(result.returncode, 1)
        self.assertIn("differs", result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `cd "$DS" && python3 test_sync_theme.py`
Expected: 4 errors/failures (the script doesn't exist yet: `can't open file ... sync-theme.py`).

- [ ] **Step 3: Write the generator**

Create `$DS/sync-theme.py`:

```python
#!/usr/bin/env python3
"""Generate the cardiffuni-v3 Xerte theme's token partial from the design system.

Reads v1/tokens.css (the single source of truth) and writes <theme>/scss/_cu-tokens.scss
with the same declarations at :root, so the theme and every page inside it share the tokens.

Usage (from any folder):
    python3 sync-theme.py                write the partial
    python3 sync-theme.py --check        report only; exit 1 if the partial is missing or out of date
    python3 sync-theme.py --theme PATH   use another theme folder
Run it after every change to v1/tokens.css, then recompile the theme. Standard library only.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "v1" / "tokens.css"
DEFAULT_THEME = Path("/Users/nanzhang/Projects/xerteonlinetoolkits/themes/site/cardiffuni-v3")
HEADER = (
    "// GENERATED by sync-theme.py from the Cardiff Resource Design System (v1/tokens.css).\n"
    "// Do not edit: change v1/tokens.css in the design system, then run sync-theme.py.\n"
)


def render():
    css = SOURCE.read_text(encoding="utf-8")
    match = re.search(r"\.cu-resource\s*\{(.*)\}", css, re.S)
    if not match:
        sys.exit(f"ERROR: no .cu-resource {{...}} block found in {SOURCE}")
    return HEADER + ":root {\n" + match.group(1).strip("\n") + "\n}\n"


def main():
    args = sys.argv[1:]
    check = "--check" in args
    theme = Path(args[args.index("--theme") + 1]) if "--theme" in args else DEFAULT_THEME
    target = theme / "scss" / "_cu-tokens.scss"
    fresh = render()
    current = target.read_text(encoding="utf-8") if target.exists() else None
    if current == fresh:
        print(f"In sync: {target} matches v1/tokens.css.")
        return 0
    if check:
        state = "is missing" if current is None else "differs from v1/tokens.css"
        print(f"OUT OF SYNC: {target} {state}. Run: python3 sync-theme.py")
        return 1
    target.write_text(fresh, encoding="utf-8")
    print(f"Updated: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the generator tests**

Run: `cd "$DS" && python3 test_sync_theme.py`
Expected: `Ran 4 tests ... OK`

- [ ] **Step 5: Add the failing theme checks**

In `$THEME/tests/check_theme.py`, add to `CHECKS`:

```python
    ("tokens", "--cu-action is dark Cardiff red", "v('var(--cu-action)')", "rgb(194, 31, 22)"),
    ("tokens", "--cu-callout-tip is Cadet", "v('var(--cu-callout-tip)')", "rgb(94, 185, 155)"),
    ("tokens", "--cu-space-6 is 24px", "v('var(--cu-space-6)','paddingTop')", "24px"),
```

Run: `cd "$THEME" && python3 tests/check_theme.py tokens`
Expected: 3 FAIL (the variables are undefined, so the probe falls back to its default value).

- [ ] **Step 6: Generate the partial and load it first**

```bash
python3 "$DS/sync-theme.py"          # expect: Updated: .../scss/_cu-tokens.scss
python3 "$DS/sync-theme.py" --check  # expect: In sync
```

In `$THEME/cardiffuni-v3.scss`, insert as the first `@use` line (before `@use "scss/_allvariables" as *;`):

```scss
@use "scss/cu-tokens"; // Design system tokens (--cu-*), GENERATED by sync-theme.py - do not edit
```

- [ ] **Step 7: Compile and run all checks**

```bash
cd "$THEME" && npx -y sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map
python3 tests/check_theme.py        # expect: smoke and tokens all PASS
grep -c -- "--cu-action:" cardiffuni-v3.css   # expect: 1
```

- [ ] **Step 8: Commit**

```bash
cd /Users/nanzhang/Projects/xerteonlinetoolkits
git add themes/site/cardiffuni-v3/scss/_cu-tokens.scss themes/site/cardiffuni-v3/cardiffuni-v3.scss \
        themes/site/cardiffuni-v3/cardiffuni-v3.css themes/site/cardiffuni-v3/cardiffuni-v3.css.map \
        themes/site/cardiffuni-v3/tests/check_theme.py
git commit -m "feat(cardiffuni-v3): load design system tokens generated by sync-theme.py

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

(`$DS/sync-theme.py` and its test live in the vault, which the vault's auto-backup commits.)

---

### Task 3: Point the theme's colour and font roles at the tokens (T3)

**Files:**
- Modify: `$THEME/scss/_allvariables.scss` (lines 29–78, 85–119 as listed, 230–232)
- Modify: `$THEME/scss/_tokens.scss` (remove duplicated primitives)
- Modify: `$THEME/tests/check_theme.py` (group `roles`)

**Interfaces:**
- Consumes: `--cu-*` tokens at `:root` (Task 2).
- Produces: these theme properties resolve to design system values: `--color-action` #C21F16, `--color-action-hover` #A11A12, `--color-status-error` #A11A12, `--color-focus` #121212, `--color-warning` #121212, `--color-warning-bg` #FFB300, `--color-text-tertiary` #666666, `--color-link-default` #045bc6, `--font-family-display` = the Franklin Gothic stack. Every other `--color-*` keeps its current value.

- [ ] **Step 1: Add the failing checks**

Add to `CHECKS`:

```python
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
```

Run: `cd "$THEME" && python3 tests/check_theme.py roles`
Expected: FAIL for focus, draft text, draft background, tertiary text and heading font (`#pageTitle` currently uses `--font-family-primary`). The rest pass.

(The heading-font check will pass only after Task 6 sets `#pageTitle` to the display font. Leave it failing in this task and note it in the commit message.)

- [ ] **Step 2: Repoint the brand, neutral, action, grey and accent properties**

In `$THEME/scss/_allvariables.scss`, replace the declarations from `--color-brand-primary:` (line 29) through `--color-accent-violet:` (line 78) with these values, keeping the existing section comments between groups:

```scss
    --color-brand-primary: var(--cu-brand-red);
    --color-brand-secondary: var(--cu-black);

    --color-white: var(--cu-white);
    --color-light: var(--cu-bg);

    --color-action: var(--cu-action);
    --color-action-hover: var(--cu-action-hover);
    --color-tint: #{t.$token-color-tint}; // not in the design system; see Red Usage Decisions
    --color-focus: var(--cu-focus);
    --color-warning: var(--cu-draft);
    --color-warning-bg: var(--cu-draft-bg);
    --color-on-dark: var(--cu-on-dark);
    --color-on-dark-muted: var(--cu-on-dark-muted);

    --color-gray-10: var(--cu-grey-10);
    --color-gray-20: var(--cu-grey-20);
    --color-gray-30: var(--cu-grey-30);
    --color-gray-40: var(--cu-grey-40);
    --color-gray-50: var(--cu-grey-50);
    --color-gray-60: var(--cu-grey-60);
    --color-gray-70: var(--cu-grey-70);
    --color-gray-80: var(--cu-grey-80);
    --color-gray-90: var(--cu-grey-90);

    --color-accent-green: var(--cu-accent-forest-green);
    --color-accent-teal: var(--cu-accent-cadet);
    --color-accent-stone: var(--cu-accent-stone);
    --color-accent-blue: var(--cu-accent-light-blue);
    --color-accent-royal: var(--cu-accent-royal-blue);
    --color-accent-navy: var(--cu-accent-midnight-blue);
    --color-accent-purple: var(--cu-accent-midnight-purple);
    --color-accent-orange: var(--cu-accent-orange);
    --color-accent-yellow: var(--cu-accent-yellow);
    --color-accent-lime: var(--cu-accent-yellow-green);
    --color-accent-indigo: var(--cu-accent-indigo);
    --color-accent-violet: var(--cu-accent-dark-violet);
```

Also change the section comment `// ACTION & INTERACTION COLORS (Design System v1.1)` to `(Design System v1.3)`, and replace the line under it (`// Red discipline: brand red is a rare signal; primary actions use --color-action.`) with `// Values come from the design system tokens (--cu-*). Red usage is decided separately.`

- [ ] **Step 3: Repoint text, link, error and font properties**

In the same file, change exactly these lines:

| Line now | Becomes |
| --- | --- |
| `--color-text-tertiary: var(--color-gray-50);` | `--color-text-tertiary: var(--cu-text-tertiary);` |
| `--color-link-default: #{t.$token-color-link};` | `--color-link-default: var(--cu-link);` |
| `--color-status-error: var(--color-action-hover);` | `--color-status-error: var(--cu-error);` |
| `--font-family-primary: #{t.$token-font-family-primary};` | `--font-family-primary: var(--cu-body);` |
| `--font-family-display: #{t.$token-font-family-display};` | `--font-family-display: var(--cu-display);` |
| `--font-family-secondary: #{t.$token-font-family-secondary};` | `--font-family-secondary: var(--cu-serif);` |

Update the file's header comment line `* Aligned with Cardiff Resource Design System v1.1` to `v1.3`.

- [ ] **Step 4: Remove the duplicated primitives**

Run: `grep -n 't\.\$token-color\|t\.\$token-font-family' "$THEME/scss/_allvariables.scss"`
Expected: exactly one line, `--color-tint: #{t.$token-color-tint};`.

In `$THEME/scss/_tokens.scss`:
- In the **BRAND COLORS** section, delete every `$token-color-*` line **except** `$token-color-tint`. Keep that line and change its comment to `// Not in the design system; kept for outline-button hover until Red Usage Decisions`.
- In **TYPOGRAPHY - PRIMITIVES**, delete the three `$token-font-family-*` lines and their comment lines, and add in their place: `// Font families come from the design system tokens (--cu-display, --cu-body, --cu-serif).`
- In the file header, replace `v3 SOURCE: Cardiff Resource Design System v1.1 (codex/DESIGN.md, design-system/v1/tokens.css).` with `Colours and font families come from the design system tokens (scss/_cu-tokens.scss, generated). This file keeps only non-colour primitives used at compile time.`

- [ ] **Step 5: Compile and run the checks**

```bash
cd "$THEME" && npx -y sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map
python3 tests/check_theme.py
```
Expected: every check PASSes except `[roles] heading font is the Franklin Gothic stack` (fixed in Task 6). If Sass reports `Undefined variable`, a file still references a deleted primitive: search with `grep -rn 'token-color\|token-font-family' scss/` and restore that one primitive.

- [ ] **Step 6: Commit**

```bash
cd /Users/nanzhang/Projects/xerteonlinetoolkits
git add themes/site/cardiffuni-v3/scss themes/site/cardiffuni-v3/cardiffuni-v3.css \
        themes/site/cardiffuni-v3/cardiffuni-v3.css.map themes/site/cardiffuni-v3/tests/check_theme.py
git commit -m "feat(cardiffuni-v3): drive colour and font roles from design system tokens

Focus becomes black, draft label black on Yellow, tertiary text grey-70.
Action, hover, error and all red uses keep their current values.
Heading-font check stays failing until the header task.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: Rules (T4)

**Files:**
- Create: `$THEME/scss/components/_rules.scss`
- Modify: `$THEME/scss/_custom-components.scss` (forward it), `$THEME/tests/fixture.html`, `$THEME/tests/check_theme.py` (group `rules`)

**Interfaces:**
- Consumes: `--cu-border`, `--cu-ink`, `--cu-space-8`.
- Produces: `<hr class="cu-rule">` (1px neutral) and `<hr class="cu-rule cu-rule-strong">` (2px charcoal), usable on any page.

- [ ] **Step 1: Add the markup and failing checks**

In `$THEME/tests/fixture.html`, replace `<!--@MARKUP@-->` with:

```html
    <hr class="cu-rule" id="rule">
    <hr class="cu-rule cu-rule-strong" id="rule-strong">
    <!--@MARKUP@-->
```

Add to `CHECKS`:

```python
    ("rules", "rule is 1px", "cs('#rule','borderTopWidth')", "1px"),
    ("rules", "rule is neutral grey-30", "cs('#rule','borderTopColor')", "rgb(204, 204, 204)"),
    ("rules", "strong rule is 2px", "cs('#rule-strong','borderTopWidth')", "2px"),
    ("rules", "strong rule is ink", "cs('#rule-strong','borderTopColor')", "rgb(18, 18, 18)"),
    ("rules", "rule has 32px space above", "cs('#rule','marginTop')", "32px"),
```

Run: `cd "$THEME" && python3 tests/check_theme.py rules`
Expected: FAIL (Bootstrap's default `hr` styling).

- [ ] **Step 2: Write the component**

Create `$THEME/scss/components/_rules.scss`:

```scss
/**
 * Rules (Cardiff Resource Design System v1.3)
 * <hr class="cu-rule">                  1px neutral rule between repeated entries or quiet sections
 * <hr class="cu-rule cu-rule-strong">   2px charcoal rule for a major boundary
 */
.cu-rule {
    height: 0;
    border: 0;
    border-top: 1px solid var(--cu-border);
    margin-block: var(--cu-space-8);
}

.cu-rule-strong {
    border-top: 2px solid var(--cu-ink);
}
```

In `$THEME/scss/_custom-components.scss`, add `@forward "components/rules";` on the line after `@forward "components/callout";`.

- [ ] **Step 3: Compile, run, commit**

```bash
cd "$THEME" && npx -y sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map
python3 tests/check_theme.py rules     # expect 5 passed
python3 tests/check_theme.py           # expect only the heading-font check failing
cd /Users/nanzhang/Projects/xerteonlinetoolkits
git add themes/site/cardiffuni-v3/scss themes/site/cardiffuni-v3/cardiffuni-v3.css \
        themes/site/cardiffuni-v3/cardiffuni-v3.css.map themes/site/cardiffuni-v3/tests
git commit -m "feat(cardiffuni-v3): add design system rules (cu-rule, cu-rule-strong)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: Seven callouts replace the v2 set (T6)

**Files:**
- Modify (replace contents): `$THEME/scss/components/_callout.scss`
- Modify: `$THEME/demos/components.html:394-438` (callout section)
- Modify: `$THEME/tests/fixture.html`, `$THEME/tests/check_theme.py` (group `callouts`)

**Interfaces:**
- Consumes: `--cu-surface`, `--cu-ink`, `--cu-space-*`, `--cu-weight-bold`, `--cu-callout-*` and `--cu-callout-*-on` tokens; Font Awesome 6 `fa-stack` (loaded by the player).
- Produces: `.cu-callout` with modifiers `.cu-callout-info`, `-tip`, `-good`, `-important`, `-warning`, `-example`, `-key` (the default when no modifier is given), plus `.cu-callout-icon` and `.cu-callout-title`. The markup is identical to the design system's, so prototype callouts paste straight into Xerte. The v2 `.callout`, `.info`, `.success`, `.warning`, `.danger` styles are removed (the theme is unpublished; no aliases).

- [ ] **Step 1: Add the markup and failing checks**

In `$THEME/tests/fixture.html`, replace `<!--@MARKUP@-->` with:

```html
    <div class="cu-callout cu-callout-tip" id="callout-tip">
      <span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-lightbulb fa-stack-1x"></i></span>
      <div><strong class="cu-callout-title">Tip</strong><p>Recommendation.</p></div>
    </div>
    <div class="cu-callout" id="callout-key">
      <span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-star fa-stack-1x"></i></span>
      <div><strong class="cu-callout-title">Key point</strong><p>Main takeaway.</p></div>
    </div>
    <div class="cu-callout cu-callout-warning" id="callout-warning"><div><strong class="cu-callout-title">Warning</strong></div></div>
    <div class="cu-callout cu-callout-good" id="callout-good"><div><strong class="cu-callout-title">Good practice</strong></div></div>
    <div class="callout info" id="old-callout"><p>Old v2 callout.</p></div>
    <!--@MARKUP@-->
```

Add to `CHECKS`:

```python
    ("callouts", "grey surface", "cs('#callout-tip','backgroundColor')", "rgb(242, 242, 242)"),
    ("callouts", "4px left rule", "cs('#callout-tip','borderLeftWidth')", "4px"),
    ("callouts", "tip rule is Cadet", "cs('#callout-tip','borderLeftColor')", "rgb(94, 185, 155)"),
    ("callouts", "tip disc is Cadet", "cs('#callout-tip .fa-stack-2x','color')", "rgb(94, 185, 155)"),
    ("callouts", "tip glyph is black", "cs('#callout-tip .fa-stack-1x','color')", "rgb(18, 18, 18)"),
    ("callouts", "no modifier = key point, black rule", "cs('#callout-key','borderLeftColor')", "rgb(18, 18, 18)"),
    ("callouts", "key point glyph is white", "cs('#callout-key .fa-stack-1x','color')", "rgb(255, 255, 255)"),
    ("callouts", "warning rule is brand red", "cs('#callout-warning','borderLeftColor')", "rgb(228, 37, 27)"),
    ("callouts", "good practice rule is Forest Green", "cs('#callout-good','borderLeftColor')", "rgb(7, 135, 62)"),
    ("callouts", "title is bold", "cs('#callout-tip .cu-callout-title','fontWeight')", "700"),
    ("callouts", "icon and text sit in a grid", "cs('#callout-tip','display')", "grid"),
    ("callouts", "square corners", "cs('#callout-tip','borderTopLeftRadius')", "0px"),
    ("callouts", "old v2 callout no longer styled", "cs('#old-callout','borderLeftWidth')", "0px"),
```

Run: `cd "$THEME" && python3 tests/check_theme.py callouts`
Expected: FAIL for every check except possibly `old v2 callout no longer styled` (run it to see the current state; it passes only if v2 used a full border rather than a left rule).

- [ ] **Step 2: Replace the callout component**

Replace the whole of `$THEME/scss/components/_callout.scss` with:

```scss
/**
 * Callouts (Cardiff Resource Design System v1.3, seven types)
 *
 * Paste in a Text element's Source view:
 * <div class="cu-callout cu-callout-tip">
 *   <span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-lightbulb fa-stack-1x"></i></span>
 *   <div><strong class="cu-callout-title">Tip</strong><p>...</p></div>
 * </div>
 *
 * Type (class)                        glyph               use
 * Information   .cu-callout-info       fa-info             extra context
 * Tip           .cu-callout-tip        fa-lightbulb        recommendation
 * Good practice .cu-callout-good       fa-check            preferred approach
 * Important     .cu-callout-important  fa-exclamation      something requiring attention
 * Warning       .cu-callout-warning    fa-minus            risk or problem
 * Example       .cu-callout-example    fa-graduation-cap   worked example
 * Key point     .cu-callout-key or no modifier   fa-star   main takeaway
 *
 * The title carries the meaning; colour and icon support it. One or two per screen.
 * Font Awesome 6.6.0 is loaded by the Xerte player; the theme does not bundle it.
 */
.cu-callout {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    gap: var(--cu-space-4);
    align-items: start;
    margin-top: var(--cu-space-6);
    padding: var(--cu-space-5) var(--cu-space-6);
    background: var(--cu-surface);
    color: var(--cu-ink);
    border-left: 4px solid var(--cu-callout, var(--cu-callout-key));

    p {
        margin-top: var(--cu-space-1);
    }
}

.cu-callout-icon {
    font-size: 14px;
    width: 2em;
    margin-top: -2px;

    .fa-stack-2x {
        color: var(--cu-callout, var(--cu-callout-key));
    }

    .fa-stack-1x {
        color: var(--cu-callout-on, var(--cu-callout-key-on));
    }
}

.cu-callout-title {
    display: block;
    font-weight: var(--cu-weight-bold);
}

.cu-callout-info { --cu-callout: var(--cu-callout-info); --cu-callout-on: var(--cu-callout-info-on); }
.cu-callout-tip { --cu-callout: var(--cu-callout-tip); --cu-callout-on: var(--cu-callout-tip-on); }
.cu-callout-good { --cu-callout: var(--cu-callout-good); --cu-callout-on: var(--cu-callout-good-on); }
.cu-callout-important { --cu-callout: var(--cu-callout-important); --cu-callout-on: var(--cu-callout-important-on); }
.cu-callout-warning { --cu-callout: var(--cu-callout-warning); --cu-callout-on: var(--cu-callout-warning-on); }
.cu-callout-example { --cu-callout: var(--cu-callout-example); --cu-callout-on: var(--cu-callout-example-on); }
.cu-callout-key { --cu-callout: var(--cu-callout-key); --cu-callout-on: var(--cu-callout-key-on); }

@media (max-width: 480px) {
    .cu-callout {
        padding: var(--cu-space-4);
    }
}
```

- [ ] **Step 3: Compile and run the checks**

```bash
cd "$THEME" && npx -y sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map
python3 tests/check_theme.py callouts   # expect 13 passed
```

If `old v2 callout no longer styled` fails, another file still styles `.callout`: `grep -rn '\.callout\b' scss/` and remove only the v2 callout rules.

- [ ] **Step 4: Update the demo page**

In `$THEME/demos/components.html`, replace lines 397–437 (both `demo-block` divs inside `<section class="demo-section" id="callouts">`) with:

```html
            <div class="demo-block">
                <div class="demo-block__title">Seven callout types (design system v1.3)</div>

                <div class="cu-callout cu-callout-info"><span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-info fa-stack-1x"></i></span><div><strong class="cu-callout-title">Information</strong><p>Extra context.</p></div></div>
                <div class="cu-callout cu-callout-tip"><span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-lightbulb fa-stack-1x"></i></span><div><strong class="cu-callout-title">Tip</strong><p>A recommendation.</p></div></div>
                <div class="cu-callout cu-callout-good"><span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-check fa-stack-1x"></i></span><div><strong class="cu-callout-title">Good practice</strong><p>The preferred approach.</p></div></div>
                <div class="cu-callout cu-callout-important"><span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-exclamation fa-stack-1x"></i></span><div><strong class="cu-callout-title">Important</strong><p>Something requiring attention.</p></div></div>
                <div class="cu-callout cu-callout-warning"><span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-minus fa-stack-1x"></i></span><div><strong class="cu-callout-title">Warning</strong><p>A risk or problem.</p></div></div>
                <div class="cu-callout cu-callout-example"><span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-graduation-cap fa-stack-1x"></i></span><div><strong class="cu-callout-title">Example</strong><p>A worked example.</p></div></div>
                <div class="cu-callout"><span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-star fa-stack-1x"></i></span><div><strong class="cu-callout-title">Key point</strong><p>The main takeaway (default when no type class is given).</p></div></div>

                <code class="code-label">.cu-callout | -info | -tip | -good | -important | -warning | -example | -key (default)</code>
            </div>
```

Open `$THEME/demos/components.html#callouts` in a browser and check that the seven callouts show a coloured disc with a glyph, a 4px coloured left rule and a grey panel.

- [ ] **Step 5: Commit**

```bash
cd /Users/nanzhang/Projects/xerteonlinetoolkits
git add themes/site/cardiffuni-v3/scss themes/site/cardiffuni-v3/demos/components.html themes/site/cardiffuni-v3/cardiffuni-v3.css \
        themes/site/cardiffuni-v3/cardiffuni-v3.css.map themes/site/cardiffuni-v3/tests
git commit -m "feat(cardiffuni-v3): replace v2 callouts with the seven design system callouts

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: White header with red top edge and red logo (T8, header)

**Files:**
- Create: `$THEME/logo_left.svg` (copy of the official file)
- Modify: `$THEME/scss/_layouts.scss:16-80` (header block: `.jumbotron` through `#pageSubTitle`)
- Modify: `$THEME/tests/check_theme.py` (group `header`)

**Interfaces:**
- Consumes: `--cu-bg`, `--cu-red`, `--cu-border`, `--cu-ink`, `--cu-muted`, `--cu-display`, `--cu-weight-section`, `--cu-tracking-heading`, `--cu-leading-heading`, `--cu-logo-width`, `--cu-space-*`.
- Produces: the Xerte player shows `logo_left.svg` top left in every project using the theme, unless the author sets their own logo (`modules/site/play.php`, `get_logo_path`).

- [ ] **Step 1: Add the failing checks**

Add to `CHECKS`:

```python
    ("header", "white background", "cs('#overview','backgroundColor')", "rgb(255, 255, 255)"),
    ("header", "no gradient", "cs('#overview','backgroundImage')", "none"),
    ("header", "no overlay", "ps('#overview','::before','content')", "none"),
    ("header", "red top edge is 4px", "cs('#overview','borderTopWidth')", "4px"),
    ("header", "red top edge is brand red", "cs('#overview','borderTopColor')", "rgb(228, 37, 27)"),
    ("header", "1px rule below", "cs('#overview','borderBottomColor')", "rgb(204, 204, 204)"),
    ("header", "no shadow", "cs('#overview','boxShadow')", "none"),
    ("header", "title is ink", "cs('#pageTitle','color')", "rgb(18, 18, 18)"),
    ("header", "subtitle is muted", "cs('#pageSubTitle','color')", "rgb(102, 102, 102)"),
    ("header", "logo file present and loaded", "String(document.querySelector('.logo.logoL').naturalWidth > 0)", "true"),
    ("header", "logo at least 60px wide", "String(parseFloat(cs('.logo.logoL','width')) >= 60)", "true"),
```

Run: `cd "$THEME" && python3 tests/check_theme.py header roles`
Expected: header checks FAIL (charcoal gradient, overlay, no logo file); `[roles] heading font` still FAILs.

- [ ] **Step 2: Add the official red logo**

```bash
cp "/Users/nanzhang/obsidian-vault/10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/Assets/CU_LogoFiles_MS/CU_LogoFiles/RGB_Screen use/SVG/Cardiff-Logo-Red.svg" \
   "$THEME/logo_left.svg"
```

Don't edit the SVG (brand rule: never redraw or recolour the logo).

- [ ] **Step 3: Replace the header styles**

In `$THEME/scss/_layouts.scss`, replace everything from `.jumbotron {` (line 16) through the end of the `#pageSubTitle { ... }` block (line 80) with:

```scss
// White header: thin brand-red top edge, official red logo top left, no gradient, overlay or shadow.
.jumbotron {
  background: var(--cu-bg);
  background-image: none;
  color: var(--cu-ink);
  border-top: 4px solid var(--cu-red);
  border-bottom: 1px solid var(--cu-border);
  box-shadow: none;
  padding: var(--cu-space-8) 0;
  text-shadow: none;

  &::before {
    content: none;
  }
}

// Logo container
#overview.logoL .logoL {
  margin-top: 0;
}

// Logo: brand minimums 60px at 375px, 70px at 414px, 80px from 480px (--cu-logo-width). Never shrink in the flex row.
.logo.logoL.themeLogo {
  width: var(--cu-logo-width);
  max-width: none;
  height: auto;
  flex: none;
}

// Logo and titles in one row
#overview.logoL .container {
  display: flex;
  align-items: center;
  gap: var(--cu-space-6);
}

.titles {
  padding: 0;
}

#pageTitle {
  font-family: var(--cu-display);
  font-weight: var(--cu-weight-section);
  letter-spacing: var(--cu-tracking-heading);
  line-height: var(--cu-leading-heading);
  color: var(--cu-ink);
  font-size: var(--font-size-3xl);
  margin: 0 0 var(--cu-space-2);
}

#pageSubTitle {
  font-weight: var(--cu-weight-regular);
  color: var(--cu-muted);
  font-size: var(--font-size-lg);
  line-height: var(--cu-leading-lead);
  padding-top: 0;
  margin-bottom: 0;
}
```

- [ ] **Step 4: Compile and run the checks**

```bash
cd "$THEME" && npx -y sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map
python3 tests/check_theme.py header roles    # expect all PASS, including the heading-font check
python3 tests/check_theme.py                 # expect all PASS
```

If `title is ink` fails, the base `custom.css` sets a more specific colour: inspect `#overview h1` rules in `modules/site/parent_templates/site/common/css/custom.css` and raise the theme selector to `#overview #pageTitle` (don't use `!important`).

- [ ] **Step 5: Commit**

```bash
cd /Users/nanzhang/Projects/xerteonlinetoolkits
git add themes/site/cardiffuni-v3/logo_left.svg themes/site/cardiffuni-v3/scss themes/site/cardiffuni-v3/cardiffuni-v3.css \
        themes/site/cardiffuni-v3/cardiffuni-v3.css.map themes/site/cardiffuni-v3/tests
git commit -m "feat(cardiffuni-v3): white header with brand-red top edge and official red logo

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 7: Navbar and sidebar (T8, navbar and sidebar)

**Files:**
- Modify: `$THEME/scss/_layouts.scss` (the `.navbar` and `.navbar-inverse .navbar-inner` blocks; the `.bs-docs-sidenav` block)
- Modify: `$THEME/tests/check_theme.py` (group `frame`)

**Interfaces:**
- Consumes: `--cu-bg`, `--cu-border`, `--cu-line`, `--cu-ink`.
- Produces: a flat white navbar with a 1px rule below; a square sidebar with 1px rules between items and no shadow. **Hover, active and selected colours are unchanged** (they are red uses awaiting Red Usage Decisions).

- [ ] **Step 1: Add the failing checks**

Add to `CHECKS`:

```python
    ("frame", "navbar has no shadow", "cs('#topnav','boxShadow')", "none"),
    ("frame", "navbar is white", "cs('#topnav .navbar-inner','backgroundColor')", "rgb(255, 255, 255)"),
    ("frame", "navbar has a 1px rule below", "cs('#topnav .navbar-inner','borderBottomWidth')", "1px"),
    ("frame", "navbar rule is grey-30", "cs('#topnav .navbar-inner','borderBottomColor')", "rgb(204, 204, 204)"),
    ("frame", "navbar links are ink", "cs('#nav li:not(.activePage) a','color')", "rgb(18, 18, 18)"),
    ("frame", "sidebar is square", "cs('#toc','borderTopLeftRadius')", "0px"),
    ("frame", "sidebar has no shadow", "cs('#toc','boxShadow')", "none"),
    ("frame", "first sidebar item is square", "cs('#toc > li:first-child > a','borderTopLeftRadius')", "0px"),
    ("frame", "sidebar items have a 1px rule below", "cs('#toc > li:nth-child(2) > a','borderBottomWidth')", "1px"),
    ("frame", "sidebar item rule is grey-20", "cs('#toc > li:nth-child(2) > a','borderBottomColor')", "rgb(229, 229, 229)"),
    ("frame", "sidebar items have no side borders", "cs('#toc > li:nth-child(2) > a','borderLeftWidth')", "0px"),
    ("frame", "active sidebar item keeps its current (red) background", "cs('#toc > li.active > a','backgroundColor')", "rgb(228, 37, 27)"),
```

Run: `cd "$THEME" && python3 tests/check_theme.py frame`
Expected: most checks FAIL. `navbar has no shadow` may already pass (v3's `--shadow-sm` is already `none`), and `active sidebar item keeps its current (red) background` passes; both must still pass after the change.

- [ ] **Step 2: Replace the navbar blocks**

In `$THEME/scss/_layouts.scss`, replace the `.navbar { ... }` block and the `.navbar-inverse .navbar-inner { ... }` block with:

```scss
.navbar {
  box-shadow: none;
  margin-bottom: 0;
}

.navbar-inverse .navbar-inner {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  background: var(--cu-bg);
  background-image: none;
  border: 0;
  border-bottom: 1px solid var(--cu-border);
  box-shadow: none;
}
```

In the block beginning `.navbar-inverse .nav-collapse .nav>li>a,` (the default link colour), change `color: var(--color-gray-80);` to `color: var(--cu-ink);`. Leave the hover and `.activePage` blocks unchanged.

- [ ] **Step 3: Replace the sidebar block**

Replace the `.bs-docs-sidenav { ... }` block (from `// Table of Contents (Sidebar)` to the end of that block) with:

```scss
// Table of Contents (Sidebar): square, flat, 1px rules between items.
// Overrides the base template's 6px radius and shadow (modules/site/parent_templates/site/common/css/custom.css).
// Active and hover colours are unchanged here; they follow Red Usage Decisions.
.bs-docs-sidenav {
  background-color: var(--cu-bg);
  border-radius: 0;
  box-shadow: none;
  border-top: 1px solid var(--cu-line);

  >li>a {
    color: var(--color-text-primary);
    margin: 0;
    border: 0;
    border-bottom: 1px solid var(--cu-line);
  }

  >li:first-child>a,
  >li:last-child>a {
    border-radius: 0;
  }

  >.active>a {
    text-shadow: none;
    box-shadow: none;
  }

  >li>a:hover {
    background-color: var(--color-bg-subtle);
  }

  a:hover .icon-chevron-right {
    opacity: 0.5;
  }

  .active .icon-chevron-right,
  .active a:hover .icon-chevron-right {
    opacity: 1;
  }
}
```

- [ ] **Step 4: Compile and run all checks**

```bash
cd "$THEME" && npx -y sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map
python3 tests/check_theme.py          # expect all groups PASS
python3 "$DS/sync-theme.py" --check   # expect: In sync
```

If a sidebar check fails because `custom.css` wins, compare selector specificity with the base rule quoted in the comment above and match it (e.g. `.nav-list.bs-docs-sidenav`), without `!important`.

- [ ] **Step 5: Commit**

```bash
cd /Users/nanzhang/Projects/xerteonlinetoolkits
git add themes/site/cardiffuni-v3/scss themes/site/cardiffuni-v3/cardiffuni-v3.css \
        themes/site/cardiffuni-v3/cardiffuni-v3.css.map themes/site/cardiffuni-v3/tests
git commit -m "feat(cardiffuni-v3): flat white navbar and square ruled sidebar

Hover, active and selected colours unchanged pending Red Usage Decisions.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 8: First test round in Docker Xerte, and records (T10)

This task is a manual test in the real editor and player, then a record of results. The theme files are read straight from the repo folder by the Docker container, so a recompiled `cardiffuni-v3.css` is live after a hard refresh (Cmd+Shift+R).

**Files:**
- Create: `$THEME/docs/test-rounds/2026-09-phase1.md`
- Modify: `$THEME/MIGRATION.md` (status table), vault `design-system/cardiffuni-v3 Mapping.md` (task status), vault `2-lane Assessment/Drafts/Assessment Menu - Xerte Build Plan.md` (Phase 1 status)

- [ ] **Step 1: Build a test page in the local project**

In the local Assessment Menu project on `http://localhost:8080` (theme `Cardiff University v3`), add a page `Theme test` (Page ID `theme-test`) with one section containing a **Text** element. In the Text element's **Source** view, paste:

```html
<p>Reading copy at 18px. A <a href="#">text link</a>.</p>
<hr class="cu-rule">
<div class="flex flex-wrap gap-lg">
  <div class="flex-300 am-lane-1"><h4>Lane 1: how to make it secure assurance of learning</h4><p>Lane 1 text.</p></div>
  <div class="flex-300 am-lane-2"><h4>Lane 2: how to make it open assessment for and as learning</h4><p>Lane 2 text.</p></div>
</div>
<hr class="cu-rule cu-rule-strong">
<div class="cu-callout cu-callout-tip"><span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-lightbulb fa-stack-1x"></i></span><div><strong class="cu-callout-title">Tip</strong><p>Callout inside the Xerte editor.</p></div></div>
<div class="cu-callout cu-callout-warning"><span class="fa-stack cu-callout-icon" aria-hidden="true"><i class="fa-solid fa-circle fa-stack-2x"></i><i class="fa-solid fa-minus fa-stack-1x"></i></span><div><strong class="cu-callout-title">Warning</strong><p>Second callout.</p></div></div>
<p><a class="button button-primary" href="#">Primary button</a></p>
```

Untick **Show Title** on the element. Save.

- [ ] **Step 2: Run the checks and record each result**

Create `$THEME/docs/test-rounds/2026-09-phase1.md` with this table, filling in *Result* (Pass / Fail + what you saw) as you go:

```markdown
# cardiffuni-v3 Phase 1 test round (Docker Xerte, local)

Date: · Xerte: local Docker (localhost:8080) · Browser:

| # | Check | How | Result |
| --- | --- | --- | --- |
| 1 | Header | Preview the project: white header, 4px red top edge, red logo top left, title in ink, no gradient or shadow | |
| 2 | Logo accessible name | Project properties: set the left logo alt text to `Cardiff University / Prifysgol Caerdydd`; inspect the `img.logoL` alt | |
| 3 | Navbar | White bar, 1px grey rule below, no shadow; hover/active colours unchanged | |
| 4 | Sidebar | On a category page: square, 1px rules, no shadow | |
| 5 | Editor keeps markup | Close the editor, reopen, open the Text element's Source view: `flex`, `flex-300`, `cu-rule`, `cu-callout`, `fa-stack` classes all still there | |
| 6 | Callouts render | Disc + glyph visible, 4px coloured rule, grey panel | |
| 7 | Lane columns | Side by side at desktop width; stacked in the browser's device toolbar at 375px | |
| 8 | Keyboard | Tab through the page: every link/button reachable, focus ring visible and black | |
| 9 | 200% zoom | Browser zoom 200%: no horizontal scrolling, nothing clipped | |
| 10 | Narrow widths | Device toolbar at 320, 375 and 414px: header logo ≥ 60px, no overflow | |
| 11 | Welsh glyphs | Add `ŵ ŷ` to the page title temporarily: headings render them in the same font as the surrounding text | |
| 12 | Mac heading font | On this Mac, headings fall back to the system font. Acceptable? (design system v1.3 accepted this; confirm it looks right) | |
| 13 | Standalone export | Editor: export/publish the project as a standalone package (zip). Unzip and open `index.htm` locally: theme, logo and callouts appear | |
| 14 | Export → import | Export the project, import it as a new project on the same local server: pages, Styles, Script and theme setting survive | |
```

- [ ] **Step 3: Fix what fails, if it's in scope**

- Failures in checks 1, 3, 4, 6, 7 or 10 are theme bugs. Add a failing check to `tests/check_theme.py` that reproduces it, fix the SCSS, recompile, and commit as in earlier tasks.
- Failures in 5 (editor strips markup), 13 or 14 are **not** fixed in this plan. Record them. They decide Phase 2 fallbacks (tabs instead of flex columns; another review route) and go back to Nan.

- [ ] **Step 4: Update the records**

In `$THEME/MIGRATION.md`, **Status** table: set step 1 to `**Done** (tokens generated from the design system, 19 September)`, and step 2 to `**Partly done**: header, navbar, sidebar (Phase 1); footer, feedback tab and back-to-top remain`. Step 3: `**Partly done**: rules and seven callouts; other components remain (mapping T7, T9)`. Step 4: `**Round 1 done**: see docs/test-rounds/2026-09-phase1.md`.

In the vault note `design-system/cardiffuni-v3 Mapping.md`, section 5, add a **Status** column to the task table: T1–T4 and T6 `Done (Phase 1)`, T8 `Header, navbar, sidebar done; rest open`, T10 `Round 1 done`; others unchanged.

In the vault note `2-lane Assessment/Drafts/Assessment Menu - Xerte Build Plan.md`, under **Phase 1**, add a line: `*Status:* done on <date>; test round results in the theme repo at docs/test-rounds/2026-09-phase1.md.` and list any open failures from checks 5, 13 and 14.

- [ ] **Step 5: Commit**

```bash
cd /Users/nanzhang/Projects/xerteonlinetoolkits
git add themes/site/cardiffuni-v3/docs themes/site/cardiffuni-v3/MIGRATION.md
git commit -m "docs(cardiffuni-v3): record Phase 1 test round and migration status

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

Don't merge the branch into `develop`; Nan decides that after reviewing the test round.
