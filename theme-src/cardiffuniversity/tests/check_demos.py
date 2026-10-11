#!/usr/bin/env python3
"""Browser checks for the hand-written demo pages (headless Chrome, standard library only).

Opens the pages in demos/ at desktop and phone widths and checks the things a unit test cannot see:
the callout icons render, a code label stays inside its block, and the section menu follows the
scroll. Reuses the runner from check_guide.py.

Usage (from the theme folder):
    python3 tests/check_demos.py
    python3 tests/check_demos.py --package dist/cardiffuniversity-demos.zip   the packaged theme, unzipped
                                                                              into a themes/site/ layout
Exit code 1 if any check fails.
"""
import argparse
import json
import sys
import tempfile
import zipfile
from pathlib import Path

import check_guide
import support

DEMOS = support.THEME / "demos"
PAGES = sorted(p.name for p in DEMOS.glob("*.html"))

FONT_LOADED = ("Array.from(document.fonts).some(function (f) {"
               " return f.family.replace(/[\"']/g, '') === 'Font Awesome 6 Free' && f.status === 'loaded'; })")
# Bootstrap 2 gives every <code> white-space: nowrap, so a long label can keep its box inside the block
# while its text runs out of the box. Both have to hold.
CODE_INSIDE_BLOCK = ("Array.from(document.querySelectorAll('.code-label')).every(function (c) {"
                     " var b = c.closest('.demo-block'); if (!b) return true;"
                     " return c.getBoundingClientRect().right <= b.getBoundingClientRect().right + 0.5"
                     " && c.scrollWidth <= c.clientWidth + 1; })")
NO_SIDEWAYS_SCROLL = "document.documentElement.scrollWidth <= window.innerWidth"
# Scroll well down, run the affix plugin's own position check, and expect the menu to be pinned in view.
MENU_FOLLOWS = ("(function () { var m = jQuery('.bs-docs-sidenav'); window.scrollTo(0, 1500);"
                " m.data('affix').checkPosition();"
                " var top = m[0].getBoundingClientRect().top;"
                " return m.hasClass('affix') && top >= 0 && top <= 150; })()")

# An example block is one a snippet is made for: it has something besides its title, description and class
# label, no hand-written <pre> already, and no data-code="skip".
EXAMPLE_BLOCKS = ("Array.from(document.querySelectorAll('.demo-block')).filter(function (b) {"
                  " return !Array.from(b.querySelectorAll('pre')).some(function (p) { return !p.closest('.demo-code'); }) && !b.closest(\"[data-code='skip']\")"
                  " && Array.from(b.children).some(function (c) {"
                  " return !/(^|\\s)(demo-block__title|demo-block__description|code-label|demo-block-title|demo-code)(\\s|$)/.test(c.className); }); })")
EVERY_EXAMPLE_HAS_A_SNIPPET = (f"(function () {{ var blocks = {EXAMPLE_BLOCKS};"
                               " return blocks.every(function (b) {"
                               " var d = b.querySelectorAll(':scope > details.demo-code');"
                               " return d.length === 1 && !d[0].open && d[0].querySelector('pre code').textContent.trim().length > 0; }); })()")
# The demo's own classes are chrome; an author who pastes them gets styling that does not exist in Xerte.
NO_DEMO_CLASSES_IN_SNIPPETS = ("Array.from(document.querySelectorAll('details.demo-code pre code'))"
                               ".every(function (c) { return !/class=\"[^\"]*\\bdemo-/.test(c.textContent); })")
SNIPPETS_HAVE_COPY_BUTTONS = ("Array.from(document.querySelectorAll('details.demo-code')).every(function (d) {"
                              " var b = d.querySelector('button'); return !!b && b.textContent.trim() === 'Copy'; })")
# Show HTML reads as a link: the theme's link colour, underlined, and the same colour a real link has.
SUMMARY_LOOKS_LIKE_A_LINK = ("(function () { var a = document.createElement('a'); a.href = '#'; document.body.appendChild(a);"
                             " var link = getComputedStyle(a).color; document.body.removeChild(a);"
                             " return Array.from(document.querySelectorAll('details.demo-code summary')).every(function (s) {"
                             " var cs = getComputedStyle(s); return cs.color === link && cs.textDecorationLine === 'underline'"
                             " && cs.cursor === 'pointer'; }); })()")
# Guidance and reference sections explain or list classes; their boxes are not copyable examples.
GUIDELINE_SECTIONS = {"bootstrap.html": "bootstrap-usage-guidelines", "colors.html": "color-usage-guidelines",
                      "components.html": "component-usage-guidelines",
                      "code-utilities.html": "utility-classes-reference",
                      "flexbox.html": "utility-class-reference"}
NO_SNIPPETS_IN_SECTION = ("(function () {{ var s = document.getElementById('{id}');"
                          " return !!s && s.querySelectorAll('.demo-block').length > 0"
                          " && s.querySelectorAll('details.demo-code').length === 0; }})()")
# With every snippet open the long lines must scroll inside their own box, not push the page sideways.
OPEN_SNIPPETS_DO_NOT_WIDEN_THE_PAGE = ("(function () { Array.from(document.querySelectorAll('details.demo-code'))"
                                       ".forEach(function (d) { d.open = true; });"
                                       " return document.documentElement.scrollWidth <= window.innerWidth; })()")
FILLED_BUTTONS_SNIPPET = (
    "(function () { var b = Array.from(document.querySelectorAll('.demo-block')).filter(function (x) {"
    " var t = x.querySelector('.demo-block__title'); return t && t.textContent.trim() === 'Filled Buttons'; })[0];"
    " return b.querySelector('details.demo-code pre code').textContent === "
    + json.dumps("\n".join(['<button class="button button-primary">Primary</button>',
                            '<button class="button button-secondary">Secondary</button>',
                            '<button class="button button-success">Success</button>',
                            '<button class="button button-primary" disabled>Disabled</button>']))
    + "; })()")

CHECKS = [(page, width, "code labels stay inside their block", CODE_INSIDE_BLOCK)
          for page in PAGES for width in (1280, 485)]
CHECKS += [(page, width, "the page does not scroll sideways", NO_SIDEWAYS_SCROLL)
           for page in PAGES for width in (1280, 485)]
CHECKS += [
    ("index.html", 1280, "the callout icons have their Font Awesome font", FONT_LOADED),
    ("index.html", 1280, "the three callouts sit side by side at the same height",
     "(function () { var r = Array.from(document.querySelectorAll('.cu-callout')).map(function (c) { return c.getBoundingClientRect(); });"
     " return r.length === 3 && Math.abs(r[0].top - r[1].top) < 1 && Math.abs(r[1].top - r[2].top) < 1"
     " && r[0].left < r[1].left && r[1].left < r[2].left"
     " && Math.abs(r[0].height - r[1].height) < 1 && Math.abs(r[1].height - r[2].height) < 1; })()"),
    ("index.html", 485, "the three callouts stack one under the other",
     "(function () { var r = Array.from(document.querySelectorAll('.cu-callout')).map(function (c) { return c.getBoundingClientRect(); });"
     " return r.length === 3 && r[0].bottom <= r[1].top + 1 && r[1].bottom <= r[2].top + 1"
     " && Math.abs(r[0].left - r[1].left) < 1 && Math.abs(r[1].left - r[2].left) < 1; })()"),
    ("code-utilities.html", 1280, "the stat tiles sit side by side at the same height",
     "(function () { var r = Array.from(document.querySelectorAll('#combining-utilities .flex-200')).map(function (c) { return c.getBoundingClientRect(); });"
     " return r.length === 3 && Math.abs(r[0].top - r[1].top) < 1 && Math.abs(r[1].top - r[2].top) < 1"
     " && r[0].left < r[1].left && r[1].left < r[2].left && Math.abs(r[0].height - r[1].height) < 1; })()"),
    ("code-utilities.html", 485, "the stat tiles stack one under the other",
     "(function () { var r = Array.from(document.querySelectorAll('#combining-utilities .flex-200')).map(function (c) { return c.getBoundingClientRect(); });"
     " return r.length === 3 && r[0].bottom <= r[1].top + 1 && r[1].bottom <= r[2].top + 1; })()"),
    ("code-utilities.html", 1280, "the person's photo and text are centred on each other",
     "(function () { var row = document.querySelector('#combining-utilities img.rounded-full').parentElement;"
     " var i = row.children[0].getBoundingClientRect(), t = row.children[1].getBoundingClientRect();"
     " return Math.abs((i.top + i.height / 2) - (t.top + t.height / 2)) < 1.5 && getComputedStyle(row.children[0]).borderRadius !== '0px'; })()"),
    ("code-utilities.html", 1280, "the banner puts its button on the right of its text",
     "(function () { var b = document.querySelector('#combining-utilities .bg-dark'); var p = b.querySelector('p').getBoundingClientRect();"
     " var a = b.querySelector('a').getBoundingClientRect(), r = b.getBoundingClientRect();"
     " return a.left > p.right && r.right - a.right < 40 && Math.abs((a.top + a.height / 2) - (p.top + p.height / 2)) < 1.5; })()"),
    ("components.html", 1280, "Bootstrap's plugins are loaded",
     "['alert', 'collapse', 'tab', 'carousel', 'affix', 'scrollspy'].every(function (n) { return typeof jQuery.fn[n] === 'function'; })"),
    ("components.html", 1280, "the Filled Buttons snippet is the example's own markup, tidied", FILLED_BUTTONS_SNIPPET),
] + [(page, 1280, "every example has a closed HTML snippet", EVERY_EXAMPLE_HAS_A_SNIPPET) for page in PAGES]
CHECKS += [("components.html", 1280, "the page has examples to show snippets for", f"{EXAMPLE_BLOCKS}.length >= 10")]
CHECKS += [(page, 1280, "no snippet carries a demo-only class", NO_DEMO_CLASSES_IN_SNIPPETS) for page in PAGES]
CHECKS += [(page, 1280, "every snippet has a Copy button", SNIPPETS_HAVE_COPY_BUTTONS) for page in PAGES]
CHECKS += [(page, 1280, "Show HTML is styled as a link", SUMMARY_LOOKS_LIKE_A_LINK) for page in PAGES]
CHECKS += [(page, 1280, "guidance and reference sections have no snippets", NO_SNIPPETS_IN_SECTION.format(id=section))
           for page, section in GUIDELINE_SECTIONS.items()]
CHECKS += [(page, 485, "open snippets do not widen the page", OPEN_SNIPPETS_DO_NOT_WIDEN_THE_PAGE) for page in PAGES]
CHECKS += [(page, 1280, "the section menu follows the scroll", MENU_FOLLOWS)
     for page in ("images-media.html", "components.html", "forms.html", "flexbox.html")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, help="run the same checks on an unzipped demos package")
    args = parser.parse_args()
    if args.package:
        with tempfile.TemporaryDirectory() as tmp:
            # Served from themes/site/<name>/, as on a Xerte server, with nothing else of the repo around.
            zipfile.ZipFile(args.package).extractall(Path(tmp) / "themes" / "site")
            return run(Path(tmp) / "themes" / "site" / "cardiffuniversity-demos")
    return run(DEMOS)


def run(folder):
    groups = {}
    for page, width, name, expression in CHECKS:
        groups.setdefault((page, width), {})[name] = expression
    failed = 0
    for (page, width), checks in groups.items():
        results = check_guide.run(folder, page, width, checks)
        for name in checks:
            actual = results.get(name, "NO RESULT")
            ok = actual == "true"
            failed += not ok
            print(f"{'PASS' if ok else 'FAIL'}  [{page} @ {width}px] {name}" + ("" if ok else f"\n      got {actual!r}"))
    print(f"\n{len(CHECKS) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
