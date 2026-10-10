#!/usr/bin/env python3
"""Package the demo pages as a hidden Xerte theme that an admin can upload (standard library only).

The demos load the theme and Font Awesome from repo paths, so they only work from a checkout. Xerte's
theme upload unzips a zip into themes/site/<name>/ and serves the files as they are, so a theme folder
that holds the demos next to a copy of the compiled theme makes them browsable at
    <site>/themes/site/cardiffuniversity-demos/index.html

Run it with ./build.sh demos-package. Upload the zip on the Themes page (Site), then disable the theme
there so it does not appear in the theme picker. Every upload replaces the folder and enables it again.
"""
import argparse
import re
import sys
import zipfile
from pathlib import Path

import theme_css

HERE = Path(__file__).resolve().parent
THEME = HERE.parent
DEMOS = THEME / "demos"
NAME = "cardiffuniversity-demos"
INFO = f"""name: {NAME}
display name: Cardiff University Theme demos
description: Demo pages for the Cardiff University theme. Hidden helper theme, do not enable.
"""
# The three places the demo pages reach outside their own folder, and where the package keeps the same file.
REWRITES = (
    ("../../../themes/site/cardiffuniversity/cardiffuniversity.css", "cardiffuniversity.css"),
    ("../../../themes/site/cardiffuniversity/logo_left.svg", "logo_left.svg"),
    (f"../../../modules/common/{theme_css.FONTAWESOME}/", f"{theme_css.FONTAWESOME}/"),
)
# Font Awesome files the demo pages need: the stylesheet and the fonts it points at.
FONT_AWESOME_PARTS = ("css/all.min.css", "webfonts", "LICENSE.txt")


def package_files():
    """Yield (path inside the theme folder, bytes) for everything the package holds."""
    yield f"{NAME}.info", INFO.encode("utf-8")
    for page in sorted(DEMOS.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        for old, new in REWRITES:
            text = text.replace(old, new)
        outside = re.search(r'(?:href|src)="(\.\./[^"]*)"', text)
        if outside:
            raise SystemExit(f"{page.name} still reaches outside the package: {outside.group(1)}")
        yield page.name, text.encode("utf-8")
    for path in sorted((DEMOS / "assets").rglob("*")):
        if path.is_file() and not path.name.startswith("."):
            yield path.relative_to(DEMOS).as_posix(), path.read_bytes()
    yield "cardiffuniversity.css", theme_css.CSS.read_bytes()
    yield "logo_left.svg", (theme_css.CSS.parent / "logo_left.svg").read_bytes()
    font_awesome = theme_css.player_path(theme_css.FONTAWESOME)
    for part in FONT_AWESOME_PARTS:
        source = font_awesome / part
        for path in sorted(source.rglob("*")) if source.is_dir() else [source]:
            if path.is_file():
                yield f"{theme_css.FONTAWESOME}/{path.relative_to(font_awesome).as_posix()}", path.read_bytes()


def build(target):
    """Write the zip to target and return its path."""
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.unlink(missing_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in package_files():
            # A fixed timestamp keeps the zip identical from one build to the next.
            info = zipfile.ZipInfo(f"{NAME}/{name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=THEME / "dist" / f"{NAME}.zip")
    args = parser.parse_args()
    zip_path = build(args.out)
    with zipfile.ZipFile(zip_path) as archive:
        count = len(archive.namelist())
    print(f"Packaged {zip_path} ({count} files, {zip_path.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
