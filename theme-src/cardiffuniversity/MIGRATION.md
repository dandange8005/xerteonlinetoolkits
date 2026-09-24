# Cardiff University theme migration status

Updated 24 September 2026. The theme follows the Cardiff Resource Design System v1.7;
Phase 1 began against v1.3, adopted v1.4's short callout markup on 20 September, and applied
the red-usage rules of v1.5 to v1.7 on 23 September. This is Nan's prototype design system,
not an approved institutional brand standard.

Developed as `cardiffuni-v3`; renamed `cardiffuniversity` ("Cardiff University Theme") on
24 September 2026. The runtime files live in `themes/site/cardiffuniversity/`; sources, demos
and tests live here in `theme-src/cardiffuniversity/`. Projects using v2 keep their theme.
The dated plans, design notes, reviews and test rounds written during development were
removed on 24 September 2026 and remain in git history.

## Current state

| Area | Status |
| --- | --- |
| Tokens | Kept in `tokens/tokens.json` and generated into `_cu-tokens.scss`; compatibility aliases and Xerte-only settings in `_allvariables.scss` |
| Phase 1 layout | White header without a top rule (left-logo, right-logo and two-logo headers in one row), charcoal navbar, quieter selected sidebar, section headings and visible focus rings; header and navbar colourways available per project |
| Components | Rules, seven callout types, page chrome (footer, feedback tab, back-to-top, glossary tip), alerts, badges, progress bars, tables, wells, lead text, carousel controls and panels implemented; card headings resized; tabs and accordions deliberately left as they are |
| Theming | `--color-brand-primary` and `--color-brand-secondary` restyle every brand-coloured part |
| Navigation | Sticky height, player lifecycle, menu resizing and reader takeover fixes committed; smooth scrolling removed |
| Validation | Docker Xerte rounds passed, including editor retention, export and re-import, Welsh-language labels, narrow screens, 200% zoom and keyboard traversal; 295 automated checks pass |
| Release | Phase 1 merged into develop on 23 September 2026 |

The charcoal navbar and red-rule selected sidebar were approved during testing. Current focus
colour is ink, `#121212`.

Automated checks cover the later work, but the page chrome, alerts, badges, progress bars,
tables, card headings, panel title label and brand-colour theming have not yet been run in the
real player.

## Remaining work

### Theme

- [ ] Navbar current-page marker: the 3px primary marker on the current-page fill is 2.76:1 for
  Cardiff red on grey-90 (3:1 is needed for a state indicator). Pre-existing; decide whether
  the fill, the marker or the requirement changes.
- [ ] Confirm whether project-specific interactive patterns stay in project-level adapters.

### Author guide

- [ ] Bundle the external placeholder images used by the demos.
- [ ] Decide whether the guide stays bundled or also gets a published home, and who maintains it.
- [ ] Decide whether component records live in the theme or the shared design system.
- [ ] Start with seven or eight frequently used components: one snippet source, examples, usage
  and editor validation evidence.
- [ ] Add task-oriented author pages, then migrate the remaining demonstrations gradually.
- [ ] Strengthen `build-reference.py --coverage` to recognise deliberate documentation rather
  than arbitrary dotted prose.
- [ ] Make the CSS parsing in `build-reference.py` string-aware before relying on it for more
  complex generated values.
- [ ] Introduce snippet, class and accessibility checks and generated-content drift checks
  incrementally.

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
