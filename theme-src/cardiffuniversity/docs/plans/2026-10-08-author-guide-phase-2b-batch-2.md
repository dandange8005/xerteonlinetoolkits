# Author Guide Phase 2b, Batch 2 (Cards and Tables) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Testing reference:** use `mattpocock-skills:tdd`, not `superpowers:test-driven-development`. Test only at the seams listed under [Seams under test](#seams-under-test). The plan already contains content that has been run against its tests, so do not delete it and rewrite it from scratch; follow each task's red, then green, steps.

**Goal:** Add the Cards and Tables component records to the author guide, written from facts in the repo, with tests that check each page names every class its component has and browser checks that prove the claims the pages make.

**Architecture:** No generator changes. Two Markdown records with TOML front-matter in `guide/content/components/`. New build-seam tests check class coverage and that the card examples load nothing from outside. New browser checks measure the real rendered examples: the stretched card link, the widescreen card image, a wide table scrolling inside its wrapper and not the page, the wrapper taking keyboard focus, and striped rows differing from plain rows.

**Tech Stack:** Python 3.11+ standard library only, headless Google Chrome for the browser checks. No new dependencies.

**Spec:** `theme-src/cardiffuniversity/docs/design-notes/2026-10-06-author-guide.md`. Glossary: `theme-src/cardiffuniversity/CONTEXT.md`. Earlier plans: `docs/plans/2026-10-08-author-guide-phase-2b-batch-1.md` (the same shape as this one).

## Where this fits

- **Batch 1 (done):** Buttons and Alerts.
- **Batch 2 (this plan):** Cards and Tables.
- **Batch 3 (a later plan):** Images, Layout and Typography.
- **2c:** two or three more task pages.

This branch is based on `feat/retire-button-outline`, which retired `button--outline` from the Buttons page (not yet merged into `develop`). It shares one test file with this plan, so the two branches should be merged in that order.

## Global Constraints

- Python 3.11 or later. Standard library only: no `pip install`, no third-party packages.
- Run every command from `theme-src/cardiffuniversity/` unless a step says otherwise.
- Do not edit the runtime folder `themes/site/cardiffuniversity/` by hand. Do not change the theme's SCSS or tokens. Out of scope.
- Guide blocks are `<div class="g-section">`, never `<section>`. Only a preview wraps examples in `<section>`.
- No deploy or GitHub Pages job. Nothing is published.
- All guide text in UK English, without em dashes, using the `CONTEXT.md` terms: content author, component, variant, part, example, text content item, page frame, guide page, drift. Never "snippet", "type" (for variants), "Text element", "user", "chrome".
- Facts shown on guide pages must come from the repo (the SCSS, the demos, the design notes, the design system). Where a sentence is the plan author's own addition it is listed under "Sources and open claims" as a **Draft**, for Nan to confirm or strike. Do not add editor evidence: neither component has been tested in the Xerte editor.
- Examples must load nothing from outside the page: no external image URLs. The demos use `picsum.photos`; the guide uses a self-contained SVG data URI.
- `python3 tools/build-reference.py --check` must keep printing `In sync`.
- Work on the branch `feat/author-guide-phase-2b-batch-2`, which already holds this plan. Commit after every task. End every commit message with the `Co-Authored-By` line from the session's attribution instructions.
- Unit tests run with `python3 -m unittest discover -s tests -p "test_*.py"`.
- Edit blocks below read: **Edit `path`:** replace the first block with the second. The first block must match the file exactly once.

## Review Focus

1. **A class the theme gives a component that its record does not mention**: the build-seam test names the missing class. Today that is every `card*` class. Test in Task 1: `test_card_page_documents_every_card_class`.
2. **The whole clickable card is one link**, because the page says so. Browser check in Task 1: "the whole clickable card is one link".
3. **A wide table scrolls inside its wrapper and does not stretch the page**, because the page says an unwrapped one does. Browser checks in Task 2: "the wide table scrolls inside its wrapper, not the page" and "the wrapper can take keyboard focus".
4. **Card examples that load something from outside the page**: a broken or tracking image URL. Test in Task 1: `test_card_examples_load_nothing_from_outside`.
5. **Narrow screens**: neither page scrolls sideways at 485px, and the wide table sits in its own scroll box. Browser checks in Tasks 1 and 2.

## Seams under test

Same boundaries as batch 1.

| Seam | What the tests observe | Test file |
| --- | --- | --- |
| `build-guide.build()` | The finished real site on disk | `test_guide_content.py` |
| The built site in Chrome | Layout and behaviour in a real browser | `check_guide.py` |

**About the first red.** Each test fails first because the page does not exist yet, which only proves the test runs. The browser checks are the behavioural proof: they click, focus and measure the rendered examples.

## Decisions this plan makes inside the spec

Each is deliberate. Nan can overrule any of them in review.

- **The first example has no `class`.** A basic card and a standard table are not variants of anything. The top example shows them, and the Variants section lists only classed examples.
- **`card__image` is a variant, not a part.** "A card with an image" is one of the ways to build a card, and a part cannot also be a variant. The Parts table lists the other card classes.
- **`cu-table-scroll` is a variant of Tables** (a wrapper example), and `table-striped` is the other.
- **Card images use a self-contained SVG data URI** (a plain grey 16:9 rectangle), not the demos' `picsum.photos` URLs. This also closes the "bundle the external placeholder images" item for these two components. The code view shows the data URI, which an author replaces with their own image.
- **Bootstrap's other table classes are not documented as variants.** The tables design note says `table-bordered`, `table-hover` and `table-condensed` were not reviewed. The record says so and tells authors to check them.
- **No claim about links inside a clickable card.** The stretched link may cover other links in the card, but the repo does not say and the plan did not measure it. It is listed as an open question.
- **Neither record has an `[editor]` table or a `since`.** Both pages say "Not tested in the Xerte editor yet" and show no "Since" row.
- **The standard table has short column headings** (Year 1, Year 2, Total). The demo's "Undergraduate" and "Postgraduate" headings made the unwrapped table 482px wide, wider than a phone's example frame, so the page scrolled sideways at 485px. That is the problem `cu-table-scroll` exists to solve, but the first example should not show it. Verified in a scratch copy.
- **No theme changes.** The card findings below are recorded for Nan and not fixed.

## Sources and open claims

Every sentence in the two records, with where it comes from. **Draft** means the plan author wrote it and Nan should confirm it.

**Cards**

| Statement | Source |
| --- | --- |
| A card groups a heading, a short description and an optional image into one block | `_cards.scss` header: "Content card container with image, heading, and description" |
| `card` is a white block with a thin border | `_cards.scss` `.card` (white background, 1px border) |
| `card__content` wraps the text and adds the padding | `_cards.scss` `&__content` |
| `card__heading` is smaller than a page heading | Cards design note, "What changed"; demo Basic Card description |
| `card__metadata` is an optional line for a category, a length or similar | `_cards.scss` header ("Optional metadata"); demo ("Category • 5 min read", "Online Course • 12 weeks") |
| `card__image` is cropped to a widescreen shape and can be an `img` or a wrapper `div` | `_cards.scss` (`aspect-ratio: var(--ratio-widescreen)`, 16 / 9, `object-fit: cover`; comment "can be wrapper div or img element itself"); checked in the browser |
| `card__link` stretches over the whole card, so the entire card is clickable | `_cards.scss` (`&::before { position: absolute; inset: 0 }`), header comment "makes entire card clickable"; checked in the browser |
| `card--clickable` adds a hover shadow, an image zoom and an arrow | `_cards.scss` `&--clickable` |
| A card is not for long text; put longer text in the page | **Draft:** the plan author's inference from the component's purpose |
| Give every card image alt text; an image that adds nothing can have an empty `alt=""` | **Draft:** standard practice, not in the demos or the design system |
| Do not use `card--clickable` without `card__link` | **Draft:** follows from the CSS (the hover effects and arrow would appear with nothing to click) |
| The shadow and zoom appear only on hover, so the arrow and the title are what show a card is a link | `_cards.scss`: the hover rules apply on `:hover`; the arrow's `::after` is always drawn. **Draft** for the conclusion |

**Tables**

| Statement | Source |
| --- | --- |
| Plain table elements are already styled by the theme; the striped example uses the `table` class with `table-striped` | Demo Tables section (plain `<table>` blocks; `class="table table-striped"`) |
| `table-striped` gives alternate rows a quiet grey tint | Tables design note, "Decisions"; `_bootstrap-components.scss` `.table-striped` (grey-10, ink text) |
| `cu-table-scroll` makes a wide table scroll inside its wrapper | Tables design note, "What changed"; `_base-elements.scss` `.cu-table-scroll` (`overflow-x: auto`); checked in the browser |
| The wrapper needs `tabindex="0"`, `role="region"` and an `aria-label` naming the table | Tables design note; demo "Wide Tables" description |
| A wide table does not scroll by itself and stretches the whole page | Tables design note, "Problem" (measured: a 14-column table made the page 3,211px wide); demo accessibility note |
| Nothing checks the wrapper's `tabindex`, `role` and `aria-label` | Tables design note, "Deferred, explicitly" |
| The theme has not reviewed `table-bordered`, `table-hover` or `table-condensed` | Tables design note, "Deferred, explicitly" |
| Captions give screen reader users context; use `thead`, `tbody` and `th` | Demo accessibility note |
| The wrapper shows the theme's focus ring when focused by keyboard | `_base-elements.scss` `.cu-table-scroll:focus-visible` |
| Striped rows are 16.7:1 with ink; captions are grey on white at 5.7:1 (measured September 2026) | Tables design note (16.73:1, 5.74:1) |
| Use a table for values that line up in rows and columns | **Draft:** summarises the demo examples (enrolment figures, a timetable, a comparison) |
| Do not use a table to lay out a page | **Draft:** standard practice, not in the repo |

## Findings outside this plan

Found while reading the sources. Not fixed here; they need Nan's decision.

- **Clickable cards break the design system's flat rule.** `.card--clickable:hover` draws `--shadow-lg`, and the design system keeps large shadows for overlays only. The image also zooms 1.05 on hover and the card uses `transition: all`. The cards design note records these as "Left as it was" on 21 September 2026.
- **Cards keep a 3px corner** (`--radius-md`), where the design system makes structural panels square. Same note.
- **The hover effects need a pointer.** The shadow and the image zoom do nothing on a touch screen or for a keyboard user.
- **Open question, not measured:** whether the stretched card link covers other links placed inside a clickable card.
- **`card__image` on a wrapper div is not cropped to fit.** `_cards.scss` says the image container "can be wrapper div or img element itself", but the rules that would size an `img` inside a wrapper are commented out. A small image stays its own size and leaves an empty strip, and a large one is cut off at the bottom only. Found in the final review. The Cards record now tells authors to put `card__image` on the `img` element.

## Changes after review (9 October 2026)

Made at Nan's request after the final review. The text above is left as it was written.

- **Card examples use placeholder photos, not an inline grey box.** This replaces the constraint
  "Examples must load nothing from outside the page" for card images: the two examples now use
  `https://picsum.photos/id/1015/600/400` and `https://picsum.photos/id/1018/600/400`. Nan suggested
  `unsplash.it/600/400`; that address now redirects to Lorem Picsum and picks a random photo each
  time, so the examples use Picsum directly with fixed ids. The cost: a reader's browser contacts
  Picsum to show the photos. The build test changed from "images are data URIs" to "images are
  Picsum placeholders with alt text".
- **Image zoom removed** from `.card--clickable:hover`. Shadow and arrow movement stay. This resolves
  the first "Findings outside this plan" item in part (the shadow stays, by decision) and removes
  the zoom from the hover-effects finding. The Cards page no longer mentions a zoom.
- **3px corner kept**, by decision. This closes the second finding. A theme check now pins it.

## File structure

| Path (under `theme-src/cardiffuniversity/` unless shown) | Responsibility |
| --- | --- |
| `guide/content/components/card.md` (create) | The Cards record |
| `guide/content/components/table.md` (create) | The Tables record |
| `tests/test_guide_content.py`, `tests/check_guide.py` (modify) | Class coverage, no external loads, and the browser proofs |
| `docs/design-notes/2026-10-06-author-guide.md`, `MIGRATION.md` (modify) | Keep the docs true |

---

### Task 1: The Cards record

**Files:**
- Create: `guide/content/components/card.md`
- Modify: `tests/test_guide_content.py`, `tests/check_guide.py`

**Interfaces:**
- Consumes: the record format; `theme_css.author_facing_classes()`; `BuiltComponentPagesTest` from batch 1 (`page()`, `shown()`).
- Produces: `components/card.html` in the built site, listing all 8 author-facing `card*` classes.

- [ ] **Step 1: Confirm the branch**

Run: `git branch --show-current`
Expected: `feat/author-guide-phase-2b-batch-2`

- [ ] **Step 2: Write the failing tests**

**Edit `tests/test_guide_content.py`:** replace

```python
    def test_components_index_lists_the_buttons(self):
```

with

```python
    def test_card_page_documents_every_card_class(self):
        expected = {c for c in theme_css.author_facing_classes() if c.startswith("card")}
        self.assertLessEqual({"card", "card--clickable", "card__image", "card__link"}, expected)  # not an empty set
        self.assertEqual(expected - self.shown("card"), set())

    def test_card_examples_load_nothing_from_outside(self):
        images = [i for frame in self.page("card").find_all(cls="g-preview") for i in frame.find_all("img")]
        self.assertGreaterEqual(len(images), 2)
        for image in images:
            self.assertTrue(image.attrs.get("src", "").startswith("data:"), image.attrs.get("src"))
            self.assertIn("alt", image.attrs)

    def test_components_index_lists_the_buttons(self):
```

**Edit `tests/check_guide.py`:** replace

```python
    ("components/callout.html", 1280, "the Cardiff logo loads",
```

with

```python
    ("components/card.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/card.html", 1280, "the whole clickable card is one link",
     "(function () { var card = document.querySelector('.g-preview .card--clickable'); card.scrollIntoView();"
     " var r = card.getBoundingClientRect(), hit = document.elementFromPoint(r.left + 30, r.bottom - 30);"
     " return !!hit && hit.closest('a') === card.querySelector('.card__link'); })()"),
    ("components/card.html", 1280, "the card image is cropped to a widescreen shape",
     "(function () { var i = document.querySelector('.g-preview .card__image').getBoundingClientRect();"
     " return Math.abs(i.width / i.height - 16 / 9) < 0.05; })()"),
    ("components/callout.html", 1280, "the Cardiff logo loads",
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"; python3 tests/check_guide.py 2>&1 | tail -2 | cut -c1-160`
Expected: `ERROR: test_card_page_documents_every_card_class` and `ERROR: test_card_examples_load_nothing_from_outside` (`FileNotFoundError` for `components/card.html`), and the browser check stops with a `FileNotFoundError` for `components/card.html`.

- [ ] **Step 4: Write the Cards record**

`guide/content/components/card.md`:

````markdown
+++
name = "card"
title = "Cards"
lead = "A card groups a heading, a short description and an optional image into one block."
group = "layout"
status = "current"
related = []
scss = ["scss/components/_cards.scss"]

[parts]
card = "The container: a white block with a thin border."
card__content = "Wraps the text and adds the padding."
card__heading = "The card title. It is smaller than a page heading."
card__metadata = "An optional line for a category, a length or similar."
card__description = "The card's short text."
card__link = "A link in the heading that stretches over the whole card, so the entire card is clickable."

[[examples]]
label = "Basic card"
purpose = "A heading and a short description"
html = '''
<div class="card">
  <div class="card__content">
    <h3 class="card__heading">Card title</h3>
    <p class="card__description">A short description of what the card is about.</p>
  </div>
</div>
'''

[[examples]]
class = "card__image"
label = "With an image"
purpose = "An image at the top, cropped to a widescreen shape. It can be an img element or a wrapper div"
html = '''
<div class="card">
  <img class="card__image" alt="A short description of the image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'%3E%3Crect width='16' height='9' fill='%23ccc'/%3E%3C/svg%3E">
  <div class="card__content">
    <h3 class="card__heading">Card with an image</h3>
    <p class="card__metadata">Category &bull; 5 min read</p>
    <p class="card__description">A card can also have a line of metadata above its description.</p>
  </div>
</div>
'''

[[examples]]
class = "card--clickable"
label = "Clickable"
purpose = "A card that is one link: the whole card is clickable, an arrow sits at the bottom right, and on hover it gets a shadow and its image zooms"
html = '''
<div class="card card--clickable">
  <img class="card__image" alt="A short description of the image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'%3E%3Crect width='16' height='9' fill='%23ccc'/%3E%3C/svg%3E">
  <div class="card__content">
    <h3 class="card__heading"><a href="https://example.org" class="card__link">Clickable card</a></h3>
    <p class="card__metadata">Online course &bull; 12 weeks</p>
    <p class="card__description">Select anywhere on the card to follow the link.</p>
  </div>
</div>
'''
+++

## When to use it

Use a card to group a heading, a short description and, if you have one, an image into a block the reader can scan. A clickable card turns the whole block into one link.

## When not to use it

A card is not for long text. It holds a heading, a short description and an optional image. Put longer text in the page itself.

## How to use it

Put the heading and the description inside `card__content`. Add `card__image` for a picture: it is cropped to a widescreen shape. For a card that is one link, add `card--clickable` and put the link in the heading with `card__link`. The link stretches over the whole card, so the whole card is clickable.

### Do

- Use a heading for the card title, and put the description under it.
- Give every card image alt text that describes it.
- Put the link in the heading when the whole card is one link.
- Replace the placeholder image in an example with your own.

### Don't

- Put long paragraphs in a card.
- Add `card--clickable` without a `card__link`. The hover effects and the arrow appear, but there is nothing to select.

## Accessibility

- In a clickable card the title is a real link inside a heading, so keyboard and screen reader users reach it as a link.
- Give each image alt text. An image that adds nothing can have an empty `alt=""`.
- The shadow and the image zoom appear only on hover, so they cannot be what tells the reader a card is a link. The arrow and the title do that.
````

- [ ] **Step 5: Run everything**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3 && python3 tests/check_guide.py 2>&1 | grep -E "FAIL|got|passed" && ./build.sh guide 2>&1 | tail -3 | cut -c1-120 && git diff --check && echo whitespace-ok`
Expected: `OK`; `44 passed, 0 failed` (the 41 existing browser checks plus 3 new); the coverage warning count falls from 66 to 58; `Built .../site (13 pages, ...)`; `whitespace-ok`.

- [ ] **Step 6: Look at the page**

Run: `open site/components/card.html`. Check that each card sits in its own frame, the image cards show a grey widescreen block, and the clickable card shows its arrow at the bottom right. Hover over the clickable card to see the shadow.

- [ ] **Step 7: Commit**

```bash
git add guide/content/components/card.md tests/test_guide_content.py tests/check_guide.py
git commit -m "feat(cardiffuniversity): add the Cards component to the author guide"
```

---

### Task 2: The Tables record

**Files:**
- Create: `guide/content/components/table.md`
- Modify: `tests/test_guide_content.py`, `tests/check_guide.py`

**Interfaces:**
- Consumes: the Cards work from Task 1 (`BuiltComponentPagesTest`).
- Produces: `components/table.html` in the built site; the Components index lists Cards and Tables.

- [ ] **Step 1: Write the failing tests**

**Edit `tests/test_guide_content.py`:** replace

```python
    def test_components_index_lists_the_buttons(self):
```

with

```python
    def test_table_page_documents_the_table_classes(self):
        # author_facing_classes() holds only cu-table-scroll here: Bootstrap defines table and table-striped.
        expected = {"table", "table-striped", "cu-table-scroll"}
        self.assertEqual(expected - self.shown("table"), set())

    def test_components_index_lists_cards_and_tables(self):
        index = parse((self.out / "components" / "index.html").read_text(encoding="utf-8"))
        hrefs = [a.attrs["href"] for card in index.find_all(cls="g-card") for a in card.find_all("a")]
        self.assertIn("card.html", hrefs)
        self.assertIn("table.html", hrefs)

    def test_components_index_lists_the_buttons(self):
```

**Edit `tests/check_guide.py`:** replace

```python
    ("components/callout.html", 1280, "the Cardiff logo loads",
```

with

```python
    ("components/table.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("components/table.html", 1280, "the wide table scrolls inside its wrapper, not the page",
     "(function () { var w = document.querySelector('.g-preview .cu-table-scroll');"
     " return w.scrollWidth > w.clientWidth && document.documentElement.scrollWidth <= window.innerWidth; })()"),
    ("components/table.html", 1280, "the wrapper can take keyboard focus",
     "(function () { var w = document.querySelector('.g-preview .cu-table-scroll'); w.focus();"
     " return document.activeElement === w; })()"),
    ("components/table.html", 1280, "striped rows differ from plain rows",
     "(function () { var rows = document.querySelectorAll('.g-preview .table-striped tbody tr');"
     " return rows.length >= 2 && getComputedStyle(rows[0].cells[0]).backgroundColor"
     " !== getComputedStyle(rows[1].cells[0]).backgroundColor; })()"),
    ("components/callout.html", 1280, "the Cardiff logo loads",
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"; python3 tests/check_guide.py 2>&1 | tail -2 | cut -c1-160`
Expected: `ERROR: test_table_page_documents_the_table_classes` (`FileNotFoundError` for `components/table.html`), `FAIL: test_components_index_lists_cards_and_tables`, and the browser check stops with a `FileNotFoundError` for `components/table.html`.

- [ ] **Step 3: Write the Tables record**

`guide/content/components/table.md`:

````markdown
+++
name = "table"
title = "Tables"
lead = "A table shows values in rows and columns, with a header row that says what each column holds."
group = "content"
status = "current"
related = []
scss = ["scss/_base-elements.scss", "scss/_bootstrap-components.scss"]

[parts]
table = "Bootstrap's table class. Plain table elements are already styled by the theme; the striped example uses this class with table-striped."

[[examples]]
label = "Standard table"
purpose = "A table with a caption, a header row and a body"
html = '''
<table>
  <caption>Student enrolment by programme, 2024/25</caption>
  <thead>
    <tr>
      <th>Programme</th>
      <th>Year&nbsp;1</th>
      <th>Year&nbsp;2</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Computer Science</td>
      <td>1,234</td>
      <td>456</td>
      <td>1,690</td>
    </tr>
    <tr>
      <td>Engineering</td>
      <td>2,105</td>
      <td>678</td>
      <td>2,783</td>
    </tr>
    <tr>
      <td>Business</td>
      <td>1,876</td>
      <td>892</td>
      <td>2,768</td>
    </tr>
  </tbody>
</table>
'''

[[examples]]
class = "table-striped"
label = "Striped rows"
purpose = "A quiet grey tint on alternate rows"
html = '''
<table class="table table-striped">
  <caption>Assessment weightings</caption>
  <thead>
    <tr>
      <th>Assessment</th>
      <th>Weighting</th>
      <th>Format</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Essay</td>
      <td>40%</td>
      <td>2,500 words</td>
    </tr>
    <tr>
      <td>Presentation</td>
      <td>20%</td>
      <td>10 minutes</td>
    </tr>
    <tr>
      <td>Exam</td>
      <td>40%</td>
      <td>Two hours</td>
    </tr>
  </tbody>
</table>
'''

[[examples]]
class = "cu-table-scroll"
label = "Wide table"
purpose = "A wrapper that makes a table wider than the page scroll inside itself, so the page does not stretch"
html = '''
<div class="cu-table-scroll" tabindex="0" role="region" aria-label="Module results by week">
  <table>
    <caption>Module results by week</caption>
    <thead>
      <tr>
        <th>Module</th>
        <th>Week&nbsp;1</th>
        <th>Week&nbsp;2</th>
        <th>Week&nbsp;3</th>
        <th>Week&nbsp;4</th>
        <th>Week&nbsp;5</th>
        <th>Week&nbsp;6</th>
        <th>Week&nbsp;7</th>
        <th>Week&nbsp;8</th>
        <th>Week&nbsp;9</th>
        <th>Week&nbsp;10</th>
        <th>Week&nbsp;11</th>
        <th>Week&nbsp;12</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Assessment design</td>
        <td>72</td>
        <td>68</td>
        <td>75</td>
        <td>81</td>
        <td>79</td>
        <td>64</td>
        <td>70</td>
        <td>77</td>
        <td>83</td>
        <td>85</td>
        <td>80</td>
        <td>88</td>
      </tr>
    </tbody>
  </table>
</div>
'''
+++

## When to use it

Use a table for values that line up in rows and columns, such as dates, scores or a comparison between options.

## When not to use it

Do not use a table to lay out a page. A table is for data.

## How to use it

Give the table a caption that names it, a `thead` with `th` header cells, and a `tbody`. If the table may be wider than the page, wrap it in `.cu-table-scroll`, and give the wrapper `tabindex="0"`, `role="region"` and an `aria-label` that names the table.

### Do

- Use a caption, a `thead` with `th` header cells, and a `tbody`.
- Wrap a table that may be wide in `.cu-table-scroll`, with `tabindex="0"`, `role="region"` and an `aria-label` that names the table.
- Add `table-striped` for a quiet grey tint on alternate rows.

### Don't

- Leave a wide table unwrapped. It does not scroll by itself and stretches the whole page.
- Leave out the wrapper's `tabindex`, `role` or `aria-label`. Nothing checks them, and without `tabindex="0"` a keyboard user may not be able to scroll the table.
- Use `table-bordered`, `table-hover` or `table-condensed` without checking them in the player first. The theme has not reviewed them.

## Accessibility

- A caption gives screen reader users the context of the table, and header cells in a `thead` say what each column holds.
- The wrapper takes keyboard focus with `tabindex="0"` and shows the theme's focus ring, so a keyboard user can scroll a wide table.
- Striped rows are a grey tint with ink text, which measured 16.7:1 in September 2026. A caption is grey on white, which measured 5.7:1.
````

- [ ] **Step 4: Update the spec and the migration status**

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
     Batch 1: buttons and alerts.
````

with

````markdown
     Batch 1: buttons and alerts. Batch 2: cards and tables.
````

**Edit `MIGRATION.md`:** replace

````markdown
components, in small batches (batch 1: buttons and alerts), and phase 2c more task pages.
````

with

````markdown
components, in small batches (batch 1: buttons and alerts; batch 2: cards and tables), and
phase 2c more task pages.
````

- [ ] **Step 5: Run everything**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3 && python3 tests/check_guide.py 2>&1 | grep -E "FAIL|got|passed" && ./build.sh guide 2>&1 | tail -3 | cut -c1-120 && git diff --check && echo whitespace-ok`
Expected: `OK`; `48 passed, 0 failed` (the 44 from Task 1 plus 4 new); the coverage warning count falls to 57 (`cu-table-scroll` is the one new class); `Built .../site (14 pages, ...)`; `whitespace-ok`.

- [ ] **Step 6: Look at the page**

Run: `open site/components/table.html`. Check that the wide table scrolls sideways inside its own frame and the page does not, that the striped table shows grey on alternate rows, and that you can Tab to the wide table and scroll it with the arrow keys.

- [ ] **Step 7: Commit**

```bash
git add guide/content/components/table.md tests/test_guide_content.py tests/check_guide.py docs/design-notes/2026-10-06-author-guide.md MIGRATION.md
git commit -m "feat(cardiffuniversity): add the Tables component to the author guide"
```

---

## Self-review

**Spec coverage.**

| Requirement | Task |
| --- | --- |
| Cards component record, every `card*` class documented | 1 |
| Tables component record, the table classes documented | 2 |
| Card examples load nothing from outside the page | 1 |
| Claims proved against the real theme (clickable card, widescreen image, wide table, wrapper focus, striped rows) | 1, 2 |
| Each claim in a record is backed by a source or flagged | "Sources and open claims" above |
| Docs stay true | 2 |

Not in batch 2, by design: Images, Layout and Typography (batch 3), task pages (2c), editor evidence (needs a Docker Xerte test), and any theme fix for the card findings.

**Manual checks after Task 2 (Nan):** read the "Sources and open claims" table and strike or reword any **Draft** line you disagree with (the "not for long text" line for Cards, "do not add `card--clickable` without a `card__link`", the table "use" and "layout" lines, and the alt-text advice); look at both pages at phone width; decide whether to run a Docker Xerte test so these records can gain an `[editor]` table.
