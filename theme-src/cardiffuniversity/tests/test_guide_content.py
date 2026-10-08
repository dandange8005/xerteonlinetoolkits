import contextlib
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import support
import theme_css
from html_tree import parse

build_guide = support.load_tool("build-guide")


class GuideContentTest(unittest.TestCase):
    def test_real_guide_passes_its_checks(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = build_guide.build(check_only=True)
        printed = out.getvalue()
        self.assertEqual(code, 0, printed)
        self.assertNotIn("ERROR", printed)
        self.assertIn("WARNING [check 2]", printed)  # coverage warns until phase 3

    def test_check_2_counts_only_what_records_must_still_cover(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            build_guide.build(check_only=True)
        match = re.search(r"(\d+) author-facing classes are not covered yet", out.getvalue())
        self.assertIsNotNone(match, out.getvalue())
        # 355 author-facing classes, 259 shown in the utility tables, so at most 96 are left for records.
        self.assertLessEqual(int(match.group(1)), 96)

    def test_built_reference_pages_list_every_token(self):
        tokens = json.loads((support.THEME / "tokens" / "tokens.json").read_text(encoding="utf-8"))
        expected = {name for group, members in tokens.items() if not group.startswith("$")
                    for name in members if not name.startswith("$")}
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "site"
            with contextlib.redirect_stdout(io.StringIO()) as printed:
                code = build_guide.build(out=out)
            self.assertEqual(code, 0, printed.getvalue())
            shown = set()
            for name in ("colours", "tokens"):
                tree = parse((out / "reference" / f"{name}.html").read_text(encoding="utf-8"))
                shown |= {c.text()[2:] for c in tree.find_all("code") if c.text().startswith("--cu-")}
            utilities = parse((out / "reference" / "utilities.html").read_text(encoding="utf-8"))
        self.assertEqual(shown, expected)
        self.assertIn("mt-4", {c.text()[1:] for c in utilities.find_all("code")})

    def test_build_runs_from_the_repo_root(self):
        result = subprocess.run([sys.executable, str(support.TOOLS / "build-guide.py"), "--check"],
                                cwd=support.REPO, capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Guide checks passed", result.stdout)


class BuiltComponentPagesTest(unittest.TestCase):
    """Builds the real guide once and reads the component pages back."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "site"
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            code = build_guide.build(out=cls.out)
        assert code == 0, printed.getvalue()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def page(self, name):
        return parse((self.out / "components" / f"{name}.html").read_text(encoding="utf-8"))

    def shown(self, name):
        """Every class a component page names in a <code>.class</code> cell."""
        return {c.text()[1:] for c in self.page(name).find_all("code") if c.text().startswith(".")}

    def test_button_page_documents_every_button_class(self):
        expected = {c for c in theme_css.author_facing_classes() if c.startswith("button")}
        self.assertLessEqual({"button", "button-primary", "button-sm", "button-lg"}, expected)  # not an empty set
        self.assertEqual(expected - self.shown("button"), set())
        self.assertIn("btn-mini", self.shown("button"))

    def test_alert_page_documents_the_alert_classes(self):
        expected = {"alert", "alert-success", "alert-info", "alert-warning", "alert-danger",
                    "alert-error", "alert-block", "close"}
        self.assertEqual(expected - self.shown("alert"), set())

    def test_alerts_and_callouts_link_to_each_other(self):
        def related(name):
            return [a.text() for a in self.page(name).find(cls="g-related").find_all("a")]
        self.assertIn("Callouts", related("alert"))
        self.assertIn("Alerts", related("callout"))

    def section_text(self, name, heading):
        for section in self.page(name).find_all(cls="g-section"):
            if section.find_all("h2") and section.find("h2").text() == heading:
                return section.text()
        raise AssertionError(f"no section headed {heading!r} on {name}")

    def variant_meta(self, name, label):
        for variant in self.page(name).find_all(cls="g-variant"):
            if variant.find("h3").text() == label:
                return variant.find(cls="g-variant-meta").text()
        raise AssertionError(f"no variant labelled {label!r} on {name}")

    def test_button_examples_work_when_pasted_into_a_text_content_item(self):
        # A button element does nothing on its own there; a link with the button classes goes somewhere.
        buttons = [b for frame in self.page("button").find_all(cls="g-preview") for b in frame.find_all("button")]
        self.assertEqual(buttons, [])
        links = [a for frame in self.page("button").find_all(cls="g-preview") for a in frame.find_all("a")]
        self.assertGreaterEqual(len(links), 15)  # one example per variant; button--small is a legacy alias
        self.assertTrue(all(a.attrs.get("href", "").startswith("https://") for a in links))

    def test_button_page_qualifies_the_size_and_focus_claims(self):
        text = self.section_text("button", "Accessibility")
        self.assertIn("with the button class", text)  # the 48px and 44px claim is about .button only
        self.assertIn("btn-mini", text)
        self.assertIn("reverse", text)  # the ink focus outline cannot be seen on a dark background

    def test_small_buttons_say_their_text_is_14px(self):
        self.assertIn("14px", self.variant_meta("button", "Small"))

    def test_the_older_compact_button_is_listed_as_legacy_and_not_taught(self):
        # button--small sets the same text size and padding as button-sm, so it is an older alias.
        labels = [v.find("h3").text() for v in self.page("button").find_all(cls="g-variant")]
        self.assertNotIn("Compact (older)", labels)
        utilities = parse((self.out / "reference" / "utilities.html").read_text(encoding="utf-8"))
        legacy = [sec for sec in utilities.find_all(cls="g-section") if sec.find("h2").text() == "Legacy classes"][0]
        rows = {r.find_all("td")[0].text(): r.find_all("td")[1].text() for r in legacy.find("tbody").find_all("tr")}
        self.assertEqual(rows.get(".button--small"), "Older alias of button-sm.")

    def test_utility_page_shows_the_rounded_sizes(self):
        utilities = parse((self.out / "reference" / "utilities.html").read_text(encoding="utf-8"))
        section = [s for s in utilities.find_all(cls="g-section") if s.find("h2").text() == "Borders and corners"][0]
        rows = {r.find_all("td")[0].text(): r.find_all("td")[1].text() for r in section.find("tbody").find_all("tr")}
        steps = (".rounded-sm", ".rounded", ".rounded-md", ".rounded-lg", ".rounded-xl")
        self.assertEqual({k: rows.get(k) for k in steps},
                         {".rounded-sm": "border-radius: 2px", ".rounded": "border-radius: 3px",
                          ".rounded-md": "border-radius: 3px", ".rounded-lg": "border-radius: 9px",
                          ".rounded-xl": "border-radius: 12px"})
        self.assertIn("same as rounded-md", section.text())

    def test_the_older_outline_button_is_listed_as_legacy_and_not_taught(self):
        # button--outline has a 2px border, a shadow and a dark hover fill, so it is not an exact alias:
        # the legacy entry names the nearest current button instead.
        self.assertNotIn("button--outline", self.shown("button"))
        utilities = parse((self.out / "reference" / "utilities.html").read_text(encoding="utf-8"))
        legacy = [sec for sec in utilities.find_all(cls="g-section") if sec.find("h2").text() == "Legacy classes"][0]
        rows = {r.find_all("td")[0].text(): r.find_all("td")[1].text() for r in legacy.find("tbody").find_all("tr")}
        self.assertEqual(rows.get(".button--outline"),
                         "Older outline button, kept so older content keeps working. "
                         "The nearest current button is button-secondary-outline.")

    def test_button_page_describes_btn_mini_accurately(self):
        parts = self.section_text("button", "Parts")
        self.assertIn("player", parts)  # the player creates the back-to-top button

    def test_every_alert_example_has_a_bold_status_word(self):
        alerts = [a for frame in self.page("alert").find_all(cls="g-preview") for a in frame.find_all(cls="alert")]
        self.assertEqual(len(alerts), 6)
        for alert in alerts:
            self.assertTrue(alert.find_all("strong"), alert.text())

    def test_alert_page_says_where_the_glyph_sits_in_a_block_alert(self):
        self.assertIn("own line", self.section_text("alert", "How to use it"))

    def test_components_index_lists_the_buttons(self):
        index = parse((self.out / "components" / "index.html").read_text(encoding="utf-8"))
        hrefs = [a.attrs["href"] for card in index.find_all(cls="g-card") for a in card.find_all("a")]
        self.assertIn("button.html", hrefs)


if __name__ == "__main__":
    unittest.main()
