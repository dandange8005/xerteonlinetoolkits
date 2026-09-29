# Brand colour theming

Implemented 24 September 2026 on `feature/cardiffuni-v3-brand-theming`. Decisions by Nan the same
day: an author who wants their own colours should set a primary and a secondary colour with
names that say what they are, as the v2 theme's override files did, not recolour `--cu-red`.

## The problem

The [theming page](../../demos/theming.html) told authors to override `--cu-red`, `--cu-action` and
`--cu-action-hover`. A green brand then read `--cu-red: #00703C`. The theme already had the
names v2 used, `--color-brand-primary` and `--color-brand-secondary`, but they were downstream
aliases, so overriding them left most of the brand in place:

- The header edge, both navbar markers, the side-menu rule and the selected-item wash read
  `--cu-red` directly and stayed Cardiff red.
- Buttons and the feedback tab read `--cu-action`, a fixed dark red.
- The navbar hard-coded ink and grey-90, so it ignored the secondary.
- **Body text read the secondary.** `--color-text-primary` pointed at `--color-brand-secondary`,
  so a navy secondary turned all body text, headings and the text mixes navy. A new check
  confirmed it against the old CSS.

## What changed

Nothing in the design system or the generated `_cu-tokens.scss` changed. The two brand names in
`_allvariables.scss` are now the project override points, and every brand-coloured part reads them.

```css
:root {
  --color-brand-primary: #00843D;
  --color-brand-secondary: #14213D;
}
```

| Follows | Parts |
| --- | --- |
| `--color-brand-primary` | Header top edge; navbar current-page marker; the rule under a navbar placed below the header; side-menu selected rule and wash; `.text-brand`, `.bg-brand`, `.text-cu-red` |
| Action shades (from the primary) | Primary and primary-outline buttons, feedback tab, `--color-text-brand` |
| `--color-brand-secondary` | Navbar, its hover and current-page fill; footer; secondary and secondary-outline buttons (including the legacy `.button--outline`); `.bg-dark`; tab underline and pills (`--color-nav-accent`); the default progress bar; back-to-top button; Do/Don't labels |
| Always ink | Body text and headings (`--color-text-primary`), reverse and ghost button text, inverse and warning badges, glossary tip, `.text-cu-black` |
| Fixed, as before | Error and the required asterisk, the Warning callout, charts, focus, links, fields, skip link, logos |

**Which dark parts follow the secondary.** The first pass kept tabs, pills, progress bars,
the back-to-top button and Do/Don't labels ink, as in-page controls. Nan moved them to the
secondary. The back-to-top button's hover and focus fill, a fixed grey-90 before, is now the
navbar's hover shade (`--color-navbar-bg-hover`): still grey-90 for Cardiff, as DESIGN.md §2
specifies, and a lighter secondary under a restyled brand. `--color-nav-accent-dark` was
considered and rejected, because it is 15% secondary and 85% black: `#030303` against the ink
button's `#121212` (1.1:1), so the hover would barely show. Text, the glossary tip, reverse and ghost button text and the inverse and warning
badges stay ink. For Cardiff nothing changes, because the secondary is ink.

**Shades are mixed from the brand.** A project should need two values, so the shades follow:

| Name | Mix | Cardiff result | Design system |
| --- | --- | --- | --- |
| `--color-action` | primary 85%, black | `#C21F17` | `--cu-action` `#C21F16` |
| `--color-action-hover` | primary 70.5%, black | `#A11A13` | `--cu-action-hover` `#A11A12` |
| `--color-tint` (outline hover) | primary 17%, white | `#FADAD8` | none (was a raw `#F8DADA`) |
| `--color-navbar-bg-hover` (new) | secondary 86%, white | `#333333` | grey-90 `#333333` |
| `--color-selected-bg` | primary 6%, white | unchanged | none |

The action reds land one step from the design system in the blue channel. A search of sRGB,
linear-sRGB and OKLab mixes with black found none that reproduces both `#C21F16` and
`#A11A12` exactly. The difference cannot be seen, and two checks hold the derived values within
one step of `--cu-action` and `--cu-action-hover`. White on them is 6.0:1 and 7.9:1, and the action
red on the new tint is 4.59:1 (4.58:1 before).

**Compatibility.** `--color-brand-primary` still reads `--cu-red` by default, so an existing
`--cu-red` override keeps working. An override of `--cu-action` or `--cu-action-hover` no longer
reaches the buttons. The only published instructions for that were on the theming page, which
had been live for a day. A project that needs specific button shades, for example a light brand
whose 85% mix fails 4.5:1 under white text, sets `--color-action` and `--color-action-hover`.

On 21 September the [token consolidation](2026-09-21-token-consolidation.md) removed
"two-variable rebranding examples" because they misled: two variables did not reach the
components. This change makes that claim true, and the checks below hold it.

## Contrast an author must check

The theme cannot check an author's colours, so the guide and the theming page list the checks.
The worked example (`#00843D` and `#14213D`) passes all of them:

| Pair | Needs | Example |
| --- | --- | --- |
| White on primary 85% with black (button) | 4.5:1 | 6.24:1 |
| White on the secondary (navbar) | 4.5:1 | 15.97:1 |
| White on secondary 86% with white (current page) | 4.5:1 | 10.37:1 |
| Primary edge on white | 3:1 | 4.81:1 |

**Found, not fixed: the current-page marker.** The 3px primary marker sits on the navbar's
current-page fill. For Cardiff red on grey-90 that is 2.76:1, below 3:1 for a state indicator.
This predates this change, but the brand colours make it visible: most pairs that pass the
button check fail here, and the example pair is 2.16:1. It is on the
[follow-up checklist](../plans/2026-09-21-follow-up.md).

## Author guide

- **Theming page:** rewritten around the two values.
  - About leads with them.
  - The blue example (three `--cu-*` overrides) is replaced by the green and navy one.
  - The live variant now shows primary, primary-outline, secondary and secondary-outline buttons.
  - The roles table and limits say what does and does not follow.
- **Colors page:** the brand swatches show their sources, Text Primary reads `--cu-ink`, the action
  values are the mixed ones, and the restyling block names the two values.
- **Code & Utilities page:** the button example reads `--color-action`.
- **`THEMING-GUIDE.md`:** has a new *Restyle the brand* section with the mapping, the mixes, the
  contrast checks and the compatibility note.

## Verification

- 292 automated checks pass (279 before).
  - **New theming checks.** Nine new `theming` checks apply the example brand (`#00703C` and
    `#1D2B4F`) through a `withBrand` fixture helper. The helper turns transitions off and settles
    the restored brand before turning them back on.
  - **What they assert:**
    - The four primary accents, the wash, the buttons, the feedback tab, the navbar, its fill,
      the footer, the secondary button and `.bg-dark` all follow.
    - Text and headings stay ink; pills, the progress bar and the back-to-top button take the secondary.
    - Error, Warning, focus and links do not move.
    - White navbar and button text reach 4.5:1.
  - **Against the old CSS:** five of the nine fail, including body text turning navy. The secondary button, pill, progress bar, back-to-top, fixed-colour and contrast checks already held.
  - **Back-to-top hover.** Two `chrome` checks read the focused button, which shares the hover
    rule: grey-90 for Cardiff, and the lighter secondary under the example brand. The second
    fails against the old CSS.
  - **Updated checks.** Two `roles` checks bound the action shades to one step of the design
    system. Five existing checks now expect the mixed values, and two now override
    `--color-brand-primary` instead of `--cu-red`.
- The generated reference is in sync, and no theme class is undocumented.
- The theming page was rendered in headless Chrome with the example brand applied, and checked by
  eye.
  - Green followed on the header edge, navbar marker, side-menu rule and buttons, and navy on the
    navbar and secondary buttons.
  - The Warning callout stayed red and the text stayed ink.

Not verified: the real Xerte player, hover states, and a project's Styles property.
