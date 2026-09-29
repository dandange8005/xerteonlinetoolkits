# Development records

Design notes and test evidence from the theme's development, 20 to 24 September 2026. They
record why each decision was made, which options were rejected, and what was deliberately left
alone. Current state and open work are in [migration status](../MIGRATION.md); these notes are
the reasoning behind it.

The split into `theme-src/` on 24 September (`d2230537a`) removed these files. They were
restored unedited on 29 September 2026, so they still use the old names and paths:

- `cardiffuni-v3` is now `cardiffuniversity`, and `themes/site/cardiffuni-v3/` is split between
  `themes/site/cardiffuniversity/` (runtime) and this folder (sources).
- Check counts are as they stood on each note's date.
- Later commits changed some decisions. On 28 September icon lists and progress bars moved to the
  brand primary (`20bd9a7d0`), selected checkboxes and radio buttons to the action colour
  (`f112b010c`), and the xs and sm font sizes below 16px (`7011b9941`). The
  [red-usage note](design-notes/2026-09-23-red-usage-remaining.md) has an addendum for the
  colour changes. Where another note and the SCSS disagree, the SCSS and git history are current.
- Links to `../plans/` and `../reviews/`, and to the old `MIGRATION.md` sections, point at files
  that were not restored. Read them from git history:
  `git show d2230537a^:themes/site/cardiffuni-v3/docs/<path>`.

| Record | Covers |
| --- | --- |
| [Documentation system](design-notes/2026-09-20-documentation-system.md) | Proposal for the author guide: component records, generator and lint rules |
| [Alerts, badges and progress bars](design-notes/2026-09-21-alerts-badges-progress.md) | Status colours and contrast; the warning-colour fix |
| [Cards, tabs and accordions](design-notes/2026-09-21-cards-tabs-accordions.md) | Why tabs and accordions were left alone; card heading size |
| [Header logos and callout titles](design-notes/2026-09-21-header-logos-and-callout-titles.md) | One-row header for every logo combination; wrapped callout titles |
| [Page chrome](design-notes/2026-09-21-page-chrome.md) | Footer, feedback tab, back-to-top and glossary tip |
| [Tables](design-notes/2026-09-21-tables.md) | The opt-in `.cu-table-scroll` wrapper, striped rows and captions |
| [Token consolidation](design-notes/2026-09-21-token-consolidation.md) | One source for shared values; `--color-light` |
| [Hardcoded-values audit](design-notes/2026-09-22-hardcoded-values-audit.md) | Details focus bug; the values kept on purpose |
| [Red usage](design-notes/2026-09-23-red-usage-remaining.md) | Where red was removed and why; the required-field asterisk |
| [Fields, skip link and demo pages](design-notes/2026-09-23-fields-skip-link-demo-pages.md) | Field borders, skip link focus, legacy columns, guide navigation |
| [Supporting assets and theming](design-notes/2026-09-23-supporting-assets-and-theming.md) | Secondary buttons, preview image, Medr removal, wells, lead text, carousel, panels |
| [Brand colour theming](design-notes/2026-09-24-brand-colour-theming.md) | The two brand colours, the mixed shades and the contrast an author must check |
| [Phase 1 test round](test-rounds/2026-09-phase1.md) | Real-player checks, including editor retention and export, and the pre-merge player check |
