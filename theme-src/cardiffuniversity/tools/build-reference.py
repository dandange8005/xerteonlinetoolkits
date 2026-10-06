#!/usr/bin/env python3
"""Generate the guide's utility reference from the compiled theme, and report what is undocumented.

The guide is for content authors, so the reference must describe classes that really exist.
Hand-written tables drift: the demos documented .w-md-50 and .image-full long after they were
gone. This reads cardiffuniversity.css instead and writes the tables into the guide between
markers, then checks every class the theme defines is either documented or deliberately not.

Usage (from the theme folder):
    python3 tools/build-reference.py            write the tables into the guide
    python3 tools/build-reference.py --check    report only; exit 1 if the guide is out of date
    python3 tools/build-reference.py --coverage list theme classes no guide page mentions

Standard library only. Shared parsing lives in tools/theme_css.py.
"""
import html
import re
import sys

from theme_css import FRAME_PREFIXES, LEGACY, THEME, theme_classes, utilities, utility_groups

GUIDE = THEME / "demos" / "code-utilities.html"
DEMOS = THEME / "demos"

START = "<!-- @generated: utility reference (tools/build-reference.py) -->"
END = "<!-- @end generated -->"


def render_tables(utils):
    used, blocks = set(), []
    for heading, guidance, rows in utility_groups(utils):
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
                <p class="demo-block__description">These classes remain for older resources; known limitations and replacements are listed below. Do not use them in new content.</p>
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
