# Focus on dark panels and the alert close button

Decided and implemented 9 October 2026. Both came out of the Buttons and Alerts pages of the author
guide, where the review measured them. Neither needed a new design decision: the design system already
says what to do.

## Focus ring on a dark panel

**Problem.** The focus ring is 2px solid ink, offset 4px. On a dark panel (`.bg-dark` is ink) an ink
ring cannot be seen, so a keyboard user could not tell which reverse button had focus. Measured on the
built Buttons page.

**Rule.** The design system says "white outline in a dark panel" (Keyboard focus, in the interaction
table). The theme already had the colour as `--focus-ring-color-on-dark`, used by the navbar and the
carousel.

**What changed** (`scss/components/_buttons.scss`).

- `.button-reverse` and `.button-reverse-outline` always use the on-dark ring colour. They exist for
  dark backgrounds, so there is no light case to protect.
- Any `.button` inside `.bg-dark` does too, so a primary button on a dark panel has the same fix.
- Width, style and offset are unchanged (2px, solid, 4px). Only the colour moves. White on ink is 18.7:1.

**Not changed.** Other focusable things in a dark panel, such as links, were not measured.

## Alert close button

**Problem.** The close button was about 13 by 20px, below the design system's 44px minimum for touch
controls ("Keep touch controls at least 44px").

**What changed** (`scss/_bootstrap-components.scss`).

- The button is at least 44 by 44px (`--btn-min-width`), with the × centred in it.
- Negative margins place the box in the alert's padding, so a one-line alert is the same height as one
  without a close button. The box stays inside the alert, 8px from its right edge.
- Bootstrap 2 offsets `.alert .close` with `position: relative; top: -2px; right: -21px`. That would push
  the larger box 13px outside the alert, so the theme resets it with `position: static`.

**Visible effect.** The × moves in from the alert's right edge (about 3px) to sit about 24px from it,
in line with the alert's padding.

**Not changed.** The × is still drawn at half opacity (0.8 on hover or focus), and the button still
shows the browser's default focus outline, not the theme's ring. Both are separate decisions.

## Checks

- Six theme checks: the three white rings, the 44 by 44 box, the box staying inside the alert, and the
  alert keeping its height. Four of them failed first (the ring read ink; the box was 13 by 20).
- A guide check focuses the reverse button on the Buttons page and expects a white ring. It was shown to
  fail when the old ink ring is forced back in.
- Checked in a rendered before and after of both changes.
