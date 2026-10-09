import unittest

import support  # noqa: F401  (puts tools/ on the path)
import theme_css


class ThemeCssTest(unittest.TestCase):
    def test_author_facing_classes_leave_out_legacy_and_page_frame(self):
        facing = theme_css.author_facing_classes()
        self.assertIn("cu-callout-tip", facing)
        self.assertTrue(facing.isdisjoint(theme_css.LEGACY))
        self.assertFalse(any(c.startswith(theme_css.FRAME_PREFIXES) for c in facing))
        self.assertLessEqual(facing, theme_css.theme_classes())

    def test_stack_classes_include_font_awesome_and_unstyled_bootstrap(self):
        known = theme_css.stack_classes()
        for cls in ("cu-callout", "fa-solid", "fa-lightbulb", "row-fluid", "span9"):
            self.assertIn(cls, known)

    def test_clickable_card_hover_adds_a_shadow_and_does_not_zoom_the_image(self):
        # Headless Chrome cannot hover, so this reads the compiled rules.
        hover = [(sel, body) for sel, body, _ in theme_css.rules(theme_css.CSS.read_text(encoding="utf-8"))
                 if ".card--clickable:hover" in sel]
        self.assertTrue(hover)  # not an empty set
        self.assertTrue(any("box-shadow" in body for sel, body in hover if sel == ".card--clickable:hover"))
        self.assertEqual([sel for sel, body in hover if "card__image" in sel or "scale(" in body], [])

    def test_player_stylesheets_exist(self):
        for name in theme_css.PLAYER_CSS + theme_css.IMPORTED_CSS:
            self.assertTrue((theme_css.PLAYER / name).is_file(), name)

    def test_utility_groups_follow_the_family_order(self):
        groups = theme_css.utility_groups({"text-lg": "font-size: 20px", "mt-4": "margin-top: 16px"})
        self.assertEqual([heading for heading, _, _ in groups], ["Spacing", "Text size"])
        self.assertEqual(groups[0][2], [("mt-4", "margin-top: 16px")])


if __name__ == "__main__":
    unittest.main()
