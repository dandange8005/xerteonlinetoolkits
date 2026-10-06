import unittest

import support  # noqa: F401
from guidelib.mdsubset import MarkdownError, Section, sections


def render(text):
    return sections(text, "test.md")


class InlineTest(unittest.TestCase):
    def test_bold_italic_and_code(self):
        [s] = render("Use **one** callout per *idea* with `cu-callout`.")
        self.assertEqual(s.html, "<p>Use <strong>one</strong> callout per <em>idea</em> with <code>cu-callout</code>.</p>")

    def test_text_is_escaped(self):
        [s] = render("Fish & chips, a < b")
        self.assertEqual(s.html, "<p>Fish &amp; chips, a &lt; b</p>")

    def test_markup_inside_code_is_allowed_and_escaped(self):
        [s] = render("Paste `<div class=\"x\">` here.")
        self.assertIn("<code>&lt;div class=&quot;x&quot;&gt;</code>", s.html)

    def test_links(self):
        [s] = render("See [Alerts](alert.html) and [the site](https://example.org).")
        self.assertIn('<a href="alert.html">Alerts</a>', s.html)
        self.assertIn('<a href="https://example.org">the site</a>', s.html)

    def test_unsafe_link_scheme_is_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "test.md:1: link scheme 'javascript:'"):
            render("[x](javascript:alert(1))")

    def test_raw_html_is_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "raw HTML is not allowed"):
            render("A <strong>bold</strong> claim.")

    def test_images_are_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "images"):
            render("![logo](logo.png)")


class BlockTest(unittest.TestCase):
    def test_sections_split_at_headings(self):
        result = render("## When to use it\n\nOne idea.\n\n### Do\n\n- Keep it short\n- Name the variant\n")
        self.assertEqual(result, [
            Section(2, "When to use it", "when-to-use-it", "<p>One idea.</p>"),
            Section(3, "Do", "do", "<ul><li>Keep it short</li><li>Name the variant</li></ul>"),
        ])

    def test_text_before_the_first_heading_is_level_0(self):
        result = render("Intro.\n\n## Next\n\nMore.")
        self.assertEqual(result[0], Section(0, "", "", "<p>Intro.</p>"))

    def test_empty_section_is_kept(self):
        result = render("## When to use it\n\n### Do\n\n- a")
        self.assertEqual(result[0].html, "")

    def test_numbered_list(self):
        [s] = render("1. Open\n2. Paste")
        self.assertEqual(s.html, "<ol><li>Open</li><li>Paste</li></ol>")

    def test_paragraph_lines_join(self):
        [s] = render("One line\nand the next.")
        self.assertEqual(s.html, "<p>One line and the next.</p>")

    def test_fenced_code_is_escaped(self):
        [s] = render("```css\n:root { --x: <b>; }\n```")
        self.assertIn('<code class="language-css">:root { --x: &lt;b&gt;; }</code>', s.html)
        self.assertIn('class="g-copy"', s.html)

    def test_unclosed_fence_is_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "not closed"):
            render("```\ncode")

    def test_only_h2_and_h3(self):
        for text in ("# Title", "#### Deep"):
            with self.assertRaisesRegex(MarkdownError, "only ## and ### headings"):
                render(text)

    def test_line_numbers_count_from_first_line(self):
        with self.assertRaisesRegex(MarkdownError, "test.md:12:"):
            sections("Fine.\n\n# Bad", "test.md", first_line=10)

    def test_unsupported_blocks(self):
        for text in ("> quote", "* star list", "  - nested", "---", "| a | b |"):
            with self.subTest(text=text), self.assertRaises(MarkdownError):
                render(text)

    def test_mixed_list_markers_are_an_error(self):
        with self.assertRaisesRegex(MarkdownError, "one marker"):
            render("- a\n1. b")

    def test_windows_line_endings(self):
        [s] = render("## A\r\n\r\nText\r\n")
        self.assertEqual(s, Section(2, "A", "a", "<p>Text</p>"))


class SlugTest(unittest.TestCase):
    def test_heading_slugs(self):
        result = render("## Brand colours\n\nText.\n\n### Don't\n\n- a")
        self.assertEqual([x.slug for x in result], ["brand-colours", "don-t"])


if __name__ == "__main__":
    unittest.main()
