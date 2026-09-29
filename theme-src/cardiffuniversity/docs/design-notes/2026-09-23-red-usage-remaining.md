# Red usage: the remaining rows

Implemented 23 September 2026. Applies the last rows of the red-usage decisions, now part of the
design system: `DESIGN.md` v1.5, §2 *Red usage*, with the asterisk as amended in v1.6. The file-and-line audit they came from is the
archived Red Usage Decisions note in the vault. The page chrome (20–21 September) and alerts,
badges and progress bars (21 September) were applied earlier; see
[page chrome](2026-09-21-page-chrome.md) and [alerts, badges and progress](2026-09-21-alerts-badges-progress.md).

## Problem

The design system now says ink does the work and red is a marker, with four jobs: identity, the
primary action, where you are, and real problems. The theme still used brand red (`#E4251B`,
through `--color-brand-primary`) for form states, list icons, code and the skip link. None of
these is one of red's four jobs, and one of them failed contrast:

| Element | Before | Contrast before |
| --- | --- | --- |
| Inline `code` text on its grey-10 fill | brand red | 4.10:1, short of 4.5:1 |
| `pre` left rule against the grey-90 block | brand red | 2.76:1 |
| Skip link text | white on brand red | 4.59:1 |
| Invalid field border on white | brand red | 4.59:1 |

## Decisions

Made by Nan on 23 September 2026 (the `h2.sectionTitle` row on 22 September), and recorded in
`DESIGN.md` §2 (v1.5; the asterisk row v1.6).

| Where | Treatment |
| --- | --- |
| Invalid fields (`select:invalid`, and the matching input and textarea rule) | Error red, `#A11A12` (`--color-status-error`). It is a real error. |
| Required-field asterisk (`label.required::after`) | Error red (`--color-status-error`), not brand red. Changed from ink in v1.6 (see below). |
| Text input, textarea and select focus border | Ink (`--color-border-focus`, the focus token). |
| Radio and checkbox checked state (`accent-color`) | Ink. **Changed 28 September to the action colour; see the [addendum](#addendum-icon-lists-progress-bars-checkboxes-and-radio-buttons-28-september).** |
| `h2.sectionTitle` | Ink. |
| Icon list `li span` | Ink. **Changed 28 September to the brand primary; see the [addendum](#addendum-icon-lists-progress-bars-checkboxes-and-radio-buttons-28-september).** |
| Inline `code` | Ink. |
| `pre` 4px left rule | The design system's `border` grey (`--cu-border`, grey-30). |
| Skip link | Ink with white text, grey-90 on hover and focus, like the back-to-top button. |
| `.text-brand`, `.bg-brand`, legacy `.text-cu-red` | Unchanged: opt-in utilities that authors choose deliberately. |
| `.cardiff-test-style` | Delete. |
| Xerte accordions and tabs | Unchanged. Constellation's red accordion and tab markers were considered and not adopted. |

## What changed

- **Fields** (`_base-elements.scss`). The validation rule takes `--color-status-error`, the same
  error red as the alerts, badges and progress bars. The asterisk takes `--color-status-error` too
  (see *The required-field asterisk*). The focus border
  of text inputs, textareas and selects is `--color-border-focus`, which resolves to ink, so the
  border now matches the ink focus ring drawn around it. Radios and checkboxes use `--cu-ink` as
  their `accent-color`.
- **Lists and code** (`_base-elements.scss`). `.list-icon li span` and inline `code` are
  `--cu-ink`. The `pre` block's left rule is `--cu-border`.
- **Skip link** (`_utilities.scss`). The background is `--cu-ink` with `--color-white` text,
  turning `--color-gray-90` on hover and focus, the same pattern as `.btn.topBtn` in
  `_xerte-components.scss`. It keeps the shared focus ring, which already sits 4px off the link.
  The rule no longer uses `--color-bg-brand`; the token itself is unchanged, since the opt-in
  brand utilities still read brand red directly.
- **Already done before today.** `h2.sectionTitle` became ink in `3c60c4011`, and
  `.cardiff-test-style` was deleted in `26e47a663` (hardcoded-values audit). Both were only
  verified here: an existing `headings` check covers the section title, and the class appears
  nowhere in the theme.
- **Author guide.** The colour page's brand-red entry no longer says the navbar and sidebar states are
  "pending Red Usage Decisions", and it names the opt-in utilities.
- **Follow-up checklist.** The red-usage item is ticked. Secondary-button semantics, which shared
  that line, stays open on its own.

Every new colour is an existing token; no raw hex was added.

## Contrast

| Element | Pair | Ratio | Needed |
| --- | --- | --- | --- |
| Invalid field border | `#A11A12` on white | 7.86:1 | 3:1 (UI boundary) |
| Focused field border | ink on white | 18.73:1 | 3:1 |
| Radio and checkbox checked state | ink on white | 18.73:1 | 3:1 |
| Required asterisk | `#A11A12` on white | 7.86:1 | 4.5:1 |
| Icon-list span | ink on white | 18.73:1 | 4.5:1 |

The radio, checkbox and icon-list rows describe 23 September. For the current colours and
ratios, see the addendum on 28 September.
| Inline `code` | ink on grey-10 | 16.73:1 | 4.5:1 (was 4.10:1) |
| `pre` left rule | grey-30 against the grey-90 block | 7.87:1 | none (decorative) |
| Skip link text, resting | white on ink | 18.73:1 | 4.5:1 |
| Skip link text, hover and focus | white on grey-90 | 12.63:1 | 4.5:1 |

The `pre` rule is decorative: the dark fill defines the block, and the rule is grey-30 against
white on its outer edge (1.61:1). The skip link's ink focus ring is offset 4px, so it is measured
against the white page (18.73:1), not against the grey-90 link (1.48:1).

## Verification

- 257 automated checks pass (240 before), including 17 new `red` checks. 14 of them failed
  against the old CSS. The other three are contrast floors that brand red already met (the
  invalid border at 3:1, the skip link text and the asterisk at 4.5:1); they now guard the new
  colours. One check recolours `--cu-red` and confirms the asterisk does not follow it.
- The first run also reported the focused text input and textarea borders as grey-30, not red.
  That was the rule's `border-color` transition: the reading was the start of the fade. The
  focus checks now switch the transition off while they read, as the back-to-top focus check
  already does, and are built from one `focused_border()` helper.
- The generated reference is in sync, and no theme class is undocumented. `git diff --check` is clean.
- The forms demo and a snippet of the changed elements (inline code, `pre`, required label,
  invalid select, radio, checkbox, skip link) were rendered in headless Chrome and reviewed by eye.

Not verified: the real Xerte player, and any project that uses these elements.

## The required-field asterisk

v1.5 made the asterisk ink ("a required field isn't an error until it fails"). Nan reviewed that
on 23 September 2026 and wanted it red, but not brand red: a theme may recolour `--cu-red`, and
the asterisk should not change with it. It takes the error red instead, which belongs with the
field's validation and stays fixed across themes. `DESIGN.md` was amended to v1.6 to match (§2
job 4, the *Never red* table and §4 *Fields*), as was the `cardiff-brand-guidelines` skill.

## Left as it was

- **The skip link and resting field borders** were left open here and decided later the same
  day: see [field borders, skip link, legacy columns and demo pages](2026-09-23-fields-skip-link-demo-pages.md).
- **`--color-bg-brand`** still resolves to brand red. No theme rule reads it now; only the colour
  page's swatch shows it. It was kept because project CSS may use it.

## Addendum: red in the author guide (23 September, later)

The guide's own demo markup and shared demo stylesheet still used brand red where the design
system says ink. These are demo styles, not theme rules, but authors copy them.

| Where | Before | After |
| --- | --- | --- |
| Guide section `h2` (`base-elements-demo.html` page style), card `h4`s, staff-profile `h3`, `.demo-card__title` (`assets/demo-styles.css`) | brand red | ink: headings are never red |
| Dark panels behind the reverse buttons (`components.html`, `base-elements-demo.html`) and the centred CTA banner (`patterns.html`) | brand red fill | ink fill |
| `.demo-block--highlight` left rule, `.demo-footer__link:hover` | brand red | ink |
| Contact list icons (`images-media.html`) | blue, green, red, orange | inherit the text colour: icons outside callouts are black or white (§4 *Icons*) |
| "Brand" heart in the icon colour row | brand red | removed; the four status icons remain |
| Flexbox feature-grid icons and their code sample | `.text-brand` | no colour class |
| Flexbox placeholder boxes (renamed `.demo-box--brand` → `.demo-box--muted`) | brand red fill | grey-70 with white text (5.74:1) |

Kept on purpose: `.demo-warning`'s red rule, which mirrors the Warning callout, and the
`colors.html` swatches, the "White text on Brand Primary" combination and the override example,
which document the brand token itself.

Verification: 257 checks pass, the reference is in sync and no theme class is undocumented. The
Patterns and Components pages were rendered in headless Chrome and reviewed by eye.

## Addendum: icon lists, progress bars, checkboxes and radio buttons (28 September)

Three elements that this note and earlier ones kept out of red now use it. Decisions by Nan;
the commits (`20bd9a7d0`, `f112b010c`) record what changed but not why.

| Element | Before | Now |
| --- | --- | --- |
| Icon-list icons (`.list-icon li span`, `_base-elements.scss`) | Ink | `--color-brand-primary`: Cardiff red, `#E4251B` |
| Default progress fill (`.bar`, `.progress-bar`, `_bootstrap-components.scss`) | `--color-brand-secondary` since 24 September (ink for Cardiff); ink before that, in the [alerts note](2026-09-21-alerts-badges-progress.md) | `--color-brand-primary`: Cardiff red, `#E4251B` |
| Checked radio buttons and checkboxes (`accent-color`, `_base-elements.scss`) | Ink | `--color-action`: the primary mixed 85% with black, `#C21F17` for Cardiff |

All three now follow the brand: a project that restyles `--color-brand-primary` recolours them.
The progress bar's status variants (success, warning, danger, info) are unchanged.

### Contrast, with Cardiff's colours

| Element | Pair | Ratio | Needed |
| --- | --- | --- | --- |
| Icon-list icon | `#E4251B` on white | 4.59:1 | 3:1 as a graphic; 4.5:1 if treated as text |
| Default progress fill against the track | `#E4251B` on grey-20 (`#E5E5E5`) | 3.64:1 | 3:1 |
| The same, against the track as drawn | `#E4251B` on Bootstrap's `#F5F5F5`–`#F9F9F9` gradient | 4.21–4.36:1 | 3:1 |
| White label on the default fill | white on `#E4251B` | 4.59:1 | 4.5:1 |
| Checked radio button and checkbox | `#C21F17` on white | 6.0:1 | 3:1 |

The label and the icon clear 4.5:1 by a small margin, so a lighter brand primary can fail
them. The theming guide lists the progress bar's checks; the icon list needs the same 3:1 on
white as the primary's edges and markers. The checked controls use the action shade, so a
brand that passes the primary-button check (white on the action colour at 4.5:1) passes here.

### Against the design system

The ink rows for these elements were recorded in `DESIGN.md` §2. The theme now differs from it
on them, which the [theming guide](../../THEMING-GUIDE.md) allows ("so the theme can differ from
the design system where Xerte needs it"). Whether `DESIGN.md` was amended to match is not
recorded in this repository.

### Verification

`9b8cf08bd` updated the automated checks and the theming page:

- The `red` checks now expect action red for checked radio buttons and checkboxes, and brand red
  for the icon-list span.
- The `status` check expects a brand-red default progress fill, and the existing checks still
  require every fill to reach 3:1 on the track and every label 4.5:1 on its fill.
- A `theming` check confirms the progress bar, icon-list icon and checked controls follow the
  example brand.

Not verified: the real Xerte player.
