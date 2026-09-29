# Header logos and wrapped callout titles

Implemented 21 September 2026. This answers review Minor 10 and Minor 13, and the right-logo
and callout-title parts of the Phase 1 validation item in the
[follow-up checklist](../plans/2026-09-21-follow-up.md). The wide-table part of that item is in
the [tables note](2026-09-21-tables.md).

## Wrapped callout titles (Minor 13): checked, no change

The review suggested that a fixed `line-height: 28px` on `.cu-callout-title` gives loose leading
on a title that wraps. I rendered a three-line title at 500px wide in both callout markups. The
lines are evenly spaced, the disc stays on the first line, and the body text follows normally.
The title's 28px leading is within 0.8px of the 28.8px body leading (18px at 1.6), so a wrapped
title is spaced like the paragraph below it. `_callout.scss` is unchanged. Nan can overrule this;
the reviewer's alternative is to apply the 28px only to the first line with `::first-line`.

## Right-logo and two-logo headers (Minor 10): fixed

A header shows a left logo, a right logo or both, according to which images the author supplies
(`application.js` adds `logoL` and `logoR` to `#overview`). The theme's one-row layout only
targeted `#overview.logoL`. Measured in headless Chrome with a 160×60 partner logo:

| Header | Problem |
| --- | --- |
| Right logo only, 800px and narrower | Logo and title stacked with no side gutter: both at x=0, the title as wide as the window. The left-logo header keeps a 24px gutter. |
| Both logos, any width | The partner logo sat next to the Cardiff logo instead of at the right edge, the title was centred (the base's `#overview.logoL.logoR .titles` is more specific than the theme's left-align rule), and at 485px the partner logo was squeezed from 160px to 67px. |
| Left logo only | Fine at every width. |

The review said a right-logo header "reverts to centred and stacked". Stacking with no gutter is
the visible defect; centring only affects the two-logo case.

### Decision

Nan chose one row everywhere, over stacking the right logo under the title below 600px and over
fixing only the right-only header. In every configuration the header is `[left logo] [title]
[right logo]`, the title is left-aligned, and the gutters match the left-logo header.

### What changed (`scss/_layouts.scss`)

- The flex row now applies to `#overview.logoR` as well as `#overview.logoL`, and the 980px
  block that stopped the base template stacking the title now covers both.
- `#overview.logoL.logoR .titles` is left-aligned, matching the base selector's specificity.
- The right logo is ordered after the title (the player's markup puts it first) and pushed to the
  far right with an auto margin. Its wrapper is `flex: 0 0 auto` with `max-width: 25%`, so it
  keeps its own size up to a quarter of the header.
- Bootstrap's clearfix (`.container::before` and `::after`) becomes two empty flex items in the
  row, and the `gap` beside each supplies the 24px side gutters, which is how the left-logo header
  has always had them. The right logo's `order` moved it past `::after` and lost its right gutter,
  so `::after` is ordered last.

Two of my first attempts were wrong, and the checks caught them:

- **A shrinkable right logo collapsed to a few pixels.** The checks first asserted only a
  maximum size, which a squeezed logo passes, so a minimum was added.
- **The 25% cap applied twice.** The player also gives the `<img>` inside the wrapper the class
  `logoR` (`application.js`), so a `.logoR` rule capped the image at 25% of its already-capped
  wrapper. The rule now selects `div.logoR`.

### Verification

- 225 automated checks pass (171 before), including 54 new `logos` checks. To support them the
  runner (`tests/check_theme.py`) can now render the fixture with a different header and window
  width for a named variant. Six variants (right logo and both logos, at 1280px, 800px and 485px)
  each check that the content stays inside the window, the title is left-aligned, the right logo
  sits right of the title on the same row, is neither squeezed nor over a quarter of the header,
  and has the same gutter as the first item; two-logo variants also check the logo order and the
  Cardiff logo's 70px minimum. 30 of the first 42 passed against the old CSS as guards of the
  wide layouts and one-row basics, and 12 failed for the reasons in the table above.
- The generated reference is in sync and no theme class is undocumented.
- Right-only and two-logo headers were rendered at 1280px and 485px and reviewed by eye.

Not verified:

- **Anything narrower than about 485px.** Headless Chrome will not go below it, so 375px and
  400px remain a manual check. The theme's rules for that range are the same 980px block, but
  they are untested here.
- **The real Xerte player, and real uploaded logos.** The partner logo is a sized grey rectangle.
  Very wide or very tall logos were not tried.
- **The base template's 480px rule.** It sits below the range testable here.

## Left as it was

- The header's left-only layout, the theme logo sizing (`--cu-logo-width`) and the header's
  colours and edges.
- A partner logo is never scaled up: `max-width` caps it, but a small image stays small.
