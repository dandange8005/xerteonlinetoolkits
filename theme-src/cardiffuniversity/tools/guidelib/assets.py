"""What each guide page loads, and copying it into the built site.

Pages link the player's stylesheets in the player's order, then the theme (the player appends it
last), then the guide's own stylesheet, which styles only the guide navigation. Paths under
vendor/player/ mirror the player's common/ folder, so the stylesheets' relative url()s still work.
"""
import shutil

import theme_css

FONTAWESOME = "fontawesome-6.6.0"
PLAYER_JS = ("js/jquery-1.9.1.min.js", "js/bootstrap.js")
# Files the player's stylesheets reach through @import or url(), and Font Awesome's licence.
REFERENCED = ("css/editorstyles.css", "img/glyphicons-halflings.png", "img/glyphicons-halflings-white.png",
              f"{FONTAWESOME}/LICENSE.txt")

STYLESHEETS = (tuple(f"vendor/player/{name}" for name in theme_css.PLAYER_CSS)
               + ("vendor/theme/cardiffuniversity.css", "assets/guide.css"))
SCRIPTS = tuple(f"vendor/player/{name}" for name in PLAYER_JS) + ("assets/guide.js",)


def copy_assets(out, guide_assets):
    """Copy the player's files, the theme and the guide's own assets into the built site."""
    player = out / "vendor" / "player"
    for name in theme_css.PLAYER_CSS + PLAYER_JS + REFERENCED:
        _copy(theme_css.PLAYER / name, player / name)
    shutil.copytree(theme_css.PLAYER / FONTAWESOME / "webfonts", player / FONTAWESOME / "webfonts", dirs_exist_ok=True)
    _copy(theme_css.CSS, out / "vendor" / "theme" / "cardiffuniversity.css")
    shutil.copytree(guide_assets, out / "assets", dirs_exist_ok=True)


def _copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
