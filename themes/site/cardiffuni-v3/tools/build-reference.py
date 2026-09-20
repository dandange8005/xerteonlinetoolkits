#!/usr/bin/env python3
"""Generate the guide's utility reference from the compiled theme, and report what is undocumented.

The guide is for content authors, so the reference must describe classes that really exist.
Hand-written tables drift: the demos documented .w-md-50 and .image-full long after they were
gone. This reads cardiffuni-v3.css instead and writes the tables into the guide between
markers, then checks every class the theme defines is either documented or deliberately not.

Usage (from the theme folder):
    python3 tools/build-reference.py            write the tables into the guide
    python3 tools/build-reference.py --check    report only; exit 1 if the guide is out of date
    python3 tools/build-reference.py --coverage list theme classes no guide page mentions

Standard library only.
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEME = HERE.parent
CSS = THEME / "cardiffuni-v3.css"
GUIDE = THEME / "demos" / "code-utilities.html"
DEMOS = THEME / "demos"
PLAYER = THEME.parents[2] / "modules" / "site" / "parent_templates" / "site" / "common"

START = "<!-- @generated: utility reference (tools/build-reference.py) -->"
END = "<!-- @end generated -->"

# Utility families, in the order they appear in the guide. Each entry is a heading, a short
# line of guidance for authors, and the class-name patterns that belong to it.
FAMILIES = [
    ("Spacing", "Margin (m) and padding (p) on all sides, or one axis: t top, b bottom, l left, r right, x sides, y top and bottom. The number is the step on the 4px scale.",
     r"^[mp][tblrxy]?-(0|px|\d+|auto)$"),
    ("Text size", "Set the size of a run of text. Body copy is already 18px, so reach for these only when a line needs to stand apart.",
     r"^text-(xs|sm|base|lg|xl|2xl|3xl|4xl)$"),
    ("Text colour", "Colour by role. Avoid colour as the only way a reader can tell two things apart.",
     r"^text-(cu-\w+|primary|secondary|tertiary|brand|inverse|muted|white|black)$"),
    ("Text style", "Weight, case and alignment.",
     r"^(font-(light|normal|medium|semibold|bold)|uppercase|lowercase|capitalize|italic|text-(left|center|right|justify))$"),
    ("Layout", "Display and position. Most page content needs none of these.",
     r"^(block|inline|inline-block|hidden|grid|flex|relative|absolute|fixed|sticky|static)$"),
    ("Flex", "Rows and columns that wrap. flex-300 means a column at least 300px wide that wraps when there is no room.",
     r"^(flex-\w+|items-\w+|justify-\w+|gap-\w+|self-\w+)$"),
    ("Width and height", "Sizing helpers.",
     r"^(w-\w+|h-\w+|max-w-\w+|min-w-\w+)$"),
    ("Borders and corners", "Corner rounding. Page content in this theme is square by default.",
     r"^rounded(-\w+)?$"),
    ("Background", "Background colour by role.",
     r"^bg-[\w-]+$"),
    ("Accessibility", "Helpers that affect what assistive technology announces.",
     r"^(visually-hidden|sr-only)$"),
    ("Rarely needed", "Overflow, stacking and pointer behaviour. Page content is flat, so the shadow classes resolve to no shadow except on overlays such as dropdowns and modals.",
     r"^(overflow-\w+|z-\d+|cursor-[\w-]+|pointer-events-\w+|shadow(-\w+)?)$"),
]

# Classes worth documenting whose rule has more declarations than a plain utility.
ALLOW_MULTI = {"visually-hidden"}

# Classes the guide deliberately does not teach, with the reason shown to authors where relevant.
LEGACY = {
    "action-link": "Legacy. Kept so older resources keep working; use link-action in new content.",
    "c10": "Legacy System 2 column width.", "c20": "Legacy System 2 column width.",
    "c30": "Legacy System 2 column width.", "c40": "Legacy System 2 column width.",
    "c60": "Legacy System 2 column width.", "c70": "Legacy System 2 column width.",
    "c80": "Legacy System 2 column width.",
    "topMargin": "Legacy System 2 spacing.", "w3": "Legacy System 2 width.",
    "org": "Legacy System 2 organisation block.",
    "screenshots": "Older alias of image-screenshots.",
}

# Classes that belong to the page frame or the editor, not to content an author writes.
FRAME_PREFIXES = (
    "navbar", "nav-", "jumbotron", "bs-docs", "activePage", "backBtn", "footer", "feedback",
    "backToTop", "logo", "titles", "pageTitle", "pageSubTitle", "sectionTitle", "contentTitle",
    "x_", "xerte", "editorStyle", "cardiff-test-style", "language-toggle", "project-info",
    "sectionSubLinks", "hideSectionMenu", "expandMain", "stickyTop", "affix", "carousel",
    "modal", "tooltip", "popover", "dropdown", "accordion", "tab-", "nav-tabs", "nav-list",
    # .focus-visible only applies the focus ring to a custom control: for developers, not authors.
    "focus-visible",
)


def rules(css):
    """Yield (selector, body, media) for every rule, tracking @media nesting."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, media, depth, i = [], None, 0, 0
    token = ""
    while i < len(css):
        ch = css[i]
        if ch == "{":
            depth += 1
            if depth == 1 and token.strip().startswith("@media"):
                media = token.strip()
                token = ""
            elif depth in (1, 2):
                selector = token.strip()
                body, j, d = "", i + 1, 1
                while j < len(css) and d:
                    if css[j] == "{":
                        d += 1
                    elif css[j] == "}":
                        d -= 1
                        if not d:
                            break
                    body += css[j]
                    j += 1
                out.append((selector, body, media))
                token = ""
                i = j
                depth -= 1
            token = ""
        elif ch == "}":
            depth -= 1
            if depth <= 0:
                media, depth = None, 0
            token = ""
        else:
            token += ch
        i += 1
    return out


def utilities():
    """Single-class rules with a short body: the theme's utility classes."""
    found = {}
    for selector, body, media in rules(CSS.read_text(encoding="utf-8")):
        if media:
            continue
        for part in selector.split(","):
            part = part.strip()
            m = re.fullmatch(r"\.(-?[A-Za-z_][\w-]*)", part)
            if not m:
                continue
            decls = [d.strip() for d in body.split(";") if d.strip()]
            if not decls or (len(decls) > 3 and m.group(1) not in ALLOW_MULTI):
                continue
            if m.group(1) in ALLOW_MULTI:
                decls = decls[:2] + ["..."]
            value = "; ".join(d.replace(" !important", "") for d in decls)
            found.setdefault(m.group(1), value)
    table = tokens()
    return {c: resolve(v, table) for c, v in found.items()}


def tokens():
    """Map custom property names to their value, from the compiled theme's :root blocks."""
    css = re.sub(r"/\*.*?\*/", "", CSS.read_text(encoding="utf-8"), flags=re.S)
    found = {}
    for body in re.findall(r":root\s*\{([^}]*)\}", css):
        for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body):
            found.setdefault(name.strip(), value.strip())
    return found


def resolve(value, table, depth=0):
    """Replace var(--x) with its value so authors read real sizes, not token names."""
    if depth > 4:
        return value

    def swap(match):
        name, fallback = match.group(1), match.group(2)
        if name in table:
            return resolve(table[name], table, depth + 1)
        return fallback.strip() if fallback else match.group(0)

    return re.sub(r"var\(\s*(--[\w-]+)\s*(?:,([^()]*))?\)", swap, value)


def theme_classes():
    css = re.sub(r"/\*.*?\*/", "", CSS.read_text(encoding="utf-8"), flags=re.S)
    own = set(re.findall(r"\.(-?[A-Za-z_][\w-]*)", css))
    for name in ("css/custom.css", "css/bootstrap.css", "css/bootstrap-responsive.css",
                 "fontawesome-6.6.0/css/all.min.css"):
        path = PLAYER / name
        if path.exists():
            other = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
            own -= set(re.findall(r"\.(-?[A-Za-z_][\w-]*)", other))
    return own


def render_tables(utils):
    used, blocks = set(), []
    for heading, guidance, pattern in FAMILIES:
        rows = sorted((c, v) for c, v in utils.items() if re.match(pattern, c) and c not in LEGACY)
        if not rows:
            continue
        used |= {c for c, _ in rows}
        body = "\n".join(
            f"                            <tr><td><code>.{html.escape(c)}</code></td>"
            f"<td>{html.escape(v)}</td></tr>"
            for c, v in rows)
        blocks.append(f"""            <div class="demo-block">
                <div class="demo-block__title">{heading}</div>
                <p class="demo-block__description">{guidance}</p>
                <table>
                    <thead>
                        <tr><th>Class</th><th>What it sets</th></tr>
                    </thead>
                    <tbody>
{body}
                    </tbody>
                </table>
            </div>""")
    legacy_rows = "\n".join(
        f"                            <tr><td><code>.{html.escape(c)}</code></td>"
        f"<td>{html.escape(why)}</td></tr>"
        for c, why in sorted(LEGACY.items()))
    blocks.append(f"""            <div class="demo-block demo-block--highlight">
                <div class="demo-block__title">Legacy classes &mdash; do not use in new content</div>
                <p class="demo-block__description">These still work so that older resources keep rendering. Do not reach for them when writing something new.</p>
                <table>
                    <thead>
                        <tr><th>Class</th><th>Why it is here</th></tr>
                    </thead>
                    <tbody>
{legacy_rows}
                    </tbody>
                </table>
            </div>""")
    return used, "\n\n".join(blocks)


def coverage(utils, documented):
    mentioned = set()
    for page in sorted(DEMOS.glob("*.html")):
        html = page.read_text(encoding="utf-8")
        mentioned |= set(re.findall(r"\.(-?[A-Za-z_][\w-]*)", html))
        for m in re.finditer(r'class="([^"]+)"', html):
            mentioned |= set(m.group(1).split())
    missing = []
    for cls in sorted(theme_classes()):
        if cls in documented or cls in mentioned or cls in LEGACY:
            continue
        if cls.startswith(FRAME_PREFIXES):
            continue
        missing.append(cls)
    return missing


def main():
    args = sys.argv[1:]
    utils = utilities()
    documented, tables = render_tables(utils)

    if "--coverage" in args:
        missing = coverage(utils, documented)
        print(f"{len(missing)} theme classes no guide page documents or shows:")
        for cls in missing:
            print("   ", cls)
        return 1 if missing else 0

    guide = GUIDE.read_text(encoding="utf-8")
    if START not in guide or END not in guide:
        sys.exit(f"ERROR: markers not found in {GUIDE}. Add {START} and {END} around the reference.")
    # lambda, not a replacement string: a CSS escape such as \f0eb in a value would otherwise
    # be read as a backreference and raise, or silently mangle the guide.
    fresh = re.sub(re.escape(START) + r".*?" + re.escape(END),
                   lambda _: START + "\n" + tables + "\n" + END, guide, flags=re.S)
    if fresh == guide:
        print(f"In sync: {GUIDE.name} matches the compiled theme ({len(documented)} classes documented).")
        return 0
    if "--check" in args:
        print(f"OUT OF DATE: {GUIDE.name} differs from the compiled theme. Run: python3 tools/build-reference.py")
        return 1
    GUIDE.write_text(fresh, encoding="utf-8")
    print(f"Updated: {GUIDE.name} ({len(documented)} classes documented).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
