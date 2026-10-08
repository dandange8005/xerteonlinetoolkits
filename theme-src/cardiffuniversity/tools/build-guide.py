#!/usr/bin/env python3
"""Build the author guide into site/, after running its five checks.

Usage (from anywhere):
    python3 tools/build-guide.py            check, then build into site/
    python3 tools/build-guide.py --check    check only; exit 1 on any error
    python3 tools/build-guide.py --out DIR  build somewhere else

Errors stop the build and nothing is written. Warnings are printed and the build continues.
Standard library only; needs Python 3.11 or later for tomllib.
"""
import sys

if sys.version_info < (3, 11):
    sys.exit("build-guide.py needs Python 3.11 or later (for tomllib).")

import argparse  # noqa: E402
import shutil  # noqa: E402
from pathlib import Path  # noqa: E402

import theme_css  # noqa: E402
from guidelib import assets, checks, pages, records, reference  # noqa: E402
from guidelib.mdsubset import MarkdownError  # noqa: E402

GUIDE = theme_css.THEME / "guide"
SITE = theme_css.THEME / "site"
MARKER = ".guide-build"


def build(guide_dir=GUIDE, out=SITE, check_only=False, last_changed=None):
    guide_dir, out = Path(guide_dir), Path(out)
    try:
        site = records.load_site(guide_dir / "site.toml")
        content = records.load_content(guide_dir / "content")
    except (records.RecordError, MarkdownError, OSError) as error:
        print(f"ERROR {error}")
        return 1
    try:
        ref = reference.load_reference(
            theme_css.THEME / "tokens" / "tokens.json", guide_dir / "reference.toml",
            theme_css.utility_groups(theme_css.utilities()), tuple(sorted(theme_css.LEGACY.items())))
    except reference.ReferenceDataError as error:
        print(f"ERROR {error}")
        return 1
    # The utility tables on the reference pages cover these classes, so check 2 need not ask for records.
    tables = {cls for _, _, rows in ref.utilities for cls, _ in rows}
    last_changed = last_changed or checks.git_last_changed(theme_css.THEME)
    findings = checks.run_all(
        content, site, theme_dir=theme_css.THEME, known=theme_css.stack_classes(),
        author_facing=theme_css.author_facing_classes(), tables=tables, last_changed=last_changed)
    for finding in findings:
        print(finding)
    errors = sum(f.level == "error" for f in findings)
    warnings = len(findings) - errors
    if errors:
        print(f"Guide not built: {errors} error(s).")
        return 1
    if check_only:
        print(f"Guide checks passed ({warnings} warning(s)).")
        return 0
    if out.exists():
        if any(out.iterdir()) and not (out / MARKER).exists():
            print(f"ERROR {out} is not empty and was not made by this tool; refusing to delete it.")
            return 1
        shutil.rmtree(out)
    # The marker goes first, so a build that fails partway still leaves a folder the next build may replace.
    out.mkdir(parents=True)
    (out / MARKER).write_text("Built by tools/build-guide.py. This folder is replaced on every build.\n",
                              encoding="utf-8")
    try:
        written = pages.write_site(out, site, content, guide_dir / "templates" / "base.html",
                                   updated=lambda path: last_changed(str(path)), ref=ref)
        assets.copy_assets(out, guide_dir / "assets")
    except OSError as error:
        print(f"ERROR the build stopped partway: {error}")
        return 1
    print(f"Built {out} ({len(written)} pages, {warnings} warning(s)).")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build the Cardiff University Theme's author guide.")
    parser.add_argument("--check", action="store_true", help="run the checks without writing the site")
    parser.add_argument("--out", type=Path, default=SITE, help="output folder (default: site/)")
    args = parser.parse_args(argv)
    return build(out=args.out.resolve(), check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
