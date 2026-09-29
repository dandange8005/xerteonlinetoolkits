# Hardcoded-values audit: bug fix and focus-ring de-duplication

Implemented 22 September 2026. First instalment of the third "Remaining theme migration" item
in the [follow-up checklist](../plans/2026-09-21-follow-up.md): "remaining hardcoded
colours/radii/shadows and red usage against the design system." A fresh audit found more ground
than one batch, so the rest is deliberately deferred; see below.

## Bug: a keyboard-focused `<details>` summary had no visible focus indicator

`components/_details.scss`'s `.details__summary:focus` set `background-color` and `box-shadow`
to `var(--color-accent-gold)`, a token that was never defined anywhere in the theme, the
generated tokens, or the design system. It also set `outline: 4px solid transparent` on purpose,
presumably meaning to replace the outline with the background/shadow treatment. With the colour
undefined, `background-color` computed to transparent and the invalid `box-shadow` declaration
was dropped entirely, so nothing was left: a keyboard user tabbing onto a details summary saw no
focus indicator of any kind. Confirmed live in headless Chrome before the fix.

**Fix:** replaced the broken treatment with the theme's standard focus ring
(`var(--focus-ring)`, `var(--focus-ring-offset)`), the same pattern every other interactive
element in the theme uses, and switched `:focus` to `:focus-visible` to match that pattern (no
ring on a mouse click). This introduces no new colour decision. Screenshotted and confirmed a
visible 2px ink outline around the summary on focus.

## De-duplication: the focus-ring fallback

Nine `:focus`/`:focus-visible` rules wrote `outline: var(--focus-ring, 2px solid var(--cu-ink,
#121212))`, spelling out a literal fallback for a token (`--focus-ring`) that is always defined
at `:root` in this same stylesheet. The fallback was dead weight, not a defence against anything
that can happen. Simplified to `outline: var(--focus-ring)` in all nine places:

- `_base-elements.scss`: the general link rule, a text input, a select, and the radio button.
- `_bootstrap-components.scss`: tab links, pill links, the accordion toggle, the carousel
  control, and breadcrumb links.

This is a pure refactor with no behaviour change, so it needed no new failing test by itself
(the fallback's literal value already equalled the real token). A direct check on `--focus-ring`
itself, plus spot checks on two of the nine sites that had no existing focus coverage
(breadcrumb link, accordion toggle), already passed before the change and continued to pass
after, which is the proof the simplification is safe. Tabs and accordions were not otherwise
touched, consistent with the earlier decision to leave them alone.

## Verification

- 237 automated checks pass (233 before): 1 new check proves the bug (failed against the old
  CSS, confirmed the failure reason, then passed after the fix), 4 new checks guard the
  refactor's safety, of which 3 already passed before any code changed.
- The generated reference is in sync and no theme class is undocumented.
- The details fix was rendered focused, in headless Chrome, and reviewed by eye.

Not verified: the real Xerte player.

## What the fresh audit found, not yet actioned

A full re-scan (the Mapping note's "17 hex / 18 rgba / 9 radii / 5 shadows" count is from 19
September, before this session's other work) found five more independent batches, deliberately
left for later decisions:

| Batch | What | Files |
| --- | --- | --- |
| Section backgrounds | `.evenSection`/`.oddSection` use raw `#ffffff`/`#f9f9f9` instead of `--color-white`/`--color-light` | `_layouts.scss` |
| Carousel | Untouched component: local `rgba()` shadows and borders, a `2px` radius, its own custom-property scale not tied to `--shadow-*` | `_bootstrap-components.scss` |
| File-type icon colours | `#dc3545` (PDF) / `#2b579a` (Word) — arguably legitimate brand-recognition colours, not theme colours | `components/_links.scss` |
| Editor iframe fallbacks | `var(--color-brand-primary, #E4251B)` and similar — may be defensive for the CKEditor iframe context; not yet checked whether necessary | `_editorstyles.scss` |
| Misc | A raised-key decorative shadow on page content (design system: shadows are overlay-only) in `_base-elements.scss`; `border-radius: 9999px !important` that should be `var(--radius-full)` in `_utilities.scss` | mixed |

`--color-tint: #F8DADA` in `_allvariables.scss` is already flagged in-code as a Red Usage
Decisions item and is out of scope here, as is the wider set of undecided Red Usage rows and
secondary-button semantics named in the same checklist line.

## Addendum: the five batches (22 September, later)

Decisions made by Nan.

| Batch | Decision |
| --- | --- |
| Section backgrounds | Fix: `.evenSection`/`.oddSection` now use `var(--color-white)`/`var(--color-light)` instead of raw `#ffffff`/`#f9f9f9`. |
| Editor iframe fallbacks | Not a real batch: `.cardiff-test-style` was the same class Nan's own Red Usage Decisions log already marked "delete (test leftover)". Deleted from `_editorstyles.scss`, and the now-unused `"cardiff-test-style"` entry removed from `build-reference.py`'s exclusion list. |
| Misc | Fixed: `.rounded-full` now uses `var(--radius-full)` instead of the identical literal `9999px`. `.carousel figcaption`'s `color: #fff` now uses `var(--color-white)`. |
| `kbd`'s raised shadow | **Kept.** A recognised web idiom for a keyboard key, distinct from the design system's "no decorative shadows" rule, which targets cards and panels, not this. |
| File-type icon colours | **Kept.** PDF red and Word blue are external brand-recognition colours, not the Cardiff palette. Commented in `_links.scss` as an intentional exception. |
| Carousel shadows and translucent colours | **Kept.** They sit on a photo, an overlay context the design system's rule already permits. The theme's only shared shadow tier with a real value, `--shadow-lg`, is a larger, softer dropdown shadow that would visibly change the controls; the translucent whites need to show the photo through them, which a solid token cannot do. Commented at the top of the carousel's `:root` block. The same reasoning applies to `--btn-reverse-outline-hover-bg`/`-active-bg` (translucent white on a dark button) and the progress-bar stripe pattern, neither of which was in the original five-batch list but is the same category; both are now commented too. |

Section backgrounds, the utility radius and the caption colour needed no failing test: the
tolerant colour comparison already used elsewhere in the suite treats `#f9f9f9` and the current
`--color-light` (about 248.5 per channel, within the check's 1.5 tolerance) as the same colour,
and `--radius-full` was already exactly `9999px`. These are honest zero-risk substitutions, not
bug fixes, so three new `audit` checks exist as regression guards rather than as proof of a
defect.

Fresh re-scan after all of this: two raw hex values remain (`--color-tint`, already a Red Usage
Decisions item; the two file-type icon colours, decided above), and every remaining `rgba()` and
non-zero radius/shadow literal is one of the three kept-on-purpose exceptions, now commented in
place.

Verification: 240 checks pass (237 before). The generated reference is in sync. No demo
references `.cardiff-test-style`, `.evenSection` or `.oddSection`, so nothing else needed
updating.

Not verified: the real Xerte player.
