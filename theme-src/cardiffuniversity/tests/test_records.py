import datetime
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401
import guide_fixture as fx
from guidelib import records
from guidelib.mdsubset import MarkdownError


class RecordsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def guide(self, **overrides):
        return fx.write_guide(self.tmp.name, **overrides)

    def component(self, text):
        guide = self.guide(CALLOUT=text)
        return records.load_component(guide / "content" / "components" / "callout.md")

    def test_component_loads(self):
        c = self.component(fx.CALLOUT)
        self.assertEqual(c.name, "callout")
        self.assertEqual(c.editor, records.Editor(True, datetime.date(2026, 9, 20), "3.14"))
        self.assertEqual(list(c.parts), ["cu-callout", "cu-callout-title", "cu-callout-icon"])
        self.assertEqual([e.variant for e in c.examples], ["cu-callout-tip", "cu-callout-warning"])
        self.assertTrue(c.examples[0].html.startswith('<div class="cu-callout cu-callout-tip">'))
        self.assertEqual(c.when_intro, "<p>Use a callout for one idea.</p>")
        self.assertEqual(c.do_html, "<ul><li>Name the variant in the title.</li></ul>")
        self.assertEqual(c.dont_html, "<ul><li>Stack more than two.</li></ul>")
        self.assertEqual(c.accessibility_html, "<p>The title says the variant in words.</p>")

    def test_crlf_record_loads(self):
        c = self.component(fx.CALLOUT.replace("\n", "\r\n"))
        self.assertEqual(c.do_html, "<ul><li>Name the variant in the title.</li></ul>")
        self.assertEqual(c.examples[0].variant, "cu-callout-tip")

    def assertComponentError(self, text, pattern):
        with self.assertRaisesRegex(records.RecordError, pattern):
            self.component(text)

    def test_name_must_match_the_file(self):
        self.assertComponentError(fx.CALLOUT.replace('name = "callout"', 'name = "callouts"'), "must match the file name")

    def test_unknown_key(self):
        self.assertComponentError(fx.CALLOUT.replace('since = "v1.4"', 'since = "v1.4"\ncolour = "red"'), "unknown front-matter key.*colour")

    def test_must_start_with_front_matter(self):
        self.assertComponentError("name = 'x'\n", "must start with a \\+\\+\\+ line")

    def test_front_matter_must_close(self):
        self.assertComponentError("+++\nname = 'callout'\n", "not closed")

    def test_invalid_toml(self):
        self.assertComponentError(fx.CALLOUT.replace('since = "v1.4"', "since = v1.4"), "not valid TOML")

    def test_xerte_version_must_be_text(self):
        self.assertComponentError(fx.CALLOUT.replace('xerte = "3.14"', "xerte = 3.14"), "'xerte' must be text")

    def test_checked_must_be_a_date(self):
        self.assertComponentError(fx.CALLOUT.replace("checked = 2026-09-20", 'checked = "20 Sep"'), "'checked' must be a date")

    def test_status(self):
        self.assertComponentError(fx.CALLOUT.replace('status = "current"', 'status = "draft"'), "status must be one of")

    def test_variant_cannot_also_be_a_part(self):
        self.assertComponentError(fx.CALLOUT.replace('cu-callout-icon = "Only', 'cu-callout-tip = "Only'), "both a variant and a part")

    def test_variant_used_twice(self):
        self.assertComponentError(fx.CALLOUT.replace('class = "cu-callout-warning"', 'class = "cu-callout-tip"'), "used twice")

    def test_needs_examples(self):
        start = fx.CALLOUT.index("[[examples]]")
        end = fx.CALLOUT.index("+++", start)
        self.assertComponentError(fx.CALLOUT[:start] + fx.CALLOUT[end:], "missing 'examples'")

    def test_headings_must_be_in_order(self):
        self.assertComponentError(fx.CALLOUT.replace("### Do\n", "### Dos\n"), "body headings must be, in order")

    def test_no_text_before_the_first_heading(self):
        self.assertComponentError(fx.CALLOUT.replace("+++\n\n## When", "+++\nHello.\n\n## When"), "text before the first heading")

    def test_do_must_not_be_empty(self):
        self.assertComponentError(fx.CALLOUT.replace("- Name the variant in the title.\n", ""), "'### Do' is empty")

    def test_body_errors_report_the_file_line(self):
        text = fx.CALLOUT.replace("Use a callout for one idea.", "Use <b>this</b>.")
        line = text.splitlines().index("Use <b>this</b>.") + 1
        with self.assertRaisesRegex(MarkdownError, f"callout.md:{line}: raw HTML"):
            self.component(text)

    def test_task_loads(self):
        guide = self.guide()
        task = records.load_task(guide / "content" / "tasks" / "draw-attention.md")
        self.assertEqual(task.components, ("callout",))
        self.assertEqual(task.example.label, "An upload reminder")
        self.assertIsNone(task.example.variant)
        self.assertEqual(task.goal_html, "<p>Make one point stand out.</p>")

    def test_task_icon_must_be_font_awesome(self):
        guide = self.guide(TASK=fx.TASK.replace('icon = "fa-lightbulb"', 'icon = "lightbulb"'))
        with self.assertRaisesRegex(records.RecordError, "Font Awesome"):
            records.load_task(guide / "content" / "tasks" / "draw-attention.md")

    def test_page_loads(self):
        guide = self.guide()
        page = records.load_page(guide / "content" / "pages" / "index.md")
        self.assertEqual(page.new_steps, ("Choose the theme.", "Paste a callout."))
        self.assertEqual(page.how, (("Choose", "Pick a component."), ("Check", "Run the checklist.")))
        self.assertEqual(page.sections, ())
        started = records.load_page(guide / "content" / "pages" / "getting-started.md")
        self.assertEqual([s.title for s in started.sections], ["Choose the theme", "Brand colours"])

    def test_site_loads(self):
        site = records.load_site(self.guide() / "site.toml")
        self.assertEqual(site.coverage, "warn")
        self.assertEqual(site.groups, (("emphasis", "Emphasis"),))
        self.assertEqual(site.menu[0], ("home", "Home"))

    def test_site_rejects_unknown_menu_pages_and_modes(self):
        for old, new, pattern in (('page = "tasks"', 'page = "colours"', "menu page must be one of"),
                                  ('coverage = "warn"', 'coverage = "maybe"', "coverage must be one of")):
            with self.subTest(new=new):
                guide = fx.write_guide(tempfile.mkdtemp(dir=self.tmp.name), SITE=fx.SITE.replace(old, new))
                with self.assertRaisesRegex(records.RecordError, pattern):
                    records.load_site(guide / "site.toml")

    def test_load_content(self):
        content = records.load_content(self.guide() / "content")
        self.assertEqual(sorted(content.components), ["callout"])
        self.assertEqual(sorted(content.tasks), ["draw-attention"])
        self.assertEqual(sorted(content.pages), ["getting-started", "index"])


if __name__ == "__main__":
    unittest.main()
