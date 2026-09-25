# Assessment Menu: Xerte conversions

Landing page designs from `prototypes/2026-09-16_assessment-menu-landing-options-v2.html`, converted
for Xerte. Which one becomes the real Home page is still open, so each is kept separately.

| Folder | What it is |
| --- | --- |
| `home-option-c/` | Option C, "Pathways" |
| `home-option-a/` | Option A, "Bold hero" |
| `home-combined/` | The combined landing (2026-09-17 landing-combined-v1) — a search-first workbench |

All three use one fragment per Xerte element and JavaScript for page behaviour. The combined page's
CSS goes in Project > Styles; Options A and C put their section-level CSS in a Home-page `<style>`
block. They differ in emphasis, which is the useful part to compare (see below).

Each folder has its own README with the page settings, section table and decisions.

## Two ways of converting a design, and when each fits

**Components first** (`home-combined/`). Build the page out of the theme's own components and
utilities — `.button`, `.cu-callout`, `.cu-rule`, `.badge`, `.link-action`, `.link-external`,
`.flex`/`.flex-NNN` — and write custom CSS only where the theme has no component. This works when the
design is already close to the theme's grain, as the combined landing is; its `styles.css` is down to
the finder's workbench layout, the studio's step list and a couple of field sizes.

**Design first** (`home-option-a/`, `home-option-c/`). Keep the prototype's distinctive components,
using `cardiffuniversity` utilities for base text, spacing and alignment. Their custom CSS uses theme
tokens for the rounded path cards, ringed question numbers, dark hero and lane bars. The recorded
panel radii and a few design-specific dimensions remain local to each option.

The first attempt at options A and C used the components-first approach and lost their designs, which
is what the split above is for. Both option READMEs record the same three deliberate departures from
their prototypes: small text raised to the design system's 16px floor, search boxes at the theme's
input height, and rounded panels kept as a recorded deviation from the design system's square panels.

## Shared conventions

- The Page Title ("Assessment Menu") and Page Subtitle are Xerte's own fields; the prototype's logo,
  top nav, "Cymraeg" button, skip link and footer are dropped, since the theme's header, section menu
  and footer already provide them.
- Draft-only prototype furniture (the review bar, the coverage table, `<span class="flag">` labels) is
  not carried over.
- Links to pages that don't exist yet still use their real Xerte form (`#home|questions`, `#exams`,
  `#browse`), so they start working as soon as those pages are created with matching IDs.
- Each folder has a `build-preview.py` that assembles a `local-preview.html` against the real theme
  CSS, for checking before pasting into Xerte.

## Project script

`project.js` (built from `src/*.js` by `build-project.py`) holds the language link that puts a
Welsh/English toggle in the header. It is separate from a page's own script; `home-option-c/script.js`
is the Home page's type search.
