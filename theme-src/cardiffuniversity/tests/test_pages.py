import datetime
import tempfile
import unittest
from pathlib import Path

import support
import guide_fixture as fx
from guidelib import pages, records, reference
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


REF = reference.Reference(
    palette=(
        reference.Group("primary", "Primary colours", "Red, white and black.", (
            reference.Token("cu-white", "#FFFFFF", "#FFFFFF", None, ""),
            reference.Token("cu-black", "#000000", "#000000", None, ""),
            reference.Token("cu-grey-aa", "#767676", "#767676", None, ""),
            reference.Token("cu-grey-low", "#777777", "#777777", None, ""))),
        reference.Group("roles", "Colour roles", "Named by job.", (
            reference.Token("cu-bg", "{cu-white}", "#FFFFFF", "cu-white", "page background"),))),
    tokens=(reference.Group("space", "Spacing", "A 4px base.", (
        reference.Token("cu-space-1", "4px", "4px", None, ""),
        reference.Token("cu-logo-width", "clamp(60px,17vw,80px)", "clamp(60px,17vw,80px)", None, "logo minimums"))),
        reference.Group("font-sizes", "Font sizes", "Sizes by role.", (
            reference.Token("cu-text-body", "18px", "18px", None, ""),))),
    utilities=(("Spacing", "Margin and padding.", (("mt-4", "margin-top: 16px"),)),
               ("Text size", "Sizes.", (("text-lg", "font-size: 20px"),))),
    legacy=(("c10", "Legacy System 2 column width."),),
    white="#FFFFFF", ink="#121212")
REFERENCE_PAGES = ["reference/colours.html", "reference/index.html", "reference/tokens.html", "reference/utilities.html"]


class ReferencePagesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        guide = fx.write_guide(cls.tmp.name, SITE=fx.SITE_WITH_REFERENCE)
        cls.out = Path(cls.tmp.name) / "site"
        cls.written = pages.write_site(cls.out, records.load_site(guide / "site.toml"),
                                       records.load_content(guide / "content"),
                                       support.GUIDE / "templates" / "base.html", ref=REF)

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

    def rows(self, relative, heading):
        return self.section(self.page(relative), heading).find("tbody").find_all("tr")

    def test_reference_pages_are_written(self):
        self.assertEqual([w for w in self.written if w.startswith("reference/")], REFERENCE_PAGES)

    def test_colour_contrast_cells(self):
        by_token = {row.find("code").text(): row for row in self.rows("reference/colours.html", "Primary colours")}
        cells = {name: [td.text() for td in row.find_all("td")] for name, row in by_token.items()}
        self.assertEqual(cells["--cu-black"][3], "21.0:1 passes AA")
        self.assertEqual(cells["--cu-grey-aa"][3], "4.5:1 passes AA")
        self.assertEqual(cells["--cu-grey-low"][3], "4.4:1 fails AA")
        self.assertEqual(cells["--cu-white"][4], "18.7:1 passes AA")

    def test_colour_swatch_shows_the_colour(self):
        row = self.rows("reference/colours.html", "Primary colours")[2]
        self.assertEqual(row.find(cls="g-swatch").attrs["style"], "background:#767676")
        self.assertEqual(row.find(cls="g-swatch").attrs["aria-hidden"], "true")

    def test_alias_and_note_are_shown(self):
        row = self.rows("reference/colours.html", "Colour roles")[0]
        self.assertEqual([c.text() for c in row.find_all(cls="g-token-note")], ["page background", "same as --cu-white"])
        self.assertEqual(row.find_all("td")[2].find("code").text(), "#FFFFFF")

    def test_colours_page_explains_the_ratios(self):
        text = self.page("reference/colours.html").find(cls="g-main").text()
        self.assertIn("WCAG AA needs 4.5:1 for body text", text)
        self.assertIn("the same whichever", text)

    def test_tokens_page_rows(self):
        rows = self.rows("reference/tokens.html", "Spacing")
        self.assertEqual([[td.text() for td in row.find_all("td")] for row in rows],
                         [["--cu-space-1", "4px", ""],
                          ["--cu-logo-width", "clamp(60px,17vw,80px)", "logo minimums"]])

    def test_tokens_page_shows_a_notes_column_only_when_a_group_has_notes(self):
        page = self.page("reference/tokens.html")
        self.assertEqual([th.text() for th in self.section(page, "Spacing").find_all("th")], ["Token", "Value", "Notes"])
        self.assertEqual([th.text() for th in self.section(page, "Font sizes").find_all("th")], ["Token", "Value"])

    def test_utilities_page_has_a_table_per_family_and_the_legacy_classes(self):
        page = self.page("reference/utilities.html")
        self.assertEqual([[td.text() for td in row.find_all("td")]
                          for row in self.rows("reference/utilities.html", "Spacing")], [[".mt-4", "margin-top: 16px"]])
        self.assertIn("Do not use them in new content", self.section(page, "Legacy classes").text())
        self.assertEqual([[td.text() for td in row.find_all("td")]
                          for row in self.rows("reference/utilities.html", "Legacy classes")],
                         [[".c10", "Legacy System 2 column width."]])

    def test_on_this_page_lists_the_groups_and_they_exist(self):
        for relative, expected in (("reference/colours.html", ["primary", "roles"]),
                                   ("reference/tokens.html", ["space", "font-sizes"]),
                                   ("reference/utilities.html", ["spacing", "text-size", "legacy-classes"])):
            page = self.page(relative)
            ids = {e.attrs["id"] for e in page.iter() if "id" in e.attrs}
            targets = [a.attrs["href"][1:] for a in page.find(cls="g-toc").find_all("a")]
            self.assertEqual(targets, expected, relative)
            self.assertLessEqual(set(targets), ids)

    def test_wide_tables_scroll_inside_their_own_region(self):
        for relative in ("reference/colours.html", "reference/tokens.html", "reference/utilities.html"):
            wraps = self.page(relative).find_all(cls="g-table-scroll")
            self.assertTrue(wraps, relative)
            for wrap in wraps:
                self.assertEqual(wrap.attrs.get("tabindex"), "0")
                self.assertEqual(wrap.attrs.get("role"), "region")
                self.assertTrue(wrap.attrs.get("aria-label"))
                self.assertEqual(len(wrap.find_all("table")), 1)

    def test_reference_menu_marks_the_current_page(self):
        side = self.page("reference/colours.html").find(cls="g-side")
        self.assertEqual([a.text() for a in side.find_all("a")], ["Overview", "Colours", "Type, space and shape", "Utility classes"])
        self.assertEqual(side.find("a", aria_current="page").text(), "Colours")
        self.assertEqual(self.page("reference/index.html").find(cls="g-side").find("a", aria_current="page").text(), "Overview")

    def test_top_menu_marks_reference(self):
        menu = self.page("reference/utilities.html").find(cls="g-top")
        self.assertEqual(menu.find("a", aria_current="page").text(), "Reference")
        self.assertEqual(menu.find("a", aria_current="page").attrs["href"], "../reference/index.html")

    def test_overview_links_to_every_reference_page(self):
        cards = self.page("reference/index.html").find_all(cls="g-card")
        self.assertEqual([c.find("a").attrs["href"] for c in cards], ["colours.html", "tokens.html", "utilities.html"])

    def test_every_reference_page_has_one_main_and_one_h1(self):
        for relative in REFERENCE_PAGES:
            page = self.page(relative)
            self.assertEqual(len(page.find_all(id="main")), 1, relative)
            self.assertEqual(len(page.find_all("h1")), 1, relative)

    def test_reference_links_resolve(self):
        for relative in REFERENCE_PAGES:
            for element in self.page(relative).iter():
                target = element.attrs.get("href") or ""
                if element.tag != "a" or not target or target.startswith(("#", "http:", "https:", "mailto:")):
                    continue
                path = (self.out / relative).parent / target.split("#")[0]
                self.assertTrue(path.resolve().is_file(), f"{relative} links to missing {target}")


class UnknownSinceTest(unittest.TestCase):
    def test_evidence_leaves_out_since_when_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            guide = fx.write_guide(tmp, CALLOUT=fx.CALLOUT.replace('since = "v1.4"\n', ""))
            out = Path(tmp) / "site"
            pages.write_site(out, records.load_site(guide / "site.toml"), records.load_content(guide / "content"),
                             support.GUIDE / "templates" / "base.html")
            page = parse((out / "components" / "callout.html").read_text(encoding="utf-8"))
        labels = [dt.text() for dt in page.find(cls="g-evidence").find_all("dt")]
        self.assertEqual(labels, ["Status", "Xerte editor", "Main class"])


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
