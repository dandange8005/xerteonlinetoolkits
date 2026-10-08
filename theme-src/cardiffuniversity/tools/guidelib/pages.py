"""Render the author guide's pages from loaded records.

Component pages follow design direction A (side menu, page, "on this page" list). The home page
and task pages follow direction B. Every page uses guide/templates/base.html.

Blocks are <div class="g-section">, never <section>: the theme styles every section element as
a Xerte page section (margins, list grids), which would reshape the guide's own layout.
"""
import html
from dataclasses import dataclass
from string import Template

from guidelib import assets
from guidelib.mdsubset import code_block

TOP_PATHS = {"home": "index.html", "getting-started": "getting-started.html",
             "tasks": "tasks/index.html", "components": "components/index.html"}
XERTE_PASTE = "In Xerte: add a Text content item, open its Source view, then paste."
LOGO_ALT = "Cardiff University / Prifysgol Caerdydd"


def _unknown(path):
    return None


@dataclass(frozen=True)
class Ctx:
    site: object
    content: object
    template: Template
    updated: object = _unknown  # path of a record -> date it last changed, or None


def esc(text):
    return html.escape(text, quote=True)


def long_date(day):
    return f"{day.day} {day:%B %Y}"


def _current(on):
    return ' aria-current="page"' if on else ""


def page_shell(ctx, *, title, root, active, body, home=False):
    styles = "\n".join(f'<link rel="stylesheet" href="{root}{href}">' for href in assets.STYLESHEETS)
    scripts = "\n".join(f'<script src="{root}{src}"></script>' for src in assets.SCRIPTS)
    return ctx.template.substitute(title=esc(title), site_title=esc(ctx.site.title), root=root, styles=styles,
                                   scripts=scripts, header=site_header(ctx, root, active, home), body=body)


def site_header(ctx, root, active, home):
    """Logo and title. The home page (direction B) puts the menu in the header; other pages
    (direction A) put it in a dark bar below."""
    brand = (f'<img class="g-logo" src="{root}{assets.LOGO}" alt="{LOGO_ALT}">'
             f'<a class="g-brand" href="{root}index.html"><span class="g-brand-title">Author guide</span>'
             '<span class="g-brand-sub">Cardiff University Xerte theme</span></a>')
    menu = top_menu(ctx, root, active)
    if home:
        return f'<header class="g-header g-header-home">{brand}{menu}</header>'
    return f'<header class="g-header">{brand}</header>{menu}'


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


def example_frame(markup):
    """The rendered example, framed, with its HTML behind a toggle (NHS service manual style).
    In Xerte, pasted HTML sits inside a section element, so the preview does too."""
    return ('<div class="g-example">'
            f'<div class="g-preview" role="group" aria-label="Rendered example"><section>{markup}</section></div>'
            f'<details class="g-code-toggle"><summary>HTML</summary>{code_block(markup)}'
            f'<p class="g-note">{XERTE_PASTE}</p></details></div>')


def variant_meta(example):
    return (f'<p class="g-variant-meta"><code>.{esc(example.variant)}</code> &middot; {esc(example.purpose)}</p>'
            if example.variant else f'<p class="g-variant-meta">{esc(example.purpose)}</p>')


def updated_line(ctx, source):
    day = ctx.updated(source)
    return f'<p class="g-updated">Page updated: {long_date(day)}</p>' if day else ""


def table(headers, rows, extra=""):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    return f'<table class="g-table {extra}"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'


def evidence(component):
    editor = component.editor
    if editor is None:
        editor_text = "Not tested in the Xerte editor yet"
    else:
        verdict = "Survives the editor" if editor.survives else "Changed by the editor"
        editor_text = f"{verdict} (checked {long_date(editor.checked)}, Xerte {esc(editor.xerte)})"
    rows = (("Status", esc(component.status.capitalize())),
            ("Since", f"Design system {esc(component.since)}"),
            ("Xerte editor", editor_text),
            ("Main class", f"<code>.{esc(next(iter(component.parts)))}</code>"))
    return '<dl class="g-evidence">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>"


def tasks_using(ctx, component):
    """Tasks whose task file lists this component, in site.toml's task order."""
    found = (ctx.content.tasks.get(name) for name in ctx.site.tasks)
    return [task for task in found if task and component.name in task.components]


def related_links(ctx, component, root):
    links = [f'<a href="{name}.html">{esc(ctx.content.components[name].title)}</a>' for name in component.related]
    links += [f'<a href="{root}tasks/{task.name}.html">Task: {esc(task.title)}</a>' for task in tasks_using(ctx, component)]
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
    """Example first, then the guidance sections in the NHS service manual's order."""
    root = "../"
    first = component.examples[0]
    others = [e for e in component.examples[1:] if e.variant]
    # The first example comes straight after the lead, with no heading (as on the NHS pages).
    top = f'<div class="g-top-example">{variant_meta(first)}{example_frame(first.html)}</div>'
    parts = [("when-to-use-it", "When to use it", component.when_html),
             ("when-not-to-use-it", "When not to use it", component.when_not_html),
             ("how-to-use-it", "How to use it",
              component.how_html + '<div class="g-cols"><div class="g-do">'
              + '<h3><i class="fa-solid fa-check" aria-hidden="true"></i> Do</h3>' + component.do_html
              + '</div><div class="g-dont"><h3><i class="fa-solid fa-xmark" aria-hidden="true"></i> Don\'t</h3>'
              + component.dont_html + "</div></div>")]
    if others:
        # Each variant is rendered once: the first example is already shown at the top.
        shown = f"<p>{esc(first.label)} is shown at the top of the page.</p>" if first.variant else ""
        blocks = "".join(f'<div class="g-variant"><h3>{esc(e.label)}</h3>{variant_meta(e)}{example_frame(e.html)}</div>'
                         for e in others)
        parts.append(("variants", "Variants", shown + blocks))
    part_rows = "".join(f"<tr><td><code>.{esc(cls)}</code></td><td>{esc(what)}</td></tr>"
                        for cls, what in component.parts.items())
    parts.append(("parts", "Parts", table(("Class", "What it is"), part_rows)))
    parts.append(("accessibility", "Accessibility", component.accessibility_html))
    parts.append(("evidence", "Evidence", evidence(component)))
    related = related_links(ctx, component, root)
    if related:
        parts.append(("related", "Related", related))
    sections = "".join(f'<div class="g-section" aria-labelledby="{sid}" role="region"><h2 id="{sid}">{esc(title)}</h2>{body}</div>'
                       for sid, title, body in parts)
    main = (f'<p class="g-crumb"><a href="index.html">Components</a> &rsaquo; {esc(component.title)}</p>'
            f'<h1>{esc(component.title)}</h1><p class="g-lead">{esc(component.lead)}</p>'
            f'{top}{sections}{updated_line(ctx, component.source)}{pager(ctx, component)}')
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
    how_block = (f'<div class="g-band" aria-labelledby="how-title" role="region"><h2 id="how-title">How each task works</h2>'
                 f'<ol class="g-steps">{how}</ol></div>') if how else ""
    body = (f'<main id="main"><div class="g-hero"><div class="g-wrap g-hero-grid"><div>'
            f'<h1>{esc(page.title)}</h1><p class="g-lead">{esc(page.lead)}</p></div>{aside}</div></div>'
            f'<div class="g-wrap"><div class="g-band" aria-labelledby="tasks-title" role="region">'
            f'<h2 id="tasks-title">Common tasks</h2>{task_tiles(ctx, root)}</div>{how_block}'
            f'{"".join(_section_html(s) for s in page.sections)}{updated_line(ctx, page.source)}</div></main>')
    return page_shell(ctx, title=page.title, root=root, active="home", body=body, home=True)


def task_page(ctx, task):
    root = "../"
    cards = "".join(f'<li class="g-card"><a href="{root}components/{name}.html">{esc(ctx.content.components[name].title)}</a>'
                    f'<p>{esc(ctx.content.components[name].lead)}</p></li>' for name in task.components)
    example = task.example
    body = (f'<main id="main" class="g-wrap g-page">'
            f'<p class="g-crumb"><a href="index.html">Tasks</a> &rsaquo; {esc(task.title)}</p>'
            f'<h1>{esc(task.title)}</h1><p class="g-lead">{esc(task.summary)}</p>'
            f'<div class="g-section" aria-labelledby="goal" role="region"><h2 id="goal">Goal</h2>{task.goal_html}</div>'
            f'<div class="g-section" aria-labelledby="use" role="region"><h2 id="use">Components to use</h2><ul class="g-cards">{cards}</ul></div>'
            f'<div class="g-section" aria-labelledby="example" role="region"><h2 id="example">Worked example: {esc(example.label)}</h2>'
            f'<p>{esc(example.purpose)}</p>{example_frame(example.html)}</div>'
            f'<div class="g-section" aria-labelledby="checklist" role="region"><h2 id="checklist">Checklist</h2>'
            f'<div class="g-checklist">{task.checklist_html}</div></div>{updated_line(ctx, task.source)}</main>')
    return page_shell(ctx, title=task.title, root=root, active="tasks", body=body)


def simple_page(ctx, page, active):
    root = ""
    content = "".join(_section_html(s) for s in page.sections)
    toc = on_this_page([(s.slug, s.title) for s in page.sections if s.level == 2])
    body = (f'<div class="g-shell g-shell-doc"><main id="main" class="g-main"><h1>{esc(page.title)}</h1>'
            f'<p class="g-lead">{esc(page.lead)}</p>{content}{updated_line(ctx, page.source)}</main>{toc}</div>')
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


def write_site(out, site, content, template_path, updated=None):
    """updated, if given, maps a record's path to the date it last changed (or None)."""
    ctx = Ctx(site, content, Template(template_path.read_text(encoding="utf-8")), updated or _unknown)
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
