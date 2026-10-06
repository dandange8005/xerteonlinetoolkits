# Author Guide Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Testing reference:** use `mattpocock-skills:tdd`, not `superpowers:test-driven-development`. Test only at the seams listed under [Seams under test](#seams-under-test). The plan already contains code that has been run against its tests, so do not delete it and rewrite it from scratch; follow each task's red, then green, steps.

**Goal:** Build phase 1 of the author guide: a standard-library Python generator that reads component records, task files and pages, runs the five build checks, and writes a static site with a home page, Getting started, one task page and one component page (callouts).

**Architecture:** `tools/theme_css.py` holds what the theme and the player's stylesheets define, shared with `build-reference.py`. A small package `tools/guidelib/` loads records (TOML front-matter through `tomllib`, a strict Markdown subset), runs the checks, renders pages with `string.Template`, and copies the player's CSS and JS. `tools/build-guide.py` is the command line entry point; `./build.sh guide` runs it after the theme build. A GitHub Actions workflow runs the build, the unit tests and a headless Chrome check on pull requests. Nothing is published.

**Tech Stack:** Python 3.11+ standard library only (`tomllib`, `html.parser`, `string.Template`, `unittest`), headless Google Chrome for the browser check, GitHub Actions. Sass 1.104.1 through `npx`, as today.

**Spec:** `theme-src/cardiffuniversity/docs/design-notes/2026-10-06-author-guide.md`. Glossary: `theme-src/cardiffuniversity/CONTEXT.md`. ADR: `theme-src/cardiffuniversity/docs/adr/0001-component-records-live-in-the-theme.md`.

## Global Constraints

- Python 3.11 or later (`tomllib`). Standard library only: no `pip install`, no third-party packages.
- Run every command from `theme-src/cardiffuniversity/` unless a step says otherwise.
- Do not edit the runtime folder `themes/site/cardiffuniversity/` by hand. Only `build.sh` writes its CSS.
- Do not change the theme's SCSS or tokens. Out of scope for the whole guide.
- The guide navigation uses only `g-` prefixed classes, never Bootstrap class names (`.nav`, `.navbar`, `.row`, `.span*`, `.btn`).
- No Cardiff logo on guide pages until the licence open item is settled.
- No deploy or GitHub Pages job. "Until the open items below are settled, nothing is published."
- All guide text in UK English, without em dashes, using the `CONTEXT.md` terms: content author, component, variant, part, example, text content item, page frame, guide navigation, guide page. Never "snippet", "type" (for variants), "Text element", "user", "chrome".
- `build-reference.py` output must not change: `python3 tools/build-reference.py --check` keeps printing `In sync`.
- Work on a new branch `feat/author-guide-phase-1` created from `docs/author-guide-spec`. Commit after every task. End every commit message with the `Co-Authored-By` line from the session's attribution instructions.
- Unit tests run with `python3 -m unittest discover -s tests -p "test_*.py"`.

## Review Focus

1. **A record saved with Windows line endings (`\r\n`)** should load exactly like one saved with `\n`. Test in Task 3: `test_crlf_record_loads`.
2. **Example HTML containing entities or code-like text** (`&amp;`, `</code>`) should render as markup in the preview and show its source literally in the code view. Test in Task 5: `test_code_view_shows_source_literally`.
3. **Running the build from another folder** (the repo root, CI) should behave the same as from the theme folder. Test in Task 7: `test_build_runs_from_the_repo_root`.
4. **An output folder holding stale pages or someone else's files**: stale guide pages disappear on rebuild, and a folder the tool did not make is never deleted. Tests in Task 6: `test_rebuild_removes_stale_pages`, `test_refuses_to_delete_a_foreign_folder`.
5. **No usable git history** (an exported copy, a file never committed, git missing): check 4 stays silent and never crashes. Tests in Task 4: `test_stale_evidence_ignores_unknown_dates`, `test_git_last_changed_outside_a_repo`.

## Seams under test

Agreed with Nan on 6 October 2026. Tests are written only at these public boundaries, and check
behaviour a content author or maintainer would notice, never internal helpers or exact markup.

| Seam | What the tests observe | Test file |
| --- | --- | --- |
| `theme_css`: `author_facing_classes()`, `stack_classes()`, `utility_groups()`, `PLAYER_CSS` | Which classes count as the theme's, as author-facing, and as known to the guide | `test_theme_css.py` |
| `mdsubset.sections()` | The HTML and section list a Markdown body produces, and the errors for anything outside the subset | `test_mdsubset.py` |
| `records.load_component()`, `load_task()`, `load_page()`, `load_site()`, `load_content()` | What a record file loads as, and the error a bad one gives | `test_records.py` |
| `checks.check_*()`, `checks.run_all()`, `checks.git_last_changed()` | The findings each check reports | `test_checks.py` |
| `pages.write_site()` | The pages written to disk, read back with a small HTML parser | `test_pages.py` |
| `build-guide.build()` | The finished site on disk, its exit code and what it prints | `test_build_guide.py`, `test_guide_content.py` |
| The built site in Chrome | Layout and behaviour in a real browser | `check_guide.py` |

Helpers such as `slugify()`, `code_block()`, `class_names()` and the individual render functions in
`pages.py` are tested only through these seams.

**About the first red in each task.** The first run of a new test file fails because the module
does not exist yet. That only proves the test runs. The behavioural reds are the bad-input tests
(each must fail for its stated reason when the code is wrong) and Task 8 Step 3, which breaks the
stylesheet on purpose and watches a browser check fail.

## Decisions this plan makes inside the spec

These are small choices the spec left open, or places the plan departs from it. Each is deliberate.

- **`tools/guidelib/` package.** The spec names only `tools/build-guide.py`. The generator is split into focused modules so each can be tested alone.
- **One template.** `guide/templates/base.html` is the only template. Component, task and home layouts loop over records, so they are Python functions in `pages.py`.
- **Fenced code blocks** are added to the Markdown subset. Getting started must show CSS for brand colours and colourways.
- **Extra front-matter fields:** `lead` on component records, `summary` and `icon` on task files, `new_steps` and `how` on pages. The spec's example record did not show them, but the pages need them.
- **No links to `demos/`.** The spec says components not yet migrated link to their `demos/` page, but `demos/` loads files from repository paths and does not work on a hosted site. Related links point only at existing records; check 3 enforces that.
- **No screenshots in Getting started yet.** They need the real Xerte editor. The page describes the settings in words; screenshots are a follow-up for Nan.
- **Sass is pinned to 1.104.1** in `build.sh`, the version local builds use today, so CI's fresh compile matches the committed CSS byte for byte.

## File structure

| Path (under `theme-src/cardiffuniversity/` unless shown) | Responsibility |
| --- | --- |
| `tools/theme_css.py` (create) | What the compiled theme and the player's stylesheets define: class sets, utility tables, legacy and page-frame lists |
| `tools/build-reference.py` (modify) | Keeps writing the demos' utility tables, now importing from `theme_css.py` |
| `tools/guidelib/__init__.py` (create) | Package marker |
| `tools/guidelib/mdsubset.py` (create) | The Markdown subset: split into sections, render, reject everything else |
| `tools/guidelib/records.py` (create) | Load and validate `site.toml`, component records, task files and pages |
| `tools/guidelib/checks.py` (create) | The five build checks |
| `tools/guidelib/pages.py` (create) | Render every guide page to HTML and write the site |
| `tools/guidelib/assets.py` (create) | The stylesheet and script lists, and copying them into the site |
| `tools/build-guide.py` (create) | Command line: check, then build into `site/` |
| `guide/templates/base.html` (create) | The page shell: head, guide navigation, footer |
| `guide/assets/guide.css`, `guide/assets/guide.js` (create) | Guide navigation styles; copy buttons and the phone menu |
| `guide/site.toml` (create) | Title, coverage mode, component groups, task order, top menu |
| `guide/content/components/callout.md` (create) | The callout component record |
| `guide/content/tasks/draw-attention.md` (create) | The first task |
| `guide/content/pages/index.md`, `getting-started.md` (create) | Home and Getting started |
| `tests/support.py`, `tests/guide_fixture.py`, `tests/html_tree.py` (create) | Test paths, a small fixture guide, and an HTML parser for reading written pages |
| `tests/test_*.py` (create) | Unit tests, one file per module |
| `tests/check_guide.py` (create) | Headless Chrome checks of the built site |
| `build.sh`, `.gitignore` (modify) | `guide` argument, Sass pin, ignore `site/` and `__pycache__/` |
| `/.github/workflows/cardiff-guide.yml` (create, repo root) | CI for pull requests |
| `THEMING-GUIDE.md`, `README.md`, `MIGRATION.md` (modify) | Maintainer commands and phase 1 status |

---

### Task 1: Shared theme facts in `tools/theme_css.py`

Move the class and table logic out of `build-reference.py` into an importable module, and add the two new sets the guide needs: author-facing classes and every class the guide's stylesheets define. `build-reference.py` output must stay identical.

**Files:**
- Create: `tools/theme_css.py`
- Modify: `tools/build-reference.py` (replace lines 16-183 and the `render_tables` loop)
- Modify: `.gitignore`
- Create: `tests/support.py`, `tests/test_theme_css.py`

**Interfaces:**
- Consumes: nothing new.
- Produces: in `theme_css`: `THEME: Path`, `REPO: Path`, `CSS: Path`, `PLAYER: Path`, `PLAYER_CSS: tuple[str, ...]`, `IMPORTED_CSS: tuple[str, ...]`, `LEGACY: dict[str, str]`, `FRAME_PREFIXES: tuple[str, ...]`, `FAMILIES`, `class_names(css: str) -> set[str]`, `theme_classes() -> set[str]`, `author_facing_classes() -> set[str]`, `stack_classes() -> set[str]`, `utilities() -> dict[str, str]`, `utility_groups(utils: dict[str, str]) -> list[tuple[str, str, list[tuple[str, str]]]]`. In `tests/support.py`: `THEME`, `TOOLS`, `REPO`, `load_tool(name: str) -> module`.

- [ ] **Step 1: Create the branch**

```bash
git switch docs/author-guide-spec
git switch -c feat/author-guide-phase-1
```

- [ ] **Step 2: Write the test support module and the failing test**

`tests/support.py`:

```python
"""Shared paths for the theme's unit tests. Importing this puts tools/ on the import path."""
import importlib.util
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
THEME = TESTS.parent  # theme-src/cardiffuniversity
REPO = THEME.parents[1]
TOOLS = THEME / "tools"
GUIDE = THEME / "guide"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def load_tool(name):
    """Import a hyphen-named script in tools/, such as build-guide.py."""
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), TOOLS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

`tests/test_theme_css.py`:

```python
import unittest

import support  # noqa: F401  (puts tools/ on the path)
import theme_css


class ThemeCssTest(unittest.TestCase):
    def test_author_facing_classes_leave_out_legacy_and_page_frame(self):
        facing = theme_css.author_facing_classes()
        self.assertIn("cu-callout-tip", facing)
        self.assertTrue(facing.isdisjoint(theme_css.LEGACY))
        self.assertFalse(any(c.startswith(theme_css.FRAME_PREFIXES) for c in facing))
        self.assertLessEqual(facing, theme_css.theme_classes())

    def test_stack_classes_include_font_awesome_and_unstyled_bootstrap(self):
        known = theme_css.stack_classes()
        for cls in ("cu-callout", "fa-solid", "fa-lightbulb", "row-fluid", "span9"):
            self.assertIn(cls, known)

    def test_player_stylesheets_exist(self):
        for name in theme_css.PLAYER_CSS + theme_css.IMPORTED_CSS:
            self.assertTrue((theme_css.PLAYER / name).is_file(), name)

    def test_utility_groups_follow_the_family_order(self):
        groups = theme_css.utility_groups({"text-lg": "font-size: 20px", "mt-4": "margin-top: 16px"})
        self.assertEqual([heading for heading, _, _ in groups], ["Spacing", "Text size"])
        self.assertEqual(groups[0][2], [("mt-4", "margin-top: 16px")])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tests -p "test_*.py" -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'theme_css'`.

- [ ] **Step 4: Create `tools/theme_css.py`**

Copy `FAMILIES`, `ALLOW_MULTI`, `LEGACY`, `FRAME_PREFIXES`, `rules`, `utilities`, `tokens` and `resolve` from `tools/build-reference.py` lines 32-171 **verbatim** into the marked place below. Everything else is new.

```python
"""What the compiled theme and the player's stylesheets define, shared by the guide tools.

build-reference.py writes the demos' utility tables from this, and build-guide.py checks the
author guide against it. Standard library only.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEME = HERE.parent  # theme-src/cardiffuniversity
REPO = THEME.parents[1]
CSS = REPO / "themes" / "site" / "cardiffuniversity" / "cardiffuniversity.css"
PLAYER = REPO / "modules" / "site" / "parent_templates" / "site" / "common"

# The player's stylesheets, in the order modules/site/player_html5/rloObject.htm links them.
# The player appends the theme after these. css/fonts.css is left out: it holds only a
# commented placeholder. custom.css @imports css/editorstyles.css, listed separately.
PLAYER_CSS = (
    "css/bootstrap.css",
    "css/bootstrap-responsive.css",
    "css/custom.css",
    "fontawesome-6.6.0/css/all.min.css",
    "fontawesome-6.6.0/css/v4-shims.min.css",
    "fontawesome-6.6.0/css/v5-font-face.min.css",
)
IMPORTED_CSS = ("css/editorstyles.css",)

# Stylesheets whose classes do not count as the theme's own. Unchanged from build-reference.py,
# so its tables and coverage report do not move.
BASE_CSS = ("css/custom.css", "css/bootstrap.css", "css/bootstrap-responsive.css",
            "fontawesome-6.6.0/css/all.min.css")

CLASS = re.compile(r"\.(-?[A-Za-z_][\w-]*)")

# ---- copied verbatim from build-reference.py: FAMILIES, ALLOW_MULTI, LEGACY, FRAME_PREFIXES,
# ---- rules(), utilities(), tokens(), resolve()


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def class_names(css):
    """Every class name a stylesheet mentions."""
    return set(CLASS.findall(strip_comments(css)))


def theme_classes():
    """Classes the theme adds beyond Bootstrap, the player's custom.css and Font Awesome."""
    own = class_names(CSS.read_text(encoding="utf-8"))
    for name in BASE_CSS:
        path = PLAYER / name
        if path.exists():
            own -= class_names(path.read_text(encoding="utf-8"))
    return own


def author_facing_classes():
    """Theme classes a content author may use: not legacy, not the page frame."""
    return {c for c in theme_classes() if c not in LEGACY and not c.startswith(FRAME_PREFIXES)}


def stack_classes():
    """Every class defined by the stylesheets the author guide loads: the player's and the theme's."""
    found = class_names(CSS.read_text(encoding="utf-8"))
    for name in PLAYER_CSS + IMPORTED_CSS:
        found |= class_names((PLAYER / name).read_text(encoding="utf-8"))
    return found


def utility_groups(utils):
    """The utility tables: (heading, guidance, [(class, value), ...]) per family, legacy left out."""
    groups = []
    for heading, guidance, pattern in FAMILIES:
        rows = sorted((c, v) for c, v in utils.items() if re.match(pattern, c) and c not in LEGACY)
        if rows:
            groups.append((heading, guidance, rows))
    return groups
```

- [ ] **Step 5: Make `build-reference.py` import from it**

In `tools/build-reference.py`, replace lines 16-183 (the imports through the end of `theme_classes()`) with:

```python
import html
import re
import sys

from theme_css import FRAME_PREFIXES, LEGACY, THEME, theme_classes, utilities, utility_groups

GUIDE = THEME / "demos" / "code-utilities.html"
DEMOS = THEME / "demos"

START = "<!-- @generated: utility reference (tools/build-reference.py) -->"
END = "<!-- @end generated -->"
```

Then replace the first five lines of `render_tables`:

```python
def render_tables(utils):
    used, blocks = set(), []
    for heading, guidance, pattern in FAMILIES:
        rows = sorted((c, v) for c, v in utils.items() if re.match(pattern, c) and c not in LEGACY)
        if not rows:
            continue
        used |= {c for c, _ in rows}
```

with:

```python
def render_tables(utils):
    used, blocks = set(), []
    for heading, guidance, rows in utility_groups(utils):
        used |= {c for c, _ in rows}
```

The rest of `render_tables`, `coverage` and `main` stay as they are. Add one line to the module docstring, after "Standard library only.": `Shared parsing lives in tools/theme_css.py.`

- [ ] **Step 6: Ignore bytecode**

Append to `.gitignore`:

```
__pycache__/
```

- [ ] **Step 7: Run the tests and the regression checks**

Run: `python3 -m unittest discover -s tests -p "test_*.py" -v`
Expected: 4 tests, `OK`.

Run: `python3 tools/build-reference.py --check`
Expected: `In sync: code-utilities.html matches the compiled theme (264 classes documented).`

Run: `python3 tools/build-reference.py --coverage`
Expected: `0 theme classes no guide page documents or shows:` and exit code 0.

Run: `git status --short`
Expected: no change to `demos/`.

- [ ] **Step 8: Commit**

```bash
git add tools/theme_css.py tools/build-reference.py tests/support.py tests/test_theme_css.py .gitignore
git commit -m "refactor(cardiffuniversity): move the theme's class facts into tools/theme_css.py"
```

---

### Task 2: The Markdown subset

**Files:**
- Create: `tools/guidelib/__init__.py`, `tools/guidelib/mdsubset.py`
- Create: `tests/test_mdsubset.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `MarkdownError(ValueError)` with message `"{source}:{line}: {message}"`; `Section(level: int, title: str, slug: str, html: str)` (frozen dataclass; `level` is 0 for text before the first heading, 2 or 3 otherwise); `slugify(title: str) -> str`; `inline(text: str, source, line: int) -> str`; `code_block(text: str, language: str = "") -> str`; `sections(text: str, source, first_line: int = 1) -> list[Section]`.

- [ ] **Step 1: Write the failing test**

`tests/test_mdsubset.py`:

```python
import unittest

import support  # noqa: F401
from guidelib.mdsubset import MarkdownError, Section, sections


def render(text):
    return sections(text, "test.md")


class InlineTest(unittest.TestCase):
    def test_bold_italic_and_code(self):
        [s] = render("Use **one** callout per *idea* with `cu-callout`.")
        self.assertEqual(s.html, "<p>Use <strong>one</strong> callout per <em>idea</em> with <code>cu-callout</code>.</p>")

    def test_text_is_escaped(self):
        [s] = render("Fish & chips, a < b")
        self.assertEqual(s.html, "<p>Fish &amp; chips, a &lt; b</p>")

    def test_markup_inside_code_is_allowed_and_escaped(self):
        [s] = render("Paste `<div class=\"x\">` here.")
        self.assertIn("<code>&lt;div class=&quot;x&quot;&gt;</code>", s.html)

    def test_links(self):
        [s] = render("See [Alerts](alert.html) and [the site](https://example.org).")
        self.assertIn('<a href="alert.html">Alerts</a>', s.html)
        self.assertIn('<a href="https://example.org">the site</a>', s.html)

    def test_unsafe_link_scheme_is_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "test.md:1: link scheme 'javascript:'"):
            render("[x](javascript:alert(1))")

    def test_raw_html_is_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "raw HTML is not allowed"):
            render("A <strong>bold</strong> claim.")

    def test_images_are_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "images"):
            render("![logo](logo.png)")


class BlockTest(unittest.TestCase):
    def test_sections_split_at_headings(self):
        result = render("## When to use it\n\nOne idea.\n\n### Do\n\n- Keep it short\n- Name the variant\n")
        self.assertEqual(result, [
            Section(2, "When to use it", "when-to-use-it", "<p>One idea.</p>"),
            Section(3, "Do", "do", "<ul><li>Keep it short</li><li>Name the variant</li></ul>"),
        ])

    def test_text_before_the_first_heading_is_level_0(self):
        result = render("Intro.\n\n## Next\n\nMore.")
        self.assertEqual(result[0], Section(0, "", "", "<p>Intro.</p>"))

    def test_empty_section_is_kept(self):
        result = render("## When to use it\n\n### Do\n\n- a")
        self.assertEqual(result[0].html, "")

    def test_numbered_list(self):
        [s] = render("1. Open\n2. Paste")
        self.assertEqual(s.html, "<ol><li>Open</li><li>Paste</li></ol>")

    def test_paragraph_lines_join(self):
        [s] = render("One line\nand the next.")
        self.assertEqual(s.html, "<p>One line and the next.</p>")

    def test_fenced_code_is_escaped(self):
        [s] = render("```css\n:root { --x: <b>; }\n```")
        self.assertIn('<code class="language-css">:root { --x: &lt;b&gt;; }</code>', s.html)
        self.assertIn('class="g-copy"', s.html)

    def test_unclosed_fence_is_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "not closed"):
            render("```\ncode")

    def test_only_h2_and_h3(self):
        for text in ("# Title", "#### Deep"):
            with self.assertRaisesRegex(MarkdownError, "only ## and ### headings"):
                render(text)

    def test_line_numbers_count_from_first_line(self):
        with self.assertRaisesRegex(MarkdownError, "test.md:12:"):
            sections("Fine.\n\n# Bad", "test.md", first_line=10)

    def test_unsupported_blocks(self):
        for text in ("> quote", "* star list", "  - nested", "---", "| a | b |"):
            with self.subTest(text=text), self.assertRaises(MarkdownError):
                render(text)

    def test_mixed_list_markers_are_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "one marker"):
            render("- a\n1. b")

    def test_windows_line_endings(self):
        [s] = render("## A\r\n\r\nText\r\n")
        self.assertEqual(s, Section(2, "A", "a", "<p>Text</p>"))


class SlugTest(unittest.TestCase):
    def test_heading_slugs(self):
        result = render("## Brand colours\n\nText.\n\n### Don't\n\n- a")
        self.assertEqual([x.slug for x in result], ["brand-colours", "don-t"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tests -p "test_mdsubset.py" -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'guidelib'`.

- [ ] **Step 3: Write the implementation**

`tools/guidelib/__init__.py`:

```python
"""The author guide generator: records, checks, pages and assets. See tools/build-guide.py."""
```

`tools/guidelib/mdsubset.py`:

```python
"""The Markdown subset the author guide allows, rendered to HTML.

Allowed: ## and ### headings, paragraphs, - and 1. lists, fenced code blocks, **bold**, *italic*,
`code` and [links](url). Anything else is an error naming the file and line, so nothing is
silently mangled. Raw HTML is not allowed: markup belongs in a record's examples.
"""
import html
import re
from dataclasses import dataclass


class MarkdownError(ValueError):
    """A construct outside the subset, with the file and line it came from."""

    def __init__(self, source, line, message):
        super().__init__(f"{source}:{line}: {message}")


@dataclass(frozen=True)
class Section:
    """The text under one heading. level is 0 for text before the first heading."""
    level: int
    title: str
    slug: str
    html: str


HEADING = re.compile(r"^(#+)\s+(\S.*)$")
BULLET = re.compile(r"^- (.+)$")
NUMBERED = re.compile(r"^\d+\. (.+)$")
FENCE = re.compile(r"^```([\w-]*)\s*$")
UNSUPPORTED = (
    (re.compile(r"^>"), "block quotes"),
    (re.compile(r"^\|"), "tables"),
    (re.compile(r"^[*+]\s"), "lists marked with * or + (use -)"),
    (re.compile(r"^\s+\S"), "indented lines (nested lists and indented code)"),
    (re.compile(r"^(-{3,}|\*{3,}|_{3,})\s*$"), "horizontal rules"),
)
RAW_HTML = re.compile(r"</?[A-Za-z!]")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
SCHEME = re.compile(r"^([A-Za-z][\w+.-]*):")
SAFE_SCHEMES = {"http", "https", "mailto"}


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def code_block(text, language=""):
    """A code view with a copy button. The button stays hidden until guide.js can make it work."""
    attr = f' class="language-{language}"' if language else ""
    return (f'<div class="g-code-wrap"><pre class="g-code"><code{attr}>{html.escape(text)}</code></pre>'
            '<button class="g-copy" type="button" hidden>Copy</button></div>')


def inline(text, source, line):
    """Render one line: code spans, links, bold and italic. Everything else is escaped."""
    out = []
    for i, part in enumerate(re.split(r"(`[^`]+`)", text)):
        if i % 2:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        if RAW_HTML.search(part):
            raise MarkdownError(source, line, "raw HTML is not allowed; put markup in an example")
        if "![" in part:
            raise MarkdownError(source, line, "images are not in the guide's Markdown subset")
        out.append(_links(part, source, line))
    return "".join(out)


def _links(text, source, line):
    out, pos = [], 0
    for match in LINK.finditer(text):
        url = match.group(2)
        scheme = SCHEME.match(url)
        if scheme and scheme.group(1).lower() not in SAFE_SCHEMES:
            raise MarkdownError(source, line, f"link scheme '{scheme.group(1)}:' is not allowed")
        out.append(_emphasis(text[pos:match.start()]))
        out.append(f'<a href="{html.escape(url)}">{_emphasis(match.group(1))}</a>')
        pos = match.end()
    out.append(_emphasis(text[pos:]))
    return "".join(out)


def _emphasis(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)


def _reject(raw, source, line):
    for pattern, what in UNSUPPORTED:
        if pattern.match(raw):
            raise MarkdownError(source, line, f"{what} are not in the guide's Markdown subset")


def _starts_block(raw):
    return bool(FENCE.match(raw) or HEADING.match(raw) or BULLET.match(raw) or NUMBERED.match(raw))


def sections(text, source, first_line=1):
    """Split text into sections at ## and ### headings, rendering each section's blocks."""
    lines = text.replace("\r\n", "\n").split("\n")
    found, level, title, chunks = [], 0, "", []
    i = 0
    while i < len(lines):
        raw, number = lines[i], first_line + i
        if not raw.strip():
            i += 1
            continue
        fence = FENCE.match(raw)
        if fence:
            end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("```")), None)
            if end is None:
                raise MarkdownError(source, number, "code block is not closed with ```")
            chunks.append(code_block("\n".join(lines[i + 1:end]), fence.group(1)))
            i = end + 1
            continue
        heading = HEADING.match(raw)
        if heading:
            if len(heading.group(1)) not in (2, 3):
                raise MarkdownError(source, number, f"only ## and ### headings are allowed, not {heading.group(1)}")
            found.append(Section(level, title, slugify(title), "\n".join(chunks)))
            level, title, chunks = len(heading.group(1)), heading.group(2).strip(), []
            i += 1
            continue
        _reject(raw, source, number)
        marker = BULLET if BULLET.match(raw) else NUMBERED if NUMBERED.match(raw) else None
        if marker:
            tag = "ul" if marker is BULLET else "ol"
            items = []
            while i < len(lines) and lines[i].strip():
                item = marker.match(lines[i])
                if not item:
                    raise MarkdownError(source, first_line + i,
                                        "a list must use one marker throughout and end with a blank line")
                items.append(f"<li>{inline(item.group(1), source, first_line + i)}</li>")
                i += 1
            chunks.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        words = []
        while i < len(lines) and lines[i].strip() and not _starts_block(lines[i]):
            _reject(lines[i], source, first_line + i)
            words.append(inline(lines[i].strip(), source, first_line + i))
            i += 1
        chunks.append(f"<p>{' '.join(words)}</p>")
    found.append(Section(level, title, slugify(title), "\n".join(chunks)))
    return [s for s in found if s.level or s.html]
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" -v`
Expected: all tests `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/guidelib/__init__.py tools/guidelib/mdsubset.py tests/test_mdsubset.py
git commit -m "feat(cardiffuniversity): add the author guide's Markdown subset"
```

---

### Task 3: Loading records

**Files:**
- Create: `tools/guidelib/records.py`
- Create: `tests/guide_fixture.py`, `tests/test_records.py`

**Interfaces:**
- Consumes: `guidelib.mdsubset.sections`, `Section`.
- Produces (all frozen dataclasses):
  - `Example(label: str, purpose: str, html: str, variant: str | None = None)`
  - `Editor(survives: bool, checked: datetime.date, xerte: str)`
  - `Component(name, title, lead, group, status, since: str, tasks: tuple[str], related: tuple[str], scss: tuple[str], editor: Editor, parts: dict[str, str], examples: tuple[Example], when_intro: str, do_html: str, dont_html: str, accessibility_html: str, source: Path)`
  - `Task(name, title, summary, icon: str, components: tuple[str], example: Example, goal_html: str, checklist_html: str, source: Path)`
  - `Page(name, title, lead: str, new_steps: tuple[str], how: tuple[tuple[str, str]], sections: tuple[Section], source: Path)`
  - `Site(title: str, coverage: str, groups: tuple[tuple[str, str]], tasks: tuple[str], menu: tuple[tuple[str, str]])` where `groups` is `(id, title)` and `menu` is `(page key, label)`
  - `Content(components: dict[str, Component], tasks: dict[str, Task], pages: dict[str, Page])`
  - `RecordError(ValueError)` with message `"{source}: {message}"`
  - `split_front_matter(text, source) -> tuple[dict, str, int]`, `load_component(path)`, `load_task(path)`, `load_page(path)`, `load_site(path)`, `load_content(content_dir) -> Content`
  - Constants `MENU_PAGES = ("home", "getting-started", "tasks", "components")`.
  - In `tests/guide_fixture.py`: strings `SITE`, `CALLOUT`, `TASK`, `INDEX`, `GETTING_STARTED`, and `write_guide(root: Path, **overrides) -> Path` (returns the guide folder; an override key such as `CALLOUT=...` replaces that file's text).

- [ ] **Step 1: Write the fixture guide**

`tests/guide_fixture.py`:

````python
"""A small, valid author guide for tests. write_guide() writes it into a temporary folder."""
import shutil
from pathlib import Path

import support

SITE = """\
title = "Test guide"
coverage = "warn"
tasks = ["draw-attention"]

[[groups]]
id = "emphasis"
title = "Emphasis"

[[menu]]
page = "home"
title = "Home"

[[menu]]
page = "getting-started"
title = "Getting started"

[[menu]]
page = "tasks"
title = "Tasks"

[[menu]]
page = "components"
title = "Components"
"""

CALLOUT = """\
+++
name = "callout"
title = "Callouts"
lead = "Pull one key idea out of the page."
group = "emphasis"
status = "current"
since = "v1.4"
tasks = ["draw-attention"]
related = []
scss = ["scss/components/_callout.scss"]

[editor]
survives = true
checked = 2026-09-20
xerte = "3.14"

[parts]
cu-callout = "The container."
cu-callout-title = "The short bold title."
cu-callout-icon = "Only for the older fa-stack markup."

[[examples]]
class = "cu-callout-tip"
label = "Tip"
purpose = "A shortcut or recommendation"
html = '''
<div class="cu-callout cu-callout-tip">
  <strong class="cu-callout-title">Tip</strong>
  <p>Fish &amp; chips.</p>
</div>
'''

[[examples]]
class = "cu-callout-warning"
label = "Warning"
purpose = "A risk the reader must avoid"
html = '''
<div class="cu-callout cu-callout-warning">
  <strong class="cu-callout-title">Warning</strong>
  <p>A risk.</p>
</div>
'''
+++

## When to use it

Use a callout for one idea.

### Do

- Name the variant in the title.

### Don't

- Stack more than two.

## Accessibility

The title says the variant in words.
"""

TASK = """\
+++
name = "draw-attention"
title = "Draw attention to something"
summary = "Make sure readers notice a tip or a warning."
icon = "fa-lightbulb"
components = ["callout"]

[example]
label = "An upload reminder"
purpose = "A paragraph with one Important callout."
html = '''
<p>Upload your file.</p>
<div class="cu-callout cu-callout-important">
  <strong class="cu-callout-title">Important</strong>
  <p>Check that the upload has finished.</p>
</div>
'''
+++

## Goal

Make one point stand out.

## Checklist

- The title names the variant.
"""

INDEX = """\
+++
name = "index"
title = "What do you want to do with your page?"
lead = "Pick a task."
new_steps = ["Choose the theme.", "Paste a callout."]

[[how]]
title = "Choose"
text = "Pick a component."

[[how]]
title = "Check"
text = "Run the checklist."
+++
"""

GETTING_STARTED = """\
+++
name = "getting-started"
title = "Getting started"
lead = "Switch a project to the theme."
+++

## Choose the theme

1. Open the project's properties.
2. Set **Theme** to Cardiff University Theme.

## Brand colours

```css
:root { --color-brand-primary: #00703C; }
```
"""

FILES = {
    "SITE": "site.toml",
    "CALLOUT": "content/components/callout.md",
    "TASK": "content/tasks/draw-attention.md",
    "INDEX": "content/pages/index.md",
    "GETTING_STARTED": "content/pages/getting-started.md",
}


def write_guide(root, **overrides):
    """Write the fixture guide into root/guide. A keyword such as CALLOUT="..." replaces that file;
    CALLOUT=None leaves the file out."""
    guide = Path(root) / "guide"
    texts = {"SITE": SITE, "CALLOUT": CALLOUT, "TASK": TASK, "INDEX": INDEX, "GETTING_STARTED": GETTING_STARTED}
    texts.update(overrides)
    for key, relative in FILES.items():
        if texts[key] is None:
            continue
        path = guide / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(texts[key], encoding="utf-8", newline="")
    for folder in ("templates", "assets"):
        real = support.GUIDE / folder
        if real.exists():
            shutil.copytree(real, guide / folder)
    return guide
````

- [ ] **Step 2: Write the failing test**

`tests/test_records.py`:

```python
import datetime
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401
import guide_fixture as fx
from guidelib import records
from guidelib.mdsubset import MarkdownError


class RecordsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def guide(self, **overrides):
        return fx.write_guide(self.tmp.name, **overrides)

    def component(self, text):
        guide = self.guide(CALLOUT=text)
        return records.load_component(guide / "content" / "components" / "callout.md")

    def test_component_loads(self):
        c = self.component(fx.CALLOUT)
        self.assertEqual(c.name, "callout")
        self.assertEqual(c.editor, records.Editor(True, datetime.date(2026, 9, 20), "3.14"))
        self.assertEqual(list(c.parts), ["cu-callout", "cu-callout-title", "cu-callout-icon"])
        self.assertEqual([e.variant for e in c.examples], ["cu-callout-tip", "cu-callout-warning"])
        self.assertTrue(c.examples[0].html.startswith('<div class="cu-callout cu-callout-tip">'))
        self.assertEqual(c.when_intro, "<p>Use a callout for one idea.</p>")
        self.assertEqual(c.do_html, "<ul><li>Name the variant in the title.</li></ul>")
        self.assertEqual(c.dont_html, "<ul><li>Stack more than two.</li></ul>")
        self.assertEqual(c.accessibility_html, "<p>The title says the variant in words.</p>")

    def test_crlf_record_loads(self):
        c = self.component(fx.CALLOUT.replace("\n", "\r\n"))
        self.assertEqual(c.do_html, "<ul><li>Name the variant in the title.</li></ul>")
        self.assertEqual(c.examples[0].variant, "cu-callout-tip")

    def assertComponentError(self, text, pattern):
        with self.assertRaisesRegex(records.RecordError, pattern):
            self.component(text)

    def test_name_must_match_the_file(self):
        self.assertComponentError(fx.CALLOUT.replace('name = "callout"', 'name = "callouts"'), "must match the file name")

    def test_unknown_key(self):
        self.assertComponentError(fx.CALLOUT.replace('since = "v1.4"', 'since = "v1.4"\ncolour = "red"'), "unknown front-matter key.*colour")

    def test_must_start_with_front_matter(self):
        self.assertComponentError("name = 'x'\n", "must start with a \\+\\+\\+ line")

    def test_front_matter_must_close(self):
        self.assertComponentError("+++\nname = 'callout'\n", "not closed")

    def test_invalid_toml(self):
        self.assertComponentError(fx.CALLOUT.replace('since = "v1.4"', "since = v1.4"), "not valid TOML")

    def test_xerte_version_must_be_text(self):
        self.assertComponentError(fx.CALLOUT.replace('xerte = "3.14"', "xerte = 3.14"), "'xerte' must be text")

    def test_checked_must_be_a_date(self):
        self.assertComponentError(fx.CALLOUT.replace("checked = 2026-09-20", 'checked = "20 Sep"'), "'checked' must be a date")

    def test_status(self):
        self.assertComponentError(fx.CALLOUT.replace('status = "current"', 'status = "draft"'), "status must be one of")

    def test_variant_cannot_also_be_a_part(self):
        self.assertComponentError(fx.CALLOUT.replace('cu-callout-icon = "Only', 'cu-callout-tip = "Only'), "both a variant and a part")

    def test_variant_used_twice(self):
        self.assertComponentError(fx.CALLOUT.replace('class = "cu-callout-warning"', 'class = "cu-callout-tip"'), "used twice")

    def test_needs_examples(self):
        start = fx.CALLOUT.index("[[examples]]")
        end = fx.CALLOUT.index("+++", start)
        self.assertComponentError(fx.CALLOUT[:start] + fx.CALLOUT[end:], "missing 'examples'")

    def test_headings_must_be_in_order(self):
        self.assertComponentError(fx.CALLOUT.replace("### Do\n", "### Dos\n"), "body headings must be, in order")

    def test_no_text_before_the_first_heading(self):
        self.assertComponentError(fx.CALLOUT.replace("+++\n\n## When", "+++\nHello.\n\n## When"), "text before the first heading")

    def test_do_must_not_be_empty(self):
        self.assertComponentError(fx.CALLOUT.replace("- Name the variant in the title.\n", ""), "'### Do' is empty")

    def test_body_errors_report_the_file_line(self):
        text = fx.CALLOUT.replace("Use a callout for one idea.", "Use <b>this</b>.")
        line = text.splitlines().index("Use <b>this</b>.") + 1
        with self.assertRaisesRegex(MarkdownError, f"callout.md:{line}: raw HTML"):
            self.component(text)

    def test_task_loads(self):
        guide = self.guide()
        task = records.load_task(guide / "content" / "tasks" / "draw-attention.md")
        self.assertEqual(task.components, ("callout",))
        self.assertEqual(task.example.label, "An upload reminder")
        self.assertIsNone(task.example.variant)
        self.assertEqual(task.goal_html, "<p>Make one point stand out.</p>")

    def test_task_icon_must_be_font_awesome(self):
        guide = self.guide(TASK=fx.TASK.replace('icon = "fa-lightbulb"', 'icon = "lightbulb"'))
        with self.assertRaisesRegex(records.RecordError, "Font Awesome"):
            records.load_task(guide / "content" / "tasks" / "draw-attention.md")

    def test_page_loads(self):
        guide = self.guide()
        page = records.load_page(guide / "content" / "pages" / "index.md")
        self.assertEqual(page.new_steps, ("Choose the theme.", "Paste a callout."))
        self.assertEqual(page.how, (("Choose", "Pick a component."), ("Check", "Run the checklist.")))
        self.assertEqual(page.sections, ())
        started = records.load_page(guide / "content" / "pages" / "getting-started.md")
        self.assertEqual([s.title for s in started.sections], ["Choose the theme", "Brand colours"])

    def test_site_loads(self):
        site = records.load_site(self.guide() / "site.toml")
        self.assertEqual(site.coverage, "warn")
        self.assertEqual(site.groups, (("emphasis", "Emphasis"),))
        self.assertEqual(site.menu[0], ("home", "Home"))

    def test_site_rejects_unknown_menu_pages_and_modes(self):
        for old, new, pattern in (('page = "tasks"', 'page = "colours"', "menu page must be one of"),
                                  ('coverage = "warn"', 'coverage = "maybe"', "coverage must be one of")):
            with self.subTest(new=new):
                guide = fx.write_guide(tempfile.mkdtemp(dir=self.tmp.name), SITE=fx.SITE.replace(old, new))
                with self.assertRaisesRegex(records.RecordError, pattern):
                    records.load_site(guide / "site.toml")

    def test_load_content(self):
        content = records.load_content(self.guide() / "content")
        self.assertEqual(sorted(content.components), ["callout"])
        self.assertEqual(sorted(content.tasks), ["draw-attention"])
        self.assertEqual(sorted(content.pages), ["getting-started", "index"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tests -p "test_records.py" -v`
Expected: FAIL with `ImportError: cannot import name 'records' from 'guidelib'`.

- [ ] **Step 4: Write the implementation**

`tools/guidelib/records.py`:

```python
"""Load the author guide's records: site.toml, component records, task files and pages.

Each record is TOML front-matter between +++ lines, read with tomllib, then a Markdown body in
the guide's subset. Anything missing, misspelt or out of order is a RecordError naming the file,
so a mistake fails the build instead of producing a wrong page.
"""
import datetime
import tomllib
from dataclasses import dataclass
from pathlib import Path

from guidelib.mdsubset import Section, sections

STATUSES = ("current", "legacy")
COVERAGE_MODES = ("warn", "fail")
MENU_PAGES = ("home", "getting-started", "tasks", "components")
COMPONENT_HEADINGS = ((2, "When to use it"), (3, "Do"), (3, "Don't"), (2, "Accessibility"))
TASK_HEADINGS = ((2, "Goal"), (2, "Checklist"))
KIND_NAMES = {str: "text", bool: "true or false", dict: "table", list: "list", datetime.date: "date (YYYY-MM-DD)"}


class RecordError(ValueError):
    def __init__(self, source, message):
        super().__init__(f"{source}: {message}")


@dataclass(frozen=True)
class Example:
    label: str
    purpose: str
    html: str
    variant: str | None = None


@dataclass(frozen=True)
class Editor:
    survives: bool
    checked: datetime.date
    xerte: str


@dataclass(frozen=True)
class Component:
    name: str
    title: str
    lead: str
    group: str
    status: str
    since: str
    tasks: tuple
    related: tuple
    scss: tuple
    editor: Editor
    parts: dict
    examples: tuple
    when_intro: str
    do_html: str
    dont_html: str
    accessibility_html: str
    source: Path


@dataclass(frozen=True)
class Task:
    name: str
    title: str
    summary: str
    icon: str
    components: tuple
    example: Example
    goal_html: str
    checklist_html: str
    source: Path


@dataclass(frozen=True)
class Page:
    name: str
    title: str
    lead: str
    new_steps: tuple
    how: tuple
    sections: tuple
    source: Path


@dataclass(frozen=True)
class Site:
    title: str
    coverage: str
    groups: tuple
    tasks: tuple
    menu: tuple


@dataclass(frozen=True)
class Content:
    components: dict
    tasks: dict
    pages: dict


def split_front_matter(text, source):
    """Return (front-matter, body text, the file line the body starts on)."""
    text = text.replace("\r\n", "\n")
    if not text.startswith("+++\n"):
        raise RecordError(source, "must start with a +++ line")
    end = text.find("\n+++\n", 3)
    if end == -1 and text.endswith("\n+++"):
        end = len(text) - 4
    if end == -1:
        raise RecordError(source, "front-matter is not closed with a +++ line")
    front = text[4:end + 1]
    try:
        data = tomllib.loads(front)
    except tomllib.TOMLDecodeError as error:
        raise RecordError(source, f"front-matter is not valid TOML ({error}; "
                                  "line 1 is the line after the opening +++)") from None
    return data, text[end + 5:], front.count("\n") + 3


def _field(data, key, kind, source, where="", required=True, default=None):
    prefix = f"{where}: " if where else ""
    if key not in data:
        if required:
            raise RecordError(source, f"{prefix}missing '{key}'")
        return default
    value = data[key]
    if kind == "strings":
        if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
            raise RecordError(source, f"{prefix}'{key}' must be a list of text")
        return tuple(value)
    ok = isinstance(value, kind)
    if kind is datetime.date:
        ok = ok and not isinstance(value, datetime.datetime)
    if kind is str:
        ok = ok and bool(value.strip())
    if not ok:
        raise RecordError(source, f"{prefix}'{key}' must be {'a ' if kind is not str else ''}{KIND_NAMES[kind]}")
    return value


def _only(data, allowed, source, where="front-matter"):
    extra = sorted(set(data) - set(allowed))
    if extra:
        raise RecordError(source, f"unknown {where} key(s): {', '.join(extra)}")


def _name(data, source):
    name = _field(data, "name", str, source)
    if name != Path(source).stem:
        raise RecordError(source, f"name '{name}' must match the file name '{Path(source).stem}'")
    return name


def _example(item, source, where, allow_variant):
    if not isinstance(item, dict):
        raise RecordError(source, f"{where} must be a table")
    _only(item, {"class", "label", "purpose", "html"} if allow_variant else {"label", "purpose", "html"}, source, where)
    variant = item.get("class")
    if variant is not None and (not isinstance(variant, str) or not variant.strip() or " " in variant.strip()):
        raise RecordError(source, f"{where}: 'class' must be one class name")
    return Example(label=_field(item, "label", str, source, where),
                   purpose=_field(item, "purpose", str, source, where),
                   html=_field(item, "html", str, source, where).strip(),
                   variant=variant.strip() if variant else None)


def _heading(spec):
    return "#" * spec[0] + " " + spec[1]


def _expect(found, expected, source):
    """Check the body's headings are exactly `expected`, in order; return the sections."""
    if found and found[0].level == 0:
        raise RecordError(source, f"text before the first heading; start the body with '{_heading(expected[0])}'")
    if tuple((s.level, s.title) for s in found) != expected:
        raise RecordError(source, "body headings must be, in order: " + ", ".join(f"'{_heading(h)}'" for h in expected))
    return found


def load_component(path):
    path = Path(path)
    data, body, line = split_front_matter(path.read_text(encoding="utf-8"), path)
    _only(data, {"name", "title", "lead", "group", "status", "since", "tasks", "related", "scss",
                 "editor", "parts", "examples"}, path)
    name = _name(data, path)
    status = _field(data, "status", str, path)
    if status not in STATUSES:
        raise RecordError(path, f"status must be one of {', '.join(STATUSES)}, not '{status}'")
    editor = _field(data, "editor", dict, path)
    _only(editor, {"survives", "checked", "xerte"}, path, "[editor]")
    parts = _field(data, "parts", dict, path)
    if not parts or not all(isinstance(v, str) and v.strip() for v in parts.values()):
        raise RecordError(path, "[parts] must map each class to a description")
    items = _field(data, "examples", list, path)
    if not items:
        raise RecordError(path, "needs at least one [[examples]] entry")
    examples = tuple(_example(item, path, f"[[examples]] entry {n}", True) for n, item in enumerate(items, 1))
    variants = [e.variant for e in examples if e.variant]
    twice = sorted({v for v in variants if variants.count(v) > 1})
    if twice:
        raise RecordError(path, f"variant class used twice: {', '.join(twice)}")
    both = sorted(set(variants) & set(parts))
    if both:
        raise RecordError(path, f"class is both a variant and a part: {', '.join(both)}")
    when, do, dont, accessibility = _expect(sections(body, path, line), COMPONENT_HEADINGS, path)
    for section in (do, dont, accessibility):
        if not section.html:
            raise RecordError(path, f"'{_heading((section.level, section.title))}' is empty")
    return Component(
        name=name, title=_field(data, "title", str, path), lead=_field(data, "lead", str, path),
        group=_field(data, "group", str, path), status=status, since=_field(data, "since", str, path),
        tasks=_field(data, "tasks", "strings", path, required=False, default=()),
        related=_field(data, "related", "strings", path, required=False, default=()),
        scss=_field(data, "scss", "strings", path, required=False, default=()),
        editor=Editor(survives=_field(editor, "survives", bool, path, "[editor]"),
                      checked=_field(editor, "checked", datetime.date, path, "[editor]"),
                      xerte=_field(editor, "xerte", str, path, "[editor]")),
        parts=dict(parts), examples=examples, when_intro=when.html, do_html=do.html,
        dont_html=dont.html, accessibility_html=accessibility.html, source=path)


def load_task(path):
    path = Path(path)
    data, body, line = split_front_matter(path.read_text(encoding="utf-8"), path)
    _only(data, {"name", "title", "summary", "icon", "components", "example"}, path)
    name = _name(data, path)
    icon = _field(data, "icon", str, path)
    if not icon.startswith("fa-"):
        raise RecordError(path, f"icon must be a Font Awesome name such as fa-lightbulb, not '{icon}'")
    components = _field(data, "components", "strings", path)
    if not components:
        raise RecordError(path, "'components' must name at least one component")
    example = _example(_field(data, "example", dict, path), path, "[example]", False)
    goal, checklist = _expect(sections(body, path, line), TASK_HEADINGS, path)
    for section in (goal, checklist):
        if not section.html:
            raise RecordError(path, f"'{_heading((section.level, section.title))}' is empty")
    return Task(name=name, title=_field(data, "title", str, path), summary=_field(data, "summary", str, path),
                icon=icon, components=components, example=example, goal_html=goal.html,
                checklist_html=checklist.html, source=path)


def load_page(path):
    path = Path(path)
    data, body, line = split_front_matter(path.read_text(encoding="utf-8"), path)
    _only(data, {"name", "title", "lead", "new_steps", "how"}, path)
    how = []
    for n, item in enumerate(_field(data, "how", list, path, required=False, default=[]), 1):
        where = f"[[how]] entry {n}"
        if not isinstance(item, dict):
            raise RecordError(path, f"{where} must be a table")
        _only(item, {"title", "text"}, path, where)
        how.append((_field(item, "title", str, path, where), _field(item, "text", str, path, where)))
    return Page(name=_name(data, path), title=_field(data, "title", str, path), lead=_field(data, "lead", str, path),
                new_steps=_field(data, "new_steps", "strings", path, required=False, default=()),
                how=tuple(how), sections=tuple(sections(body, path, line)), source=path)


def load_site(path):
    path = Path(path)
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise RecordError(path, f"not valid TOML ({error})") from None
    _only(data, {"title", "coverage", "groups", "tasks", "menu"}, path, "site.toml")
    coverage = _field(data, "coverage", str, path)
    if coverage not in COVERAGE_MODES:
        raise RecordError(path, f"coverage must be one of {', '.join(COVERAGE_MODES)}, not '{coverage}'")
    groups = []
    for n, item in enumerate(_field(data, "groups", list, path), 1):
        where = f"[[groups]] entry {n}"
        if not isinstance(item, dict):
            raise RecordError(path, f"{where} must be a table")
        _only(item, {"id", "title"}, path, where)
        groups.append((_field(item, "id", str, path, where), _field(item, "title", str, path, where)))
    menu = []
    for n, item in enumerate(_field(data, "menu", list, path), 1):
        where = f"[[menu]] entry {n}"
        if not isinstance(item, dict):
            raise RecordError(path, f"{where} must be a table")
        _only(item, {"page", "title"}, path, where)
        page = _field(item, "page", str, path, where)
        if page not in MENU_PAGES:
            raise RecordError(path, f"{where}: menu page must be one of {', '.join(MENU_PAGES)}, not '{page}'")
        menu.append((page, _field(item, "title", str, path, where)))
    tasks = _field(data, "tasks", "strings", path, required=False, default=())
    for label, values in (("group id", [g for g, _ in groups]), ("task", list(tasks)), ("menu page", [m for m, _ in menu])):
        twice = sorted({v for v in values if values.count(v) > 1})
        if twice:
            raise RecordError(path, f"{label} listed twice: {', '.join(twice)}")
    return Site(title=_field(data, "title", str, path), coverage=coverage, groups=tuple(groups),
                tasks=tasks, menu=tuple(menu))


def load_content(content_dir):
    content_dir = Path(content_dir)

    def load(folder, loader):
        return {path.stem: loader(path) for path in sorted((content_dir / folder).glob("*.md"))}

    return Content(components=load("components", load_component), tasks=load("tasks", load_task),
                   pages=load("pages", load_page))
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" -v`
Expected: all tests `OK`.

- [ ] **Step 6: Commit**

```bash
git add tools/guidelib/records.py tests/guide_fixture.py tests/test_records.py
git commit -m "feat(cardiffuniversity): load and validate author guide records"
```

---

### Task 4: The five build checks

**Files:**
- Create: `tools/guidelib/checks.py`
- Create: `tests/test_checks.py`

**Interfaces:**
- Consumes: `records.Content`, `Component`, `Task`, `Page`, `Site`, `Example`, `Editor`.
- Produces: `Finding(level: str, check: int, source: str, message: str)` (frozen; `level` is `"error"` or `"warning"`; `str(finding)` gives `"ERROR [check 1] source: message"`); `scan(html: str)` returning an object with `.classes: set[str]`, `.images_without_alt: int`, `.empty_headings: int`; `check_classes_exist(content, known)`, `check_coverage(content, author_facing, tables, mode)`, `check_references(content, site, theme_dir)`, `check_stale_evidence(content, last_changed)`, `check_examples(content)`, each `-> list[Finding]`; `git_last_changed(theme_dir) -> Callable[[str], datetime.date | None]`; `run_all(content, site, *, theme_dir, known, author_facing, tables, last_changed) -> list[Finding]`.

- [ ] **Step 1: Write the failing test**

`tests/test_checks.py`:

```python
import datetime
import tempfile
import unittest
from pathlib import Path

import support
from guidelib import checks
from guidelib.records import Component, Content, Editor, Example, Page, Site, Task

TIP = Example("Tip", "A tip", '<div class="cu-callout cu-callout-tip"><p>x</p></div>', "cu-callout-tip")
KNOWN = {"cu-callout", "cu-callout-tip", "cu-callout-title", "fa-solid"}


def component(**changes):
    fields = dict(name="callout", title="Callouts", lead="One idea.", group="emphasis", status="current",
                  since="v1.4", tasks=(), related=(), scss=(), editor=Editor(True, datetime.date(2026, 9, 20), "3.14"),
                  parts={"cu-callout": "The container."}, examples=(TIP,), when_intro="",
                  do_html="<ul><li>a</li></ul>", dont_html="<ul><li>b</li></ul>",
                  accessibility_html="<p>c</p>", source=Path("components/callout.md"))
    fields.update(changes)
    return Component(**fields)


def task(**changes):
    fields = dict(name="draw-attention", title="Draw attention", summary="s", icon="fa-lightbulb",
                  components=("callout",), example=Example("Upload", "p", '<p class="fa-solid">x</p>'),
                  goal_html="<p>g</p>", checklist_html="<ul><li>c</li></ul>", source=Path("tasks/draw-attention.md"))
    fields.update(changes)
    return Task(**fields)


INDEX = Page("index", "Home", "Lead", (), (), (), Path("pages/index.md"))
SITE = Site("Guide", "warn", (("emphasis", "Emphasis"),), (), (("home", "Home"),))


def content(components=(), tasks=(), pages=(INDEX,)):
    return Content({c.name: c for c in components}, {t.name: t for t in tasks}, {p.name: p for p in pages})


def messages(findings):
    return [f"{f.level} {f.check} {f.message}" for f in findings]


class ClassesExistTest(unittest.TestCase):
    def test_known_classes_pass(self):
        self.assertEqual(checks.check_classes_exist(content([component()], [task()]), KNOWN), [])

    def test_unknown_example_class_is_an_error(self):
        bad = Example("Tip", "t", '<div class="cu-callout cu-calout-tip"></div>')
        [finding] = checks.check_classes_exist(content([component(examples=(bad,))]), KNOWN)
        self.assertEqual((finding.level, finding.check), ("error", 1))
        self.assertIn("cu-calout-tip", finding.message)

    def test_unknown_part_is_an_error(self):
        found = checks.check_classes_exist(content([component(parts={"cu-gone": "x"})]), KNOWN)
        self.assertEqual(messages(found), ["error 1 class 'cu-gone' is not defined by the theme or the player's stylesheets"])


class CoverageTest(unittest.TestCase):
    def test_warn_mode_counts_what_is_missing(self):
        [finding] = checks.check_coverage(content([component()]), {"cu-callout", "cu-callout-tip", "box", "card"}, set(), "warn")
        self.assertEqual(finding.level, "warning")
        self.assertIn("2 author-facing classes are not covered yet: box, card", finding.message)

    def test_fail_mode_is_an_error(self):
        [finding] = checks.check_coverage(content([component()]), {"box"}, set(), "fail")
        self.assertEqual(finding.level, "error")

    def test_tables_and_records_claim_classes(self):
        self.assertEqual(checks.check_coverage(content([component()]), {"cu-callout", "cu-callout-tip", "mt-4"}, {"mt-4"}, "fail"), [])

    def test_warn_mode_shows_at_most_ten(self):
        many = {f"c{n:02}" for n in range(15)}
        [finding] = checks.check_coverage(content(), many, set(), "warn")
        self.assertTrue(finding.message.endswith("and 5 more"))


class ReferencesTest(unittest.TestCase):
    def test_valid_references(self):
        good = content([component(tasks=("draw-attention",))], [task()])
        site = Site("Guide", "warn", SITE.groups, ("draw-attention",), SITE.menu)
        self.assertEqual(checks.check_references(good, site, support.THEME), [])

    def test_broken_references(self):
        bad = component(group="layout", tasks=("missing-task",), related=("alert",), scss=("scss/nope.scss",))
        found = messages(checks.check_references(content([bad], [task(components=("button",))]), SITE, support.THEME))
        self.assertIn("error 3 group 'layout' is not in site.toml", found)
        self.assertIn("error 3 task 'missing-task' has no task file", found)
        self.assertIn("error 3 related component 'alert' has no record", found)
        self.assertIn("error 3 SCSS file 'scss/nope.scss' does not exist", found)
        self.assertIn("error 3 component 'button' has no record", found)
        self.assertIn("error 3 task 'draw-attention' is not listed in site.toml tasks", found)

    def test_listed_task_without_a_file(self):
        site = Site("Guide", "warn", SITE.groups, ("ghost",), SITE.menu)
        self.assertIn("error 3 listed task 'ghost' has no task file", messages(checks.check_references(content(), site, support.THEME)))

    def test_menu_needs_its_page(self):
        site = Site("Guide", "warn", SITE.groups, (), (("home", "Home"), ("getting-started", "Getting started")))
        self.assertIn("error 3 menu entry 'getting-started' needs pages/getting-started.md",
                      messages(checks.check_references(content(), site, support.THEME)))

    def test_home_page_is_required(self):
        self.assertIn("error 3 the home page pages/index.md is missing",
                      messages(checks.check_references(content(pages=()), SITE, support.THEME)))


class StaleEvidenceTest(unittest.TestCase):
    def test_newer_scss_warns(self):
        stale = component(scss=("scss/components/_callout.scss",))
        [finding] = checks.check_stale_evidence(content([stale]), lambda path: datetime.date(2026, 9, 28))
        self.assertEqual((finding.level, finding.check), ("warning", 4))
        self.assertIn("changed on 2026-09-28, after the editor evidence of 2026-09-20", finding.message)

    def test_older_scss_is_fine(self):
        fresh = component(scss=("scss/components/_callout.scss",))
        self.assertEqual(checks.check_stale_evidence(content([fresh]), lambda path: datetime.date(2026, 9, 1)), [])

    def test_stale_evidence_ignores_unknown_dates(self):
        unknown = component(scss=("scss/components/_callout.scss",))
        self.assertEqual(checks.check_stale_evidence(content([unknown]), lambda path: None), [])

    def test_git_last_changed_inside_the_repo(self):
        changed = checks.git_last_changed(support.THEME)("scss/components/_callout.scss")
        self.assertIsInstance(changed, datetime.date)

    def test_git_last_changed_outside_a_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "x.scss").write_text("a{}", encoding="utf-8")
            self.assertIsNone(checks.git_last_changed(Path(tmp))("x.scss"))


class ExamplesTest(unittest.TestCase):
    def check(self, markup):
        return messages(checks.check_examples(content([component(examples=(Example("E", "p", markup),))])))

    def test_image_without_alt_warns(self):
        self.assertEqual(self.check('<img src="a.png">'), ["warning 5 example 'E' has an image without alt text"])

    def test_empty_alt_is_allowed(self):
        self.assertEqual(self.check('<img src="a.png" alt="">'), [])

    def test_empty_heading_warns(self):
        self.assertEqual(self.check('<h3><i class="fa-solid fa-star"></i></h3>'), ["warning 5 example 'E' has an empty heading"])

    def test_heading_with_text_is_fine(self):
        self.assertEqual(self.check("<h3>Title</h3>"), [])


class RunAllTest(unittest.TestCase):
    def test_collects_every_check(self):
        findings = checks.run_all(content([component(parts={"cu-gone": "x"})]), SITE, theme_dir=support.THEME,
                                  known=KNOWN, author_facing={"box"}, tables=set(), last_changed=lambda p: None)
        self.assertEqual(sorted({f.check for f in findings}), [1, 2])
        self.assertEqual(str(findings[0]), "ERROR [check 1] components/callout.md: class 'cu-gone' is not defined by the theme or the player's stylesheets")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tests -p "test_checks.py" -v`
Expected: FAIL with `ImportError: cannot import name 'checks' from 'guidelib'`.

- [ ] **Step 3: Write the implementation**

`tools/guidelib/checks.py`:

```python
"""The author guide's five build checks. Each returns findings; any error stops the build.

1 classes exist   2 coverage   3 references   4 stale editor evidence   5 example accessibility
"""
import datetime
import subprocess
from dataclasses import dataclass
from html.parser import HTMLParser


@dataclass(frozen=True)
class Finding:
    level: str  # "error" or "warning"
    check: int
    source: str
    message: str

    def __str__(self):
        return f"{self.level.upper()} [check {self.check}] {self.source}: {self.message}"


class _Scan(HTMLParser):
    """Collects an example's class names, images without alt text and empty headings."""
    HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self):
        super().__init__()
        self.classes, self.images_without_alt, self.empty_headings = set(), 0, 0
        self._heading, self._text = None, ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.classes.update((attrs.get("class") or "").split())
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt += 1
        if tag in self.HEADINGS:
            self._heading, self._text = tag, ""

    def handle_data(self, data):
        if self._heading:
            self._text += data

    def handle_endtag(self, tag):
        if tag == self._heading:
            if not self._text.strip():
                self.empty_headings += 1
            self._heading = None


def scan(markup):
    parser = _Scan()
    parser.feed(markup)
    parser.close()
    return parser


def _examples(content):
    """Every example in the guide, with the file it came from."""
    for component in content.components.values():
        for example in component.examples:
            yield component.source, example
    for task in content.tasks.values():
        yield task.source, task.example


def _claimed(component):
    return set(component.parts) | {e.variant for e in component.examples if e.variant}


def check_classes_exist(content, known):
    """Check 1: every class a record names or an example uses is defined somewhere the guide loads."""
    findings = []
    for component in content.components.values():
        for cls in sorted(_claimed(component) - known):
            findings.append(Finding("error", 1, str(component.source),
                                    f"class '{cls}' is not defined by the theme or the player's stylesheets"))
    for source, example in _examples(content):
        for cls in sorted(scan(example.html).classes - known):
            findings.append(Finding("error", 1, str(source),
                                    f"example '{example.label}' uses class '{cls}', which no stylesheet defines"))
    return findings


def check_coverage(content, author_facing, tables, mode):
    """Check 2: every author-facing class is claimed by a record or shown in a generated table."""
    claimed = set(tables)
    for component in content.components.values():
        claimed |= _claimed(component)
    missing = sorted(author_facing - claimed)
    if not missing:
        return []
    shown = missing if mode == "fail" else missing[:10]
    more = "" if len(shown) == len(missing) else f" and {len(missing) - len(shown)} more"
    return [Finding("error" if mode == "fail" else "warning", 2, "guide",
                    f"{len(missing)} author-facing classes are not covered yet: {', '.join(shown)}{more}")]


def check_references(content, site, theme_dir):
    """Check 3: every group, task, related component, SCSS file and menu page exists."""
    findings = []

    def error(source, message):
        findings.append(Finding("error", 3, str(source), message))

    groups = {group for group, _ in site.groups}
    for component in content.components.values():
        if component.group not in groups:
            error(component.source, f"group '{component.group}' is not in site.toml")
        for name in component.tasks:
            if name not in content.tasks:
                error(component.source, f"task '{name}' has no task file")
        for name in component.related:
            if name not in content.components:
                error(component.source, f"related component '{name}' has no record")
        for path in component.scss:
            if not (theme_dir / path).is_file():
                error(component.source, f"SCSS file '{path}' does not exist")
    for task in content.tasks.values():
        for name in task.components:
            if name not in content.components:
                error(task.source, f"component '{name}' has no record")
    for name in sorted(set(content.tasks) - set(site.tasks)):
        error(content.tasks[name].source, f"task '{name}' is not listed in site.toml tasks")
    for name in site.tasks:
        if name not in content.tasks:
            error("site.toml", f"listed task '{name}' has no task file")
    if "index" not in content.pages:
        error("content/pages", "the home page pages/index.md is missing")
    for page, _ in site.menu:
        if page == "getting-started" and page not in content.pages:
            error("site.toml", "menu entry 'getting-started' needs pages/getting-started.md")
    return findings


def check_stale_evidence(content, last_changed):
    """Check 4: warn when a component's SCSS changed after its editor evidence was recorded."""
    findings = []
    for component in content.components.values():
        for path in component.scss:
            changed = last_changed(path)
            if changed and changed > component.editor.checked:
                findings.append(Finding(
                    "warning", 4, str(component.source),
                    f"{path} changed on {changed.isoformat()}, after the editor evidence of "
                    f"{component.editor.checked.isoformat()}; re-test in Xerte and update [editor]"))
    return findings


def git_last_changed(theme_dir):
    """A function giving the date of the last commit to a path, or None when git cannot say."""
    def last_changed(path):
        try:
            result = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=theme_dir,
                                    capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            return None
        text = result.stdout.strip()
        if result.returncode or not text:
            return None
        try:
            return datetime.date.fromisoformat(text)
        except ValueError:
            return None
    return last_changed


def check_examples(content):
    """Check 5: warn about images without alt text and empty headings in examples."""
    findings = []
    for source, example in _examples(content):
        found = scan(example.html)
        if found.images_without_alt:
            findings.append(Finding("warning", 5, str(source), f"example '{example.label}' has an image without alt text"))
        if found.empty_headings:
            findings.append(Finding("warning", 5, str(source), f"example '{example.label}' has an empty heading"))
    return findings


def run_all(content, site, *, theme_dir, known, author_facing, tables, last_changed):
    return (check_classes_exist(content, known)
            + check_coverage(content, author_facing, tables, site.coverage)
            + check_references(content, site, theme_dir)
            + check_stale_evidence(content, last_changed)
            + check_examples(content))
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" -v`
Expected: all tests `OK`.

- [ ] **Step 5: Commit**

```bash
git add tools/guidelib/checks.py tests/test_checks.py
git commit -m "feat(cardiffuniversity): add the author guide's five build checks"
```

---

### Task 5: Page rendering, the template and the guide's assets

**Files:**
- Create: `tools/guidelib/assets.py` (constants only in this task; `copy_assets` comes in Task 6)
- Create: `tools/guidelib/pages.py`
- Create: `guide/templates/base.html`, `guide/assets/guide.css`, `guide/assets/guide.js`
- Create: `tests/html_tree.py`, `tests/test_pages.py`

**Interfaces:**
- Consumes: `records.*`, `mdsubset.code_block`, `theme_css.PLAYER_CSS`.
- Produces: in `assets`: `STYLESHEETS: tuple[str, ...]`, `SCRIPTS: tuple[str, ...]` (hrefs relative to the site root, in load order), `PLAYER_JS`, `REFERENCED`, `FONTAWESOME`. In `pages`: `TOP_PATHS: dict[str, str]`, `XERTE_PASTE: str`, `Ctx(site, content, template)`, `component_page(ctx, component) -> str`, `task_page(ctx, task) -> str`, `home_page(ctx, page) -> str`, `simple_page(ctx, page, active) -> str`, `components_index(ctx) -> str`, `tasks_index(ctx) -> str`, `write_site(out: Path, site, content, template_path: Path) -> list[str]` (relative paths written). Tests use only `write_site`. In `tests/html_tree.py`: `parse(text) -> Element`; `Element.tag`, `.attrs`, `.classes`, `.text()`, `.find_all(tag=None, cls=None, **attrs)`, `.find(...)` (raises `AssertionError` when nothing matches). Attribute keywords use `_` for `-`, so `aria_current="page"` matches `aria-current="page"`.

- [ ] **Step 1: Write the test helper and the failing test**

`tests/html_tree.py`:

```python
"""A tiny HTML tree for tests: parse a page, then find elements by tag, class or attribute."""
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Element:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []

    @property
    def classes(self):
        return set((self.attrs.get("class") or "").split())

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def iter(self):
        for child in self.children:
            if isinstance(child, Element):
                yield child
                yield from child.iter()

    def find_all(self, tag=None, cls=None, **attrs):
        wanted = {key.replace("_", "-"): value for key, value in attrs.items()}
        return [e for e in self.iter()
                if (tag is None or e.tag == tag) and (cls is None or cls in e.classes)
                and all(e.attrs.get(key) == value for key, value in wanted.items())]

    def find(self, tag=None, cls=None, **attrs):
        found = self.find_all(tag, cls, **attrs)
        if not found:
            raise AssertionError(f"no element matching tag={tag} class={cls} {attrs}")
        return found[0]


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = self.current = Element("#root", [])

    def handle_starttag(self, tag, attrs):
        element = Element(tag, attrs, self.current)
        self.current.children.append(element)
        if tag not in VOID:
            self.current = element

    def handle_startendtag(self, tag, attrs):
        self.current.children.append(Element(tag, attrs, self.current))

    def handle_endtag(self, tag):
        node = self.current
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.current = node.parent

    def handle_data(self, data):
        self.current.children.append(data)


def parse(text):
    builder = _Builder()
    builder.feed(text)
    builder.close()
    return builder.root
```

`tests/test_pages.py`:

```python
import tempfile
import unittest
from pathlib import Path

import support
import guide_fixture as fx
from guidelib import pages, records
from html_tree import parse

PLAYER_ORDER = ["vendor/player/css/bootstrap.css", "vendor/player/css/bootstrap-responsive.css",
                "vendor/player/css/custom.css", "vendor/player/fontawesome-6.6.0/css/all.min.css",
                "vendor/player/fontawesome-6.6.0/css/v4-shims.min.css",
                "vendor/player/fontawesome-6.6.0/css/v5-font-face.min.css",
                "vendor/theme/cardiffuniversity.css", "assets/guide.css"]


class WrittenSiteTest(unittest.TestCase):
    """Writes the fixture guide with pages.write_site() and reads the pages back."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        guide = fx.write_guide(cls.tmp.name)
        cls.content = records.load_content(guide / "content")
        cls.out = Path(cls.tmp.name) / "site"
        cls.written = pages.write_site(cls.out, records.load_site(guide / "site.toml"), cls.content,
                                       support.GUIDE / "templates" / "base.html")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def page(self, relative):
        return parse((self.out / relative).read_text(encoding="utf-8"))

    def section(self, page, heading):
        for section in page.find_all("section"):
            if section.find_all("h2") and section.find("h2").text() == heading:
                return section
        raise AssertionError(f"no section headed {heading!r}")

    def test_writes_every_page(self):
        self.assertEqual(self.written, ["components/callout.html", "components/index.html", "getting-started.html",
                                        "index.html", "tasks/draw-attention.html", "tasks/index.html"])

    def test_preview_renders_the_first_example(self):
        preview = self.section(self.page("components/callout.html"), "Preview and code").find(cls="g-preview")
        self.assertEqual(preview.find(cls="cu-callout-title").text(), "Tip")

    def test_code_view_shows_source_literally(self):
        section = self.section(self.page("components/callout.html"), "Preview and code")
        code = section.find(cls="g-code-wrap").find("code")
        self.assertEqual(code.text(), self.content.components["callout"].examples[0].html)
        self.assertIn("Fish &amp; chips.", code.text())
        self.assertIn("Fish & chips.", section.find(cls="g-preview").text())

    def test_paste_instruction_uses_the_glossary(self):
        self.assertIn("add a Text content item, open its Source view",
                      self.section(self.page("components/callout.html"), "Preview and code").text())

    def test_variants_table(self):
        rows = self.section(self.page("components/callout.html"), "Variants").find("tbody").find_all("tr")
        self.assertEqual([[td.text() for td in row.find_all("td")] for row in rows],
                         [[".cu-callout-tip", "Tip", "A shortcut or recommendation"],
                          [".cu-callout-warning", "Warning", "A risk the reader must avoid"]])

    def test_parts_table(self):
        rows = self.section(self.page("components/callout.html"), "Parts").find("tbody").find_all("tr")
        self.assertEqual([row.find("td").text() for row in rows], [".cu-callout", ".cu-callout-title", ".cu-callout-icon"])

    def test_editor_evidence(self):
        meta = self.page("components/callout.html").find(cls="g-meta").text()
        self.assertIn("Survives the Xerte editor", meta)
        self.assertIn("checked 20 September 2026", meta)
        self.assertIn("Xerte 3.14", meta)

    def test_do_and_dont(self):
        section = self.section(self.page("components/callout.html"), "When to use it")
        self.assertEqual([li.text() for li in section.find(cls="g-do").find_all("li")], ["Name the variant in the title."])
        self.assertEqual([li.text() for li in section.find(cls="g-dont").find_all("li")], ["Stack more than two."])

    def test_on_this_page_links_resolve(self):
        page = self.page("components/callout.html")
        ids = {e.attrs["id"] for e in page.iter() if "id" in e.attrs}
        targets = [a.attrs["href"][1:] for a in page.find(cls="g-toc").find_all("a")]
        self.assertEqual(targets, ["preview", "variants", "parts", "when-to-use-it", "accessibility", "related"])
        self.assertLessEqual(set(targets), ids)

    def test_side_menu_marks_the_current_component(self):
        current = self.page("components/callout.html").find(cls="g-side").find("a", aria_current="page")
        self.assertEqual(current.text(), "Callouts")

    def test_top_menu(self):
        menu = self.page("components/callout.html").find(cls="g-top")
        self.assertEqual([a.text() for a in menu.find_all("a")], ["Home", "Getting started", "Tasks", "Components"])
        self.assertEqual(menu.find("a", aria_current="page").text(), "Components")

    def test_stylesheets_load_in_player_order_then_the_theme(self):
        for relative, prefix in (("index.html", ""), ("components/callout.html", "../")):
            hrefs = [link.attrs["href"] for link in self.page(relative).find_all("link", rel="stylesheet")]
            self.assertEqual(hrefs, [prefix + href for href in PLAYER_ORDER])

    def test_page_links_resolve(self):
        for relative in self.written:
            for element in self.page(relative).iter():
                target = element.attrs.get("href") or ""
                if element.tag != "a" or not target or target.startswith(("#", "http:", "https:", "mailto:")):
                    continue
                path = (self.out / relative).parent / target.split("#")[0]
                self.assertTrue(path.resolve().is_file(), f"{relative} links to missing {target}")

    def test_home_tiles_and_new_steps(self):
        home = self.page("index.html")
        tile = home.find(cls="g-task")
        self.assertEqual(tile.find("a").text(), "Draw attention to something")
        self.assertEqual(tile.find(cls="g-uses").text(), "Uses: callouts")
        self.assertEqual(home.find(cls="g-new").find("a").attrs["href"], "getting-started.html")
        self.assertEqual([li.find("strong").text() for li in home.find(cls="g-steps").find_all("li")], ["Choose", "Check"])

    def test_task_page(self):
        page = self.page("tasks/draw-attention.html")
        self.assertEqual(self.section(page, "Components to use").find("a").text(), "Callouts")
        example = self.section(page, "Worked example: An upload reminder")
        self.assertEqual(example.find(cls="g-preview").find(cls="cu-callout-title").text(), "Important")
        self.assertEqual([li.text() for li in self.section(page, "Checklist").find_all("li")], ["The title names the variant."])

    def test_getting_started(self):
        page = self.page("getting-started.html")
        links = page.find(cls="g-toc").find_all("a")
        self.assertEqual([a.text() for a in links], ["Choose the theme", "Brand colours"])
        headings = {h.attrs.get("id"): h.text() for h in page.find(cls="g-main").find_all("h2")}
        for a in links:
            self.assertEqual(headings.get(a.attrs["href"][1:]), a.text())
        self.assertIn(":root { --color-brand-primary: #00703C; }", page.find("code", cls="language-css").text())

    def test_every_page_has_one_main_and_one_h1(self):
        for relative in self.written:
            page = self.page(relative)
            self.assertEqual(len(page.find_all(id="main")), 1, relative)
            self.assertEqual(len(page.find_all("h1")), 1, relative)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tests -p "test_pages.py" -v`
Expected: FAIL with `ImportError: cannot import name 'pages' from 'guidelib'`.

- [ ] **Step 3: Write `tools/guidelib/assets.py` (constants)**

```python
"""What each guide page loads, and copying it into the built site.

Pages link the player's stylesheets in the player's order, then the theme (the player appends it
last), then the guide's own stylesheet, which styles only the guide navigation. Paths under
vendor/player/ mirror the player's common/ folder, so the stylesheets' relative url()s still work.
"""
import shutil

import theme_css

FONTAWESOME = "fontawesome-6.6.0"
PLAYER_JS = ("js/jquery-1.9.1.min.js", "js/bootstrap.js")
# Files the player's stylesheets reach through @import or url(), and Font Awesome's licence.
REFERENCED = ("css/editorstyles.css", "img/glyphicons-halflings.png", "img/glyphicons-halflings-white.png",
              f"{FONTAWESOME}/LICENSE.txt")

STYLESHEETS = (tuple(f"vendor/player/{name}" for name in theme_css.PLAYER_CSS)
               + ("vendor/theme/cardiffuniversity.css", "assets/guide.css"))
SCRIPTS = tuple(f"vendor/player/{name}" for name in PLAYER_JS) + ("assets/guide.js",)
```

- [ ] **Step 4: Write the template**

`guide/templates/base.html`:

```html
<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title · $site_title</title>
$styles
</head>
<body class="g-body">
<a class="g-skip" href="#main">Skip to content</a>
<header class="g-header">
  <a class="g-brand" href="${root}index.html">$site_title</a>
</header>
$top_menu
$body
<footer class="g-footer">
  <p>$site_title. Examples use the compiled Cardiff University Theme and the Xerte player's own stylesheets.</p>
</footer>
$scripts
</body>
</html>
```

- [ ] **Step 5: Write `tools/guidelib/pages.py`**

```python
"""Render the author guide's pages from loaded records.

Component pages follow design direction A (side menu, page, "on this page" list). The home page
and task pages follow direction B. Every page uses guide/templates/base.html.
"""
import html
from dataclasses import dataclass
from string import Template

from guidelib import assets
from guidelib.mdsubset import code_block

TOP_PATHS = {"home": "index.html", "getting-started": "getting-started.html",
             "tasks": "tasks/index.html", "components": "components/index.html"}
XERTE_PASTE = "In Xerte: add a Text content item, open its Source view, then paste."


@dataclass(frozen=True)
class Ctx:
    site: object
    content: object
    template: Template


def esc(text):
    return html.escape(text, quote=True)


def long_date(day):
    return f"{day.day} {day:%B %Y}"


def _current(on):
    return ' aria-current="page"' if on else ""


def page_shell(ctx, *, title, root, active, body):
    styles = "\n".join(f'<link rel="stylesheet" href="{root}{href}">' for href in assets.STYLESHEETS)
    scripts = "\n".join(f'<script src="{root}{src}"></script>' for src in assets.SCRIPTS)
    return ctx.template.substitute(title=esc(title), site_title=esc(ctx.site.title), root=root, styles=styles,
                                   scripts=scripts, top_menu=top_menu(ctx, root, active), body=body)


def top_menu(ctx, root, active):
    links = "".join(f'<a href="{root}{TOP_PATHS[key]}"{_current(key == active)}>{esc(label)}</a>'
                    for key, label in ctx.site.menu)
    return f'<nav class="g-top" aria-label="Guide sections">{links}</nav>'


def ordered_components(ctx):
    """[(group title, [components sorted by title]), ...] in site.toml's group order."""
    out = []
    for group, title in ctx.site.groups:
        members = sorted((c for c in ctx.content.components.values() if c.group == group), key=lambda c: c.title)
        if members:
            out.append((title, members))
    return out


def side_menu(ctx, root, active):
    blocks = []
    for title, members in ordered_components(ctx):
        items = "".join(f'<li><a href="{root}components/{c.name}.html"{_current(c.name == active)}>{esc(c.title)}</a></li>'
                        for c in members)
        blocks.append(f"<h2>{esc(title)}</h2><ul>{items}</ul>")
    return ('<nav class="g-side" aria-label="Components">'
            '<button class="g-side-toggle" type="button" aria-expanded="true" aria-controls="g-side-list" hidden>'
            'Components menu</button>'
            f'<div class="g-side-list" id="g-side-list">{"".join(blocks)}</div></nav>')


def on_this_page(entries):
    items = "".join(f'<li><a href="#{slug}">{esc(title)}</a></li>' for slug, title in entries)
    return f'<nav class="g-toc" aria-label="On this page"><h2>On this page</h2><ol>{items}</ol></nav>'


def preview(markup):
    return ('<p class="g-preview-label">Preview</p>'
            f'<div class="g-preview" role="group" aria-label="Rendered example">{markup}</div>')


def table(headers, rows):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    return f'<table class="g-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'


def editor_text(editor):
    verdict = "Survives the Xerte editor" if editor.survives else "Changed by the Xerte editor"
    return f"{verdict} · checked {long_date(editor.checked)} · Xerte {editor.xerte}"


def related_links(ctx, component, root):
    links = [f'<a href="{name}.html">{esc(ctx.content.components[name].title)}</a>' for name in component.related]
    links += [f'<a href="{root}tasks/{name}.html">Task: {esc(ctx.content.tasks[name].title)}</a>' for name in component.tasks]
    items = "".join(f"<li>{link}</li>" for link in links)
    return f'<ul class="g-related">{items}</ul>' if links else ""


def pager(ctx, component):
    flat = [c for _, members in ordered_components(ctx) for c in members]
    if len(flat) < 2:
        return ""
    names = [c.name for c in flat]
    i = names.index(component.name)
    before = f'<a href="{flat[i - 1].name}.html">&larr; {esc(flat[i - 1].title)}</a>' if i > 0 else "<span></span>"
    after = f'<a href="{flat[i + 1].name}.html">{esc(flat[i + 1].title)} &rarr;</a>' if i < len(flat) - 1 else "<span></span>"
    return f'<nav class="g-pager" aria-label="Previous and next">{before}{after}</nav>'


def component_page(ctx, component):
    root = "../"
    first = component.examples[0]
    variants = [e for e in component.examples if e.variant]
    chips = "".join(f'<span class="g-chip">{chip}</span>' for chip in (
        esc(component.status.capitalize()), f"Since {esc(component.since)}", esc(editor_text(component.editor)),
        f"Class: <code>.{esc(next(iter(component.parts)))}</code>"))
    parts = [("preview", "Preview and code",
              preview(first.html) + code_block(first.html) + f'<p class="g-note">{XERTE_PASTE}</p>')]
    if variants:
        rows = "".join(f"<tr><td><code>.{esc(e.variant)}</code></td><td>{esc(e.label)}</td><td>{esc(e.purpose)}</td></tr>"
                       for e in variants)
        parts.append(("variants", "Variants",
                      preview("".join(e.html for e in variants)) + table(("Class", "Variant", "Use it for"), rows)))
    part_rows = "".join(f"<tr><td><code>.{esc(cls)}</code></td><td>{esc(what)}</td></tr>"
                        for cls, what in component.parts.items())
    parts.append(("parts", "Parts", table(("Class", "What it is"), part_rows)))
    parts.append(("when-to-use-it", "When to use it",
                  component.when_intro + '<div class="g-cols"><div class="g-do"><h3>Do</h3>' + component.do_html
                  + "</div><div class=\"g-dont\"><h3>Don't</h3>" + component.dont_html + "</div></div>"))
    parts.append(("accessibility", "Accessibility", component.accessibility_html))
    related = related_links(ctx, component, root)
    if related:
        parts.append(("related", "Related", related))
    sections = "".join(f'<section aria-labelledby="{sid}"><h2 id="{sid}">{esc(title)}</h2>{body}</section>'
                       for sid, title, body in parts)
    main = (f'<p class="g-crumb"><a href="index.html">Components</a> &rsaquo; {esc(component.title)}</p>'
            f'<h1>{esc(component.title)}</h1><p class="g-lead">{esc(component.lead)}</p>'
            f'<div class="g-meta">{chips}</div>{sections}{pager(ctx, component)}')
    body = (f'<div class="g-shell">{side_menu(ctx, root, component.name)}'
            f'<main id="main" class="g-main">{main}</main>'
            f'{on_this_page([(sid, title) for sid, title, _ in parts])}</div>')
    return page_shell(ctx, title=component.title, root=root, active="components", body=body)


def task_tiles(ctx, root):
    tiles = []
    for name in ctx.site.tasks:
        task = ctx.content.tasks[name]
        uses = ", ".join(ctx.content.components[c].title.lower() for c in task.components)
        tiles.append(f'<li class="g-task"><i class="fa-solid {esc(task.icon)}" aria-hidden="true"></i>'
                     f'<h3><a href="{root}tasks/{task.name}.html">{esc(task.title)}</a></h3>'
                     f'<p>{esc(task.summary)}</p><p class="g-uses">Uses: {esc(uses)}</p></li>')
    return f'<ul class="g-tasks">{"".join(tiles)}</ul>'


def _section_html(section):
    if not section.level:
        return section.html
    return f'<h{section.level} id="{section.slug}">{esc(section.title)}</h{section.level}>{section.html}'


def home_page(ctx, page):
    root = ""
    aside = ""
    if page.new_steps and "getting-started" in ctx.content.pages:
        steps = "".join(f"<li>{esc(step)}</li>" for step in page.new_steps)
        aside = ('<aside class="g-new" aria-labelledby="g-new-title"><h2 id="g-new-title">New to the theme?</h2>'
                 f'<ol>{steps}</ol><p><a href="getting-started.html">Start here</a></p></aside>')
    how = "".join(f"<li><strong>{esc(title)}</strong> <span>{esc(text)}</span></li>" for title, text in page.how)
    how_block = (f'<section class="g-band" aria-labelledby="how-title"><h2 id="how-title">How each task works</h2>'
                 f'<ol class="g-steps">{how}</ol></section>') if how else ""
    body = (f'<main id="main"><section class="g-hero"><div class="g-wrap g-hero-grid"><div>'
            f'<h1>{esc(page.title)}</h1><p class="g-lead">{esc(page.lead)}</p></div>{aside}</div></section>'
            f'<div class="g-wrap"><section class="g-band" aria-labelledby="tasks-title">'
            f'<h2 id="tasks-title">Common tasks</h2>{task_tiles(ctx, root)}</section>{how_block}'
            f'{"".join(_section_html(s) for s in page.sections)}</div></main>')
    return page_shell(ctx, title=page.title, root=root, active="home", body=body)


def task_page(ctx, task):
    root = "../"
    cards = "".join(f'<li class="g-card"><a href="{root}components/{name}.html">{esc(ctx.content.components[name].title)}</a>'
                    f'<p>{esc(ctx.content.components[name].lead)}</p></li>' for name in task.components)
    example = task.example
    body = (f'<main id="main" class="g-wrap g-page">'
            f'<p class="g-crumb"><a href="index.html">Tasks</a> &rsaquo; {esc(task.title)}</p>'
            f'<h1>{esc(task.title)}</h1><p class="g-lead">{esc(task.summary)}</p>'
            f'<section aria-labelledby="goal"><h2 id="goal">Goal</h2>{task.goal_html}</section>'
            f'<section aria-labelledby="use"><h2 id="use">Components to use</h2><ul class="g-cards">{cards}</ul></section>'
            f'<section aria-labelledby="example"><h2 id="example">Worked example: {esc(example.label)}</h2>'
            f'<p>{esc(example.purpose)}</p>{preview(example.html)}{code_block(example.html)}'
            f'<p class="g-note">{XERTE_PASTE}</p></section>'
            f'<section aria-labelledby="checklist"><h2 id="checklist">Checklist</h2>'
            f'<div class="g-checklist">{task.checklist_html}</div></section></main>')
    return page_shell(ctx, title=task.title, root=root, active="tasks", body=body)


def simple_page(ctx, page, active):
    root = ""
    content = "".join(_section_html(s) for s in page.sections)
    toc = on_this_page([(s.slug, s.title) for s in page.sections if s.level == 2])
    body = (f'<div class="g-shell g-shell-doc"><main id="main" class="g-main"><h1>{esc(page.title)}</h1>'
            f'<p class="g-lead">{esc(page.lead)}</p>{content}</main>{toc}</div>')
    return page_shell(ctx, title=page.title, root=root, active=active, body=body)


def components_index(ctx):
    root = "../"
    groups = "".join(
        f"<h2>{esc(title)}</h2><ul class=\"g-cards\">"
        + "".join(f'<li class="g-card"><a href="{c.name}.html">{esc(c.title)}</a><p>{esc(c.lead)}</p></li>' for c in members)
        + "</ul>" for title, members in ordered_components(ctx))
    body = (f'<div class="g-shell g-shell-two">{side_menu(ctx, root, None)}<main id="main" class="g-main">'
            f'<h1>Components</h1><p class="g-lead">Every component the guide covers so far, grouped by what it is for.</p>'
            f'{groups}</main></div>')
    return page_shell(ctx, title="Components", root=root, active="components", body=body)


def tasks_index(ctx):
    root = "../"
    body = (f'<main id="main" class="g-wrap g-page"><h1>Tasks</h1>'
            f'<p class="g-lead">Start from what you want to do.</p>{task_tiles(ctx, root)}</main>')
    return page_shell(ctx, title="Tasks", root=root, active="tasks", body=body)


def write_site(out, site, content, template_path):
    ctx = Ctx(site, content, Template(template_path.read_text(encoding="utf-8")))
    rendered = {"index.html": home_page(ctx, content.pages["index"]),
                "components/index.html": components_index(ctx), "tasks/index.html": tasks_index(ctx)}
    for name, page in content.pages.items():
        if name != "index":
            rendered[f"{name}.html"] = simple_page(ctx, page, name if name in TOP_PATHS else None)
    for component in content.components.values():
        rendered[f"components/{component.name}.html"] = component_page(ctx, component)
    for task in content.tasks.values():
        rendered[f"tasks/{task.name}.html"] = task_page(ctx, task)
    for relative, text in rendered.items():
        path = out / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return sorted(rendered)
```

- [ ] **Step 6: Write the guide's stylesheet**

`guide/assets/guide.css`:

```css
/* Author guide: the guide navigation and page layout only. The theme styles everything else,
   including every example. Only g- classes here, never Bootstrap class names, so the theme's
   rules for those cannot reshape the guide. Colours come from the theme's --cu-* roles. */

/* The theme makes body a flex container for the player's layout. Guide pages are plain
   documents, and as flex items their columns would grow to fit the longest line of code. */
.g-body { display: block; margin: 0; padding: 0; background: var(--cu-bg); color: var(--cu-ink); }
.g-body [hidden] { display: none !important; }

.g-skip { position: absolute; left: -9999px; top: 8px; z-index: 100; padding: 8px 12px; background: var(--cu-white); color: var(--cu-ink); }
.g-skip:focus { left: 8px; }

.g-header { padding: 16px 32px; background: var(--cu-white); border-bottom: 4px solid var(--color-brand-primary); }
.g-brand { font: 700 22px/1.2 var(--cu-display); color: var(--cu-ink); text-decoration: none; }
.g-brand:hover { text-decoration: underline; }

.g-top { display: flex; flex-wrap: wrap; padding: 0 32px; background: var(--cu-grey-90); }
.g-top a { padding: 12px 18px; color: var(--cu-white); text-decoration: none; border-bottom: 3px solid transparent; }
.g-top a:hover { background: var(--cu-grey-80); }
.g-top a[aria-current="page"] { border-bottom-color: var(--color-brand-primary); font-weight: 700; }
.g-top a:focus-visible { outline: 3px solid var(--cu-white); outline-offset: -3px; }

.g-shell { display: grid; grid-template-columns: 270px minmax(0, 1fr) 220px; max-width: 1480px; margin: 0 auto; }
.g-shell-two { grid-template-columns: 270px minmax(0, 1fr); }
.g-shell-doc { grid-template-columns: minmax(0, 1fr) 220px; max-width: 1180px; }
.g-main { min-width: 0; padding: 32px 48px 80px; }
.g-wrap { max-width: 1180px; margin: 0 auto; padding: 0 24px; }
.g-page { padding-top: 32px; padding-bottom: 80px; }

.g-side { align-self: start; position: sticky; top: 0; max-height: 100vh; overflow: auto; padding: 24px 0; border-right: 1px solid var(--cu-line); }
.g-side h2 { margin: 20px 24px 6px; padding: 0; border: 0; font-size: 14px; letter-spacing: .06em; text-transform: uppercase; color: var(--cu-grey-80); }
.g-side ul { list-style: none; margin: 0; padding: 0; }
.g-side a { display: block; padding: 7px 24px; color: var(--cu-ink); text-decoration: none; border-left: 3px solid transparent; }
.g-side a:hover { background: var(--cu-surface); }
.g-side a[aria-current="page"] { border-left-color: var(--color-brand-primary); background: var(--cu-surface); font-weight: 700; }
.g-side-toggle { width: calc(100% - 32px); margin: 0 16px; padding: 10px 14px; background: var(--cu-white); color: var(--cu-ink); border: 1px solid var(--cu-grey-80); font-size: 16px; text-align: left; }

.g-toc { align-self: start; position: sticky; top: 0; padding: 32px 24px; border-left: 1px solid var(--cu-line); }
.g-toc h2 { margin: 0 0 8px; padding: 0; border: 0; font-size: 14px; letter-spacing: .06em; text-transform: uppercase; color: var(--cu-grey-80); }
.g-toc ol { list-style: none; margin: 0; padding: 0; }
.g-toc a { display: block; padding: 5px 0; color: var(--cu-ink); }

.g-side a:focus-visible, .g-toc a:focus-visible, .g-side-toggle:focus-visible, .g-brand:focus-visible { outline: 3px solid var(--cu-ink); outline-offset: 2px; }

.g-crumb { margin: 0 0 8px; color: var(--cu-grey-80); }
.g-lead { margin: 0 0 16px; font-size: 20px; }
.g-meta { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 24px; }
.g-chip { padding: 3px 10px; border: 1px solid var(--cu-grey-80); font-size: 16px; }
.g-main section > h2, .g-page section > h2 { margin-top: 48px; padding-top: 16px; border-top: 2px solid var(--cu-grey-90); }
.g-note { margin-top: 8px; color: var(--cu-grey-80); }

.g-preview-label { display: inline-block; margin: 16px 0 0; padding: 6px 12px; background: var(--cu-surface); border: 1px solid var(--cu-line); border-bottom: 0; font-size: 14px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--cu-grey-80); }
.g-preview { padding: 24px; border: 1px solid var(--cu-line); background: var(--cu-white); }

.g-code-wrap { position: relative; }
.g-code { margin: 0; padding: 16px 88px 16px 16px; overflow-x: auto; background: var(--cu-black); color: var(--cu-white); border: 0; border-radius: 0; font: 15px/1.5 ui-monospace, Menlo, Consolas, monospace; white-space: pre; word-break: normal; word-wrap: normal; }
.g-code code { padding: 0; background: none; color: inherit; border: 0; font: inherit; white-space: inherit; }
.g-copy { position: absolute; top: 8px; right: 8px; padding: 6px 10px; background: var(--cu-white); color: var(--cu-ink); border: 0; font-size: 14px; cursor: pointer; }
.g-copy:focus-visible { outline: 3px solid var(--cu-white); outline-offset: 2px; }

.g-table { width: 100%; margin-top: 16px; border-collapse: collapse; }
.g-table th, .g-table td { padding: 8px 12px; border: 1px solid var(--cu-line); text-align: left; vertical-align: top; }
.g-table th { background: var(--cu-surface); }

.g-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 16px; }
.g-do, .g-dont { padding: 16px; background: var(--cu-surface); border-top: 4px solid; }
.g-do { border-top-color: var(--cu-callout-good); }
.g-dont { border-top-color: var(--cu-error); }
.g-do h3, .g-dont h3 { margin-top: 0; font-size: 18px; }

.g-related, .g-cards, .g-tasks { list-style: none; margin: 16px 0 0; padding: 0; }
.g-related li { margin: 0 0 6px; }
.g-cards, .g-tasks { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }
.g-card, .g-task { position: relative; padding: 20px; border: 1px solid var(--cu-line); border-top: 4px solid var(--cu-ink); background: var(--cu-white); }
.g-card a, .g-task h3 a { font-weight: 700; color: var(--cu-ink); }
.g-task h3 { margin: 8px 0; font-size: 20px; }
.g-task i { font-size: 24px; }
.g-task p { margin: 0 0 8px; }
.g-uses { color: var(--cu-grey-80); font-size: 16px; }

.g-hero { background: var(--cu-surface); border-bottom: 4px solid var(--color-brand-primary); }
.g-hero-grid { display: grid; grid-template-columns: 7fr 5fr; gap: 48px; align-items: center; padding-top: 56px; padding-bottom: 48px; }
.g-new { padding: 20px; background: var(--cu-white); border-top: 4px solid var(--cu-ink); }
.g-new h2 { margin: 0 0 8px; padding: 0; border: 0; font-size: 20px; }
.g-band { padding-top: 48px; }
.g-steps { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; margin: 16px 0 0; padding: 0; list-style: none; counter-reset: step; }
.g-steps li { padding-top: 12px; border-top: 4px solid var(--cu-ink); counter-increment: step; }
.g-steps li::before { content: counter(step); display: block; margin-bottom: 6px; font: 700 32px/1 var(--cu-display); }
.g-steps strong, .g-steps span { display: block; }

.g-pager { display: flex; justify-content: space-between; margin-top: 64px; padding-top: 16px; border-top: 1px solid var(--cu-line); }
.g-footer { margin-top: 64px; padding: 24px 32px; background: var(--cu-surface); border-top: 4px solid var(--cu-grey-90); font-size: 16px; }

@media (max-width: 1100px) {
  .g-shell { grid-template-columns: 240px minmax(0, 1fr); }
  .g-shell-doc { grid-template-columns: minmax(0, 1fr); }
  .g-toc { display: none; }
}

@media (max-width: 800px) {
  .g-shell, .g-shell-two { grid-template-columns: minmax(0, 1fr); }
  .g-side { position: static; max-height: none; padding: 12px 0; border-right: 0; border-bottom: 1px solid var(--cu-line); }
  .g-main { padding: 24px 16px 64px; }
  .g-header, .g-top { padding-left: 16px; padding-right: 16px; }
  .g-wrap { padding: 0 16px; }
  .g-cols, .g-hero-grid { grid-template-columns: minmax(0, 1fr); }
  .g-hero-grid { padding-top: 32px; padding-bottom: 32px; }
}
```

- [ ] **Step 7: Write the guide's script**

`guide/assets/guide.js`:

```javascript
// Author guide: copy buttons and the phone-width component menu. The page works without this
// script: the buttons stay hidden and the menu stays open.
(function () {
  "use strict";

  document.querySelectorAll(".g-code-wrap").forEach(function (wrap) {
    var button = wrap.querySelector(".g-copy");
    var code = wrap.querySelector("code");
    if (!button || !code || !navigator.clipboard) return;
    button.hidden = false;
    button.addEventListener("click", function () {
      navigator.clipboard.writeText(code.textContent).then(function () {
        button.textContent = "Copied";
      }, function () {
        button.textContent = "Copy failed: select the code instead";
      });
      window.setTimeout(function () { button.textContent = "Copy"; }, 2000);
    });
  });

  var side = document.querySelector(".g-side");
  if (!side) return;
  var toggle = side.querySelector(".g-side-toggle");
  var list = side.querySelector(".g-side-list");
  var narrow = window.matchMedia("(max-width: 800px)");

  function show(open) {
    toggle.setAttribute("aria-expanded", String(open));
    list.hidden = !open;
  }
  function apply() {
    toggle.hidden = !narrow.matches;
    show(!narrow.matches);
  }
  toggle.addEventListener("click", function () {
    show(toggle.getAttribute("aria-expanded") !== "true");
  });
  narrow.addEventListener("change", apply);
  apply();
})();
```

- [ ] **Step 8: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" -v`
Expected: all tests `OK`.

- [ ] **Step 9: Commit**

```bash
git add tools/guidelib/assets.py tools/guidelib/pages.py guide/templates/base.html guide/assets/guide.css guide/assets/guide.js tests/html_tree.py tests/test_pages.py
git commit -m "feat(cardiffuniversity): render the author guide's pages"
```

---

### Task 6: The build command

**Files:**
- Modify: `tools/guidelib/assets.py` (add `copy_assets`)
- Create: `tools/build-guide.py`
- Modify: `build.sh`, `.gitignore`
- Create: `tests/test_build_guide.py`

**Interfaces:**
- Consumes: everything above.
- Produces: `assets.copy_assets(out: Path, guide_assets: Path) -> None`. In `build-guide.py`: `GUIDE`, `SITE`, `MARKER = ".guide-build"`, `build(guide_dir=GUIDE, out=SITE, check_only=False, last_changed=None) -> int` (0 or 1), `main(argv=None) -> int`. `./build.sh guide`.

- [ ] **Step 1: Write the failing test**

`tests/test_build_guide.py`:

```python
import contextlib
import io
import re
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

    def test_refuses_to_delete_a_foreign_folder(self):
        self.out.mkdir()
        keep = self.out / "keep.txt"
        keep.write_text("mine", encoding="utf-8")
        code, printed = self.build()
        self.assertEqual(code, 1)
        self.assertIn("refusing to delete", printed)
        self.assertTrue(keep.exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tests -p "test_build_guide.py" -v`
Expected: FAIL with `FileNotFoundError` for `tools/build-guide.py`.

- [ ] **Step 3: Add `copy_assets` to `tools/guidelib/assets.py`**

Append:

```python
def copy_assets(out, guide_assets):
    """Copy the player's files, the theme and the guide's own assets into the built site."""
    player = out / "vendor" / "player"
    for name in theme_css.PLAYER_CSS + PLAYER_JS + REFERENCED:
        _copy(theme_css.PLAYER / name, player / name)
    shutil.copytree(theme_css.PLAYER / FONTAWESOME / "webfonts", player / FONTAWESOME / "webfonts", dirs_exist_ok=True)
    _copy(theme_css.CSS, out / "vendor" / "theme" / "cardiffuniversity.css")
    shutil.copytree(guide_assets, out / "assets", dirs_exist_ok=True)


def _copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
```

- [ ] **Step 4: Write `tools/build-guide.py`**

```python
#!/usr/bin/env python3
"""Build the author guide into site/, after running its five checks.

Usage (from anywhere):
    python3 tools/build-guide.py            check, then build into site/
    python3 tools/build-guide.py --check    check only; exit 1 on any error
    python3 tools/build-guide.py --out DIR  build somewhere else

Errors stop the build and nothing is written. Warnings are printed and the build continues.
Standard library only; needs Python 3.11 or later for tomllib.
"""
import sys

if sys.version_info < (3, 11):
    sys.exit("build-guide.py needs Python 3.11 or later (for tomllib).")

import argparse  # noqa: E402
import shutil  # noqa: E402
from pathlib import Path  # noqa: E402

import theme_css  # noqa: E402
from guidelib import assets, checks, pages, records  # noqa: E402
from guidelib.mdsubset import MarkdownError  # noqa: E402

GUIDE = theme_css.THEME / "guide"
SITE = theme_css.THEME / "site"
MARKER = ".guide-build"


def build(guide_dir=GUIDE, out=SITE, check_only=False, last_changed=None):
    guide_dir, out = Path(guide_dir), Path(out)
    try:
        site = records.load_site(guide_dir / "site.toml")
        content = records.load_content(guide_dir / "content")
    except (records.RecordError, MarkdownError, OSError) as error:
        print(f"ERROR {error}")
        return 1
    findings = checks.run_all(
        content, site, theme_dir=theme_css.THEME, known=theme_css.stack_classes(),
        author_facing=theme_css.author_facing_classes(), tables=set(),
        last_changed=last_changed or checks.git_last_changed(theme_css.THEME))
    for finding in findings:
        print(finding)
    errors = sum(f.level == "error" for f in findings)
    warnings = len(findings) - errors
    if errors:
        print(f"Guide not built: {errors} error(s).")
        return 1
    if check_only:
        print(f"Guide checks passed ({warnings} warning(s)).")
        return 0
    if out.exists():
        if any(out.iterdir()) and not (out / MARKER).exists():
            print(f"ERROR {out} is not empty and was not made by this tool; refusing to delete it.")
            return 1
        shutil.rmtree(out)
    written = pages.write_site(out, site, content, guide_dir / "templates" / "base.html")
    assets.copy_assets(out, guide_dir / "assets")
    (out / MARKER).write_text("Built by tools/build-guide.py. This folder is replaced on every build.\n",
                              encoding="utf-8")
    print(f"Built {out} ({len(written)} pages, {warnings} warning(s)).")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build the Cardiff University Theme's author guide.")
    parser.add_argument("--check", action="store_true", help="run the checks without writing the site")
    parser.add_argument("--out", type=Path, default=SITE, help="output folder (default: site/)")
    args = parser.parse_args(argv)
    return build(out=args.out.resolve(), check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Wire it into `build.sh` and pin Sass**

In `build.sh`, change the usage comment block (lines 4-6) to:

```bash
#   ./build.sh            tokens.json -> scss/_cu-tokens.scss, compile SCSS into
#                         themes/site/cardiffuniversity/cardiffuniversity.css, check the author guide
#   ./build.sh package    the same, then zip the runtime folder into dist/cardiffuniversity.zip
#   ./build.sh guide      the same, then check and build the author guide into site/
```

Change line 18 from `npx -y sass@1 --no-source-map` to:

```bash
# Pinned so CI's compile matches the committed CSS byte for byte. Update both together.
npx -y sass@1.104.1 --no-source-map "$HERE/$NAME.scss" "$RUNTIME/$NAME.css"
```

Insert before the `if [ "${1:-}" = "package" ]` block:

```bash
if [ "${1:-}" = "guide" ]; then
    python3 "$HERE/tools/build-guide.py"
fi
```

Append to `.gitignore`:

```
site/
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" -v`
Expected: all tests `OK`.

Run: `./build.sh` then `git status --short`
Expected: the build prints `Compiled ...` and `In sync`; `git status` shows only the files this task changed (the CSS is unchanged, which proves the pinned Sass matches).

- [ ] **Step 7: Commit**

```bash
git add tools/guidelib/assets.py tools/build-guide.py build.sh .gitignore tests/test_build_guide.py
git commit -m "feat(cardiffuniversity): add ./build.sh guide to check and build the author guide"
```

---

### Task 7: Phase 1 content

**Files:**
- Create: `guide/site.toml`, `guide/content/components/callout.md`, `guide/content/tasks/draw-attention.md`, `guide/content/pages/index.md`, `guide/content/pages/getting-started.md`
- Create: `tests/test_guide_content.py`

**Interfaces:**
- Consumes: the build from Task 6.
- Produces: the real guide. Later phases add records beside these.

Facts used below, so the content invents nothing: the Phase 1 test round (`docs/test-rounds/2026-09-phase1.md`, 20 September 2026, row 5) found the Xerte editor kept the `cu-callout` and `fa-stack` classes through a save and reopen. `version.txt` gives Xerte 3.14. The Xerte editor's property labels (Theme, Left Logo, Right Logo, Hide Default Logo, Description, Styles, Stylesheet) come from `modules/site/parent_templates/site/wizards/en-GB/data.xwd`. Brand colours and colourways come from `THEMING-GUIDE.md`.

- [ ] **Step 1: Write the failing test**

`tests/test_guide_content.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tests -p "test_guide_content.py" -v`
Expected: FAIL: `ERROR .../guide/site.toml: [Errno 2] No such file or directory`.

- [ ] **Step 3: Write `guide/site.toml`**

```toml
title = "Cardiff University Theme author guide"
# "warn" until phase 3 has migrated the remaining demo pages; then "fail".
coverage = "warn"
# Task tiles on the home page, in this order.
tasks = ["draw-attention"]

[[menu]]
page = "home"
title = "Home"

[[menu]]
page = "getting-started"
title = "Getting started"

[[menu]]
page = "tasks"
title = "Tasks"

[[menu]]
page = "components"
title = "Components"

# Component groups in the side menu, in this order. Empty groups are not shown.
[[groups]]
id = "content"
title = "Content"

[[groups]]
id = "emphasis"
title = "Emphasis"

[[groups]]
id = "layout"
title = "Layout"

[[groups]]
id = "interaction"
title = "Interaction"
```

- [ ] **Step 4: Write `guide/content/components/callout.md`**

```markdown
+++
name = "callout"
title = "Callouts"
lead = "Pull one key idea out of the page with a short title and a few lines of text. The theme draws the icon."
group = "emphasis"
status = "current"
since = "v1.4"
tasks = ["draw-attention"]
related = []
scss = ["scss/components/_callout.scss"]

[editor]
survives = true
checked = 2026-09-20
xerte = "3.14"

[parts]
cu-callout = "The container. On its own it gives the Key point variant."
cu-callout-title = "The short bold title. Always say the variant in words."
cu-callout-icon = "Only for the older fa-stack icon markup, which still works. Leave it out of new callouts."

[[examples]]
class = "cu-callout-tip"
label = "Tip"
purpose = "A recommendation or shortcut"
html = '''
<div class="cu-callout cu-callout-tip">
  <strong class="cu-callout-title">Tip</strong>
  <p>Keep a callout to two or three lines so it stays easy to scan.</p>
</div>
'''

[[examples]]
class = "cu-callout-info"
label = "Information"
purpose = "Extra context that helps but is not essential"
html = '''
<div class="cu-callout cu-callout-info">
  <strong class="cu-callout-title">Information</strong>
  <p>Extra context.</p>
</div>
'''

[[examples]]
class = "cu-callout-good"
label = "Good practice"
purpose = "The preferred approach"
html = '''
<div class="cu-callout cu-callout-good">
  <strong class="cu-callout-title">Good practice</strong>
  <p>The preferred approach.</p>
</div>
'''

[[examples]]
class = "cu-callout-important"
label = "Important"
purpose = "Something that needs the reader's attention"
html = '''
<div class="cu-callout cu-callout-important">
  <strong class="cu-callout-title">Important</strong>
  <p>Something requiring attention.</p>
</div>
'''

[[examples]]
class = "cu-callout-warning"
label = "Warning"
purpose = "A risk or problem the reader must avoid"
html = '''
<div class="cu-callout cu-callout-warning">
  <strong class="cu-callout-title">Warning</strong>
  <p>A risk or problem.</p>
</div>
'''

[[examples]]
class = "cu-callout-example"
label = "Example"
purpose = "A worked example"
html = '''
<div class="cu-callout cu-callout-example">
  <strong class="cu-callout-title">Example</strong>
  <p>A worked example.</p>
</div>
'''

[[examples]]
class = "cu-callout-key"
label = "Key point"
purpose = "The main takeaway. Leaving the variant class off gives the same result"
html = '''
<div class="cu-callout cu-callout-key">
  <strong class="cu-callout-title">Key point</strong>
  <p>The main takeaway.</p>
</div>
'''
+++

## When to use it

Use a callout when one idea must stand out from the text around it, so a reader who skims still sees it.

### Do

- Keep each callout to one idea.
- Start with a short title that names the variant, such as Tip or Warning.
- Keep the text to two or three lines.

### Don't

- Put more than one or two callouts on a screen.
- Use the Warning variant for something minor. Keep it for a real risk.
- Put long paragraphs, tables or other callouts inside a callout.

## Accessibility

- The title says the variant in words, so the meaning never depends on colour or the icon.
- The theme draws the icon as decoration, so screen readers skip it.
- Keep the title. Without it, a callout is only a coloured box to someone using a screen reader.
```

- [ ] **Step 5: Write `guide/content/tasks/draw-attention.md`**

```markdown
+++
name = "draw-attention"
title = "Draw attention to something"
summary = "Make sure readers notice a tip, a warning or a key point."
icon = "fa-lightbulb"
components = ["callout"]

[example]
label = "An upload reminder"
purpose = "Two short paragraphs with one Important callout between them."
html = '''
<p>Upload your file before the deadline shown on the submission page.</p>
<div class="cu-callout cu-callout-important">
  <strong class="cu-callout-title">Important</strong>
  <p>Check that your upload has finished before you close the page.</p>
</div>
<p>You can upload a new version until the deadline.</p>
'''
+++

## Goal

Make one point stand out from the text around it, so a reader who skims the page still sees it.

## Checklist

- The callout holds one idea, and its title names the variant.
- The point still makes sense without its colour or icon.
- There are no more than two callouts on the screen.
- You chose the Warning variant only for a real risk.
```

- [ ] **Step 6: Write `guide/content/pages/index.md`**

```markdown
+++
name = "index"
title = "What do you want to do with your page?"
lead = "Pick a task to see which components to use, the HTML to paste into Xerte, and how to check the result."
new_steps = [
  "Set your project's Theme property to Cardiff University Theme.",
  "Set your logos and, if you need them, your colours.",
  "Paste your first callout into a Text content item.",
]

[[how]]
title = "Choose"
text = "See which component fits what you want to do."

[[how]]
title = "Copy"
text = "Copy the example's HTML from the guide."

[[how]]
title = "Adjust"
text = "Paste it into a Text content item's Source view and change the words."

[[how]]
title = "Check"
text = "Go through the task's checklist before you publish."
+++
```

- [ ] **Step 7: Write `guide/content/pages/getting-started.md`**

````markdown
+++
name = "getting-started"
title = "Getting started"
lead = "Switch a Xerte site project to the Cardiff University Theme, then set its logos and colours."
+++

## Choose the theme

1. Open your site project in the Xerte editor.
2. Open the project's top-level properties.
3. Set **Theme** to **Cardiff University Theme**.
4. Preview the project to check the new look.

## Logos

The header shows a logo on the left by default. Use the **Left Logo** and **Right Logo** properties to change the logos:

- **File** sets the image.
- **Description** is the logo's text for screen readers. Fill it in for every logo.
- **Hide Default Logo** removes that side's default logo.

## Brand colours

The theme uses two brand colours. To change them for one project, add the optional **Styles** property to the project's top-level properties and paste:

```css
:root {
  --color-brand-primary: #00703C;   /* main brand colour */
  --color-brand-secondary: #1D2B4F; /* dark supporting colour */
}
```

Change the two values to your colours. Then check the contrast: white text on a button in your primary colour needs a ratio of at least 4.5:1, and so does white navbar text on your secondary colour.

## Header colourways

By default the header is white and the navbar is ink with a red rule underneath. To switch one project to another colourway, paste one of these into its **Styles** property.

### Light grey nav

```css
:root {
  --color-navbar-bg: #E6E6E6;
  --color-navbar-item-hover: #FFFFFF;
  --color-navbar-text: #121212;
  --color-navbar-rule: #121212;
  --color-navbar-focus: #121212;
}
```

### Charcoal header

```css
:root {
  --color-header-bg: #1F1F1F;
  --color-header-text: #FFFFFF;
  --color-header-subtext: #C8C8C8;
  --color-header-border: #1F1F1F;
}
```

### Charcoal header, light nav

```css
:root {
  --color-header-bg: #1F1F1F;
  --color-header-text: #FFFFFF;
  --color-header-subtext: #C8C8C8;
  --color-header-border: #1F1F1F;
  --color-navbar-bg: #E6E6E6;
  --color-navbar-item-hover: #FFFFFF;
  --color-navbar-text: #121212;
  --color-navbar-focus: #121212;
}
```

Every colourway keeps text at 4.5:1 or better against its background. If you choose other colours, check the contrast yourself.

## The page frame

The player draws the page frame around your content: the header and logos, the navbar, the section menu, the footer, the feedback tab, the back-to-top button and the glossary tip. You set these in the project's properties in Xerte. You do not paste them into a Text content item, so the guide has no component pages for them.
````

- [ ] **Step 8: Run the tests and build the real guide**

Run: `python3 -m unittest discover -s tests -p "test_*.py" -v`
Expected: all tests `OK`.

Run: `./build.sh guide`
Expected, at the end:

```
WARNING [check 2] guide: 345 author-facing classes are not covered yet: ... and 335 more
WARNING [check 4] .../guide/content/components/callout.md: scss/components/_callout.scss changed on 2026-09-28, after the editor evidence of 2026-09-20; re-test in Xerte and update [editor]
Built .../theme-src/cardiffuniversity/site (6 pages, 2 warning(s)).
```

The coverage count may differ slightly; it must be a warning, not an error. The check 4 warning is correct: the 28 September token rename (`60ad0a48f`) touched the callout SCSS after the 20 September editor test. Do not change the `[editor]` date to silence it. Nan re-tests in Xerte and updates the date.

Open `site/index.html` in Chrome and click through to the callout page. Confirm by eye: the callouts look as they do in Xerte, the copy buttons appear, and the side menu is on the left.

- [ ] **Step 9: Commit**

```bash
git add guide/site.toml guide/content tests/test_guide_content.py
git commit -m "feat(cardiffuniversity): add the author guide's phase 1 content"
```

---

### Task 8: Browser check

**Files:**
- Create: `tests/check_guide.py`

**Interfaces:**
- Consumes: `build-guide.build(out=...)` from Task 6, the real content from Task 7.
- Produces: `python3 tests/check_guide.py`, exit 0 when every check passes. Used by CI in Task 9.

- [ ] **Step 1: Write the check**

`tests/check_guide.py`:

```python
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
```

- [ ] **Step 2: Run it**

Run: `python3 tests/check_guide.py`
Expected: `13 passed, 0 failed`.

If a check fails, fix the cause in `guide/assets/guide.css` or `guide.js` (or `pages.py`), not in the check. The checks state what the spec requires.

- [ ] **Step 3: Prove a check can fail**

Temporarily delete `display: block;` from the `.g-body` rule in `guide/assets/guide.css`, run `python3 tests/check_guide.py`, and confirm `[tasks/draw-attention.html @ 485px] no sideways scroll` fails. (The theme makes `body` a flex container, so without that line the task page's `<main>` grows to the width of the longest code line.) Then revert with `git checkout guide/assets/guide.css` and run again: `13 passed, 0 failed`.

- [ ] **Step 4: Commit**

```bash
git add tests/check_guide.py
git commit -m "test(cardiffuniversity): add headless Chrome checks for the author guide"
```

---

### Task 9: CI workflow and maintainer docs

**Files:**
- Create: `.github/workflows/cardiff-guide.yml` (at the repository root)
- Modify: `THEMING-GUIDE.md` (the "Build and checks" section), `README.md` (the "Maintain the theme" section), `MIGRATION.md` (the "Author guide" section)

**Interfaces:**
- Consumes: `./build.sh guide`, the unit tests, `tests/check_guide.py`.
- Produces: a pull request check named "Cardiff theme author guide".

- [ ] **Step 1: Write the workflow**

`.github/workflows/cardiff-guide.yml`:

```yaml
name: Cardiff theme author guide

on:
  pull_request:
    paths:
      - "theme-src/cardiffuniversity/**"
      - "themes/site/cardiffuniversity/**"
      - ".github/workflows/cardiff-guide.yml"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  check:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: theme-src/cardiffuniversity
    steps:
      - uses: actions/checkout@v4
        with:
          # Check 4 reads commit dates; a shallow clone would make every record look stale.
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - name: Build the theme and the guide
        run: ./build.sh guide
      - name: The committed CSS matches the SCSS
        run: git diff --exit-code -- ../../themes/site/cardiffuniversity/cardiffuniversity.css scss/_cu-tokens.scss
      - name: Unit tests
        run: python3 -m unittest discover -s tests -p "test_*.py" -v
      - name: Browser checks
        run: CHROME="$(command -v google-chrome)" python3 tests/check_guide.py
```

- [ ] **Step 2: Validate the workflow locally**

Run: `python3 -c "import sys; print(open('../../.github/workflows/cardiff-guide.yml').read().count('run:'))"`
Expected: `5`.

The workflow first runs on the pull request in Task 9's Step 6. There is no deploy job: publishing waits for the open items in the spec.

- [ ] **Step 3: Update `THEMING-GUIDE.md`**

In the "Build and checks" code block, add these lines after `./build.sh package ...`:

```bash
./build.sh guide        # compile, then check and build the author guide into site/
python3 tools/build-guide.py --check
python3 -m unittest discover -s tests -p "test_*.py"
python3 tests/check_guide.py
```

After the paragraph that starts "Commit the compiled CSS with SCSS changes", add:

```markdown
The author guide's sources are in `guide/`: one component record per component in
`guide/content/components/`, task pages in `guide/content/tasks/`, and the navigation in
`guide/site.toml`. `tools/build-guide.py` checks them against the compiled CSS before it writes
anything; the spec is `docs/design-notes/2026-10-06-author-guide.md`. Sass is pinned in
`build.sh` so the CI workflow's compile matches the committed CSS; update the pin with care.
```

- [ ] **Step 4: Update `README.md`**

In "Maintain the theme", add a bullet after the migration status bullet:

```markdown
- [Author guide spec](docs/design-notes/2026-10-06-author-guide.md): the hosted guide for content
  authors, built from `guide/` with `./build.sh guide`.
```

- [ ] **Step 5: Update `MIGRATION.md`**

In the "Author guide" section, tick the first item that phase 1 delivers and add a status line above the list:

```markdown
Phase 1 of the [author guide](docs/design-notes/2026-10-06-author-guide.md) is built: the
generator, the five build checks, Getting started, one task page and the callout component.
It is not published. Phase 2 adds the reference pages and seven more components.
```

Change `- [ ] Start with seven or eight frequently used components` to stay unticked (phase 2), and change `- [ ] Introduce example, class and accessibility checks and generated-content drift checks incrementally.` to `- [x] ...` with ` Done in phase 1 (checks 1 to 5).` appended.

- [ ] **Step 6: Run everything, then commit and open the pull request**

Run: `./build.sh guide && python3 -m unittest discover -s tests -p "test_*.py" && python3 tests/check_guide.py && git diff --check`
Expected: the guide builds with 2 warnings, all unit tests `OK`, `13 passed, 0 failed`, and no whitespace errors.

```bash
git add ../../.github/workflows/cardiff-guide.yml THEMING-GUIDE.md README.md MIGRATION.md
git commit -m "ci(cardiffuniversity): check the author guide on pull requests"
```

Ask Nan before pushing the branch or opening a pull request.

---

## Self-review

**Spec coverage.**

| Spec requirement | Task |
| --- | --- |
| Layout `guide/`, `tools/build-guide.py`, `site/` git-ignored, `./build.sh guide` | 5, 6 |
| `tools/theme_css.py` shared with `build-reference.py` | 1 |
| Guide loads the player's stylesheets in order, then the theme; jQuery 1.9.1 and `bootstrap.js`; no `cardiffuniversity.js` | 5 (`assets.STYLESHEETS`, `SCRIPTS`), 6 |
| Guide navigation uses only `g-` classes | 5 (`guide.css`), 8 (layout checks) |
| Page frame in Getting started, not as components | 7 |
| Home and task pages (direction B), component pages (direction A), no search box | 5, 7 |
| `site.toml` for groups, menu, task order; menu items without pages left out | 3, 4 (check 3), 5 |
| Phone menu below 800px; "on this page" hidden below 1100px | 5, 8 |
| Component page sections in order | 5 |
| Record format: TOML, `examples`, `parts`, Markdown subset, fixed headings | 2, 3 |
| Checks 1 to 5 with their results | 4, 6 |
| CI: full history, Python 3.11+, Node, committed CSS check | 9 |
| Unit tests, browser check, manual checks | 1-8; manual checks listed below |
| Phase 1 scope: one task, callouts, Getting started, home | 7 |

Not covered, by design: reference pages and check 2's generated tables (phase 2), publishing (open items), screenshots in Getting started (needs the real Xerte editor), links to `demos/` (cannot work on a hosted site; see "Decisions this plan makes").

**Manual checks after Task 9 (Nan):** keyboard traversal of the side menu, the top menu and the copy buttons; a read at 200% zoom; the copy button on a served page (`python3 -m http.server -d site` from the theme folder, then open `http://localhost:8000`); re-test the callouts in the Docker Xerte editor and update `[editor]` in `callout.md`.
