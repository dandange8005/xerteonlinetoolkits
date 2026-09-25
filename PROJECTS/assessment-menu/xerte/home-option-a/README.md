# Home page: option A (Bold hero), converted for Xerte

Source: `prototypes/2026-09-16_assessment-menu-landing-options-v2.html#option-A`, keeping the
prototype's own design. Same structure as `home-option-c/`: one fragment per Xerte element, the page
CSS in a Home-page HTML element, the type search in the project Script field.

The design is the prototype's, not a reassembly out of theme components: the dark hero with its lane
diagram, the strip card straddling the bottom of the hero, the numbered question cards, the lane
tint rows, the category tiles. What changed is where the values come from — colour, spacing, type,
shadow and focus resolve through the `cardiffuniversity` theme's custom properties.
Base text, spacing and alignment use its utility classes in the fragments; the custom CSS keeps the
hero, overlapping strip, numbered cards, lane tints and category tiles.

## Where each file goes in Xerte

| File | Goes in |
| --- | --- |
| `styles.css` | an HTML element on this page, inside `<style>` tags — **not** Project > Styles |
| `script.js` | Project > Optional properties > Script (identical to option C's) |
| `sN-*.html` | one Xerte element each, in the section shown below (Source view) |

`styles.css` styles `section` itself, so it must stay page-level. The player only keeps the current
page's sections in the DOM, so a `<style>` block pasted into an element on this page applies to this
page alone. The frame overrides also check for the Option A hero. Project > Styles would still load
the option-specific `am-*` component rules on every page and could clash with another Home option.

## Page settings

| Setting | Value |
| --- | --- |
| Page ID / Page Link | `home` / `Home` |
| Page Title | Assessment Menu |
| Page Subtitle | Designing meaningful, inclusive and future-focused assessment |
| Section menu | Hide Menu + Expand Main Contents |

## Sections

| Section ID | Fragment |
| --- | --- |
| `intro` | `s1-hero.html` |
| `tool` | `s2-strip.html` |
| `questions` | `s3-questions.html` |
| `briefs` | `s4-briefs.html` |
| `categories` | `s5-categories.html` |
| `alongside` | `s6-alongside.html` |

**Only `intro` and `tool` need their Section ID set.** Every section gets a full-width band and the
white/grey alternation from the generic `section` rules, so the IDs are needed only where a section
differs from that default: `intro` is the dark hero band, and `tool` has no band of its own so its
card can float over the bottom edge of the hero. The other four fall out of `:nth-child(odd/even)` in
the right order.

In the editor the ID is the section's optional property group "Section ID" (`customLinkID` in the
data); the player uses it as the section's DOM id, falling back to its position (`page1section1`) when
blank. IDs are case-sensitive, must be unique across the project, and must not contain the words
*page*, *section* or *content*. Setting all six is still worthwhile for the in-page links, and it
makes the CSS readable — but only the two above change how the page looks.

**The player's section titles are hidden by CSS, not by a setting** — Xerte has no "hide section
title" option. This design puts a small eyebrow label above each heading ("Start here", "In brief",
"17 assessment types"), and the player renders its Section Title above anything an element can add,
so each fragment carries its own `.am-sec-head` (eyebrow, `h2`, standfirst) and `styles.css` hides
`.page-header`. Keeping the text in the HTML also keeps it translatable for the Welsh project, which
a CSS `content` eyebrow would not.

Still give every section a meaningful Section Title even though it is not shown: the section element
keeps `aria-labelledby` pointing at the hidden heading, so that text becomes the section's accessible
name for screen-reader users navigating by region.

The same block also hides the per-section "Top" link (`.topBtn`) and the paragraph the player wraps
it in, which would otherwise leave about 29px of dead space at the foot of every section.

Links to a section use `#home|section-id`. The category tiles and "browse all 17 types" point at
`#exams`, `#class-tests`, `#portfolios`, `#multimedia`, `#oral`, `#practical`, `#written` and
`#browse`, so they start working as soon as those pages exist with those Page IDs.

## Token mapping and recorded deviations

Colour, spacing, type, shadow and focus resolve through the theme. As in option C, three differences
from the prototype are deliberate:

1. **Small text moved up to 16px**, the design system's floor for labels and captions (the eyebrow,
   hints and tile counts were 14–15px).
2. **The search box is `--min-input-height` (56px)**, matching every other input in the theme.
3. **Rounded panels are kept as a recorded deviation** from `--radius-card` (square). The 12px panels
   and 6px search box are declared as `--am-radius-*` at the top of `styles.css`.

The lane tints and their label colours have no design-system equivalent, so they are mixed from
`--cu-accent-light-blue` and `--cu-accent-forest-green` with `color-mix` — the labels darkened enough
to clear 4.5:1 on their own tint — rather than picked by hand. The hero's lane diagram is the
prototype's inline SVG with those same custom properties in place of its hardcoded hex.

The category tiles use Font Awesome icons (already loaded by the Xerte player, and used elsewhere in
the theme) rather than the prototype's bespoke inline SVG line-icons. Their type counts are written
into the HTML rather than computed, so the section needs no script.

## What the "NO TOC Page Template" block does

The top of `styles.css` is the house homepage template, unchanged: it hides the section menu, drops
the `.row-fluid .span9` left margin so main content is centred, removes the navbar's bottom margin,
and replaces the base template's boxed section panels with full-width bands — each section painting
its background through a pseudo-element that spans the viewport, alternating white and grey by
position. Underneath it sit the two exceptions by ID (`#intro` dark, `#tool` bandless), then the
page's own components.

Two rules were added to it for this page, both explained in the file: hiding `section > .page-header`
(Xerte has no "hide section title" setting) and the paragraph holding the per-section "Top" link.

The bands no longer use `width: 100vw`. `100vw` includes the scrollbar, which made the page scroll
sideways by about 8px. Each band is now the section's own box spread outwards with
`box-shadow: 0 0 0 100vmax var(--am-band)` and trimmed vertically with `clip-path: inset(0 -100vmax)`.
A box-shadow adds no scrollable overflow, so the sideways scroll is gone, and because the clip-path
sits on the pseudo-element rather than the section, nothing inside the section is clipped — the
search results still drop below the band. Each section sets one colour, in `--am-band`.

## One name to keep clear

`script.js` writes each result's category as `<span class="am-cat">`, so `.am-cat` belongs to the
search results. The category tiles are `.am-tile` / `.am-tiles` for that reason — naming them
`.am-cat` made the tile border and padding leak into the dropdown.

## Preview

`python3 build-preview.py` stitches the fragments into `local-preview.html` inside the real page frame
(theme CSS, bootstrap, Font Awesome, jQuery), linking `styles.css` and `script.js` rather than
inlining them.

## Checked on a real page

Built in Xerte and checked in the player: the six bands paint, the strip card straddles the bottom of
the dark hero (it needs its own `tool` section next to `intro` for that), the type-ahead search runs
from inside its HTML element, and the category tiles link out correctly.

Two fixes came out of that check and are already in `styles.css`:

1. **Visited links on dark.** The theme sets visited colours with `a:where(…):visited`, which outranks
   a single class, so once a category page had been visited the "Browse all types" tile reverted to
   link blue on black. The tile rules now name `:link` and `:visited` to match that specificity.
   Worth remembering for any link placed on a dark band.
2. **Section furniture.** The hidden `.page-header` and `.topBtn` rules described above.
3. **Sideways scroll.** Fixed by the box-shadow bands described above. An earlier note here suggested
   `html { overflow-x: clip; }`; that was wrong — measured on the live page, the property computes to
   `clip` and the page still scrolls 7.5px, because the overflow propagates to the viewport.

## Watch out for

**Section IDs must be unique across the whole project, not just the page.** This project has Option A,
B and C as pages, and options A and C both want `intro`, `questions` and `alongside`. Option A's are
set; C and B are still on the player's positional fallback. Before giving Option C its IDs, prefix
them per page (`a-intro` / `c-intro`, and so on) and update the two ID rules in each stylesheet to
match, or deep links will resolve to whichever section the player finds first.
