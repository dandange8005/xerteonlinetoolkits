"""The author guide's five build checks. Each returns findings; any error stops the build.

1 classes exist   2 coverage   3 references   4 stale editor evidence   5 example accessibility
"""
import datetime
import subprocess
from dataclasses import dataclass
from html.parser import HTMLParser


@dataclass(frozen=True)
class Finding:
    level: str  # "error" or "warning"
    check: int
    source: str
    message: str

    def __str__(self):
        return f"{self.level.upper()} [check {self.check}] {self.source}: {self.message}"


class _Scan(HTMLParser):
    """Collects an example's class names, images without alt text, empty headings and unbalanced tags."""
    HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
    # HTML lets these end without an end tag, so a missing end tag is not a mistake.
    OPTIONAL_END = {"p", "li", "dt", "dd", "tr", "td", "th", "thead", "tbody", "tfoot", "caption", "colgroup",
                    "option", "optgroup"}

    def __init__(self):
        super().__init__()
        self.classes, self.images_without_alt, self.empty_headings = set(), 0, 0
        self._heading, self._text = None, ""
        self._open, self._problems = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.classes.update((attrs.get("class") or "").split())
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt += 1
        if tag in self.HEADINGS:
            self._heading, self._text = tag, ""
        if tag not in self.VOID and tag not in self.OPTIONAL_END:
            self._open.append(tag)

    def handle_startendtag(self, tag, attrs):
        # In HTML a trailing slash does not close an element: <i/> is an open <i>. Only void
        # elements such as <br/> and <img/> are complete.
        self.handle_starttag(tag, attrs)
        if tag in self.VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self._heading:
            self._text += data

    def handle_endtag(self, tag):
        if tag not in self.VOID and tag not in self.OPTIONAL_END:
            self._close(tag)
        if tag == self._heading:
            if not self._text.strip():
                self.empty_headings += 1
            self._heading = None

    def _close(self, tag):
        if self._open and self._open[-1] == tag:
            self._open.pop()
        elif tag in self._open:
            self._problems.append(f"<{self._open[-1]}> is not closed before </{tag}>")
            while self._open.pop() != tag:
                pass
        else:
            self._problems.append(f"</{tag}> has no start tag")

    @property
    def unbalanced(self):
        """Problems found so far, plus every element still open."""
        return self._problems + [f"<{tag}> is not closed" for tag in self._open]


def scan(markup):
    parser = _Scan()
    parser.feed(markup)
    parser.close()
    return parser


def _examples(content):
    """Every example in the guide, with the file it came from."""
    for component in content.components.values():
        for example in component.examples:
            yield component.source, example
    for task in content.tasks.values():
        yield task.source, task.example


def _claimed(component):
    return set(component.parts) | {e.variant for e in component.examples if e.variant}


def check_classes_exist(content, known):
    """Check 1: every class a record names or an example uses is defined somewhere the guide loads."""
    findings = []
    for component in content.components.values():
        for cls in sorted(_claimed(component) - known):
            findings.append(Finding("error", 1, str(component.source),
                                    f"class '{cls}' is not defined by the theme or the player's stylesheets"))
    for source, example in _examples(content):
        for cls in sorted(scan(example.html).classes - known):
            findings.append(Finding("error", 1, str(source),
                                    f"example '{example.label}' uses class '{cls}', which no stylesheet defines"))
    return findings


def check_coverage(content, author_facing, tables, mode):
    """Check 2: every author-facing class is claimed by a record or shown in a generated table."""
    claimed = set(tables)
    for component in content.components.values():
        claimed |= _claimed(component)
    missing = sorted(author_facing - claimed)
    if not missing:
        return []
    shown = missing if mode == "fail" else missing[:10]
    more = "" if len(shown) == len(missing) else f" and {len(missing) - len(shown)} more"
    return [Finding("error" if mode == "fail" else "warning", 2, "guide",
                    f"{len(missing)} author-facing classes are not covered yet: {', '.join(shown)}{more}")]


def check_references(content, site, theme_dir):
    """Check 3: every group, task, related component, SCSS file and menu page exists."""
    findings = []

    def error(source, message):
        findings.append(Finding("error", 3, str(source), message))

    groups = {group for group, _ in site.groups}
    for component in content.components.values():
        if component.group not in groups:
            error(component.source, f"group '{component.group}' is not in site.toml")
        for name in component.related:
            if name not in content.components:
                error(component.source, f"related component '{name}' has no record")
        for path in component.scss:
            if not (theme_dir / path).is_file():
                error(component.source, f"SCSS file '{path}' does not exist")
    for task in content.tasks.values():
        for name in task.components:
            if name not in content.components:
                error(task.source, f"component '{name}' has no record")
    for name in sorted(set(content.tasks) - set(site.tasks)):
        error(content.tasks[name].source, f"task '{name}' is not listed in site.toml tasks")
    for name in site.tasks:
        if name not in content.tasks:
            error("site.toml", f"listed task '{name}' has no task file")
    if "index" not in content.pages:
        error("content/pages", "the home page pages/index.md is missing")
    for page, _ in site.menu:
        if page == "getting-started" and page not in content.pages:
            error("site.toml", "menu entry 'getting-started' needs pages/getting-started.md")
    return findings


def check_stale_evidence(content, last_changed):
    """Check 4: warn when a component's SCSS changed after its editor evidence was recorded."""
    findings = []
    for component in content.components.values():
        if component.editor is None:
            continue
        for path in component.scss:
            changed = last_changed(path)
            if changed and changed > component.editor.checked:
                findings.append(Finding(
                    "warning", 4, str(component.source),
                    f"{path} changed on {changed.isoformat()}, after the editor evidence of "
                    f"{component.editor.checked.isoformat()}; re-test in Xerte and update [editor]"))
    return findings


def git_last_changed(theme_dir):
    """A function giving the date of the last commit to a path, or None when git cannot say."""
    def last_changed(path):
        try:
            result = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=theme_dir,
                                    capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            return None
        text = result.stdout.strip()
        if result.returncode or not text:
            return None
        try:
            return datetime.date.fromisoformat(text)
        except ValueError:
            return None
    return last_changed


def check_examples(content):
    """Check 5: warn about images without alt text and empty headings in examples."""
    findings = []
    for source, example in _examples(content):
        found = scan(example.html)
        if found.images_without_alt:
            findings.append(Finding("warning", 5, str(source), f"example '{example.label}' has an image without alt text"))
        if found.empty_headings:
            findings.append(Finding("warning", 5, str(source), f"example '{example.label}' has an empty heading"))
        if found.unbalanced:
            findings.append(Finding("warning", 5, str(source),
                                    f"example '{example.label}' has unbalanced HTML: {found.unbalanced[0]}"))
    return findings


def run_all(content, site, *, theme_dir, known, author_facing, tables, last_changed):
    return (check_classes_exist(content, known)
            + check_coverage(content, author_facing, tables, site.coverage)
            + check_references(content, site, theme_dir)
            + check_stale_evidence(content, last_changed)
            + check_examples(content))
