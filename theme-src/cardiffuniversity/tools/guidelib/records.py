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
COMPONENT_HEADINGS = ((2, "When to use it"), (2, "When not to use it"), (2, "How to use it"),
                      (3, "Do"), (3, "Don't"), (2, "Accessibility"))
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
    when_html: str
    when_not_html: str
    how_html: str
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


def _read(path):
    """A record's text. A UTF-8 byte order mark is dropped; any other encoding names the file."""
    try:
        return Path(path).read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        raise RecordError(path, "is not saved as UTF-8; save it as UTF-8 and build again") from None


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
    data, body, line = split_front_matter(_read(path), path)
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
    when, when_not, how, do, dont, accessibility = _expect(sections(body, path, line), COMPONENT_HEADINGS, path)
    for section in (when, when_not, do, dont, accessibility):
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
        parts=dict(parts), examples=examples, when_html=when.html, when_not_html=when_not.html,
        how_html=how.html, do_html=do.html, dont_html=dont.html, accessibility_html=accessibility.html,
        source=path)


def load_task(path):
    path = Path(path)
    data, body, line = split_front_matter(_read(path), path)
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
    data, body, line = split_front_matter(_read(path), path)
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
        data = tomllib.loads(_read(path))
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
