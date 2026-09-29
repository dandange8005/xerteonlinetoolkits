# Field borders, skip link, legacy columns and demo pages

Implemented 23 September 2026, after the merge of `feature/cardiffuni-v3-ds-v1.3` into develop.
It settles two items the [red-usage note](2026-09-23-red-usage-remaining.md) left open, fixes
three layout bugs found in the player (legacy columns, breadcrumb padding, asset-link underline),
and reorganises the author guide.

## Decisions

Made by Nan on 23 September 2026, after comparing the options side by side (a private comparison
page with keyboard-testable specimens of each option).

| Item | Options | Chosen |
| --- | --- | --- |
| Skip link colour when it appears | A: grey-90 on hover and focus (as applied); B: ink on focus, grey-90 on hover only | **B** |
| Resting field border | A: 2px grey-30 (1.61:1); B: 2px grey-60 (3.95:1); C: 2px grey-70 (5.74:1); D: 1px grey-70, as DESIGN.md §4 already specifies (5.74:1) | **D** |

## What changed

### Skip link (`_utilities.scss`)

The skip link sits off-screen until it has focus, so its focus colour is the only colour anyone
sees. Under A that was grey-90, and the ink resting colour was never visible. It now keeps the ink
while focused; grey-90 is on hover only. The back-to-top button keeps grey-90 on hover and focus,
because it is visible at rest and the change shows focus. `DESIGN.md` §2 was amended to v1.7 to
match (the skip link has its own row in the *Never red* table), and the theme's stated version
references follow.

### Field borders (`_base-elements.scss`)

Text inputs, textareas and selects now have a 1px `--cu-muted` (grey-70) border, as `DESIGN.md`
§4 *Fields* specifies, in place of 2px grey-30.

- **Contrast.** The resting border is 5.74:1 on white, up from 1.61:1; WCAG 1.4.11 asks for 3:1.
- **Hover.** The grey-50 hover border (2.85:1) would have been lighter than the new resting
  border, so hover is now the `--cu-surface` fill the design system specifies. The border and
  the transition cover the fill.
- **Same thickness in every state.** Focus (ink border plus the 2px ink focus ring) and invalid
  (error red) keep the 1px width, so the field does not shift between states.
- **Size.** A field is 2px shorter and narrower inside than before, because the border is 1px
  thinner on each side. Padding was not changed.

Checkboxes and radios are unaffected: the browser draws their unchecked outline.

### Legacy columns (`_legacy.scss`)

`.flexContainer` has a gap, and `.c50` and the other column classes were plain percentages, so two
`.c50` items plus one gap came to more than 100% and the second wrapped under the first. Bootstrap 2
does not set `box-sizing: border-box`, so an item's padding and border also added to its width.
The bug came over unchanged from the original `cardiffuni` theme.

- Each `.cNN` width is now its percentage minus its share of the gap:
  `calc(50% - var(--legacy-flex-gap) * 0.5)`. A row of n columns loses (n − 1) gaps in total and
  each column's share is (1 − its fraction) of one gap, so any set of columns that adds up to 100
  fits on one row. The ten classes are generated from one Sass list.
- The gap is a local custom property, `--legacy-flex-gap` (default `--spacing-md`), so the widths
  follow if a project changes it.
- `.flexItem` and the column classes use `box-sizing: border-box`.

### Breadcrumb (`_bootstrap-components.scss`)

Breadcrumb items in a page section had 8px of left padding from the base list rule
(`section ul li`), which `.breadcrumb > li` never overrode. It now sets `padding-left: 0`.

### Asset link (`components/_links.scss`)

The file-download card was underlined at rest under its icon, name and label. The player's
`custom.css` underlines `section a:not(...)`, specificity (0,1,2), which beat the single
`.link-asset` class; the theme only removed the underline on hover. The card now has no
underline in any state: its grey fill and hover outline mark it as a link. A `section a.link-asset`
rule matches the player's specificity, and the theme loads after it. The icon also gets a fixed
1.25em box, because the PDF and Word glyphs differ in width and pushed the names out of line.
The Components page now shows a Word example next to the PDF one.

### Author guide (`demos/`)

- **Navigation order.** Colors moves up to follow Typography. The order on every page is Home,
  Typography, Colors, Lists & Tables, Images, Media & Icons, Forms, Components, Bootstrap, Code &
  Utilities, Patterns, Flexbox. The Home page cards follow it, and every page's footer now links
  to the previous and next page in that order (several skipped or pointed backwards before).
- **New Bootstrap page** (`bootstrap.html`). Alerts, badges and labels, progress bars,
  breadcrumbs, tabs and accordions moved from Components, with their usage guidelines. Both pages
  open with an About section that points to the other. Pills, carousel, panels and wells have no
  examples yet; tables stay on Lists & Tables.
- **Legacy flexbox examples** (`flexbox.html`). One 50/50 example became five blocks: how the
  columns work (including which classes exist), two columns (50/50, 40/60, 30/70, 20/80), three
  to five columns, wrapping onto new rows, and an image-and-text layout using the legacy `h3`,
  `.topMargin` and `img` rules. Code snippets on the page now keep their line breaks.

## Verification

- 270 automated checks pass (257 before):
  - 1 `breadcrumb` check, failing before the fix;
  - 4 `legacy` checks (50/50, 33/33/33 and 30/70 rows fill one row; two `.c50` match), 3 of which
    failed before;
  - 6 `fields` checks (1px grey-70 border on input, textarea and select; 3:1 or better; 1px on
    focus and when invalid), all failing before;
  - the skip-link focus check now expects ink;
  - 2 `links` checks (no underline at rest inside a section, which failed before; names line up
    for PDF and Word icons). The fixture's asset link sits in a section: outside one, the player
    rule does not apply and the first check passed against the old CSS.
- The resting-border checks switch the border transition off while they read, because an earlier
  focus check leaves a field fading back from ink.
- The generated reference is in sync, no theme class is undocumented, and every nav link, footer
  link and section anchor in the guide resolves.
- Rendered in headless Chrome and reviewed by eye: the legacy columns and breadcrumb, the new
  Bootstrap page, and the new legacy examples.

Not verified: hover states (headless checks cannot hover), and the real Xerte player.
