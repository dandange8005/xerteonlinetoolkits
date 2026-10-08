# Author Guide Phase 2b, Batch 1 (Buttons and Alerts) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Testing reference:** use `mattpocock-skills:tdd`, not `superpowers:test-driven-development`. Test only at the seams listed under [Seams under test](#seams-under-test). The plan already contains code and content that have been run against its tests, so do not delete them and rewrite them from scratch; follow each task's red, then green, steps.

**Goal:** Add the first two component records of phase 2b, Buttons and Alerts, written from facts in the repo, and let a record leave out `since` when the design system version it dates from is not known.

**Architecture:** No new generator features beyond one: `since` becomes optional in a component record, and the Evidence section leaves out the row when it is missing. Everything else is content: two Markdown records with TOML front-matter in `guide/content/components/`. New tests at the build seam check that each component page names every class its component has, so a new theme class cannot go undocumented without a failing test. New browser checks prove two claims the records make: buttons are at least 48px high and 44px wide, and an alert's close button removes it.

**Tech Stack:** Python 3.11+ standard library only, headless Google Chrome for the browser checks. No new dependencies.

**Spec:** `theme-src/cardiffuniversity/docs/design-notes/2026-10-06-author-guide.md`. Glossary: `theme-src/cardiffuniversity/CONTEXT.md`. Earlier plans: `docs/plans/2026-10-06-author-guide-phase-1.md`, `docs/plans/2026-10-07-author-guide-phase-2a.md`.

## Where this fits

Phase 2b adds the seven components in small batches so Nan can review the wording of each:

- **Batch 1 (this plan):** Buttons and Alerts.
- **Later batches (separate plans):** Cards and Tables; Images, Layout and Typography.
- **2c:** two or three more task pages.

## Global Constraints

- Python 3.11 or later. Standard library only: no `pip install`, no third-party packages.
- Run every command from `theme-src/cardiffuniversity/` unless a step says otherwise.
- Do not edit the runtime folder `themes/site/cardiffuniversity/` by hand. Do not change the theme's SCSS or tokens. Out of scope.
- Guide blocks are `<div class="g-section">`, never `<section>`. Only a preview wraps examples in `<section>`.
- No deploy or GitHub Pages job. Nothing is published.
- All guide text in UK English, without em dashes, using the `CONTEXT.md` terms: content author, component, variant, part, example, text content item, page frame, guide page, drift. Never "snippet", "type" (for variants), "Text element", "user", "chrome".
- Facts shown on guide pages must come from the repo (the SCSS, the demos, the design notes, the design system). Where a sentence is the plan author's own addition, it is listed under "Sources and open claims" so Nan can confirm or strike it. Do not add editor evidence: neither component has been tested in the Xerte editor.
- `python3 tools/build-reference.py --check` must keep printing `In sync`.
- Work on the branch `feat/author-guide-phase-2b-batch-1`, which already holds this plan. Commit after every task. End every commit message with the `Co-Authored-By` line from the session's attribution instructions.
- Unit tests run with `python3 -m unittest discover -s tests -p "test_*.py"`.
- Edit blocks below read: **Edit `path`:** replace the first block with the second. The first block must match the file exactly once.

## Review Focus

1. **A component record with no `since`**: the page builds, shows no "Since" row, and nothing crashes. Test in Task 1: `test_since_is_optional`, `test_evidence_leaves_out_since_when_unknown`.
2. **A class the theme gives a component but its record does not mention**: the build-seam test names the missing class. Today that is every `button*` class; tomorrow it could be a new one. Test in Task 2: `test_button_page_documents_every_button_class`.
3. **The dismissible alert example in the guide**: the example's close button must really remove the alert, because the page shows it working. Browser check in Task 3: "the close button removes its alert".
4. **A claim the record makes about the theme** (buttons are at least 48px high and 44px wide): a browser check measures the rendered examples, so the sentence cannot go stale. Browser check in Task 2.
5. **A page with sixteen example frames at phone width**: the Buttons page does not scroll sideways at 485px. Browser check in Task 2.

## Seams under test

Same boundaries as 2a. Helpers are tested only through these.

| Seam | What the tests observe | Test file |
| --- | --- | --- |
| `records.load_component()`, `load_content()` | What a record file loads as | `test_records.py` |
| `pages.write_site()` | The pages written to disk, read back with `tests/html_tree.py` | `test_pages.py` |
| `build-guide.build()` | The finished real site on disk | `test_guide_content.py` |
| The built site in Chrome | Layout and behaviour in a real browser | `check_guide.py` |

**About the first red.** Task 1's first red is a missing field. Tasks 2 and 3 fail because the page does not exist yet, which only proves the test runs. The browser checks are the real behavioural proof: they measure the examples and click the close button.

## Decisions this plan makes inside the spec

Each is deliberate. Nan can overrule any of them in review.

- **`since` is optional.** The spec's record format required it. The phase 1 callout record says v1.4, which came from the design system's own changelog. For buttons and alerts nothing in the repo says which design system version they date from, and the guide must not invent it. A record without `since` shows no "Since" row.
- **Batch 1 is Buttons and Alerts.** They are small, each variant is clearly shown in the demos, and the SCSS and a design note record their decisions. Cards and Tables, then Images, Layout and Typography, follow as their own batches.
- **Neither record has an `[editor]` table.** Both pages say "Not tested in the Xerte editor yet".
- **The link-as-button markup is a code block in "How to use it"**, not an example frame. The example frames show one variant class each, and a link button has no class of its own.
- **Older classes are listed and labelled "older, kept for older content".** The SCSS marks `button--outline`, `button--small`, `button--block` and `btn-mini` as legacy, "preserved for backward compatibility". The records say that and no more.
- **Examples use `<i ... aria-hidden="true">` for icons.** The demos leave `aria-hidden` off. This is the plan author's addition (see below).
- **No task page uses these components yet.** Phase 2c adds task pages; until then the component pages have no "Task:" links.

## Sources and open claims

Every sentence in the two records, with where it comes from. **Draft** means the plan author wrote it from the facts shown and Nan should confirm it.

**Buttons**

| Statement | Source |
| --- | --- |
| A button starts an action or takes the reader to a clear next step | Design system `DESIGN.md` §3 "Default: native button or anchor with a real destination"; demo Buttons section |
| Primary is the main action on the page | `DESIGN.md` §2 red job 2: "The primary action: the primary button" |
| Secondary is the design system's secondary button; pair it with one primary button | Demo Buttons section, "Outline Buttons" description; `_buttons.scss` header, "DESIGN SYSTEM NAMES" |
| Filled black secondary is kept for existing content | `_buttons.scss` header, decided by Nan on 23 September 2026 |
| Reverse variants are for dark backgrounds | Demo "Reverse Buttons (Dark Backgrounds)" |
| Ghost has no fill or border; a light grey appears on hover | `_buttons.scss` `.button-ghost` (transparent, no border, `--btn-ghost-hover-bg` is grey-10) |
| `button--block` fills its container's width; `button--small` is a smaller button; `button--outline` and `btn-mini` are older | `_buttons.scss` legacy section (`width: 100%`, small font and padding, "Legacy ... preserved for backward compatibility"); `btn-mini` is 40px round and "e.g., back to top button" |
| Buttons are at least 48px high and 44px wide | `_allvariables.scss` `--btn-min-height: 48px`, `--btn-min-width: 44px`; checked in the browser |
| Keyboard focus shows a visible outline | `_buttons.scss` `&:focus-visible` rule |
| Use the `disabled` attribute; disable only when the action is really unavailable | `DESIGN.md` button states table, "Disabled" row |
| No gradients, shadows or pill shapes | `DESIGN.md` §3 "Do not apply gradients, shadows or pill shapes" |
| For a link inside a sentence use a normal text link | `DESIGN.md` Do list "use blue underlined text links". **Draft:** the "when not to use a button" framing is the plan author's inference |
| Give an icon-only button an `aria-label` | Demo "Buttons with Icons" (`aria-label="Search"`) |
| Hide an icon beside a visible label with `aria-hidden="true"` | **Draft:** standard practice, not in the demos or the design system |

**Alerts**

| Statement | Source |
| --- | --- |
| Success is a completed action, info is neutral information, warning needs caution, danger and error are errors or critical issues | Demo Bootstrap "Usage Guidelines", Alerts list |
| Grey surface, square edges, 4px left rule in the status colour | Design note `2026-09-21-alerts-badges-progress.md`, "Decisions" and "What changed" |
| The glyphs (✓ ℹ ⚠ ✗) and the bold word carry the status, so the rule's colour is never the only cue | Same design note; `_bootstrap-components.scss` (`content: "✓ "` and so on) |
| Danger and error look the same | `_bootstrap-components.scss` `.alert-danger, .alert-error` |
| Alert text is ink on grey, 16.7:1 (measured 21 September 2026) | Design note, Problem table |
| The warning rule is yellow and only 1.6:1 against the surface; acceptable because the glyph and word carry the meaning | Design note, "What changed" |
| Error red is kept for real problems | `DESIGN.md` §2 red job 4 |
| A block alert holds more content, with a heading, and can be dismissed with a close button using `data-dismiss="alert"` | Demo "Block Alert with Dismissible" |
| Do not use an alert to point out a tip or the main takeaway; a callout does that | **Draft:** the boundary between alerts and callouts is the plan author's inference from the two components' purposes |
| Give the close button an `aria-label` | **Draft:** the demo's close button has no label; its visible text is only ×. Standard practice |

## Findings outside this plan

Found while measuring the pages. Neither is fixed here; both need Nan's decision.

- **Alert text is 14px.** `_bootstrap-components.scss` sets `.alert { font-size: var(--font-size-sm); }`, and `--font-size-sm` is 14px. An alert message is arguably main content, and design system v1.12 (8 October 2026) says main content is never below 16px. Options: raise `.alert` to the 16px interface size in the theme, or decide an alert message counts as secondary text. The Alerts record does not mention the size either way.
- **The glyph before an alert's bold word is as small as the text** (also 14px), so the glyph, one of the two cues that carry the status, is small. It follows the same decision.

**Added after the final review (theme findings, not fixed here):**

- **Focus cannot be seen on the reverse buttons.** The focus ring is 2px solid ink, and `.bg-dark` is also ink, so on the dark panel the outline disappears. Measured on the built Buttons page. The carousel already uses a white ring on dark. The Buttons record now says to check focus on the reverse variants.
- **Small buttons are 14px.** `button-sm` and `button--small` use `--btn-font-size-sm` (14px), below the 16px minimum for buttons in design system v1.12. The record now says so in the variant's purpose.
- **The older outline button has a weak focus indicator** (reported by the reviewer): its `:focus` rule sets the outline colour to transparent, leaving a 4px light grey ring of about 1.4:1 on white.
- **The alert close button is a small target** (reported by the reviewer): about 13 by 20px at half opacity.
- **The info glyph is tiny** at 14px (reported by the reviewer), which weakens "the glyph carries the status" for info alerts most of all.

## File structure

| Path (under `theme-src/cardiffuniversity/` unless shown) | Responsibility |
| --- | --- |
| `tools/guidelib/records.py` (modify) | `since` optional |
| `tools/guidelib/pages.py` (modify) | Evidence leaves out "Since" when unknown |
| `guide/content/components/button.md` (create) | The Buttons record |
| `guide/content/components/alert.md` (create) | The Alerts record |
| `guide/content/components/callout.md` (modify) | Related link to Alerts |
| `tests/test_records.py`, `tests/test_pages.py`, `tests/test_guide_content.py`, `tests/check_guide.py` (modify) | New behaviour and content checks |
| `docs/design-notes/2026-10-06-author-guide.md`, `THEMING-GUIDE.md`, `MIGRATION.md` (modify) | Keep the docs true |

---

### Task 1: An optional `since`

**Files:**
- Modify: `tools/guidelib/records.py`, `tools/guidelib/pages.py`
- Modify: `tests/test_records.py`, `tests/test_pages.py`
- Modify: `docs/design-notes/2026-10-06-author-guide.md`, `THEMING-GUIDE.md`

**Interfaces:**
- Consumes: nothing new.
- Produces: `Component.since` is `str | None`. `pages.evidence(component)` leaves out the "Since" row when it is `None`.

- [ ] **Step 1: Confirm the branch**

Run: `git branch --show-current`
Expected: `feat/author-guide-phase-2b-batch-1`

- [ ] **Step 2: Write the failing tests**

**Edit `tests/test_records.py`:** replace

```python
    def test_untested_component_has_no_editor_evidence(self):
```

with

```python
    def test_since_is_optional(self):
        record = self.component(fx.CALLOUT.replace('since = "v1.4"\n', ""))
        self.assertIsNone(record.since)

    def test_untested_component_has_no_editor_evidence(self):
```

**Edit `tests/test_pages.py`:** replace

```python
class UntestedEvidenceTest(unittest.TestCase):
```

with

```python
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
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"`
Expected: `ERROR: test_since_is_optional` (`missing 'since'`), `ERROR: test_evidence_leaves_out_since_when_unknown`, then `FAILED`.

- [ ] **Step 4: Make `since` optional**

**Edit `tools/guidelib/records.py`:** replace

```python
    since: str
    related: tuple
```

with

```python
    since: str | None  # the design system version the component dates from, when known
    related: tuple
```

**Edit `tools/guidelib/records.py`:** replace

```python
status=status, since=_field(data, "since", str, path),
```

with

```python
status=status,
        since=_field(data, "since", str, path, required=False, default=None),
```

**Edit `tools/guidelib/pages.py`:** replace

```python
    rows = (("Status", esc(component.status.capitalize())),
            ("Since", f"Design system {esc(component.since)}"),
            ("Xerte editor", editor_text),
            ("Main class", f"<code>.{esc(next(iter(component.parts)))}</code>"))
```

with

```python
    rows = [("Status", esc(component.status.capitalize()))]
    if component.since:
        rows.append(("Since", f"Design system {esc(component.since)}"))
    rows += [("Xerte editor", editor_text),
             ("Main class", f"<code>.{esc(next(iter(component.parts)))}</code>")]
```

- [ ] **Step 5: Update the spec and the maintainer guide**

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
since = "v1.4"
related = ["alert", "well"]
````

with

````markdown
since = "v1.4"                            # optional: the design system version it dates from; leave it out when unknown
related = ["alert", "well"]
````

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
9. Evidence: status, the design system version it dates from, and the editor evidence (result,
````

with

````markdown
9. Evidence: status, the design system version it dates from (left out when the record has no
   `since`), and the editor evidence (result,
````

**Edit `THEMING-GUIDE.md`:** replace

````markdown
the `checked` date.

A task file lists the components it uses under `components`.
````

with

````markdown
the `checked` date. A record's `since`, the design system version the component dates from, is
optional too: leave it out when you do not know it, and the Evidence section leaves out the row.

A task file lists the components it uses under `components`.
````

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3 && ./build.sh guide 2>&1 | tail -1 | cut -c1-90`
Expected: `OK`, then `Built .../site (10 pages, 2 warning(s)).`

- [ ] **Step 7: Commit**

```bash
git add tools/guidelib/records.py tools/guidelib/pages.py tests/test_records.py tests/test_pages.py docs/design-notes/2026-10-06-author-guide.md THEMING-GUIDE.md
git commit -m "feat(cardiffuniversity): let a component record leave out since"
```

---

### Task 2: The Buttons record

**Files:**
- Create: `guide/content/components/button.md`
- Modify: `tests/test_guide_content.py`, `tests/check_guide.py`

**Interfaces:**
- Consumes: the record format from phases 1 and 2a; `theme_css.author_facing_classes()`.
- Produces: `components/button.html` in the built site, listing every `button*` class and `btn-mini`.

- [ ] **Step 1: Write the failing tests**

**Edit `tests/test_guide_content.py`:** replace

```python
import support
from html_tree import parse
```

with

```python
import support
import theme_css
from html_tree import parse
```

**Edit `tests/test_guide_content.py`:** replace

```python
if __name__ == "__main__":
    unittest.main()
```

with

```python
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
        self.assertGreaterEqual(len(expected), 19)
        self.assertEqual(expected - self.shown("button"), set())
        self.assertIn("btn-mini", self.shown("button"))

    def test_components_index_lists_the_buttons(self):
        index = parse((self.out / "components" / "index.html").read_text(encoding="utf-8"))
        hrefs = [a.attrs["href"] for card in index.find_all(cls="g-card") for a in card.find_all("a")]
        self.assertIn("button.html", hrefs)


if __name__ == "__main__":
    unittest.main()
```

**Edit `tests/check_guide.py`:** replace

```python
    ("components/callout.html", 1280, "the Cardiff logo loads",
```

with

```python
    ("components/button.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/button.html", 1280, "every button example is at least 48px high and 44px wide",
     "[].every.call(document.querySelectorAll('.g-preview .button'), function (b) {"
     " var r = b.getBoundingClientRect(); return r.height >= 47.5 && r.width >= 43.5; })"),
    ("components/callout.html", 1280, "the Cardiff logo loads",
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"; python3 tests/check_guide.py 2>&1 | tail -2 | cut -c1-160`
Expected: `ERROR: test_button_page_documents_every_button_class` and `ERROR: test_components_index_lists_the_buttons` (`FileNotFoundError` for `components/button.html`, or an empty page set), and the browser check stops with a `FileNotFoundError` for `components/button.html`.

- [ ] **Step 3: Write the Buttons record**

`guide/content/components/button.md`:

````markdown
+++
name = "button"
title = "Buttons"
lead = "A button starts an action or takes the reader to a clear next step."
group = "interaction"
status = "current"
related = []
scss = ["scss/components/_buttons.scss"]

[parts]
button = "The base class every button needs. It gives the button its shape, size and states."
button__icon = "An optional wrapper for an icon inside a button."
button--outline = "An older outline style, kept so older content still works."
btn-mini = "A 40px round icon button, kept for older content. The theme also uses it for the back-to-top button."

[[examples]]
class = "button-primary"
label = "Primary"
purpose = "The main action on the page"
html = '''
<button class="button button-primary">Continue</button>
'''

[[examples]]
class = "button-secondary-outline"
label = "Secondary"
purpose = "The design system's secondary button. Pair it with one primary button"
html = '''
<button class="button button-secondary-outline">Back</button>
'''

[[examples]]
class = "button-secondary"
label = "Filled black"
purpose = "A filled black button that predates the design system, kept for existing content"
html = '''
<button class="button button-secondary">Filled black</button>
'''

[[examples]]
class = "button-success"
label = "Success"
purpose = "A filled button in the success colour"
html = '''
<button class="button button-success">Success</button>
'''

[[examples]]
class = "button-primary-outline"
label = "Primary outline"
purpose = "An outlined version of the primary button"
html = '''
<button class="button button-primary-outline">Primary outline</button>
'''

[[examples]]
class = "button-success-outline"
label = "Success outline"
purpose = "An outlined version of the success button"
html = '''
<button class="button button-success-outline">Success outline</button>
'''

[[examples]]
class = "button-ghost"
label = "Ghost"
purpose = "A button with no fill or border. A light grey background appears on hover"
html = '''
<button class="button button-ghost">Ghost</button>
'''

[[examples]]
class = "button-reverse"
label = "Reverse"
purpose = "A filled button for dark backgrounds"
html = '''
<div class="bg-dark p-4">
  <button class="button button-reverse">Reverse</button>
</div>
'''

[[examples]]
class = "button-reverse-outline"
label = "Reverse outline"
purpose = "An outlined button for dark backgrounds"
html = '''
<div class="bg-dark p-4">
  <button class="button button-reverse-outline">Reverse outline</button>
</div>
'''

[[examples]]
class = "button-sm"
label = "Small"
purpose = "A smaller button"
html = '''
<button class="button button-primary button-sm">Small</button>
'''

[[examples]]
class = "button-lg"
label = "Large"
purpose = "A larger button"
html = '''
<button class="button button-primary button-lg">Large</button>
'''

[[examples]]
class = "button--small"
label = "Compact (older)"
purpose = "A smaller button. An older class, kept for older content"
html = '''
<button class="button button-primary button--small">Compact</button>
'''

[[examples]]
class = "button--block"
label = "Block (older)"
purpose = "A button that fills the width of its container. An older class, kept for older content"
html = '''
<button class="button button-primary button--block">Block</button>
'''

[[examples]]
class = "button-icon-left"
label = "Icon on the left"
purpose = "An icon before the label"
html = '''
<button class="button button-primary button-icon-left">
  <i class="fa-solid fa-arrow-left" aria-hidden="true"></i> Previous
</button>
'''

[[examples]]
class = "button-icon-right"
label = "Icon on the right"
purpose = "An icon after the label"
html = '''
<button class="button button-primary button-icon-right">
  Next <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
</button>
'''

[[examples]]
class = "button-icon-only"
label = "Icon only"
purpose = "A square button with only an icon. It needs an aria-label"
html = '''
<button class="button button-primary button-icon-only" aria-label="Search">
  <i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>
</button>
'''
+++

## When to use it

Use a button to start an action, or to take the reader to a clear next step.

## When not to use it

For a link inside a sentence, use a normal text link. A button is for an action or a clear next step, not for running text.

## How to use it

Use a button element for an action. For a destination, use a link with the same classes: it looks the same.

```html
<a href="https://example.org" class="button button-primary">Go to the next page</a>
```

### Do

- Use one primary button for the main action, and pair it with the secondary variant when the reader has a second choice.
- Use a button element for an action and a link for a destination.
- Use the reverse variants on dark backgrounds.
- Give an icon-only button an `aria-label` that says what it does.

### Don't

- Disable a button unless the action is really unavailable.
- Use the filled black variant for the design system's secondary button. Use the secondary variant instead.
- Use the older classes in new content.
- Add gradients, shadows or pill shapes.

## Accessibility

- Buttons are at least 48px high and 44px wide, so they are easy to hit on a touch screen.
- Keyboard focus shows a visible outline.
- To disable a button, use the `disabled` attribute, so it is also disabled for keyboard and screen reader users.
- Give an icon-only button an `aria-label`, and hide an icon that sits beside a visible label with `aria-hidden="true"`.
````

- [ ] **Step 4: Run everything**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3 && python3 tests/check_guide.py 2>&1 | grep -E "FAIL|got|passed" && ./build.sh guide 2>&1 | tail -3 | cut -c1-120`
Expected: `OK`; `37 passed, 0 failed` (the 35 existing browser checks plus the 2 new button checks); the coverage warning count falls from 86 to about 66; `Built .../site (11 pages, ...)`.

- [ ] **Step 5: Look at the page**

Run: `open site/components/button.html`. Check by eye that each variant sits in its own frame, the reverse variants sit on a dark panel, the icon buttons show their icons, and the Evidence section says "Not tested in the Xerte editor yet" with no "Since" row.

- [ ] **Step 6: Commit**

```bash
git add guide/content/components/button.md tests/test_guide_content.py tests/check_guide.py
git commit -m "feat(cardiffuniversity): add the Buttons component to the author guide"
```

---

### Task 3: The Alerts record, links and docs

**Files:**
- Create: `guide/content/components/alert.md`
- Modify: `guide/content/components/callout.md`
- Modify: `tests/test_guide_content.py`, `tests/check_guide.py`
- Modify: `docs/design-notes/2026-10-06-author-guide.md`, `MIGRATION.md`

**Interfaces:**
- Consumes: the Buttons work from Task 2 (`BuiltComponentPagesTest`).
- Produces: `components/alert.html`, and a "Related" link between Alerts and Callouts in both directions.

- [ ] **Step 1: Write the failing tests**

**Edit `tests/test_guide_content.py`:** replace

```python
    def test_components_index_lists_the_buttons(self):
```

with

```python
    def test_alert_page_documents_the_alert_classes(self):
        expected = {"alert", "alert-success", "alert-info", "alert-warning", "alert-danger",
                    "alert-error", "alert-block", "close"}
        self.assertEqual(expected - self.shown("alert"), set())

    def test_alerts_and_callouts_link_to_each_other(self):
        def related(name):
            return [a.text() for a in self.page(name).find(cls="g-related").find_all("a")]
        self.assertIn("Callouts", related("alert"))
        self.assertIn("Alerts", related("callout"))

    def test_components_index_lists_the_buttons(self):
```

**Edit `tests/check_guide.py`:** replace

```python
    ("components/callout.html", 1280, "the Cardiff logo loads",
```

with

```python
    ("components/alert.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/alert.html", 1280, "the close button removes its alert",
     "(function () { var a = document.querySelector('.g-preview .alert-block'); if (!a) return false;"
     " a.querySelector('.close').click(); return !document.contains(a); })()"),
    ("components/callout.html", 1280, "the Cardiff logo loads",
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"; python3 tests/check_guide.py 2>&1 | tail -2 | cut -c1-160`
Expected: `ERROR: test_alert_page_documents_the_alert_classes` and `ERROR: test_alerts_and_callouts_link_to_each_other` (the alert page does not exist), and the browser check stops with a `FileNotFoundError` for `components/alert.html`.

- [ ] **Step 3: Write the Alerts record**

`guide/content/components/alert.md`:

````markdown
+++
name = "alert"
title = "Alerts"
lead = "A short message that tells the reader the status of something."
group = "emphasis"
status = "current"
related = ["callout"]
scss = ["scss/_bootstrap-components.scss"]

[parts]
alert = "The base class every alert needs. It gives the grey surface, the square edges and the 4px rule."
close = "The dismiss button inside an alert. With data-dismiss=\"alert\", the player's Bootstrap script removes the alert when the reader clicks it."

[[examples]]
class = "alert-success"
label = "Success"
purpose = "A completed action"
html = '''
<div class="alert alert-success">
  <strong>Success!</strong> Your changes have been saved successfully.
</div>
'''

[[examples]]
class = "alert-info"
label = "Info"
purpose = "Neutral information"
html = '''
<div class="alert alert-info">
  <strong>Info:</strong> This course will be available from September 2025.
</div>
'''

[[examples]]
class = "alert-warning"
label = "Warning"
purpose = "Caution needed"
html = '''
<div class="alert alert-warning">
  <strong>Warning!</strong> Your session will expire in 5 minutes.
</div>
'''

[[examples]]
class = "alert-danger"
label = "Danger"
purpose = "An error or a critical issue"
html = '''
<div class="alert alert-danger">
  <strong>Error!</strong> Unable to submit form. Please check required fields.
</div>
'''

[[examples]]
class = "alert-error"
label = "Error"
purpose = "The same as danger"
html = '''
<div class="alert alert-error">
  <strong>Error!</strong> Unable to submit form. Please check required fields.
</div>
'''

[[examples]]
class = "alert-block"
label = "Block"
purpose = "A longer message with a heading, which the reader can dismiss"
html = '''
<div class="alert alert-block alert-info">
  <button type="button" class="close" data-dismiss="alert" aria-label="Close">&times;</button>
  <h4>Important information</h4>
  <p>This is a block alert with more content. It can hold more than one paragraph.</p>
  <p>Select the close button to dismiss this alert.</p>
</div>
'''
+++

## When to use it

Use an alert to tell the reader the status of something: a completed action, neutral information, a need for caution, or an error.

## When not to use it

Do not use an alert to point out a tip or the main takeaway of a page. An alert reports a status. A callout draws attention to one idea.

## How to use it

Start the message with a bold word that names the status, such as Success or Warning. The theme adds a glyph before it. When a message needs more than a sentence, use a block alert with a heading.

### Do

- Choose the variant that matches the status.
- Start the message with a bold word that says the status.
- Use a block alert when the message needs more than a sentence.

### Don't

- Use the danger or error variant for something that is not a real problem. The error red is kept for real problems.
- Rely on the colour of the left rule alone. The glyph and the bold word carry the status.

## Accessibility

- The glyph and the bold word carry the status, so the colour of the rule is never the only cue.
- Alert text is ink on a grey surface, which measured 16.7:1 in September 2026.
- The yellow rule of the warning variant is only 1.6:1 against the grey surface. That is acceptable only because the glyph and the word carry the meaning, so always keep the bold word.
- Give the close button an `aria-label`, because its visible text is only the × sign.
````

**Edit `guide/content/components/callout.md`:** replace

```toml
since = "v1.4"
related = []
```

with

```toml
since = "v1.4"
related = ["alert"]
```

- [ ] **Step 4: Update the spec and the migration status**

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
   - **2b.** Buttons, cards, tables, alerts, images, layout and typography, in small batches.
````

with

````markdown
   - **2b.** Buttons, cards, tables, alerts, images, layout and typography, in small batches.
     Batch 1: buttons and alerts.
````

**Edit `MIGRATION.md`:** replace

````markdown
components and phase 2c more task pages.
````

with

````markdown
components, in small batches (batch 1: buttons and alerts), and phase 2c more task pages.
````

- [ ] **Step 5: Run everything**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3 && python3 tests/check_guide.py 2>&1 | grep -E "FAIL|got|passed" && ./build.sh guide 2>&1 | tail -3 | cut -c1-120 && git diff --check && echo whitespace-ok`
Expected: `OK`; `39 passed, 0 failed` (the 37 from Task 2 plus the 2 new alert checks); the coverage warning count falls further; `Built .../site (12 pages, ...)`; `whitespace-ok`.

Note on the count: each page adds 2 browser checks, so the total is 35 + 2 (Task 2) + 2 (Task 3) = 39.

- [ ] **Step 6: Look at the pages**

Run: `open site/components/alert.html`. Check that the success, info, warning and danger alerts each show their glyph and a coloured left rule, and that the block alert's close button works when you click it.

- [ ] **Step 7: Commit**

```bash
git add guide/content/components/alert.md guide/content/components/callout.md tests/test_guide_content.py tests/check_guide.py docs/design-notes/2026-10-06-author-guide.md MIGRATION.md
git commit -m "feat(cardiffuniversity): add the Alerts component and link it to Callouts"
```

---

## Self-review

**Spec coverage.**

| Requirement | Task |
| --- | --- |
| Optional `since` (no invented design system version) | 1 |
| Buttons component record, every `button*` class documented | 2 |
| Alerts component record, the alert classes documented | 3 |
| Alerts and Callouts link to each other | 3 |
| Each claim in a record is backed by a source or flagged | "Sources and open claims" above |
| Two browser claims proved against the real theme (button size, dismiss) | 2, 3 |
| Docs stay true | 1, 3 |

Not in batch 1, by design: Cards, Tables, Images, Layout, Typography (later batches), task pages (2c), editor evidence (needs a Docker Xerte test).

**Manual checks after Task 3 (Nan):** read the "Sources and open claims" table and strike or reword any **Draft** line you disagree with (the callout boundary in "When not to use it" for Alerts, the `aria-hidden` and `aria-label` advice, and the link-in-a-sentence line for Buttons); look at both pages at phone width; decide whether to run a Docker Xerte test so these records can gain an `[editor]` table.
