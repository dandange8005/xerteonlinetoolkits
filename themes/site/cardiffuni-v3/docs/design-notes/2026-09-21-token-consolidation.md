# One source for shared theme values

Implemented 21 September 2026, after the user identified overlapping token layers.

## Problem

The generated design-system tokens and `_tokens.scss` independently defined typography,
spacing, radii, shadows and motion. `_allvariables.scss` mixed both sources. New rules used
`--cu-*` directly, while existing components consumed independent values with older names.
Changing one source could therefore change only part of a page. The old rebranding example
asked authors to override two names, without covering the remaining colour roles.

## Decision

Keep `_cu-tokens.scss` as the generated shared source and `_allvariables.scss` as the Xerte
adapter. Remove `_tokens.scss`: its only active consumer used interpolation to emit CSS
custom properties; nothing required those values for Sass calculations or media queries.

Existing CSS names remain available. Shared sizes, weights, leading, tracking, spacing,
control radius, overlay shadows and fast motion now resolve to `--cu-*` roles. Brand-primary
now follows `--cu-red`, the role used by newer layout rules, rather than bypassing it to the
palette. Background, border, muted text and success aliases likewise follow their roles.
The spacing-32 extension derives from twice the shared spacing-16 value.

Values with no shared role stay in the adapter: control and border geometry, grid columns,
z-indexes, intermediate typography utility steps, longer transitions and the existing
outline-button tint. They are explicitly Xerte settings, not another copy of the shared scale.
Structural zero radii stay zero when the shared control radius changes.

The generated file and the external design-system source were not changed. Source roles
and theme aliases remain at `:root`. Project overrides set the shared role once at the root;
subtree theme switching is not a supported automatic remapping mechanism. Old custom-property
names can still override their own consumers. Downstream Sass code importing the removed
private `_tokens.scss` would need migrating to the CSS properties.

See [the theming guide](../../THEMING-GUIDE.md) for the override table and the separate
workflow for an institutional fork. A brand-role override is not a complete rebrand.

## Verification

- Sass compiled successfully; CSS, source map and utility reference regenerated.
- 110 headless Chrome checks passed, including ten new shared-override checks.
- All non-custom computed CSS properties matched the pre-change snapshot across 83 fixture
  elements at 1280 × 900. This is fixture evidence, not a full-player or cross-browser audit.
- Overrides verified brand, spacing, body font and size, heading sizes, bold weight, control
  radius, overlay shadow, duration/easing and continued use of a legacy component override.
- The colour test disables the player's header transition while reading its target colour.
- `_cu-tokens.scss` is byte-identical to the pre-change copy; no old Sass token references remain.
- Generated-reference sync and coverage checks passed; `git diff --check` passed.

The existing real-player, Welsh and export follow-ups remain in the release checklist.

## Change-set record

Recorded on `feature/cardiffuni-v3-ds-v1.3` with the commit titled
`refactor(cardiffuni-v3): consolidate tokens and reconcile theme documentation`.
The same change set includes the preceding review tidy-up: ink focus fallbacks, stricter
fixture checks, legacy list warnings, updated v1.4 metadata, current README/theming guidance,
and the preserved migration baseline. The compiled stylesheet, source map and generated
reference are included. The [review](../reviews/2026-09-20-final-branch-review.md),
[test record](../test-rounds/2026-09-phase1.md) and
[follow-up checklist](../plans/2026-09-21-follow-up.md) distinguish completed work from
remaining player checks and wider migration work. The upstream issue report is a local draft.

This records local changes only; no push, merge or deployment is included.

## Addendum: `--color-light` is an off-white again (21 September, later)

`--color-light` and `--color-white` were the same white. That was not a side effect of the
consolidation: v2 defined `light` as `#f9fafb` ("off-white for backgrounds"), and the first v3
commit set it to white on purpose, noting "v2 used off-white #f9fafb", to follow the design
system's white "main paper". The only consumer was `--color-bg-body`, so the token decided the
page background.

Nan asked for the off-white back, but not for the page. Decisions:

- `--color-light` is `color-mix(in srgb, var(--cu-bg) 50%, var(--cu-surface) 50%)`: half way
  between the design system's white and its grey-10 surface, about `#F9F9F9` (248.5 per channel).
  It is neutral, has no raw hex, and follows both shared roles; v2's `#f9fafb` has a faint blue
  tint that no design-system grey has.
- `--color-bg-body` now uses `--cu-bg` directly, so **the page background is unchanged and stays
  white**. Nothing rendered by the theme uses `--color-light`; it is available to authors and
  appears in the colours demo.

Verification: 229 checks pass (225 before). Four new checks cover the value (off-white, neutral,
follows the shared roles when grey-10 is overridden) and that the page background is white; the
first and last of those failed or passed as expected before the change.
