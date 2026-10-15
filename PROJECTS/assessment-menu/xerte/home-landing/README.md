# Home page: landing, from the Hannah and Carys layout doc

Source: `Landing Page Layout For Nan.docx` (content and layout), built on the `cardiffuniversity`
theme stylesheet. The doc's comments pick the look of each section from the existing options:

| Doc section | Fragment | Look |
| --- | --- | --- |
| A design tool, not a list of recommendations | `01-intro.html` | Option B: big type, white background, B's menu illustration (classes renamed `lp-*`) |
| Six questions to inform your thinking | `02-questions.html` | Option A's heading and numbered cards |
| What else do I need to know before I get started? | `03-know.html` | Built in HTML from the doc: three "asks" cards, Lane 1 / Lane 2 cards (the category pages' `.am-lane` classes), the two-lane text |
| Browse by category (+ search) | `04-browse.html` | Option A's cards, with A's type search |
| Use this menu alongside / Further reading | `05-alongside.html` | Option A's footer, unchanged in content |

The tab row in the doc (Home, All types, Exams…) is the Xerte page menu; the player draws it.

## Where each file goes in Xerte

| File | Goes in |
| --- | --- |
| `styles.css` | an HTML element on this page, inside `<style>` tags — **not** Project > Styles |
| the category pages' `styles.css` | Project > Optional properties > Styles (already there; this page's Lane 1 / Lane 2 cards use its `.am-lanes` / `.am-lane` classes) |
| `../home-option-a/script.js` | Project > Optional properties > Script (the type search; identical to option C's) |
| `NN-*.html` | one Xerte element each, in the section shown below (Source view) |

Same reasoning as option A: `styles.css` styles `section` itself, so it stays page-level. Everything
is scoped by `body:has(.lp-intro)` and every class is `lp-` prefixed, so it cannot clash with the other
options. The search keeps the `am-search` / `am-results` class names because the shared script is bound
to them; their rules are in this `styles.css`.

## Page settings

| Setting | Value |
| --- | --- |
| Page ID / Page Link | `home` / `Home` |
| Page Title | Assessment Menu |
| Page Subtitle | Designing inclusive, authentic and future-focused assessment |
| Section menu | Hide Menu + Expand Main Contents |

## Sections

| Section ID | Section Title (hidden by CSS, still the accessible name) | Fragment |
| --- | --- | --- |
| `l-intro` | A design tool, not a list of recommendations | `01-intro.html` |
| `l-questions` | Six questions to inform your thinking | `02-questions.html` |
| `l-know` | What else do I need to know before I get started? | `03-know.html` |
| `l-browse` | Browse by category | `04-browse.html` |
| `l-alongside` | Use this menu alongside | `05-alongside.html` |

No section needs its Section ID for the look: the white/grey bands fall out of `:nth-child(odd/even)`.
The IDs are `l-` prefixed because options A and C already use `intro`, `questions` and `alongside`, and
IDs must be unique across the project.

## Content decisions

- **Toolkit links.** Four questions link to their toolkit pages (programme-level approach, authentic
  assessment, inclusive assessment and feedback, GenAI). The first was given as `http://`; it is
  `https://` here to match the others.
- **Two questions have no link yet:** "What do students need to demonstrate?" shows *Start from your
  learning outcomes (link to follow)*; "Why is this assessment the most appropriate way…" has no link
  line. Add them when the toolkit pages exist.
- **The three "asks" cards** are HTML (neutral grey with a red left edge), not the doc's
  screenshot, so they stay translatable and meet contrast.
- **Category counts** are written in (2, 3, 3, 3, 3, 1, 2 = 17), as in option A.
- **Footer.** The doc's footer was an empty two-column table headed "Use this menu alongside…" and
  "Further reading", so it carries option A's content. Two items there are still *(link to follow)*.

## Open points from the doc's comments (not decided here)

1. Carys: use the six questions from the toolkit rather than the ones from the assessment type pages?
   This page follows the doc as written (toolkit wording).
2. Carys: keep *"Please see the assessment menu types for examples of Lane 1 and 2 assessments."*?
   It is included, as in the doc.

## Preview

`python3 build-preview.py` stitches the fragments into `local-preview.html` inside the real page frame
(theme CSS, bootstrap, Font Awesome, jQuery), linking `styles.css` and option A's `script.js`. Open it
over a local server (`python3 -m http.server` from the repo root), not `file://`.

Checked in the browser at 1280px and at the narrowest the browser allows (485px): the five bands paint,
nothing scrolls sideways, the type search lists matches, tiles show their Font Awesome icons.
Not yet checked in real Xerte.

Note: `home-option-a/build-preview.py` points Font Awesome at `modules/site/…/common/fontawesome-6.6.0`,
which does not exist in this checkout, so its preview shows no tile icons. This folder's builder uses
`modules/common/fontawesome-6.6.0`. A one-line fix for option A if you want it.
