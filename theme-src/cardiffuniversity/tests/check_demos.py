#!/usr/bin/env python3
"""Browser checks for the hand-written demo pages (headless Chrome, standard library only).

Opens the pages in demos/ at desktop and phone widths and checks the things a unit test cannot see:
the callout icons render, a code label stays inside its block, and the section menu follows the
scroll. Reuses the runner from check_guide.py.

Usage (from the theme folder):
    python3 tests/check_demos.py
Exit code 1 if any check fails.
"""
import sys

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
    ("components.html", 1280, "Bootstrap's plugins are loaded",
     "['alert', 'collapse', 'tab', 'carousel', 'affix', 'scrollspy'].every(function (n) { return typeof jQuery.fn[n] === 'function'; })"),
] + [(page, 1280, "the section menu follows the scroll", MENU_FOLLOWS)
     for page in ("images-media.html", "components.html", "forms.html", "flexbox.html")]


def main():
    groups = {}
    for page, width, name, expression in CHECKS:
        groups.setdefault((page, width), {})[name] = expression
    failed = 0
    for (page, width), checks in groups.items():
        results = check_guide.run(DEMOS, page, width, checks)
        for name in checks:
            actual = results.get(name, "NO RESULT")
            ok = actual == "true"
            failed += not ok
            print(f"{'PASS' if ok else 'FAIL'}  [{page} @ {width}px] {name}" + ("" if ok else f"\n      got {actual!r}"))
    print(f"\n{len(CHECKS) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
