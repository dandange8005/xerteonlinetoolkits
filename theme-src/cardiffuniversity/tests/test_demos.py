"""What the hand-written demo pages must contain. The browser checks are in check_demos.py."""
import re
import unittest

import support
import theme_css
from html_tree import parse

DEMOS = support.THEME / "demos"
PAGES = sorted(DEMOS.glob("*.html"))
FONT_AWESOME = "fontawesome-6.6.0/css/all.min.css"


def classes_in(text):
    """Every class named in a class attribute, in live markup and in the escaped samples beside it."""
    for match in re.finditer(r'class="([^"]+)"', text):
        yield from match.group(1).split()


class DemoPagesTest(unittest.TestCase):
    def test_there_are_demo_pages(self):
        self.assertGreaterEqual(len(PAGES), 10)

    def test_no_demo_uses_a_legacy_class(self):
        # Authors copy what the demos show, so a legacy class here is teaching it.
        found = {}
        for page in PAGES:
            used = {c for c in classes_in(page.read_text(encoding="utf-8")) if c in theme_css.LEGACY}
            if used:
                found[page.name] = sorted(used)
        self.assertEqual(found, {})

    def test_pages_that_use_font_awesome_or_callouts_load_the_font(self):
        # A callout's icon is a Font Awesome character. Without the stylesheet it is an empty square.
        missing = []
        for page in PAGES:
            text = page.read_text(encoding="utf-8")
            uses = any(c.startswith("fa-") or c.startswith("cu-callout") for c in classes_in(text))
            if uses and FONT_AWESOME not in text:
                missing.append(page.name)
        self.assertEqual(missing, [])

    def test_the_homepage_callouts_sit_in_one_responsive_row(self):
        # The theme's flex utilities: a wrapping flex row whose items have a flex-basis class.
        page = parse((DEMOS / "index.html").read_text(encoding="utf-8"))
        callouts = page.find_all(cls="cu-callout")
        self.assertEqual(len(callouts), 3)
        row = callouts[0].parent
        self.assertTrue({"flex", "flex-wrap"} <= row.classes, row.classes)
        for callout in callouts:
            self.assertIs(callout.parent, row)
            self.assertIn("flex-300", callout.classes)

    def test_the_demos_bootstrap_script_is_bootstrap(self):
        # It was once a saved error message ("Couldn't find the requested release version"), so tabs,
        # collapse, alerts and the scroll highlight never worked on the demo pages.
        script = (DEMOS / "assets" / "bootstrap" / "bootstrap.min.js").read_text(encoding="utf-8")
        self.assertGreater(len(script), 20000)
        for plugin in ("affix", "scrollspy", "collapse", "tab", "alert", "carousel"):
            self.assertIn(plugin, script)

    def test_pages_with_a_section_menu_pin_it(self):
        # The player pins the menu with Bootstrap's affix plugin. Demo pages need their own script for it.
        script = DEMOS / "assets" / "demo-sidebar.js"
        self.assertTrue(script.exists())
        unpinned = [p.name for p in PAGES
                    if "bs-docs-sidenav" in p.read_text(encoding="utf-8")
                    and "assets/demo-sidebar.js" not in p.read_text(encoding="utf-8")]
        self.assertEqual(unpinned, [])


if __name__ == "__main__":
    unittest.main()
