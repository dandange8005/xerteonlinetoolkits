import json
import tempfile
import unittest
from pathlib import Path

import support
from guidelib import reference

TOKENS = {
    "$description": "Test tokens.",
    "primary": {
        "$description": "Tier 1",
        "cu-white": {"$value": "#FFFFFF"},
        "cu-black": {"$value": "#121212"},
        "cu-red": {"$value": "#E4251B"},
    },
    "roles": {
        "cu-bg": {"$value": "{cu-white}"},
        "cu-link": {"$value": "#045bc6", "$description": "recorded deviation"},
    },
    "space": {"cu-space-1": {"$value": "4px"}},
}

COPY = """\
[[groups]]
id = "primary"
title = "Primary colours"
intro = "Red, white and black."
colour = true

[[groups]]
id = "roles"
title = "Colour roles"
intro = "Named by job."
colour = true

[[groups]]
id = "space"
title = "Spacing"
intro = "A 4px base."
"""

UTILITIES = (("Spacing", "Margin and padding.", (("mt-4", "margin-top: 16px"),)),)
LEGACY = (("c10", "Legacy System 2 column width."),)


class LoadReferenceTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def load(self, tokens=TOKENS, copy=COPY):
        (self.dir / "tokens.json").write_text(json.dumps(tokens), encoding="utf-8")
        (self.dir / "reference.toml").write_text(copy, encoding="utf-8")
        return reference.load_reference(self.dir / "tokens.json", self.dir / "reference.toml", UTILITIES, LEGACY)

    def assertLoadError(self, pattern, **kwargs):
        with self.assertRaisesRegex(reference.ReferenceDataError, pattern):
            self.load(**kwargs)

    def test_colour_groups_and_other_groups_are_split(self):
        ref = self.load()
        self.assertEqual([g.id for g in ref.palette], ["primary", "roles"])
        self.assertEqual([g.id for g in ref.tokens], ["space"])

    def test_titles_and_intros_come_from_the_copy_file(self):
        ref = self.load()
        self.assertEqual((ref.palette[0].title, ref.palette[0].intro), ("Primary colours", "Red, white and black."))
        self.assertEqual(ref.tokens[0].title, "Spacing")

    def test_alias_is_resolved_and_remembered(self):
        roles = self.load().palette[1].tokens
        self.assertEqual(roles[0], reference.Token("cu-bg", "{cu-white}", "#FFFFFF", "cu-white", ""))

    def test_note_is_kept(self):
        roles = self.load().palette[1].tokens
        self.assertEqual(roles[1].note, "recorded deviation")
        self.assertEqual(roles[1].resolved, "#045bc6")

    def test_white_and_ink_come_from_the_tokens(self):
        ref = self.load()
        self.assertEqual((ref.white, ref.ink), ("#FFFFFF", "#121212"))

    def test_utilities_and_legacy_pass_through(self):
        ref = self.load()
        self.assertEqual(ref.utilities, UTILITIES)
        self.assertEqual(ref.legacy, LEGACY)

    def test_utility_classes_sort_numbers_in_order(self):
        rows = (("m-10", "margin: 40px"), ("m-2", "margin: 8px"), ("m-1", "margin: 4px"),
                ("mb-2", "margin-bottom: 8px"))
        self.load()
        ref = reference.load_reference(self.dir / "tokens.json", self.dir / "reference.toml",
                                       (("Spacing", "Margins.", rows),), LEGACY)
        self.assertEqual([cls for cls, _ in ref.utilities[0][2]], ["m-1", "m-2", "m-10", "mb-2"])

    def test_colour_group_with_a_value_that_is_not_hex(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["roles"]["cu-overlay"] = {"$value": "rgba(0,0,0,.5)"}
        self.assertLoadError(r"token cu-overlay in colour group roles must be a #RRGGBB colour", tokens=tokens)

    def test_a_group_not_marked_as_colour_stays_off_the_colours_page(self):
        copy = COPY.replace('intro = "Named by job."\ncolour = true', 'intro = "Named by job."')
        ref = self.load(copy=copy)
        self.assertEqual([g.id for g in ref.palette], ["primary"])
        self.assertEqual([g.id for g in ref.tokens], ["roles", "space"])

    def test_colour_key_must_be_true_or_false(self):
        self.assertLoadError(r"entry 1: 'colour' must be true or false",
                             copy=COPY.replace("colour = true", 'colour = "yes"', 1))

    def test_empty_token_group(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["space"] = {"$description": "nothing here"}
        self.assertLoadError(r"token group space has no tokens", tokens=tokens)

    def test_numeric_value_is_read_as_text(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["space"]["cu-weight"] = {"$value": 600}
        self.assertEqual(self.load(tokens=tokens).tokens[0].tokens[1].value, "600")

    def test_token_without_a_value(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["space"]["cu-bad"] = {"$description": "no value"}
        self.assertLoadError(r"token cu-bad in group space has no \$value", tokens=tokens)

    def test_token_defined_in_two_groups(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["roles"]["cu-white"] = {"$value": "#000000"}
        self.assertLoadError(r"token cu-white is defined in more than one group: primary, roles", tokens=tokens)

    def test_alias_inside_a_longer_value_is_resolved(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["space"]["cu-ring"] = {"$value": "0 0 0 2px {cu-white}"}
        ring = self.load(tokens=tokens).tokens[0].tokens[1]
        self.assertEqual((ring.resolved, ring.alias_of), ("0 0 0 2px #FFFFFF", None))

    def test_alias_inside_a_longer_value_to_nothing(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["space"]["cu-ring"] = {"$value": "0 0 0 2px {cu-nope}"}
        self.assertLoadError(r"token cu-ring refers to \{cu-nope\}, which does not exist", tokens=tokens)

    def test_tokens_file_that_is_not_utf8(self):
        (self.dir / "tokens.json").write_bytes('{"primary": {"cu-white": {"$value": "\u2019"}}}'.encode("cp1252", "replace")
                                               + b"\x92")
        (self.dir / "reference.toml").write_text(COPY, encoding="utf-8")
        with self.assertRaisesRegex(reference.ReferenceDataError, r"tokens\.json: cannot read"):
            reference.load_reference(self.dir / "tokens.json", self.dir / "reference.toml", UTILITIES, LEGACY)

    def test_token_group_without_an_entry(self):
        self.assertLoadError(r"reference\.toml: no entry for token group\(s\): space",
                             copy=COPY.split('[[groups]]\nid = "space"')[0])

    def test_entry_for_a_missing_group(self):
        self.assertLoadError(r"tokens\.json does not have: shadows",
                             copy=COPY + '\n[[groups]]\nid = "shadows"\ntitle = "Shadows"\nintro = "Flat."\n')

    def test_alias_to_nothing(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["roles"]["cu-bg"]["$value"] = "{cu-nope}"
        self.assertLoadError(r"token cu-bg refers to \{cu-nope\}, which does not exist", tokens=tokens)

    def test_alias_loop(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["roles"]["cu-a"] = {"$value": "{cu-b}"}
        tokens["roles"]["cu-b"] = {"$value": "{cu-a}"}
        self.assertLoadError(r"token cu-[ab] is part of an alias loop", tokens=tokens)

    def test_white_and_ink_are_required(self):
        tokens = json.loads(json.dumps(TOKENS))
        del tokens["primary"]["cu-white"]
        tokens["roles"]["cu-bg"]["$value"] = "#FFFFFF"
        self.assertLoadError(r"need a cu-white token", tokens=tokens)

    def test_copy_entry_needs_every_key(self):
        self.assertLoadError(r"\[\[groups\]\] entry 1: missing 'intro'",
                             copy='[[groups]]\nid = "primary"\ntitle = "Primary"\n')

    def test_copy_group_id_must_be_a_slug(self):
        self.assertLoadError(r"entry 1: id must use only a-z, 0-9 and hyphens",
                             copy='[[groups]]\nid = "Primary Colours"\ntitle = "t"\nintro = "i"\n')

    def test_copy_group_listed_twice(self):
        self.assertLoadError(r"group 'primary' is listed twice", copy=COPY + COPY.split("\n\n")[0] + "\n")

    def test_unreadable_tokens_file(self):
        with self.assertRaisesRegex(reference.ReferenceDataError, r"tokens\.json: cannot read"):
            reference.load_reference(self.dir / "tokens.json", self.dir / "reference.toml", UTILITIES, LEGACY)

    def test_real_tokens_are_all_described(self):
        """Every token group in the real tokens.json has an entry in the real guide/reference.toml."""
        ref = reference.load_reference(support.THEME / "tokens" / "tokens.json", support.GUIDE / "reference.toml",
                                       UTILITIES, LEGACY)
        names = {t.name for g in ref.palette + ref.tokens for t in g.tokens}
        self.assertIn("cu-brand-red", names)
        self.assertIn("cu-space-4", names)
        self.assertIn("cu-brand-red", {t.name for t in ref.palette[0].tokens})
        self.assertNotIn("cu-space-4", {t.name for g in ref.palette for t in g.tokens})


class ContrastTest(unittest.TestCase):
    def test_black_on_white_is_21(self):
        self.assertEqual(reference.ratio_text(reference.contrast("#000000", "#FFFFFF")), "21.0:1")

    def test_contrast_is_the_same_whichever_colour_is_the_text(self):
        self.assertEqual(reference.contrast("#E4251B", "#FFFFFF"), reference.contrast("#FFFFFF", "#E4251B"))

    def test_white_on_the_ink_colour(self):
        self.assertEqual(reference.ratio_text(reference.contrast("#FFFFFF", "#121212")), "18.7:1")

    def test_aa_boundary_never_reads_as_passing(self):
        # #767676 on white is the lightest grey that passes AA for body text (4.54:1);
        # #777777 is just under (4.48:1). The failing one must not round up to 4.5:1.
        passing = reference.contrast("#767676", "#FFFFFF")
        failing = reference.contrast("#777777", "#FFFFFF")
        self.assertEqual((reference.ratio_text(passing), reference.passes_aa(passing)), ("4.5:1", True))
        self.assertEqual((reference.ratio_text(failing), reference.passes_aa(failing)), ("4.4:1", False))


if __name__ == "__main__":
    unittest.main()
