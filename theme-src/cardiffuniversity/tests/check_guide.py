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
    ("components/callout.html", 1280, "in-page headings are calmer than the page title",
     "parseFloat(getComputedStyle(document.getElementById('when-to-use-it')).fontSize) <= 32"),
    ("components/callout.html", 1280, "side menu group headings are in sentence case",
     "getComputedStyle(document.querySelector('.g-side h2')).textTransform === 'none'"),
    ("components/callout.html", 1280, "the HTML toggle starts closed and opens",
     "(function () { var d = document.querySelector('.g-code-toggle'); var closed = !d.open;"
     " d.querySelector('summary').click(); return closed && d.open"
     " && d.querySelector('.g-code').getBoundingClientRect().height > 0; })()"),
    ("components/callout.html", 1280, "the top menu uses the 16px interface size",
     "[].every.call(document.querySelectorAll('.g-top a'), function (a) { return getComputedStyle(a).fontSize === '16px'; })"),
    ("components/callout.html", 1280, "the side menu links and group headings use the 16px interface size",
     "[].every.call(document.querySelectorAll('.g-side a, .g-side h2'), function (e) { return getComputedStyle(e).fontSize === '16px'; })"),
    ("index.html", 1280, "the home page menu uses the 16px interface size",
     "[].every.call(document.querySelectorAll('.g-top a'), function (a) { return getComputedStyle(a).fontSize === '16px'; })"),
    ("components/callout.html", 1280, "the on this page list uses the 16px interface size",
     "[].every.call(document.querySelectorAll('.g-toc a'), function (a) { return getComputedStyle(a).fontSize === '16px'; })"),
    ("components/callout.html", 1280, "the on this page heading is 16px, in sentence case",
     "(function () { var c = getComputedStyle(document.querySelector('.g-toc h2'));"
     " return c.fontSize === '16px' && c.textTransform === 'none'; })()"),
    ("reference/index.html", 1280, "a card title is underlined on hover",
     "(function () { var link = document.querySelector('.g-card a'), found = false;"
     " [].forEach.call(document.styleSheets, function (sheet) {"
     "  var rules; try { rules = sheet.cssRules; } catch (e) { return; }"
     "  [].forEach.call(rules, function (rule) {"
     "   if (!rule.selectorText || rule.selectorText.indexOf(':hover') < 0) return;"
     "   rule.selectorText.split(',').forEach(function (sel) {"
     "    if (!/:hover\\s+/.test(sel)) return;"  # the card is hovered, not the link itself
     "    try { if (link.matches(sel.replace(/:hover/g, '').trim()) && /underline/.test(rule.style.textDecorationLine || rule.style.textDecoration)) found = true; } catch (e) {}"
     "   });"
     "  });"
     " });"
     " return found; })()"),
    ("reference/index.html", 1280, "the whole card is a link, not just its title",
     "(function () { var card = document.querySelector('.g-card'), r = card.getBoundingClientRect();"
     " var hit = document.elementFromPoint(r.right - 12, r.bottom - 12);"
     " return !!hit && hit.closest('a') === card.querySelector('a'); })()"),
    ("reference/index.html", 1280, "a focused card shows an outline",
     "(function () { var card = document.querySelector('.g-card'); card.querySelector('a').focus();"
     " var c = getComputedStyle(card); return c.outlineStyle === 'solid' && c.outlineWidth === '3px'; })()"),
    ("components/button.html", 1280, "the small and large examples differ from the default button",
     "(function () { var q = function (c) { return getComputedStyle(document.querySelector('.g-preview .' + c)); };"
     " var d = q('button-primary'), s = q('button-sm'), l = q('button-lg');"
     " return parseFloat(s.fontSize) < parseFloat(d.fontSize) && parseFloat(s.paddingTop) < parseFloat(d.paddingTop)"
     " && parseFloat(l.paddingTop) > parseFloat(d.paddingTop) && parseFloat(l.paddingLeft) > parseFloat(d.paddingLeft); })()"),
    ("components/button.html", 1280, "the icon-only example is a 48px square",
     "(function () { var b = document.querySelector('.g-preview .button-icon-only').getBoundingClientRect();"
     " return Math.abs(b.width - b.height) < 1 && Math.abs(b.width - 48) < 1; })()"),
    ("components/button.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/button.html", 1280, "every button example is at least 48px high and 44px wide",
     "[].every.call(document.querySelectorAll('.g-preview .button'), function (b) {"
     " var r = b.getBoundingClientRect(); return r.height >= 47.5 && r.width >= 43.5; })"),
    ("components/alert.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/alert.html", 1280, "the close button removes its alert",
     "(function () { var a = document.querySelector('.g-preview .alert-block'); if (!a) return false;"
     " a.querySelector('.close').click(); return !document.contains(a); })()"),
    ("components/card.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/card.html", 1280, "the whole clickable card is one link",
     "(function () { var card = document.querySelector('.g-preview .card--clickable'); card.scrollIntoView();"
     " var r = card.getBoundingClientRect(), hit = document.elementFromPoint(r.left + 30, r.bottom - 30);"
     " return !!hit && hit.closest('a') === card.querySelector('.card__link'); })()"),
    ("components/card.html", 1280, "the card image is cropped to a widescreen shape",
     "(function () { var i = document.querySelector('.g-preview .card__image').getBoundingClientRect();"
     " return Math.abs(i.width / i.height - 16 / 9) < 0.05; })()"),
    ("components/table.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/table.html", 1280, "the wide table scrolls inside its wrapper, not the page",
     "(function () { var w = document.querySelector('.g-preview .cu-table-scroll');"
     " return w.scrollWidth > w.clientWidth && document.documentElement.scrollWidth <= window.innerWidth; })()"),
    ("components/table.html", 1280, "the wrapper can take keyboard focus",
     "(function () { var w = document.querySelector('.g-preview .cu-table-scroll'); w.focus();"
     " return document.activeElement === w; })()"),
    ("components/table.html", 1280, "striped rows differ from plain rows",
     "(function () { var rows = document.querySelectorAll('.g-preview .table-striped tbody tr');"
     " return rows.length >= 2 && getComputedStyle(rows[0].cells[0]).backgroundColor"
     " !== getComputedStyle(rows[1].cells[0]).backgroundColor; })()"),
    ("components/callout.html", 1280, "the Cardiff logo loads",
     "document.querySelector('header img').naturalWidth > 0"),
    ("getting-started.html", 1280, "headings are spaced from the text above",
     "parseFloat(getComputedStyle(document.getElementById('logos')).marginTop) >= 32"),
    ("getting-started.html", 1280, "list lines have room to read",
     "parseFloat(getComputedStyle(document.querySelector('.g-main li')).lineHeight) >= 24"),
    ("getting-started.html", 1280, "on this page marks the first section at the top",
     "document.querySelector('.g-toc a[aria-current=\"location\"]').getAttribute('href') === '#choose-the-theme'"),
    ("getting-started.html", 1280, "on this page follows the scroll",
     "(function () { var h = document.getElementById('header-colourways');"
     " window.scrollTo(0, h.getBoundingClientRect().top + window.scrollY - 10);"
     " window.dispatchEvent(new Event('scroll'));"
     " return document.querySelector('.g-toc a[aria-current=\"location\"]').getAttribute('href') === '#header-colourways'; })()"),
    ("index.html", 1280, "task tiles are wide enough for their titles",
     "document.querySelector('.g-task').getBoundingClientRect().width >= 300"),
    ("reference/colours.html", 1280, "colour swatches are visible",
     "document.querySelector('.g-swatch').getBoundingClientRect().width >= 24"),
    ("reference/colours.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("reference/colours.html", 485, "the colour table scrolls inside its own box",
     "(function () { var b = document.querySelector('.g-table-scroll'); return b.scrollWidth > b.clientWidth; })()"),
    ("reference/utilities.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("reference/index.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
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
