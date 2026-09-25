# Home page: combined landing, converted for Xerte

Source: `prototypes/codex/2026-09-17_assessment-menu-landing-combined-v1.html`, converted one section
at a time. English only for now. Welsh will be a separate Xerte project, linked from a language link
in the header.

This page is built from the theme's own components and utilities wherever one exists — `.button`,
`.cu-callout`, `.cu-rule`, `.badge`, `.link-action`, `.link-external`, `.flex`/`.flex-NNN`, `.text-*`,
`.font-*` — with `styles.css` holding only the few patterns the theme has no component for. That is
the opposite emphasis from `../home-option-a/` and `../home-option-c/`, which keep their prototypes'
own CSS; this design is close enough to the theme's grain that components carry most of it.

Each `NN-name.html` is one fragment to paste into Xerte. `python3 build-preview.py` stitches them into
`local-preview.html` (real `cardiffuni-v3` CSS, the player's section markup, `styles.css`,
`../project.js`) so they can be checked before pasting. `python3 ../build-project.py` builds
`../project.js` from `../src/*.js`.

## Where each file goes in Xerte

| File | Goes in |
| --- | --- |
| `styles.css` | Project > Optional properties > Styles |
| `../project.js` | Project > Optional properties > Script (adds the language link to the header) |
| `NN-*.html` | one Xerte element each, in the section shown below |

The finder's and studio's own JavaScript sits inside their fragments, so each interactive section is
self-contained and only loads where it is used. `project.js` stays for project-wide behaviour.

## Home page settings

| Setting | Value |
| --- | --- |
| Page ID / Page Link | `home` / `Home` |
| Page Title | Assessment Menu |
| Page Subtitle | Find an assessment type. Ask the right questions. |
| Section menu | Hide Menu + Expand Main Contents |

The prototype's h1 became the Page Subtitle (the key phrase); its lead sentence is the first paragraph
of section 1.

## Sections

| # | Fragment | Xerte element | Section ID | Section Title | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | `01-intro.html` | Text (Source view) | `intro` | leave empty | Converted |
| 2 | `02-finder.html` | HTML Code | `finder` | Find an assessment type | Converted |
| 3 | `03-questions.html` | HTML Code | `questions` | Six questions for the conversation | Converted |
| 4 | `04-lanes.html` | Text (Source view) | `lanes` | Let learning outcomes lead | Converted |
| 5 | `05-guidance.html` | Text (Source view) | `guidance` | Wider guidance | Converted |

For every element, untick Show Title. Links to a section use `#home|section-id`. A finder result links
to `#category-page|type-section`, e.g. `#portfolios|annotated-bibliography`, so results start working
as soon as those pages exist with matching IDs.

## What each section does

**Finder** — search, category filters, a result count, a list/grid toggle and the 17 type records,
all rendered from a table at the top of the fragment. Checked in the browser: filtering to Portfolios
gives 3 of 17, searching within a filter narrows correctly, the grid toggle switches columns, and the
no-match message appears.

**Design studio** — the six questions one at a time, with a note per question, a step list showing
which questions have notes, and a "Copy design notes" button. Notes live in the page only: moving to
another Xerte page, reloading or closing clears them, which the standfirst says plainly. Checked in
the browser: notes persist while stepping back and forth, and the first/last steps disable the right
buttons.

## Components used in place of prototype CSS

| Prototype | Here |
| --- | --- |
| `.btn` / `.btn.secondary` | `.button button-primary` / `.button button-secondary-outline` |
| `.filter` / `.view-toggle`, pressed state | `.button button-secondary-outline button-sm`, swapped for the filled `.button-secondary` when pressed |
| `.guide-card` / `.guide-card.lane2` | `.cu-callout cu-callout-info` / `.cu-callout cu-callout-good` |
| `.d1`'s 2px rule | `<hr class="cu-rule cu-rule-strong">` |
| `.badge` (draft label) | `.badge` plus `.am-draft`, which only supplies the design system's `--color-draft` / `--color-draft-bg` pair |
| Type record's "View" link | `.link-action` |
| External resource links (`↗`) | `.link-external` |
| Two-column blocks | `.flex .flex-wrap .gap-xl` with `.flex-300` |

The pressed state swaps the button class rather than recolouring it: `.button-secondary-outline` sets
its text colour with `!important`, so an override rendered black on black. Swapping to the theme's
filled button needs no custom CSS at all.

`styles.css` is therefore limited to the finder's two-column workbench and result rows, the studio's
step list and stage, the search and note field sizing, and the draft label's colour pair.

## Dropped from the prototype

Own `:root` tokens, `.btn`, `.wrap` and masthead (the theme provides them), the skip link (Xerte has
its own), the `<noscript>` list (Xerte needs JavaScript), the Cymraeg toggle button (now the header
link), and the `data-en` / `data-cy` attributes. The small eyebrow labels above each heading ("Start
here", "Design studio", "Two-lane approach", "Use alongside") are also dropped: Xerte renders the
Section Title above anything an element can add, so there is nowhere to put them. The already-converted
`01-intro.html` had set that precedent with the hero's own eyebrow.

**One link was removed rather than converted.** The prototype's "Assessment Design Guide · prototype"
resource pointed at a `file:///Users/...` path inside a personal Obsidian vault, which would break for
everyone else and leaks a local path into a published page. It is now "Assessment Design Guide (link
to follow)" — swap in the real URL when there is one.

## Theme changes needed (not made; the theme repo has work in progress)

1. **Language toggle** (`scss/components/_language.scss`). It is white text for the old dark banner, so it is invisible on
   the white header (checked). The version below matches the prototype's `.lang` button and was tested in the preview
   with the link at 1280px and 390px. Replace the `#language-toggle` rules with:

   ```scss
   #language-toggle {
       position: absolute;
       top: var(--cu-space-6);
       right: var(--cu-space-6);
       display: inline-flex;
       align-items: center;
       justify-content: center;
       gap: var(--cu-space-2);
       min-width: 44px;              // icon-only below 980px, still a 44px target
       min-height: 44px;
       padding: var(--cu-space-2) var(--cu-space-3);
       border: 1px solid var(--cu-ink);
       border-radius: var(--radius-control);
       background: var(--cu-white);
       color: var(--cu-ink);
       font-size: var(--font-size-base);
       font-weight: 700;
       line-height: 1.2;
       text-decoration: none;

       &:hover,
       &:focus {
           background: var(--cu-grey-10);
           color: var(--cu-ink);
           text-decoration: none;
       }

       i { margin: 0; font-size: 1.25rem; }
   }
   ```

   Keep the existing `@media (max-width: 980px)` rule that hides `.language-toggle-text`. Also fix the note in
   `demos/components.html` (line 594): the player does not place the toggle; the project script does.
   The absolute position can collide with a long Page Title on narrow phones; recheck with the header work.
2. **`.lead`** (`scss/_bootstrap-components.scss`, line 808): grey-60 `#808080` at weight 300 is about 4:1 on white
   (below 4.5:1). Use `--cu-grey-70`, weight 400, line-height 1.55 (the design system's lead).
3. **Section panels** (yours): the base template's 10px radius and 20px side padding on `.oddSection` / `.evenSection`.
4. **A pressed/toggle state for buttons.** Filter and view toggles are a common pattern and the theme
   has no `aria-pressed` styling; swapping classes works but a `.button[aria-pressed="true"]` rule
   (without `!important` fighting) would be better.

## Still to confirm in real Xerte

- A section with no heading sits directly under the navbar in the preview; check when first pasted.
- The Welsh project's URL (until then the header link stays hidden).
- Whether the studio's grey panel reads as distinct from an alternating grey section band; in the
  preview the two greys are close.
- Clipboard access for "Copy design notes" inside the player (it needs a secure context; the button
  falls back to a message asking the user to copy manually).
