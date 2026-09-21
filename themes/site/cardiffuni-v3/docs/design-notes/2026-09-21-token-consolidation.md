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
