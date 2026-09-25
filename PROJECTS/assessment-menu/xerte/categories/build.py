#!/usr/bin/env python3
"""Build one category page's Xerte fragments from the prototype's data, plus a local preview.

Every category page has the same shape (an "About" section, then one section per assessment
type), so the markup lives here once and the content comes from the prototype's menuData JSON.
Run: python3 build.py exams   (writes exams/NN-*.html and exams/local-preview.html)
"""
import html
import os
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE.parents[1] / "prototypes/2026-09-15_assessment-menu-xerte-prototype-v1.html"
XERTE = HERE.parents[3]  # repo root
THEME = XERTE / "themes/site/cardiffuniversity"
COMMON = XERTE / "modules/site/parent_templates/site/common"

LANES = {
    1: "Secure assurance of learning",
    2: "Open assessment for and as learning",
}
FIELDS = [
    ("What is it?", "What is it?"),
    ("What's it for?", "What's it for?"),
    ("AI considerations", "AI considerations"),
]
LATER_FIELDS = [
    ("Authenticity", "Authenticity"),
    ("Inclusive design and reasonable adjustments", "Inclusive Design and Reasonable Adjustments"),
]


def tidy(markup):
    """Collapse the source's line breaks and trailing spaces inside rich-text fields."""
    markup = re.sub(r"\s*\n\s*", " ", markup or "").strip()
    markup = re.sub(r"\s+(</(?:p|li)>)", r"\1", markup)
    markup = re.sub(r"(</(?:p|li)>)(?:\s*\1)+", r"\1", markup)  # the source has a few doubled closers
    return re.sub(r">\s*(<(?:p|ul|/ul|li)>)", r">\n\1", markup)


def usually(text):
    """"Usually Lane 1", but "Usually either lane": only the lane numbers keep their capital."""
    return "Usually " + re.sub(r"^Either lane$", "either lane", text)


def pill(text):
    """A lane pill is tinted for the lane it names; anything else stays neutral."""
    lane = re.match(r"(?:Usually )?Lane ([12])", text)
    either = text.lower().startswith("usually either")
    modifier = f" am-pill--lane{lane.group(1)}" if lane else " am-pill--either" if either else ""
    return f'<span class="am-pill{modifier}">{html.escape(text)}</span>'


def lane_card(data, t, n):
    lane = t["lanes"].get(str(n), {})
    body = tidy(lane.get("how"))
    if lane.get("example"):
        body += f'<h5 class="am-lane__label">Example</h5>{tidy(lane["example"])}'
    if lane.get("case"):
        body += f'<h5 class="am-lane__label">Case study</h5>{tidy(lane["case"])}'
    if t["notNormally"] == n:
        # The type leans to the other lane: say so first, and keep any existing text behind a toggle.
        note = f'<div class="am-lane__not-normally">{tidy(data["notNormally"][str(n)])}</div>'
        body = note + (
            f'<details class="am-lane__review"><summary>Lane {n} text in the current menu '
            f'(under review)</summary>{body}</details>' if body else ""
        )
    return (
        f'<div class="am-lane am-lane--{n}"><h4 class="am-lane__title">Lane {n}</h4>'
        f'<p class="am-lane__subtitle">{LANES[n]}</p>'
        f'{body or "<p>Content needed.</p>"}</div>'
    )


def fields(t, pairs):
    return "\n".join(
        f"<h3>{title}</h3>\n{tidy(t['fields'][key])}" for title, key in pairs if t["fields"].get(key)
    )


def about_fragment(data, cat, types):
    """Lists the category's own types, then those shared with it, each linking to its home page."""
    def item(t):
        home = "" if t["cat"] == cat["id"] else f' <span class="text-secondary">(in {data["catName"][t["cat"]]})</span>'
        return (
            f'  <li><a href="#{t["cat"]}|{t["id"]}">{html.escape(t["name"])}</a>: '
            f'{html.escape(usually(t["usually"]).replace("Usually", "usually", 1))}{home}</li>'
        )
    return f"<p>{html.escape(cat['intro'])}</p>\n<ul>\n" + "\n".join(map(item, types)) + "\n</ul>\n"


def type_fragment(data, t):
    summary = [pill(usually(t["usually"])), pill(t["other"])]
    summary += [f'<span class="am-pill am-pill--muted">Also in {data["catName"][c]}</span>' for c in t["also"]]
    note = (
        f'<p class="am-note"><strong>To resolve:</strong> {html.escape(t["note"])}</p>' if t["note"] else ""
    )
    voice = "".join(
        f'<blockquote class="quote"><p>{quote}</p></blockquote>'
        for quote in re.findall(r"<p>(.*?)</p>", tidy(t["fields"].get("Student Voice")))
    )
    parts = [
        f'<div class="am-pills">{"".join(summary)}</div>',
        note,
        fields(t, FIELDS),
        "<h3>Lane 1 and Lane 2</h3>",
        f'<div class="am-lanes">\n{lane_card(data, t, 1)}\n{lane_card(data, t, 2)}\n</div>',
        '<div class="cu-callout cu-callout-tip"><strong class="cu-callout-title">Practical considerations</strong>'
        '\n<p>Content needed: rooms and lab space, staff time '
        "and marking load at scale, timetabling, and resourcing adjustments.</p></div>",
        fields(t, LATER_FIELDS),
        f"<h3>Student voice</h3>\n{voice}" if voice else "",
        '<p><a class="link-action" href="#browse">Back to all assessment types</a></p>',
    ]
    return "\n".join(p for p in parts if p) + "\n"


def rel(path, cat):
    """Relative link from the preview, so it loads over file:// and from a local server alike."""
    return os.path.relpath(path, HERE / cat["id"])


BROWSE_SCRIPT = """<script>
(function () {
  var search = document.getElementById('amBrowseSearch');
  var filters = document.getElementById('amBrowseFilters');
  var cards = document.getElementById('amBrowseCards');
  var count = document.getElementById('amBrowseCount');
  var empty = document.getElementById('amBrowseEmpty');
  if (!search || !filters || !cards) { return; }

  var items = Array.prototype.slice.call(cards.children);
  var cat = 'all';

  /* The pressed state swaps the theme's outline button for its filled one, rather
     than recolouring it: .button-secondary-outline sets its text colour with !important. */
  function buttonClass(pressed) {
    return 'button ' + (pressed ? 'button-secondary' : 'button-secondary-outline') + ' button-sm';
  }

  function update() {
    var q = search.value.trim().toLowerCase();
    var shown = 0;
    items.forEach(function (card) {
      var match = (cat === 'all' || card.getAttribute('data-cats').split(' ').indexOf(cat) !== -1) &&
        card.getAttribute('data-search').indexOf(q) !== -1;
      card.hidden = !match;
      if (match) { shown += 1; }
    });
    count.textContent = shown + ' of ' + items.length + ' assessment types';
    empty.hidden = shown !== 0;
  }

  function setCategory(next) {
    cat = next;
    Array.prototype.forEach.call(filters.querySelectorAll('[data-cat]'), function (b) {
      var pressed = b.getAttribute('data-cat') === cat;
      b.setAttribute('aria-pressed', String(pressed));
      b.className = buttonClass(pressed);
    });
    update();
  }

  search.addEventListener('input', update);
  filters.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-cat]');
    if (btn) { setCategory(btn.getAttribute('data-cat')); }
  });
  document.getElementById('amBrowseReset').addEventListener('click', function () {
    search.value = '';
    setCategory('all');
  });
  update();
})();
</script>"""


def browse_card(data, t):
    cats = [t["cat"], *t["also"]]
    words = " ".join([t["name"], t["summary"], t["usually"], t["other"], *(data["catName"][c] for c in cats)])
    pills = pill(usually(t["usually"])) + "".join(
        f'<span class="am-pill am-pill--muted">{data["catName"][c]}</span>' for c in cats
    )
    return (
        f'<div class="card card--clickable" data-cats="{" ".join(cats)}" data-search="{html.escape(words.lower())}">'
        f'<div class="card__content"><h3 class="card__heading text-xl"><a class="card__link" href="#{t["cat"]}|{t["id"]}">'
        f'{html.escape(t["name"])}</a></h3><p class="card__description">{html.escape(t["summary"])}</p>'
        f'<div class="am-pills">{pills}</div></div></div>'
    )


def browse_fragment(data):
    def filter_button(cat_id, name, pressed=False):
        kind = "button-secondary" if pressed else "button-secondary-outline"
        return (
            f'<button class="button {kind} button-sm" type="button" data-cat="{cat_id}" '
            f'aria-pressed="{str(pressed).lower()}">{html.escape(name)}</button>'
        )

    buttons = filter_button("all", "All", True) + "".join(filter_button(c["id"], c["short"]) for c in data["categories"])
    cards = "\n".join(browse_card(data, t) for t in sorted(data["types"], key=lambda t: t["name"].casefold()))
    return f"""<p>Search all {len(data["types"])} types, or filter by category. Each card opens the full entry.</p>
<div class="am-browse-controls">
<label for="amBrowseSearch"><span class="block font-bold mb-2">Search assessment types</span>
<input id="amBrowseSearch" type="search" placeholder="Try viva, portfolio or reflection" autocomplete="off">
</label>
<div class="am-filters" id="amBrowseFilters" role="group" aria-label="Filter by category">{buttons}</div>
<p class="text-secondary text-base" id="amBrowseCount" role="status"></p>
</div>
<div class="am-cards" id="amBrowseCards">
{cards}
</div>
<p class="text-secondary" id="amBrowseEmpty" hidden>No types match. Try another word, or <button class="button button-secondary-outline button-sm" id="amBrowseReset" type="button">show all types</button></p>
{BROWSE_SCRIPT}
"""


def preview(cat, sections):
    blocks = "\n".join(
        f'<section id="{sid}" class="{"oddSection" if n % 2 else "evenSection"}">'
        f'<div class="page-header"><h2 class="sectionTitle">{html.escape(title)}</h2></div>\n'
        f'{(HERE / cat["id"] / frag).read_text()}</section>'
        for n, (sid, title, frag) in enumerate(sections, start=1)
    )
    toc = "".join(f'<li><a href="#{sid}">{html.escape(title)}</a></li>' for sid, title, _ in sections)
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Assessment Menu · {html.escape(cat['name'])} preview</title>
<link rel="stylesheet" href="{rel(COMMON / 'css/bootstrap.css', cat)}">
<link rel="stylesheet" href="{rel(COMMON / 'css/bootstrap-responsive.css', cat)}">
<link rel="stylesheet" href="{rel(COMMON / 'css/fonts.css', cat)}">
<link rel="stylesheet" href="{rel(COMMON / 'css/custom.css', cat)}">
<link rel="stylesheet" href="{rel(COMMON / 'fontawesome-6.6.0/css/all.min.css', cat)}">
<link rel="stylesheet" href="{rel(THEME / 'cardiffuniversity.css', cat)}">
<!-- Project > Optional properties > Styles -->
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<header class="jumbotron logoL"><div class="container">
  <div class="logoL"><img class="logo logoL themeLogo" src="{rel(THEME / 'logo_left.svg', cat)}" alt="Cardiff University / Prifysgol Caerdydd"></div>
  <div class="titles"><h1 id="pageTitle">{html.escape(cat['name'])}</h1><p id="pageSubTitle">{html.escape(cat['intro'])}</p></div>
</div></header>
<div class="container"><div class="row-fluid">
<div class="span3 bs-docs-sidebar" id="contentTable"><ul class="nav nav-list bs-docs-sidenav" id="toc">{toc}</ul></div>
<div class="span9" id="mainContent" role="main">
{blocks}
</div></div></div>
</body>
</html>
"""


BROWSE = {
    "id": "browse",
    "name": "Browse all assessment types",
    "intro": "Search the full list or filter by category",
}


def write(out, sections, cat):
    (out / "local-preview.html").write_text(preview(cat, sections))
    print(f"wrote {out}: " + ", ".join(f for _, _, f in sections))


def main(cat_id):
    source = SOURCE.read_text()
    data = json.loads(re.search(r'id="menuData">(.*?)</script>', source, re.S).group(1))
    out = HERE / cat_id
    out.mkdir(exist_ok=True)

    if cat_id == "browse":
        (out / "01-all-types.html").write_text(browse_fragment(data))
        return write(out, [("all-types", "All assessment types", "01-all-types.html")], BROWSE)

    cat = next(c for c in data["categories"] if c["id"] == cat_id)
    types = [t for t in data["types"] if t["cat"] == cat_id]
    shared = [t for t in data["types"] if cat_id in t["also"]]

    # (Section ID, Section Title, fragment). Type section IDs match the Home finder's links.
    sections = [(f"{cat_id}-about", "About this category", "01-about.html")]
    (out / "01-about.html").write_text(about_fragment(data, cat, types + shared))
    for n, t in enumerate(types, start=2):
        frag = f"{n:02d}-{t['id']}.html"
        (out / frag).write_text(type_fragment(data, t))
        sections.append((t["id"], t["name"], frag))
    write(out, sections, cat)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "exams")
