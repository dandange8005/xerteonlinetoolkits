# Alerts, badges and progress bars

Implemented 21 September 2026. Part of the second item under "Remaining theme migration" in the
[follow-up checklist](../plans/2026-09-21-follow-up.md); tabs, accordions, cards, tables and the
rest of that item are not covered here.

## Problem

These three components still used the v2 palette, and measuring them against the theme's own
tokens showed accessibility failures:

| Component | Before | After |
| --- | --- | --- |
| Alert text, info | 4.30:1 | 16.73:1 |
| Alert text, warning | 4.05:1 | 16.73:1 |
| Badge and label, default (white text) | 3.95:1 | 5.74:1 |
| Badge and label, info | 3.24:1 | 6.33:1 |
| Progress label on the warning fill | 2.97:1 | 5.53:1 |
| Progress label on the info fill | 3.24:1 | 6.33:1 |
| Warning fill against the track | 2.36:1 | 4.39:1 |
| Info fill against the track | 2.57:1 | 5.03:1 |

Alerts also used rounded corners, pastel tints built with `color-mix`, and a full 1px border.
The progress track drew an inset shadow. Danger and error states, and the default progress fill,
used brand red (`#E4251B`), and the Red Usage Decisions note had no decision for them.

## Decisions

Made by Nan on 21 September 2026, and recorded in the Red Usage Decisions note.

| Where | Treatment |
| --- | --- |
| Danger and error red (alerts, badges and labels, progress) | The design system's error red, `#A11A12` (`--color-status-error`), the same as input errors. |
| Default progress fill | Ink (`#121212`). |
| Alert look | Follows the design system's callouts: grey surface, square edges, 4px left rule in the status colour. |

## What changed

- **Alerts** (`_bootstrap-components.scss`). The `--color-bg-subtle` surface (grey-10), ink text,
  no outer border and no rounding. The left rule takes the status colour: Forest Green for
  success, link blue for info, Yellow for warning, error red for danger and error. The
  ✓ ℹ ⚠ ✗ prefixes stay, and the bold word carries the status alongside the glyph, so the rule is
  reinforcement and not the only cue. Against the grey-10 surface the rules measure 4.13:1
  (success), 5.66:1 (info) and 7.02:1 (danger and error); the Yellow warning rule is only 1.60:1,
  which is acceptable only because the glyph and the word carry the meaning. A heading inside an
  alert now inherits ink. Bootstrap gave each variant's `h4` its own colour (green, blue, brown
  and a red shared by danger and error), which the old tints hid.
- **Badges and labels.** Default fill grey-70 (was grey-60). Info is link blue (was the light
  accent blue). Danger and important are the error red. Success and warning already passed and
  are untouched.
- **Progress bars.** The inset shadow is gone (Bootstrap draws it too, so the theme sets
  `box-shadow: none` explicitly) and the track is square. The default fill is ink. Danger is the
  error red, info is link blue, and warning is `--color-accent-orange-dark`, a new token: orange
  mixed 70% with black, the same derivation as `--color-brand-primary-dark`. Success is unchanged.
- **Demo.** Each of the three sections says what the look is and why.

## Verification

- 156 automated checks pass (133 before), including 23 new `status` checks. 20 of the first 22
  failed against the old CSS; the other 2 guard the alert glyph prefix and the Forest Green
  success rule, which were already right. The progress-shadow check kept failing after the first
  fix, because deleting the theme's declaration left Bootstrap's own shadow showing; the theme now
  sets `none` explicitly. The alert-heading check was added after the first render showed a blue
  heading, and it failed against Bootstrap's colours before the fix.
- The contrast checks loop over every variant, so a new variant with weak contrast would fail.
  The contrast helper in the fixture was fixed to read `color(srgb …)` values, which is how
  `color-mix` results serialise; the numbers it reports match hand calculation.
- The generated reference is in sync and no theme class is undocumented.
- The three demo sections were rendered in headless Chrome and reviewed by eye.

Not verified: the real Xerte player, and any project that uses these components.

## Left as it was

- **Progress track colour.** Bootstrap paints a light gradient (`#f5f5f5` to `#f9f9f9`) over the
  theme's grey-20 track, so the token colour was never visible, before or after this change. The
  checks measure against grey-20, which is the darker case, so the real contrast is a little
  higher. Making the track match the token, or removing the gradient, would change how every
  progress bar looks and was not part of what was approved.
- **Striped and animated bars.** Reduced motion already stops the stripe animation, through the
  global rule in `_enhancements.scss`. The stripes are a white overlay on the fill, so their
  contrast was not measured separately.
- **Radius on badges and labels.** They keep their pill and small-radius shapes; the control
  radius question belongs to the hardcoded-values audit.
- **Block alert layout.** The glyph still sits on its own line above a heading, as before.
- **The wider Red Usage rows** (inputs, radios, skip link and others) remain undecided.

## Addendum: warning status colour was the same as ink (22 September)

`--color-status-warning` resolved to black, by two hops: `--color-status-warning` →
`--color-warning` → the Draft label's `--cu-draft` → `--cu-black`. It was not a deliberate
choice; the design system defines no general "warning" role, only `draft`/`draft-bg` for its
one specific black-on-Yellow label. The v3 theme's own `--color-warning` got mapped onto that
role because the two concepts look similar, and a separate status token then aliased to it.

Two real consumers were affected: the `.text-warning` utility (`_utilities.scss`) rendered as
plain ink, indistinguishable from body text, and a warning triangle icon in the images-media
demo was a plain black triangle. `.alert-warning` was unaffected: it uses
`--color-accent-yellow` directly and never touches this chain.

**Fix:**

- `--color-warning` / `--color-warning-bg` are renamed `--color-draft` / `--color-draft-bg`,
  since the Draft label is their only use. Not documented anywhere as a supported override
  point, so nothing depends on the old names.
- `--color-status-warning` now resolves to `--color-accent-orange-dark` (introduced in the
  original alerts/badges/progress work, above), 5.52:1 on white. The raw accent orange is
  2.97:1 and Yellow is 1.79:1, both short of 4.5:1 for text and icons.
- `--color-status-warning-bg` is removed. It was unused, and no other status token
  (`success`, `error`, `info`) has a `-bg` counterpart, so it was not a pattern to preserve.

Verification: 233 checks pass (229 before). Four new checks assert the warning text and icon
match the darkened orange (not ink), read at 4.5:1 on white, and that the Draft label is
unaffected by the rename; two existing `roles` checks were updated to the new token names.
The generated reference is in sync. Rendered and reviewed by eye.
