#!/usr/bin/env python3
"""Stitch the NN-*.html fragments into local-preview.html, inside the cardiffuni-v3 page frame.

The fragments, styles.css and ../project.js are what gets pasted into Xerte; this file only exists to
check them against the real theme CSS. styles.css and ../project.js are linked, not inlined, so the
preview cannot drift from the source. Run: python3 build-preview.py
"""
from pathlib import Path

HERE = Path(__file__).parent
XERTE = Path.home() / "Projects/xerteonlinetoolkits"
THEME = XERTE / "themes/site/cardiffuni-v3"
COMMON = XERTE / "modules/site/parent_templates/site/common"

# Mirror the Home page settings in Xerte (see README.md).
PAGE_TITLE = "Assessment Menu"
PAGE_SUBTITLE = "Find an assessment type. Ask the right questions."

# One entry per Xerte Section: (Section ID, Section Title, [fragments in that section]).
# An empty title is a section with Show Title unticked.
SECTIONS = [
    ("intro", "", ["01-intro.html"]),
    ("finder", "Find an assessment type", ["02-finder.html"]),
    ("questions", "Six questions for the conversation", ["03-questions.html"]),
    ("lanes", "Let learning outcomes lead", ["04-lanes.html"]),
    ("guidance", "Wider guidance", ["05-guidance.html"]),
]

blocks = []
for n, (section_id, title, fragments) in enumerate(SECTIONS, start=1):
    parity = "oddSection" if n % 2 else "evenSection"  # the player adds these by position
    header = (
        f'<div class="page-header"><h2 id="{section_id}_title" class="sectionTitle">{title}</h2></div>'
        if title else ""
    )
    body = "\n".join((HERE / f).read_text() for f in fragments)
    blocks.append(f'<section id="{section_id}" class="{parity}">{header}\n{body}</section>')

project_js = HERE.parent / "project.js"
extra_js = (
    f'<script>window.AM_LANGUAGE_URL = "#";</script><script src="{project_js.as_uri()}"></script>'
    if project_js.exists() else ""
)

html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Assessment Menu · Home (combined) preview</title>
<link rel="stylesheet" href="{(COMMON / 'css/bootstrap.css').as_uri()}">
<link rel="stylesheet" href="{(COMMON / 'css/bootstrap-responsive.css').as_uri()}">
<link rel="stylesheet" href="{(COMMON / 'css/fonts.css').as_uri()}">
<link rel="stylesheet" href="{(COMMON / 'css/custom.css').as_uri()}">
<link rel="stylesheet" href="{(COMMON / 'fontawesome-6.6.0/css/all.min.css').as_uri()}">
<link rel="stylesheet" href="{(THEME / 'cardiffuni-v3.css').as_uri()}">
<!-- Project > Optional properties > Styles -->
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="jumbotron logoL" id="overview"><div class="container">
  <div class="logoL"><img class="logo logoL themeLogo" src="{(THEME / 'logo_left.svg').as_uri()}" alt="Cardiff University / Prifysgol Caerdydd"></div>
  <div class="titles"><h1 id="pageTitle">{PAGE_TITLE}</h1><p id="pageSubTitle">{PAGE_SUBTITLE}</p></div>
</div></header>
<div id="pageLinks"><div class="navbar navbar-inverse" role="navigation"><div class="navbar-inner"><div class="container"><div class="nav-collapse collapse">
  <ul class="nav"><li class="activePage"><a href="#">Home</a></li><li><a href="#">Browse all</a></li><li><a href="#">Exams</a></li></ul>
</div></div></div></div></div>
<!-- Home page: Hide Menu + Expand Main Contents, so the content is full width -->
<div class="container"><div class="row-fluid">
<div class="span3 bs-docs-sidebar hideSectionMenu expandMain" id="contentTable"><ul class="nav nav-list bs-docs-sidenav affix" id="toc"></ul></div>
<div class="span9 expandMain" id="mainContent" role="main">
{chr(10).join(blocks)}
</div></div></div>
<footer class="footer"><div class="container"><div class="row-fluid"><p>Developed by the Digital Education Team, Learning and Teaching Academy, Cardiff University</p></div></div></footer>
<script src="{(COMMON / 'js/jquery-1.9.1.min.js').as_uri()}"></script>
{extra_js}
</body>
</html>
"""
out = HERE / "local-preview.html"
out.write_text(html)
print(f"wrote {out} ({len(blocks)} sections)")
