import datetime
import tempfile
import unittest
from pathlib import Path

import support
from guidelib import checks
from guidelib.records import Component, Content, Editor, Example, Page, Site, Task

TIP = Example("Tip", "A tip", '<div class="cu-callout cu-callout-tip"><p>x</p></div>', "cu-callout-tip")
KNOWN = {"cu-callout", "cu-callout-tip", "cu-callout-title", "fa-solid"}


def component(**changes):
    fields = dict(name="callout", title="Callouts", lead="One idea.", group="emphasis", status="current",
                  since="v1.4", tasks=(), related=(), scss=(), editor=Editor(True, datetime.date(2026, 9, 20), "3.14"),
                  parts={"cu-callout": "The container."}, examples=(TIP,), when_html="<p>w</p>", when_not_html="<p>n</p>", how_html="",
                  do_html="<ul><li>a</li></ul>", dont_html="<ul><li>b</li></ul>",
                  accessibility_html="<p>c</p>", source=Path("components/callout.md"))
    fields.update(changes)
    return Component(**fields)


def task(**changes):
    fields = dict(name="draw-attention", title="Draw attention", summary="s", icon="fa-lightbulb",
                  components=("callout",), example=Example("Upload", "p", '<p class="fa-solid">x</p>'),
                  goal_html="<p>g</p>", checklist_html="<ul><li>c</li></ul>", source=Path("tasks/draw-attention.md"))
    fields.update(changes)
    return Task(**fields)


INDEX = Page("index", "Home", "Lead", (), (), (), Path("pages/index.md"))
SITE = Site("Guide", "warn", (("emphasis", "Emphasis"),), (), (("home", "Home"),))


def content(components=(), tasks=(), pages=(INDEX,)):
    return Content({c.name: c for c in components}, {t.name: t for t in tasks}, {p.name: p for p in pages})


def messages(findings):
    return [f"{f.level} {f.check} {f.message}" for f in findings]


class ClassesExistTest(unittest.TestCase):
    def test_known_classes_pass(self):
        self.assertEqual(checks.check_classes_exist(content([component()], [task()]), KNOWN), [])

    def test_unknown_example_class_is_an_error(self):
        bad = Example("Tip", "t", '<div class="cu-callout cu-calout-tip"></div>')
        [finding] = checks.check_classes_exist(content([component(examples=(bad,))]), KNOWN)
        self.assertEqual((finding.level, finding.check), ("error", 1))
        self.assertIn("cu-calout-tip", finding.message)

    def test_unknown_part_is_an_error(self):
        found = checks.check_classes_exist(content([component(parts={"cu-gone": "x"})]), KNOWN)
        self.assertEqual(messages(found), ["error 1 class 'cu-gone' is not defined by the theme or the player's stylesheets"])


class CoverageTest(unittest.TestCase):
    def test_warn_mode_counts_what_is_missing(self):
        [finding] = checks.check_coverage(content([component()]), {"cu-callout", "cu-callout-tip", "box", "card"}, set(), "warn")
        self.assertEqual(finding.level, "warning")
        self.assertIn("2 author-facing classes are not covered yet: box, card", finding.message)

    def test_fail_mode_is_an_error(self):
        [finding] = checks.check_coverage(content([component()]), {"box"}, set(), "fail")
        self.assertEqual(finding.level, "error")

    def test_tables_and_records_claim_classes(self):
        self.assertEqual(checks.check_coverage(content([component()]), {"cu-callout", "cu-callout-tip", "mt-4"}, {"mt-4"}, "fail"), [])

    def test_warn_mode_shows_at_most_ten(self):
        many = {f"c{n:02}" for n in range(15)}
        [finding] = checks.check_coverage(content(), many, set(), "warn")
        self.assertTrue(finding.message.endswith("and 5 more"))


class ReferencesTest(unittest.TestCase):
    def test_valid_references(self):
        good = content([component(tasks=("draw-attention",))], [task()])
        site = Site("Guide", "warn", SITE.groups, ("draw-attention",), SITE.menu)
        self.assertEqual(checks.check_references(good, site, support.THEME), [])

    def test_broken_references(self):
        bad = component(group="layout", tasks=("missing-task",), related=("alert",), scss=("scss/nope.scss",))
        found = messages(checks.check_references(content([bad], [task(components=("button",))]), SITE, support.THEME))
        self.assertIn("error 3 group 'layout' is not in site.toml", found)
        self.assertIn("error 3 task 'missing-task' has no task file", found)
        self.assertIn("error 3 related component 'alert' has no record", found)
        self.assertIn("error 3 SCSS file 'scss/nope.scss' does not exist", found)
        self.assertIn("error 3 component 'button' has no record", found)
        self.assertIn("error 3 task 'draw-attention' is not listed in site.toml tasks", found)

    def test_listed_task_without_a_file(self):
        site = Site("Guide", "warn", SITE.groups, ("ghost",), SITE.menu)
        self.assertIn("error 3 listed task 'ghost' has no task file", messages(checks.check_references(content(), site, support.THEME)))

    def test_menu_needs_its_page(self):
        site = Site("Guide", "warn", SITE.groups, (), (("home", "Home"), ("getting-started", "Getting started")))
        self.assertIn("error 3 menu entry 'getting-started' needs pages/getting-started.md",
                      messages(checks.check_references(content(), site, support.THEME)))

    def test_home_page_is_required(self):
        self.assertIn("error 3 the home page pages/index.md is missing",
                      messages(checks.check_references(content(pages=()), SITE, support.THEME)))


class StaleEvidenceTest(unittest.TestCase):
    def test_newer_scss_warns(self):
        stale = component(scss=("scss/components/_callout.scss",))
        [finding] = checks.check_stale_evidence(content([stale]), lambda path: datetime.date(2026, 9, 28))
        self.assertEqual((finding.level, finding.check), ("warning", 4))
        self.assertIn("changed on 2026-09-28, after the editor evidence of 2026-09-20", finding.message)

    def test_older_scss_is_fine(self):
        fresh = component(scss=("scss/components/_callout.scss",))
        self.assertEqual(checks.check_stale_evidence(content([fresh]), lambda path: datetime.date(2026, 9, 1)), [])

    def test_untested_component_has_no_stale_evidence(self):
        untested = component(editor=None, scss=("scss/components/_callout.scss",))
        self.assertEqual(checks.check_stale_evidence(content([untested]), lambda path: datetime.date(2026, 9, 28)), [])

    def test_stale_evidence_ignores_unknown_dates(self):
        unknown = component(scss=("scss/components/_callout.scss",))
        self.assertEqual(checks.check_stale_evidence(content([unknown]), lambda path: None), [])

    def test_git_last_changed_inside_the_repo(self):
        changed = checks.git_last_changed(support.THEME)("scss/components/_callout.scss")
        self.assertIsInstance(changed, datetime.date)

    def test_git_last_changed_outside_a_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "x.scss").write_text("a{}", encoding="utf-8")
            self.assertIsNone(checks.git_last_changed(Path(tmp))("x.scss"))


class ExamplesTest(unittest.TestCase):
    def check(self, markup):
        return messages(checks.check_examples(content([component(examples=(Example("E", "p", markup),))])))

    def test_image_without_alt_warns(self):
        self.assertEqual(self.check('<img src="a.png">'), ["warning 5 example 'E' has an image without alt text"])

    def test_empty_alt_is_allowed(self):
        self.assertEqual(self.check('<img src="a.png" alt="">'), [])

    def test_empty_heading_warns(self):
        self.assertEqual(self.check('<h3><i class="fa-solid fa-star"></i></h3>'), ["warning 5 example 'E' has an empty heading"])

    def test_heading_with_text_is_fine(self):
        self.assertEqual(self.check("<h3>Title</h3>"), [])


class RunAllTest(unittest.TestCase):
    def test_collects_every_check(self):
        findings = checks.run_all(content([component(parts={"cu-gone": "x"})]), SITE, theme_dir=support.THEME,
                                  known=KNOWN, author_facing={"box"}, tables=set(), last_changed=lambda p: None)
        self.assertEqual(sorted({f.check for f in findings}), [1, 2])
        self.assertEqual(str(findings[0]), "ERROR [check 1] components/callout.md: class 'cu-gone' is not defined by the theme or the player's stylesheets")


if __name__ == "__main__":
    unittest.main()
