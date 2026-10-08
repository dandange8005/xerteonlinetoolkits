import datetime
import tempfile
import unittest
from pathlib import Path

import support
import guide_fixture as fx
from guidelib import pages, records
from html_tree import parse

PLAYER_ORDER = ["vendor/player/css/bootstrap.css", "vendor/player/css/bootstrap-responsive.css",
                "vendor/player/css/custom.css", "vendor/player/fontawesome-6.6.0/css/all.min.css",
                "vendor/player/fontawesome-6.6.0/css/v4-shims.min.css",
                "vendor/player/fontawesome-6.6.0/css/v5-font-face.min.css",
                "vendor/theme/cardiffuniversity.css", "assets/guide.css"]


class WrittenSiteTest(unittest.TestCase):
    """Writes the fixture guide with pages.write_site() and reads the pages back."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        guide = fx.write_guide(cls.tmp.name)
        cls.content = records.load_content(guide / "content")
        cls.out = Path(cls.tmp.name) / "site"
        # Only the callout record has a known last change, so other pages show no date.
        cls.written = pages.write_site(cls.out, records.load_site(guide / "site.toml"), cls.content,
                                       support.GUIDE / "templates" / "base.html",
                                       updated=lambda path: datetime.date(2026, 10, 6) if path.name == "callout.md" else None)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def page(self, relative):
        return parse((self.out / relative).read_text(encoding="utf-8"))

    def section(self, page, heading):
        for section in page.find_all(cls="g-section"):
            if section.find_all("h2") and section.find("h2").text() == heading:
                return section
        raise AssertionError(f"no section headed {heading!r}")

    def test_writes_every_page(self):
        self.assertEqual(self.written, ["components/callout.html", "components/index.html", "getting-started.html",
                                        "index.html", "tasks/draw-attention.html", "tasks/index.html"])

    def test_example_renders_the_first_example(self):
        example = self.page("components/callout.html").find(cls="g-top-example")
        self.assertEqual(example.find(cls="g-preview").find(cls="cu-callout-title").text(), "Tip")
        self.assertIn(".cu-callout-tip", example.find(cls="g-variant-meta").text())

    def test_code_starts_behind_a_closed_html_toggle(self):
        toggle = self.page("components/callout.html").find(cls="g-top-example").find("details", cls="g-code-toggle")
        self.assertNotIn("open", toggle.attrs)
        self.assertEqual(toggle.find("summary").text().strip(), "HTML")
        self.assertIn("add a Text content item, open its Source view", toggle.text())

    def test_code_view_shows_source_literally(self):
        section = self.page("components/callout.html").find(cls="g-top-example")
        code = section.find(cls="g-code-toggle").find("code")
        self.assertEqual(code.text(), self.content.components["callout"].examples[0].html)
        self.assertIn("Fish &amp; chips.", code.text())
        self.assertIn("Fish & chips.", section.find(cls="g-preview").text())

    def test_each_other_variant_has_its_own_example_and_code(self):
        section = self.section(self.page("components/callout.html"), "Variants")
        self.assertIn("Tip is shown at the top of the page.", section.text())
        [warning] = section.find_all(cls="g-variant")
        self.assertEqual(warning.find("h3").text(), "Warning")
        self.assertIn(".cu-callout-warning", warning.find(cls="g-variant-meta").text())
        self.assertIn("A risk the reader must avoid", warning.find(cls="g-variant-meta").text())
        self.assertEqual(warning.find(cls="g-preview").find(cls="cu-callout-title").text(), "Warning")
        self.assertEqual(warning.find(cls="g-code-toggle").find("code").text(),
                         self.content.components["callout"].examples[1].html)

    def test_parts_table(self):
        rows = self.section(self.page("components/callout.html"), "Parts").find("tbody").find_all("tr")
        self.assertEqual([row.find("td").text() for row in rows], [".cu-callout", ".cu-callout-title", ".cu-callout-icon"])

    def test_guidance_sections_come_from_the_record(self):
        page = self.page("components/callout.html")
        self.assertIn("Use a callout for one idea.", self.section(page, "When to use it").text())
        self.assertIn("text every reader must read anyway", self.section(page, "When not to use it").text())
        how = self.section(page, "How to use it")
        self.assertIn("Keep it short.", how.text())
        self.assertEqual([li.text() for li in how.find(cls="g-do").find_all("li")], ["Name the variant in the title."])
        self.assertEqual([li.text() for li in how.find(cls="g-dont").find_all("li")], ["Stack more than two."])

    def test_evidence(self):
        evidence = self.section(self.page("components/callout.html"), "Evidence").find("dl")
        rows = dict(zip([dt.text() for dt in evidence.find_all("dt")], [dd.text() for dd in evidence.find_all("dd")]))
        self.assertEqual(rows["Status"], "Current")
        self.assertEqual(rows["Since"], "Design system v1.4")
        self.assertEqual(rows["Xerte editor"], "Survives the editor (checked 20 September 2026, Xerte 3.14)")
        self.assertEqual(rows["Main class"], ".cu-callout")

    def test_no_status_chips_above_the_content(self):
        self.assertEqual(self.page("components/callout.html").find_all(cls="g-chip"), [])

    def test_page_updated_date(self):
        self.assertEqual(self.page("components/callout.html").find(cls="g-updated").text(), "Page updated: 6 October 2026")
        self.assertEqual(self.page("tasks/draw-attention.html").find_all(cls="g-updated"), [])

    def test_component_page_lists_the_tasks_that_use_it(self):
        related = self.section(self.page("components/callout.html"), "Related")
        link = related.find("a", href="../tasks/draw-attention.html")
        self.assertEqual(link.text(), "Task: Draw attention to something")

    def test_on_this_page_links_resolve(self):
        page = self.page("components/callout.html")
        ids = {e.attrs["id"] for e in page.iter() if "id" in e.attrs}
        targets = [a.attrs["href"][1:] for a in page.find(cls="g-toc").find_all("a")]
        self.assertEqual(targets, ["when-to-use-it", "when-not-to-use-it", "how-to-use-it", "variants",
                                   "parts", "accessibility", "evidence", "related"])
        self.assertLessEqual(set(targets), ids)

    def test_side_menu_marks_the_current_component(self):
        current = self.page("components/callout.html").find(cls="g-side").find("a", aria_current="page")
        self.assertEqual(current.text(), "Callouts")

    def test_top_menu(self):
        menu = self.page("components/callout.html").find(cls="g-top")
        self.assertEqual([a.text() for a in menu.find_all("a")], ["Home", "Getting started", "Tasks", "Components"])
        self.assertEqual(menu.find("a", aria_current="page").text(), "Components")

    def test_stylesheets_load_in_player_order_then_the_theme(self):
        for relative, prefix in (("index.html", ""), ("components/callout.html", "../")):
            hrefs = [link.attrs["href"] for link in self.page(relative).find_all("link", rel="stylesheet")]
            self.assertEqual(hrefs, [prefix + href for href in PLAYER_ORDER])

    def test_page_links_resolve(self):
        for relative in self.written:
            for element in self.page(relative).iter():
                target = element.attrs.get("href") or ""
                if element.tag != "a" or not target or target.startswith(("#", "http:", "https:", "mailto:")):
                    continue
                path = (self.out / relative).parent / target.split("#")[0]
                self.assertTrue(path.resolve().is_file(), f"{relative} links to missing {target}")

    def test_home_tiles_and_new_steps(self):
        home = self.page("index.html")
        tile = home.find(cls="g-task")
        self.assertEqual(tile.find("a").text(), "Draw attention to something")
        self.assertEqual(tile.find(cls="g-uses").text(), "Uses: callouts")
        self.assertEqual(home.find(cls="g-new").find("a").attrs["href"], "getting-started.html")
        self.assertEqual([li.find("strong").text() for li in home.find(cls="g-steps").find_all("li")], ["Choose", "Check"])

    def test_task_page(self):
        page = self.page("tasks/draw-attention.html")
        self.assertEqual(self.section(page, "Components to use").find("a").text(), "Callouts")
        example = self.section(page, "Worked example: An upload reminder")
        self.assertEqual(example.find(cls="g-preview").find(cls="cu-callout-title").text(), "Important")
        self.assertEqual([li.text() for li in self.section(page, "Checklist").find_all("li")], ["The title names the variant."])

    def test_getting_started(self):
        page = self.page("getting-started.html")
        links = page.find(cls="g-toc").find_all("a")
        self.assertEqual([a.text() for a in links], ["Choose the theme", "Brand colours"])
        headings = {h.attrs.get("id"): h.text() for h in page.find(cls="g-main").find_all("h2")}
        for a in links:
            self.assertEqual(headings.get(a.attrs["href"][1:]), a.text())
        self.assertIn(":root { --color-brand-primary: #00703C; }", page.find("code", cls="language-css").text())

    def test_header_shows_the_cardiff_logo(self):
        for relative, prefix in (("index.html", ""), ("components/callout.html", "../")):
            logo = self.page(relative).find("header").find("img")
            self.assertEqual(logo.attrs["src"], prefix + "vendor/theme/logo_left.svg")
            self.assertEqual(logo.attrs["alt"], "Cardiff University / Prifysgol Caerdydd")

    def test_home_header_holds_the_menu_and_other_pages_put_it_below(self):
        self.assertEqual(len(self.page("index.html").find("header").find_all(cls="g-top")), 1)
        callout = self.page("components/callout.html")
        self.assertEqual(callout.find("header").find_all(cls="g-top"), [])
        self.assertEqual(len(callout.find_all(cls="g-top")), 1)

    def test_each_variant_is_rendered_once(self):
        page = self.page("components/callout.html")
        for variant in ("cu-callout-tip", "cu-callout-warning"):
            self.assertEqual(len(page.find_all(cls=variant)), 1, variant)

    def test_every_page_has_one_main_and_one_h1(self):
        for relative in self.written:
            page = self.page(relative)
            self.assertEqual(len(page.find_all(id="main")), 1, relative)
            self.assertEqual(len(page.find_all("h1")), 1, relative)


class TaskLinksTest(unittest.TestCase):
    def test_a_new_task_appears_on_the_component_page_without_editing_the_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            guide = fx.write_guide(tmp, TASK_B=fx.TASK_B, SITE=fx.SITE_TWO)
            out = Path(tmp) / "site"
            pages.write_site(out, records.load_site(guide / "site.toml"), records.load_content(guide / "content"),
                             support.GUIDE / "templates" / "base.html")
            related = parse((out / "components" / "callout.html").read_text(encoding="utf-8")).find(cls="g-related")
        self.assertEqual([a.text() for a in related.find_all("a")],
                         ["Task: Draw attention to something", "Task: Add a tip to a page"])


class UntestedEvidenceTest(unittest.TestCase):
    def test_untested_component_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            untested = fx.CALLOUT.replace('[editor]\nsurvives = true\nchecked = 2026-09-20\nxerte = "3.14"\n\n', "")
            guide = fx.write_guide(tmp, CALLOUT=untested)
            out = Path(tmp) / "site"
            pages.write_site(out, records.load_site(guide / "site.toml"), records.load_content(guide / "content"),
                             support.GUIDE / "templates" / "base.html")
            page = parse((out / "components" / "callout.html").read_text(encoding="utf-8"))
        evidence = page.find(cls="g-evidence")
        rows = dict(zip([dt.text() for dt in evidence.find_all("dt")], [dd.text() for dd in evidence.find_all("dd")]))
        self.assertEqual(rows["Xerte editor"], "Not tested in the Xerte editor yet")
        self.assertEqual(rows["Status"], "Current")


if __name__ == "__main__":
    unittest.main()
