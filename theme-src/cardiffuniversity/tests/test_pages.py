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
        cls.written = pages.write_site(cls.out, records.load_site(guide / "site.toml"), cls.content,
                                       support.GUIDE / "templates" / "base.html")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def page(self, relative):
        return parse((self.out / relative).read_text(encoding="utf-8"))

    def section(self, page, heading):
        for section in page.find_all("section"):
            if section.find_all("h2") and section.find("h2").text() == heading:
                return section
        raise AssertionError(f"no section headed {heading!r}")

    def test_writes_every_page(self):
        self.assertEqual(self.written, ["components/callout.html", "components/index.html", "getting-started.html",
                                        "index.html", "tasks/draw-attention.html", "tasks/index.html"])

    def test_preview_renders_the_first_example(self):
        preview = self.section(self.page("components/callout.html"), "Preview and code").find(cls="g-preview")
        self.assertEqual(preview.find(cls="cu-callout-title").text(), "Tip")

    def test_code_view_shows_source_literally(self):
        section = self.section(self.page("components/callout.html"), "Preview and code")
        code = section.find(cls="g-code-wrap").find("code")
        self.assertEqual(code.text(), self.content.components["callout"].examples[0].html)
        self.assertIn("Fish &amp; chips.", code.text())
        self.assertIn("Fish & chips.", section.find(cls="g-preview").text())

    def test_paste_instruction_uses_the_glossary(self):
        self.assertIn("add a Text content item, open its Source view",
                      self.section(self.page("components/callout.html"), "Preview and code").text())

    def test_variants_table(self):
        rows = self.section(self.page("components/callout.html"), "Variants").find("tbody").find_all("tr")
        self.assertEqual([[td.text() for td in row.find_all("td")] for row in rows],
                         [[".cu-callout-tip", "Tip", "A shortcut or recommendation"],
                          [".cu-callout-warning", "Warning", "A risk the reader must avoid"]])

    def test_parts_table(self):
        rows = self.section(self.page("components/callout.html"), "Parts").find("tbody").find_all("tr")
        self.assertEqual([row.find("td").text() for row in rows], [".cu-callout", ".cu-callout-title", ".cu-callout-icon"])

    def test_editor_evidence(self):
        meta = self.page("components/callout.html").find(cls="g-meta").text()
        self.assertIn("Survives the Xerte editor", meta)
        self.assertIn("checked 20 September 2026", meta)
        self.assertIn("Xerte 3.14", meta)

    def test_do_and_dont(self):
        section = self.section(self.page("components/callout.html"), "When to use it")
        self.assertEqual([li.text() for li in section.find(cls="g-do").find_all("li")], ["Name the variant in the title."])
        self.assertEqual([li.text() for li in section.find(cls="g-dont").find_all("li")], ["Stack more than two."])

    def test_on_this_page_links_resolve(self):
        page = self.page("components/callout.html")
        ids = {e.attrs["id"] for e in page.iter() if "id" in e.attrs}
        targets = [a.attrs["href"][1:] for a in page.find(cls="g-toc").find_all("a")]
        self.assertEqual(targets, ["preview", "variants", "parts", "when-to-use-it", "accessibility", "related"])
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

    def test_every_page_has_one_main_and_one_h1(self):
        for relative in self.written:
            page = self.page(relative)
            self.assertEqual(len(page.find_all(id="main")), 1, relative)
            self.assertEqual(len(page.find_all("h1")), 1, relative)


if __name__ == "__main__":
    unittest.main()
