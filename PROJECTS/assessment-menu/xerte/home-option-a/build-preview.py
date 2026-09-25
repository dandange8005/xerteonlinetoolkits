#!/usr/bin/env python3
"""Stitch the section fragments into local-preview.html, inside the Cardiff theme page frame.

The fragments, styles.css and script.js are what gets pasted into Xerte; this file only exists to
check them against the real theme CSS. styles.css and script.js are linked, not inlined, so the
preview cannot drift from the source. Run: python3 build-preview.py
"""
from pathlib import Path

HERE = Path(__file__).parent
XERTE = Path.home() / "Projects/xerteonlinetoolkits"
THEME = XERTE / "themes/site/cardiffuniversity"
COMMON = XERTE / "modules/site/parent_templates/site/common"

PAGE_TITLE = "Assessment Menu"
PAGE_SUBTITLE = "Designing meaningful, inclusive and future-focused assessment"

# One entry per Xerte Section: (Section ID, Section Title, [fragments in that section]).
# The Section ID must be set in the editor: the player uses it as the section's DOM id, and
# styles.css hangs the full-width bands off those ids. The titles are hidden by styles.css but
# still name the section for screen readers, so they are written out here as the player does.
SECTIONS = [
    ("intro", "Introduction", ["s1-hero.html"]),
    ("tool", "A design tool, not a list of replacements", ["s2-strip.html"]),
    ("questions", "Six questions to design with", ["s3-questions.html"]),
    ("briefs", "What shapes the menu", ["s4-briefs.html"]),
    ("categories", "Browse by category", ["s5-categories.html"]),
    ("alongside", "Use this menu alongside", ["s6-alongside.html"]),
]

# Mirrors what the player emits around each section, checked against a real page: the section
# carries aria-labelledby, the title sits in a .page-header, and a "Top" link is appended in its
# own paragraph. The player does not add oddSection/evenSection classes here.
blocks = []
for section_id, title, fragments in SECTIONS:
    header = f'<div class="page-header"><h2 id="{section_id}_title" class="sectionTitle">{title}</h2></div>'
    body = "\n".join((HERE / f).read_text() for f in fragments)
    top = '<p><br><a class="topBtn btn btn-mini pull-right" href="#skipLink">Top</a></p>'
    blocks.append(
        f'<section id="{section_id}" aria-labelledby="{section_id}_title">{header}\n{body}\n{top}</section>'
    )

html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Assessment Menu · Home (option A) preview</title>
<link rel="stylesheet" href="{(COMMON / 'css/bootstrap.css').as_uri()}">
<link rel="stylesheet" href="{(COMMON / 'css/bootstrap-responsive.css').as_uri()}">
<link rel="stylesheet" href="{(COMMON / 'css/fonts.css').as_uri()}">
<link rel="stylesheet" href="{(COMMON / 'css/custom.css').as_uri()}">
<link rel="stylesheet" href="{(COMMON / 'fontawesome-6.6.0/css/all.min.css').as_uri()}">
<link rel="stylesheet" href="{(THEME / 'cardiffuniversity.css').as_uri()}">
<!-- Home-page style block, linked here for local preview -->
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
<div class="container"><div class="row-fluid">
<div class="span3 bs-docs-sidebar hideSectionMenu expandMain" id="contentTable"><ul class="nav nav-list bs-docs-sidenav affix" id="toc"></ul></div>
<div class="span9 expandMain" id="mainContent" role="main">
{chr(10).join(blocks)}
</div></div></div>
<footer class="footer"><div class="container"><div class="row-fluid"><p>Developed by the Digital Education Team, Learning and Teaching Academy, Cardiff University</p></div></div></footer>
<script src="{(COMMON / 'js/jquery-1.9.1.min.js').as_uri()}"></script>
<!-- Project > Optional properties > Script -->
<script src="script.js"></script>
</body>
</html>
"""
out = HERE / "local-preview.html"
out.write_text(html)
print(f"wrote {out} ({len(blocks)} sections)")
