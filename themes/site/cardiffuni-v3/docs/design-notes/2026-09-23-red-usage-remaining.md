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
| Radio and checkbox checked state (`accent-color`) | Ink. |
| `h2.sectionTitle` | Ink. |
| Icon list `li span` | Ink. |
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

- **The skip link is never seen in ink.** It sits off-screen until it has focus, and focus turns
  it grey-90, so ink only shows if the pointer is over the link while it is off-screen, which
  cannot happen. This follows the decision ("grey-90 on hover and focus") exactly. If the skip
  link should read as ink when it appears, the focus rule should keep the ink background and only
  hover should use grey-90.
- **Resting field borders.** Text inputs, textareas and selects rest on a grey-30 border, which
  is 1.61:1 on white, short of the 3:1 WCAG 1.4.11 asks for a field boundary. This is not a red
  row and was not part of what was approved.
- **Red in the author guide's own demo markup.** A few examples set brand red with inline styles
  (`h4` headings and a panel on the base-elements page, a banner and a heading on the patterns
  page). These are demo content, not theme rules; the headings contradict the "headings are
  never red" rule and could be changed separately.
- **`--color-bg-brand`** still resolves to brand red. No theme rule reads it now; only the colour
  page's swatch shows it. It was kept because project CSS may use it.
