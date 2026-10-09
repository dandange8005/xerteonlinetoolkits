# Cardiff University theme migration status

Updated 29 September 2026. The theme follows the Cardiff Resource Design System v1.7;
Phase 1 began against v1.3, adopted v1.4's short callout markup on 20 September, and applied
the red-usage rules of v1.5 to v1.7 on 23 September. This is Nan's prototype design system,
not an approved institutional brand standard.

Developed as `cardiffuni-v3`; renamed `cardiffuniversity` ("Cardiff University Theme") on
24 September 2026. The runtime files live in `themes/site/cardiffuniversity/`; sources, demos
and tests live here in `theme-src/cardiffuniversity/`. Projects using v2 keep their theme.
The dated plans and reviews written during development were removed on 24 September 2026 and
remain in git history. The design notes and the Phase 1 test round were restored on
29 September to [development records](docs/README.md).

## Current state

| Area | Status |
| --- | --- |
| Tokens | Kept in `tokens/tokens.json` and generated into `_cu-tokens.scss`; compatibility aliases and Xerte-only settings in `_allvariables.scss` |
| Phase 1 layout | White header without a top rule (left-logo, right-logo and two-logo headers in one row), charcoal navbar, quieter selected sidebar, section headings and visible focus rings; header and navbar colourways available per project |
| Components | Rules, seven callout variants, page frame parts (footer, feedback tab, back-to-top, glossary tip), alerts, badges, progress bars, tables, wells, lead text, carousel controls and panels implemented; card headings resized; tabs and accordions deliberately left as they are |
| Theming | `--color-brand-primary` and `--color-brand-secondary` restyle every brand-coloured part |
| Navigation | Sticky height, player lifecycle, menu resizing and reader takeover fixes committed; smooth scrolling removed |
| Validation | Docker Xerte rounds passed, including editor retention, export and re-import, Welsh-language labels, narrow screens, 200% zoom and keyboard traversal; 295 automated checks pass |
| Release | Phase 1 merged into develop on 23 September 2026 |

The charcoal navbar and red-rule selected sidebar were approved during testing. Current focus
colour is ink, `#121212`.

The [pre-merge player check](docs/test-rounds/2026-09-phase1.md#pre-merge-player-check-23-september-2026)
on 23 September passed base elements, the header, navbar, section menu and footer, and the
custom and Bootstrap components, including tables, alerts, badges, progress bars and cards.
Automated checks cover the later work, but these have not yet been run in the real player:

- Everything from 24 September on: the header without a top rule, header and navbar
  colourways, the panel frame and title label, brand-colour theming, and the 28 September
  changes (brand-primary icon lists and progress bars, action-coloured checkboxes and radio
  buttons, font sizes below 16px).
- The feedback tab, back-to-top button and glossary tip, which the check did not list.
- Possibly the field borders, skip link, wells, lead text and carousel controls committed on
  the evening of 23 September: the record does not say whether the check came before or
  after them.

## Remaining work

### Theme

- [ ] Navbar current-page marker: the 3px primary marker on the current-page fill is 2.76:1 for
  Cardiff red on grey-90 (3:1 is needed for a state indicator). Pre-existing; decide whether
  the fill, the marker or the requirement changes.
- [ ] Confirm whether project-specific interactive patterns stay in project-level adapters.

### Known limitations

Left as they were on purpose, or found and not fixed. Each is still true of the current SCSS;
the linked note has the detail.

- **Tables** ([note](docs/design-notes/2026-09-21-tables.md)). A wide table that an author does
  not wrap in `.cu-table-scroll` still stretches the page; automatic containment was declined.
  Nothing checks that authors give the wrapper `tabindex="0"`, `role="region"` and an
  `aria-label`. The header style, row hover and `.table-bordered`, `.table-hover` and
  `.table-condensed` were not reviewed.
- **Page frame** ([note](docs/design-notes/2026-09-21-page-chrome.md)). The feedback tab's
  markup was inferred from the v2 CSS and has not been checked against a real project. The tab
  stays at `top: 62%` on narrow screens and may overlap content. In the footer's "replace"
  mode the player's inline 10px left margin on `#customFooter` misaligns it with the page. The
  glossary tip keeps the base template's 4px radius.
- **Cards, tabs and accordions** ([note](docs/design-notes/2026-09-21-cards-tabs-accordions.md)).
  Tabs and accordions were not reviewed, restyled or tested in this migration. Cards keep a
  3px corner and a large shadow on `.card--clickable:hover` (both kept on purpose, 9 October
  2026) and `transition: all`. The 1.05 image zoom on hover was removed on 9 October 2026.
- **Focus on dark panels and the alert close button** ([note](docs/design-notes/2026-10-09-dark-focus-and-alert-close.md)).
  Reverse buttons, and any button in `.bg-dark`, show a white focus ring; the alert close button is a
  44px target. Both follow the design system.
- **Progress bars** ([note](docs/design-notes/2026-09-21-alerts-badges-progress.md)).
  Bootstrap's light gradient covers the grey-20 track, so the track token has never been
  visible; the contrast checks measure against grey-20, the darker case.
- **Header logos** ([note](docs/design-notes/2026-09-21-header-logos-and-callout-titles.md)).
  Widths below about 485px, very wide or very tall partner logos, and the base template's 480px
  rule are untested. A small partner logo is never scaled up.

### Author guide

The proposal behind these items is in the
[documentation system design note](docs/design-notes/2026-09-20-documentation-system.md).

Phase 1 of the [author guide](docs/design-notes/2026-10-06-author-guide.md) is built: the
generator, the five build checks, Getting started, one task page and the callout component.
It is not published. Phase 2a adds the reference pages (colours, type and spacing, utility
classes), an honest "Not tested in the Xerte editor yet" state for component records, one source
for task and component links, and a check for unbalanced example HTML. Phase 2b adds seven more
components, in small batches (batch 1: buttons and alerts; batch 2: cards and tables), and
phase 2c more task pages.

- [ ] Bundle the external placeholder images used by the demos.
- [ ] Decide whether the guide stays bundled or also gets a published home, and who maintains it.
- [x] Decide whether component records live in the theme or the shared design system: in the
  theme ([ADR 0001](docs/adr/0001-component-records-live-in-the-theme.md)).
- [ ] Start with seven or eight frequently used components: one source for each example, usage
  advice and editor evidence.
- [ ] Add task-oriented author pages, then migrate the remaining demonstrations gradually.
- [ ] Strengthen `build-reference.py --coverage` to recognise deliberate documentation rather
  than arbitrary dotted prose.
- [ ] Make the CSS parsing in `build-reference.py` string-aware before relying on it for more
  complex generated values.
- [x] Introduce example, class and accessibility checks and generated-content drift checks
  incrementally. Done in phase 1 (checks 1 to 5).

### Upstream

- [ ] Report the malformed theme script tag to Xerte. In
  `modules/site/parent_templates/site/common/js/application.js`, `cssSetUp('theme')` appends
  `'<script src="'+ themePath + theme + '/'+ theme+ '.js"' + '</script>'`, which has no `>`
  after the `src` value. The fix is `'.js">' + '</script>'`. jQuery still loads the script, so
  this is a markup correction; confirm the script still loads once in editor preview, playback
  and a standalone export. Not yet submitted.

## Sources

The theme was built from the Cardiff Resource Design System, kept in the Obsidian vault at
`10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/design-system/`
(`DESIGN.md` for intent, `cardiffuni-v3 Mapping.md` for the broader migration). Since
24 September 2026 the theme keeps its own tokens in `tokens/tokens.json`; the design system
is a reference, not a build input. For build and check commands see [THEMING-GUIDE.md](THEMING-GUIDE.md).
