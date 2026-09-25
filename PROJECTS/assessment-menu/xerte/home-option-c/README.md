# Home page: option C (Pathways), converted for Xerte

Source: `prototypes/2026-09-16_assessment-menu-landing-options-v2.html#option-C`, keeping the
prototype's own design. The structure follows `2026-09-16_xerte-home-option-c/`: one fragment per
Xerte element, the page CSS in a Home-page HTML element, the type search in the project Script field.

The design is the prototype's, not a reassembly out of theme components: rounded path cards, circular
step numbers, circular ringed question numbers, the dark briefs panel, the grey alongside panel. What
changed is where the values come from — colour, spacing, type, shadow and focus all resolve through
the `cardiffuniversity` theme's custom properties, so the page follows the theme if it changes.
Base text, spacing and alignment use its utility classes in the fragments; custom CSS keeps the
rounded path cards, ringed questions, dark briefs panel and alongside panel.

## Where each file goes in Xerte

| File | Goes in |
| --- | --- |
| `styles.css` | an HTML element on this page, inside `<style>` tags — **not** Project > Styles |
| `script.js` | Project > Optional properties > Script |
| `sN-*.html` | one Xerte element each, in the section shown below (Source view) |

## Page settings

| Setting | Value |
| --- | --- |
| Page ID / Page Link | `home` / `Home` |
| Page Title | Assessment Menu |
| Page Subtitle | Designing meaningful, inclusive and future-focused assessment |
| Section menu | Hide Menu + Expand Main Contents |

## Sections

| Section ID | Section Title | Fragments |
| --- | --- | --- |
| `intro` | leave empty (untick Show Title) | `s1-intro.html` |
| `start` | Where would you like to start? | `s2-paths.html`, `s2-policy.html` |
| `questions` | Six questions to design with | `s3-questions.html` |
| `in-brief` | What shapes the menu | `s4-briefs.html` |
| `alongside` | Use this menu alongside | `s5-alongside.html` |

Links to a section use `#home|section-id`. The category chips and "Browse all types" point at
`#exams`, `#class-tests`, `#portfolios`, `#multimedia`, `#oral`, `#practical`, `#written` and
`#browse`, so they start working as soon as those pages exist with those Page IDs. `script.js` holds
the same IDs, plus a section ID per assessment type, in its `AM_TYPES` table.

## Token mapping

Every hardcoded value in the earlier version now resolves through the theme. The exact matches:
`#C21F16` → `--color-action`, `#E4251B` → `--color-brand-primary`, `#121212` → `--color-text-primary`,
`#666666` → `--color-text-secondary`, `#CCCCCC` → `--color-border-default`, `#e5e5e5` →
`--color-border-light`, `#F2F2F2` → `--color-bg-subtle`, `#333` → `--color-gray-90`. Spacing moved to
the `--spacing-*` scale, type to `--font-size-*` / `--font-weight-*` / `--line-height-*`, the card and
dropdown shadows to `--shadow-lg` / `--shadow-dropdown`, and the on-dark focus ring to
`--focus-ring-*`.

Three deliberate differences from the earlier version:

1. **Small text moved up to 16px.** The design system sets 16px as the floor for labels and captions,
   so the hints, chips and result categories (previously 15.2px / 14.4px) now use `--font-size-base`.
2. **The search box is `--min-input-height` (56px), not 48px**, so it matches every other input in
   the theme.
3. **Rounded panels are kept as a recorded deviation.** The design system keeps structural panels
   square (`--radius-card: 0`). This page's 16px cards, 12px alongside panel and 6px search box are
   declared as `--am-radius-*` at the top of `styles.css` and commented as such; pill chips and the
   circular numbers use the theme's own `--radius-full`.

The two on-dark lane accents have no design-system equivalent, so they are mixed from the DS accents
(`color-mix` of `--cu-accent-light-blue` and `--cu-accent-forest-green` with white) rather than picked
by hand, which keeps Lane 1 blue / Lane 2 green consistent with the callout colours used elsewhere.

## Two things styles.css fixes in the base template

Both are scoped so the category pages are unaffected:

1. **Full-width bands.** The base template gives every section a boxed panel (10px radius, 20px side
   padding). The prototype has full-width alternating bands, so the five Home sections opt out and
   paint their background through a pseudo-element spanning the viewport. Delete that block to go back
   to Xerte's panels.
2. **`.row-fluid .span9.expandMain { margin-left: 0 }`.** The base template's `.row-fluid .span9`
   margin (2.564%) is more specific than the player's own `.expandMain { margin-left: 0 }`, so main
   content sits 30px right of centre and the bands inherit the offset. Matching the base selector's
   specificity is what makes the reset stick, and it only applies to pages set to Expand Main Contents.

The bands no longer use `width: 100vw`, which included the scrollbar and made the page scroll
sideways. Each band is the section's own box spread outwards with `box-shadow: 0 0 0 100vmax
var(--am-band)` and trimmed vertically with `clip-path: inset(0 -100vmax)`. A box-shadow adds no
scrollable overflow, and the clip-path sits on the pseudo-element rather than the section, so the
search dropdown can still extend past the band without being clipped — measured at 0px of sideways
scroll with the dropdown 73px past the section edge.

Because `styles.css` now styles `section` itself, it must stay in a `<style>` block on this page
rather than Project > Styles: the player keeps only the current page's sections in the DOM, so
page-level CSS is scoped to this page, while Project > Styles would restyle every page in the project.

**Section IDs must be unique across the whole project.** Option A already uses `intro`, `questions`
and `alongside`, so prefix this page's (`c-intro`, `c-start`, …) before setting them, or deep links
will resolve to whichever section the player finds first. Nothing in this stylesheet depends on the
IDs any more — the bands alternate by position — so the IDs are only needed for linking.

## Also changed from the reference folder

- `class="sr-only"` on the search label became `class="visually-hidden"`. Bootstrap 2.3 has no
  `.sr-only`, so the label would have been visible; `.visually-hidden` is the theme's own utility.
- The chips and search results opt out of the base template's "underline every link in a section"
  rule, since both are bordered controls rather than prose links. Prose links stay underlined.

## Preview

`python3 build-preview.py` stitches the fragments into `local-preview.html` inside the real page frame
(theme CSS, bootstrap, Font Awesome, jQuery), linking `styles.css` and `script.js` rather than inlining
them, so the preview cannot drift from what you paste into Xerte.

## Still to confirm in real Xerte

- The section IDs above must match the Section IDs set in Xerte, or the full-width bands and the
  `#home|...` links won't resolve.
- Whether the player leaves enough room below the search card for the results dropdown on a narrow
  screen.
