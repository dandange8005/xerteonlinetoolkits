# cardiffuni-v3 migration status

Updated 21 September 2026. Theme v3 follows the Cardiff Resource Design System v1.4;
Phase 1 began against v1.3 and adopted v1.4's short callout markup on 20 September.
The branch name `feature/cardiffuni-v3-ds-v1.3` records that starting point, not a separate
current specification. This is Nan's prototype design system, not an approved institutional brand standard.

## Current state

| Area | Status |
| --- | --- |
| Tokens | Generated from the design system; duplicate Sass scale removed; compatibility aliases and Xerte-only settings in `_allvariables.scss` |
| Phase 1 layout | White header with red top edge, charcoal navbar, quieter selected sidebar, section headings and visible focus rings implemented |
| Components | Rules, seven callout types and page chrome (footer, feedback tab, back-to-top, glossary tip) implemented; remaining components need migration |
| Navigation | Sticky height, player lifecycle, menu resizing and reader takeover fixes committed; smooth scrolling removed |
| Validation | First Docker Xerte round passed, including editor retention, export and re-import; see the dated test record |
| Documentation | Author demos and generated reference exist; README and theming instructions reconciled on 21 September |
| Release | Phase 1 sign-off and merge decision pending |

The header decision is settled: white with a thin red top edge. The charcoal navbar and
red-rule selected sidebar were approved during testing. The original white-navbar proposal
and stronger red selection are superseded. Current focus colour is ink, `#121212`.

## Remaining work

Use [the follow-up checklist](docs/plans/2026-09-21-follow-up.md) for the next work batches:
review tidy-up, release validation, remaining layout and components, supporting assets,
and the proposed author documentation system. A full Welsh-language pass remains;
the first round checked Welsh glyphs rather than every translated interface.

## Sources and records

- [Phase 1 plan](docs/plans/2026-09-19-phase1-theme-slice.md): historical implementation instructions.
- [Test round and later navigation fixes](docs/test-rounds/2026-09-phase1.md).
- [Branch review](docs/reviews/2026-09-20-final-branch-review.md): original findings with current disposition.
- [Original migration baseline](docs/design-notes/2026-09-17-migration-baseline.md): preserved proposals and early measurements.
- [Documentation-system proposal](docs/design-notes/2026-09-20-documentation-system.md): not yet implemented.

The canonical design-system folder is in the Obsidian vault at
`10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/design-system/`.
`DESIGN.md` defines intent; `v1/tokens.css` supplies tokens; `cardiffuni-v3 Mapping.md`
tracks the broader migration. Read those sources before extending the visual system.

The theme is isolated under `themes/site/cardiffuni-v3/`; projects using v2 keep their theme.
The [token consolidation note](docs/design-notes/2026-09-21-token-consolidation.md) explains
the source-to-alias mapping and supported project overrides. For build and check commands see [THEMING-GUIDE.md](THEMING-GUIDE.md).
