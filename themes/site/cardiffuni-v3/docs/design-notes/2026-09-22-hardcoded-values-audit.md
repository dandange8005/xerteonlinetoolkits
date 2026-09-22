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
