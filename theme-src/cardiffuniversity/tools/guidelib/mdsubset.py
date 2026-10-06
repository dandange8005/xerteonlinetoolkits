"""The Markdown subset the author guide allows, rendered to HTML.

Allowed: ## and ### headings, paragraphs, - and 1. lists, fenced code blocks, **bold**, *italic*,
`code` and [links](url). Anything else is an error naming the file and line, so nothing is
silently mangled. Raw HTML is not allowed: markup belongs in a record's examples.
"""
import html
import re
from dataclasses import dataclass


class MarkdownError(ValueError):
    """A construct outside the subset, with the file and line it came from."""

    def __init__(self, source, line, message):
        super().__init__(f"{source}:{line}: {message}")


@dataclass(frozen=True)
class Section:
    """The text under one heading. level is 0 for text before the first heading."""
    level: int
    title: str
    slug: str
    html: str


HEADING = re.compile(r"^(#+)\s+(\S.*)$")
BULLET = re.compile(r"^- (.+)$")
NUMBERED = re.compile(r"^\d+\. (.+)$")
FENCE = re.compile(r"^```([\w-]*)\s*$")
UNSUPPORTED = (
    (re.compile(r"^>"), "block quotes"),
    (re.compile(r"^\|"), "tables"),
    (re.compile(r"^[*+]\s"), "lists marked with * or + (use -)"),
    (re.compile(r"^\s+\S"), "indented lines (nested lists and indented code)"),
    (re.compile(r"^(-{3,}|\*{3,}|_{3,})\s*$"), "horizontal rules"),
)
RAW_HTML = re.compile(r"</?[A-Za-z!]")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
SCHEME = re.compile(r"^([A-Za-z][\w+.-]*):")
SAFE_SCHEMES = {"http", "https", "mailto"}


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def code_block(text, language=""):
    """A code view with a copy button. The button stays hidden until guide.js can make it work."""
    attr = f' class="language-{language}"' if language else ""
    return (f'<div class="g-code-wrap"><pre class="g-code"><code{attr}>{html.escape(text)}</code></pre>'
            '<button class="g-copy" type="button" hidden>Copy</button></div>')


def inline(text, source, line):
    """Render one line: code spans, links, bold and italic. Everything else is escaped."""
    out = []
    for i, part in enumerate(re.split(r"(`[^`]+`)", text)):
        if i % 2:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        if RAW_HTML.search(part):
            raise MarkdownError(source, line, "raw HTML is not allowed; put markup in an example")
        if "![" in part:
            raise MarkdownError(source, line, "images are not in the guide's Markdown subset")
        out.append(_links(part, source, line))
    return "".join(out)


def _links(text, source, line):
    out, pos = [], 0
    for match in LINK.finditer(text):
        url = match.group(2)
        scheme = SCHEME.match(url)
        if scheme and scheme.group(1).lower() not in SAFE_SCHEMES:
            raise MarkdownError(source, line, f"link scheme '{scheme.group(1)}:' is not allowed")
        out.append(_emphasis(text[pos:match.start()]))
        out.append(f'<a href="{html.escape(url)}">{_emphasis(match.group(1))}</a>')
        pos = match.end()
    out.append(_emphasis(text[pos:]))
    return "".join(out)


def _emphasis(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)


def _reject(raw, source, line):
    for pattern, what in UNSUPPORTED:
        if pattern.match(raw):
            raise MarkdownError(source, line, f"{what} are not in the guide's Markdown subset")


def _starts_block(raw):
    return bool(FENCE.match(raw) or HEADING.match(raw) or BULLET.match(raw) or NUMBERED.match(raw))


def sections(text, source, first_line=1):
    """Split text into sections at ## and ### headings, rendering each section's blocks."""
    lines = text.replace("\r\n", "\n").split("\n")
    found, level, title, chunks = [], 0, "", []
    i = 0
    while i < len(lines):
        raw, number = lines[i], first_line + i
        if not raw.strip():
            i += 1
            continue
        fence = FENCE.match(raw)
        if fence:
            end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("```")), None)
            if end is None:
                raise MarkdownError(source, number, "code block is not closed with ```")
            chunks.append(code_block("\n".join(lines[i + 1:end]), fence.group(1)))
            i = end + 1
            continue
        heading = HEADING.match(raw)
        if heading:
            if len(heading.group(1)) not in (2, 3):
                raise MarkdownError(source, number, f"only ## and ### headings are allowed, not {heading.group(1)}")
            found.append(Section(level, title, slugify(title), "\n".join(chunks)))
            level, title, chunks = len(heading.group(1)), heading.group(2).strip(), []
            i += 1
            continue
        _reject(raw, source, number)
        marker = BULLET if BULLET.match(raw) else NUMBERED if NUMBERED.match(raw) else None
        if marker:
            tag = "ul" if marker is BULLET else "ol"
            items = []
            while i < len(lines) and lines[i].strip():
                item = marker.match(lines[i])
                if not item:
                    raise MarkdownError(source, first_line + i,
                                        "a list must use one marker throughout and end with a blank line")
                items.append(f"<li>{inline(item.group(1), source, first_line + i)}</li>")
                i += 1
            chunks.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        words = []
        while i < len(lines) and lines[i].strip() and not _starts_block(lines[i]):
            _reject(lines[i], source, first_line + i)
            words.append(inline(lines[i].strip(), source, first_line + i))
            i += 1
        chunks.append(f"<p>{' '.join(words)}</p>")
    found.append(Section(level, title, slugify(title), "\n".join(chunks)))
    return [s for s in found if s.level or s.html]
