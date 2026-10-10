"""What the compiled theme and the player's stylesheets define, shared by the guide tools.

build-reference.py writes the demos' utility tables from this, and build-guide.py checks the
author guide against it. Standard library only.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEME = HERE.parent  # theme-src/cardiffuniversity
REPO = THEME.parents[1]
CSS = REPO / "themes" / "site" / "cardiffuniversity" / "cardiffuniversity.css"
PLAYER = REPO / "modules" / "site" / "parent_templates" / "site" / "common"
# Font Awesome moved out of the player's folder into modules/common (the player links it from there).
COMMON = REPO / "modules" / "common"
FONTAWESOME = "fontawesome-6.6.0"


def player_path(name):
    """Where one of the player's files lives: Font Awesome in modules/common, the rest beside the player."""
    return (COMMON if name.split("/")[0] == FONTAWESOME else PLAYER) / name

# The player's stylesheets, in the order modules/site/player_html5/rloObject.htm links them.
# The player appends the theme after these. css/fonts.css is left out: it holds only a
# commented placeholder. custom.css @imports css/editorstyles.css, listed separately.
PLAYER_CSS = (
    "css/bootstrap.css",
    "css/bootstrap-responsive.css",
    "css/custom.css",
    "fontawesome-6.6.0/css/all.min.css",
    "fontawesome-6.6.0/css/v4-shims.min.css",
    "fontawesome-6.6.0/css/v5-font-face.min.css",
)
IMPORTED_CSS = ("css/editorstyles.css",)

# Stylesheets whose classes do not count as the theme's own. Unchanged from build-reference.py,
# so its tables and coverage report do not move.
BASE_CSS = ("css/custom.css", "css/bootstrap.css", "css/bootstrap-responsive.css",
            "fontawesome-6.6.0/css/all.min.css")

CLASS = re.compile(r"\.(-?[A-Za-z_][\w-]*)")

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
    ("Borders and corners", "Corner rounding, from rounded-sm to rounded-xl. Plain rounded is the same as rounded-md. Page content in this theme is square by default.",
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
    "list--tick": "Known bug: icons stack on multi-item lists. Use Font Awesome icons per item instead.",
    "list--cross": "Known bug: icons stack on multi-item lists. Use Font Awesome icons per item instead.",
    "action-link": "Legacy. Kept so older resources keep working; use link-action in new content.",
    "c10": "Legacy System 2 column width.", "c20": "Legacy System 2 column width.",
    "c30": "Legacy System 2 column width.", "c40": "Legacy System 2 column width.",
    "c60": "Legacy System 2 column width.", "c70": "Legacy System 2 column width.",
    "c80": "Legacy System 2 column width.",
    "topMargin": "Legacy System 2 spacing.", "w3": "Legacy System 2 width.",
    "org": "Legacy System 2 organisation block.",
    "screenshots": "Older alias of image-screenshots.",
    "button--small": "Older alias of button-sm.",
    "button--outline": "Older outline button, kept so older content keeps working. The nearest current button is button-secondary-outline.",
}

# Classes that belong to the page frame or the editor, not to content an author writes.
FRAME_PREFIXES = (
    "navbar", "nav-", "jumbotron", "bs-docs", "activePage", "backBtn", "footer", "feedback",
    "backToTop", "logo", "titles", "pageTitle", "pageSubTitle", "sectionTitle", "contentTitle",
    "x_", "xerte", "editorStyle", "language-toggle", "project-info",
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




def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def class_names(css):
    """Every class name a stylesheet mentions."""
    return set(CLASS.findall(strip_comments(css)))


def theme_classes():
    """Classes the theme adds beyond Bootstrap, the player's custom.css and Font Awesome."""
    own = class_names(CSS.read_text(encoding="utf-8"))
    for name in BASE_CSS:
        path = player_path(name)
        if path.exists():
            own -= class_names(path.read_text(encoding="utf-8"))
    return own


def author_facing_classes():
    """Theme classes a content author may use: not legacy, not the page frame."""
    return {c for c in theme_classes() if c not in LEGACY and not c.startswith(FRAME_PREFIXES)}


def stack_classes():
    """Every class defined by the stylesheets the author guide loads: the player's and the theme's."""
    found = class_names(CSS.read_text(encoding="utf-8"))
    for name in PLAYER_CSS + IMPORTED_CSS:
        found |= class_names(player_path(name).read_text(encoding="utf-8"))
    return found


def utility_groups(utils):
    """The utility tables: (heading, guidance, [(class, value), ...]) per family, legacy left out."""
    groups = []
    for heading, guidance, pattern in FAMILIES:
        rows = sorted((c, v) for c, v in utils.items() if re.match(pattern, c) and c not in LEGACY)
        if rows:
            groups.append((heading, guidance, rows))
    return groups
