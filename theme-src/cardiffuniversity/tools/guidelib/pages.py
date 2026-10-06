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
