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
    ("callouts", "simple markup: disc drawn in CSS, tip colour", "ps('#callout-tip-simple','::before','backgroundColor')", "rgb(94, 185, 155)"),
    ("callouts", "simple markup: glyph colour on the disc", "ps('#callout-tip-simple','::before','color')", "rgb(18, 18, 18)"),
    ("callouts", "simple markup: disc is 28px", "ps('#callout-tip-simple','::before','width')", "28px"),
    ("callouts", "simple markup: no modifier = key point, black disc", "ps('#callout-key-simple','::before','backgroundColor')", "rgb(18, 18, 18)"),
    ("callouts", "authored fa-stack markup draws no CSS disc", "ps('#callout-tip','::before','content')", "none"),
    ("callouts", "both markup forms align their titles at the same x",
     "(function(){var a=document.querySelector('#callout-tip .cu-callout-title').getBoundingClientRect(),"
     "b=document.querySelector('#callout-tip-simple .cu-callout-title').getBoundingClientRect();"
     "return String(Math.abs(a.left-b.left)<=0.5)})()", "true"),
    ("callouts", "simple markup: disc centred on the title line (within 1px)",
     "(function(){var c=document.querySelector('#callout-tip-simple'),s=getComputedStyle(c,'::before'),"
     "r=c.getBoundingClientRect(),t=c.querySelector('.cu-callout-title').getBoundingClientRect();"
     "var top=r.top+parseFloat(getComputedStyle(c).paddingTop);"
     "return String(Math.abs((top+parseFloat(s.height)/2)-(t.top+t.height/2))<=1)})()", "true"),
    ("callouts", "icon disc centred on the title's first line (within 1px)",
     "(function(){var i=document.querySelector('#callout-tip .cu-callout-icon').getBoundingClientRect(),"
     "t=document.querySelector('#callout-tip .cu-callout-title').getBoundingClientRect();"
     "return String(Math.abs((i.top+i.height/2)-(t.top+t.height/2))<=1)})()", "true"),
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
    ("frame", "navbar has no shadow", "cs('#topnav','boxShadow')", "none"),
    ("frame", "navbar is charcoal", "cs('#topnav .navbar-inner','backgroundColor')", "rgb(18, 18, 18)"),
    ("frame", "navbar above the header carries no rule (the header's red edge does)", "cs('#topnav .navbar-inner','borderBottomWidth')", "0px"),
    ("frame", "navbar below the header has a 4px rule", "cs('#pageLinks .navbar-inner','borderBottomWidth')", "4px"),
    ("frame", "navbar below-header rule is brand red", "cs('#pageLinks .navbar-inner','borderBottomColor')", "rgb(228, 37, 27)"),
    ("frame", "navbar links are white", "cs('#nav li:not(.activePage) a','color')", "rgb(255, 255, 255)"),
    ("frame", "current page sits on a lighter dark", "cs('#nav li.activePage a','backgroundColor')", "rgb(51, 51, 51)"),
    ("frame", "current page is underlined in brand red", "cs('#nav li.activePage a','boxShadow')", "rgb(228, 37, 27) 0px -3px 0px 0px inset"),
    ("frame", "sidebar is square", "cs('#toc','borderTopLeftRadius')", "0px"),
    ("frame", "sidebar has no shadow", "cs('#toc','boxShadow')", "none"),
    ("frame", "sidebar has a 1px frame", "cs('#toc','borderTopWidth')", "1px"),
    ("frame", "sidebar frame is grey-30", "cs('#toc','borderTopColor')", "rgb(204, 204, 204)"),
    ("frame", "first sidebar item is square", "cs('#toc > li:first-child > a','borderTopLeftRadius')", "0px"),
    ("frame", "sidebar items have a 1px rule below", "cs('#toc > li:nth-child(2) > a','borderBottomWidth')", "1px"),
    ("frame", "sidebar item rule is grey-20", "cs('#toc > li:nth-child(2) > a','borderBottomColor')", "rgb(229, 229, 229)"),
    ("frame", "last sidebar item has no rule below the frame", "cs('#toc > li:last-child > a','borderBottomWidth')", "0px"),
    ("frame", "selected sidebar item has a 4px red left rule", "cs('#toc > li.active > a','borderLeftWidth')", "4px"),
    ("frame", "selected sidebar left rule is brand red", "cs('#toc > li.active > a','borderLeftColor')", "rgb(228, 37, 27)"),
    ("frame", "selected sidebar item sits on a pale red wash", "cs('#toc > li.active > a','backgroundColor')", "color(srgb 0.993647 0.948706 0.946353)"),
    ("frame", "selected sidebar text is ink, not white on red", "cs('#toc > li.active > a','color')", "rgb(18, 18, 18)"),
    ("frame", "selected and unselected sidebar text line up", "(function(){var a=document.querySelector('#toc > li.active > a'),b=document.querySelector('#toc > li:nth-child(2) > a');return String(getComputedStyle(a).paddingLeft===getComputedStyle(b).paddingLeft&&getComputedStyle(a).borderLeftWidth===getComputedStyle(b).borderLeftWidth)})()", "true"),
    # The base template clears floats with `section { overflow: auto }` (custom.css), which also
    # clips a focus ring painted outside the section box - reported in test round 1.
    ("focus", "sections do not clip what is painted outside them", "cs('#test-section','overflow')", "visible"),
    ("focus", "sections still contain their floats", "cs('#test-section','display')", "flow-root"),
    ("focus", "float containment still works (section is as tall as its float)",
     "(function(){var s=document.querySelector('#test-section');return String(s.getBoundingClientRect().height>=60)})()", "true"),
    ("focus", "focus ring is 2px, offset 4px, ink",
     "(function(){var b=document.querySelector('#focus-btn');b.style.outline='var(--focus-ring)';b.style.outlineOffset='var(--focus-ring-offset)';"
     "var s=getComputedStyle(b);return s.outlineWidth+' '+s.outlineOffset+' '+s.outlineColor})()", "2px 4px rgb(18, 18, 18)"),
    # Test round 1: the toggle overflowed the bar and the header painted over the overflow.
    # Forcing it taller than the bar proves the bar now grows to contain it.
    ("frame", "navbar toggle stays inside the bar, even when taller than it",
     "(function(){var b=document.querySelector('#pageNavBtn');b.style.display='block';b.style.minHeight='64px';"
     "var r=b.getBoundingClientRect(),bar=document.querySelector('#topnav .navbar-inner').getBoundingClientRect();"
     "var ok=r.bottom<=bar.bottom+0.5&&r.top>=bar.top-0.5;b.style.display='';b.style.minHeight='';return String(ok)})()", "true"),
    # cardiffuni-v3.js publishes --cu-sticky-nav (the sticky page menu's height). These assert
    # the fallbacks that apply when it is absent or the bar is not sticky.
    ("focus", "sections carry a scroll margin for the sticky page menu", "cs('#test-section','scrollMarginTop')", "16px"),
    ("frame", "affixed section menu clears the top of the viewport", "cs('#toc-affixed','top')", "24px"),
    ("frame", "affixed section menu scrolls instead of being cut off", "cs('#toc-affixed','overflowY')", "auto"),
    # Xerte marks a page section's heading with .sectionTitle; it should read as the design
    # system's section heading (h2), not a lighter red variant of it.
    ("headings", "section title is ink, not red", "cs('#section-title','color')", "rgb(18, 18, 18)"),
    ("headings", "section title uses the display font", "cs('#section-title','fontFamily').split(',')[0].trim()", '"Franklin Gothic Heavy"'),
    ("headings", "section title weight matches a section heading", "cs('#section-title','fontWeight')", "800"),
    ("headings", "section title is the same size as a plain h2",
     "String(cs('#section-title','fontSize')===cs('#plain-h2','fontSize'))", "true"),
    ("headings", "section title keeps the heading's tight leading",
     "String(cs('#section-title','lineHeight')===cs('#plain-h2','lineHeight'))", "true"),
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
