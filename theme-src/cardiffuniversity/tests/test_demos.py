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

    def test_every_table_scroll_wrapper_is_reachable_and_named(self):
        # The Tables page teaches tabindex, role and aria-label on the wrapper. Nothing else checks them.
        bad = []
        for page in PAGES:
            for wrapper in parse(page.read_text(encoding="utf-8")).find_all(cls="cu-table-scroll"):
                if (wrapper.attrs.get("tabindex") != "0" or wrapper.attrs.get("role") != "region"
                        or not (wrapper.attrs.get("aria-label") or "").strip()):
                    bad.append(page.name)
        self.assertEqual(bad, [])

    def test_every_page_loads_the_snippet_script_and_styles(self):
        # demo-code.js adds the Show HTML snippets; the browser checks only see pages that load it.
        missing = []
        for page in PAGES:
            tree = parse(page.read_text(encoding="utf-8"))
            has_script = [s for s in tree.find_all("script") if s.attrs.get("src") == "assets/demo-code.js"]
            has_styles = [s for s in tree.find_all("link") if s.attrs.get("href") == "assets/demo-code.css"]
            if not (has_script and has_styles):
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

    def test_utility_combinations_use_only_real_author_classes(self):
        # The section shows what authors can build by combining utilities, so every class in it must be one
        # they can use: defined by the player's stylesheets or the theme, and not legacy. The demo's own chrome
        # classes do not count. (text-center, for one, comes from Bootstrap but is in the utility reference.)
        page = parse((DEMOS / "code-utilities.html").read_text(encoding="utf-8"))
        section = page.find(id="combining-utilities")
        self.assertIsNotNone(section)
        self.assertNotIn("data-code", section.attrs)  # unlike the reference above it, these have Show HTML
        blocks = section.find_all(cls="demo-block")
        self.assertGreaterEqual(len(blocks), 5)
        used = {c for el in section.iter() for c in el.classes
                if not c.startswith(("demo-", "code-label"))}
        self.assertEqual(sorted(used - theme_css.stack_classes()), [])
        self.assertEqual(sorted(used & set(theme_css.LEGACY)), [])
        self.assertIn("#combining-utilities", [a.attrs.get("href") for a in page.find_all("a")])

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
