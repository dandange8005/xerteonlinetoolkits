# cardiffuni-v3 — migration to the Cardiff Resource Design System

Working notes for moving the Xerte site theme onto the shared Cardiff design system.
Written 17 September 2026. Update it as the work proceeds.

## Goal

`cardiffuni-v3` is a fork of `cardiffuni-v2` restyled to follow the **Cardiff Resource
Design System v1.3**. Xerte keeps its own page structure — top navbar, header banner,
sidebar contents list, sections, footer. Only the visual language changes: colour roles,
typography, controls, spacing, rules and restrained red.

The reference guide page is **not** a layout to copy. It is an example of the design
language applied to one page.

### Sources

| What | Where |
|---|---|
| Specification | `design-system/DESIGN.md` (spec v1.3) in the Cardiff University Design System vault project |
| Tokens and component CSS | `design-system/v1/tokens.css`, `components.css` |
| Implementation and host notes | `design-system/Implementation.md` |
| Visual reference | `design-system/cardiff-resource-design-guide.html` |
| Theme audit and task list | `design-system/cardiffuni-v3 Mapping.md` |
| Phase 1 plan | `docs/plans/2026-09-19-phase1-theme-slice.md` (this repo) |

Vault path: `10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/design-system/`

The design system is Nan's prototype system. It is not an approved institutional brand
standard, and its font stacks are fallbacks, not licensed Marr Sans / Darby Serif.

## Status

| Step | State |
|---|---|
| 1. Fork the theme and remap tokens | **Done** |
| 2. Page layout: navbar, header, sidebar, sections, footer | Not started |
| 3. Components: tabs, accordions, cards, callouts, alerts, tables | Not started |
| 4. Test in Xerte, both languages, keyboard, zoom, narrow widths | Not started |
| 5. Tidy docs, preview image and the Medr override | Not started |

Nothing outside `themes/site/cardiffuni-v3/` has been touched. `cardiffuni-v2` and any
project using it are unaffected. The folder is still untracked in git.

---

## Step 1 — done

### Theme fork

- Copied `cardiffuni-v2/` to `cardiffuni-v3/`, renamed `cardiffuni-v3.{scss,css,css.map,jpg,info}`.
- `cardiffuni-v3.info`: name `cardiffuni-v3`, display name "Cardiff University v3", enabled.
- Deleted the leftover `.bak` files in `scss/` and `demos/`.
- Demo pages now link `cardiffuni-v3.css`.
- Removed the Inter web font import from `cardiffuni-v3.scss`; the design system uses
  system and Franklin Gothic fallback stacks.

### Token changes

In `scss/_tokens.scss` (primitives) and `scss/_allvariables.scss` (semantic layer).
Values from the specification carry a `[DS]` comment.

| Area | v2 | v3 |
|---|---|---|
| Action colours | none | `--color-action` `#C21F16`, `--color-action-hover` `#A11A12`, `--color-tint` `#F8DADA` |
| Primary button | brand red, 2px border, weight 500, 44px tall | action red, 1px border, weight 700, 48px tall, 12×20px padding, 12px gap |
| Primary outline | red tint mixes | action red with `--color-tint` on hover |
| Secondary outline | charcoal mixes | white fill, charcoal border, grey hover — this is the design system's "secondary" button |
| Ghost button | red text | charcoal text, grey hover |
| Links | `#0645AD`, visited purple | `#045bc6`, visited same as default |
| Focus ring | yellow `#fdcd0d`, 2px offset | `#7F140E`, 2px wide, 4px offset; white ring token for dark panels |
| Status | orange warning, brand-red error | warning `#65501c` on `#faf3dd`, error `#A11A12`, info = link blue |
| Body background | off-white `#f9fafb` | white |
| Fonts | Marr Sans / Inter | body `system-ui`, new `--font-family-display` Franklin Gothic stack, serif for rare numerals |
| Font sizes | fluid 12–16px | no size below 16px; `--font-size-body` 18px, `--font-size-lead` 20px |
| Headings | fluid scale, unused `--h*` tokens | h1 `clamp(44px, 5.5vw, 76px)` 850, h2 `clamp(30px, 3.2vw, 44px)` 800, h3 30px 750, h4–h6 bold body font; line height 1.1 and tracking −0.035em on h1–h3 |
| Radius | 4 / 8 / 12 / 16 / 24px | `sm` and `md` 3px for controls; `lg`, `xl`, `2xl` flattened to 0; `--radius-card` 0 |
| Shadows | small and medium in use | `none`; `lg`/`xl` kept **for overlays only** |
| Spacing | 8px rhythm, no 28/36/56 | added `--spacing-7` 28px, `-9` 36px, `-14` 56px |
| Container | 1280px | 1240px |
| Motion | 150ms `ease` | 160ms `cubic-bezier(.16, 1, .3, 1)` |
| Control sizes | 44px touch target | plus `--min-input-height` 56px, `--min-textarea-height` 112px, 48px buttons |

### Other step 1 edits

- `scss/_base-elements.scss`: `body` now uses `--font-size-body` and line height 1.6.
  h1–h6 were hardcoded to the size scale; they now read the `--h1-…`–`--h6-…` tokens,
  which v2 defined but never used. Heading sizes are therefore controlled from
  `_allvariables.scss` alone.
- Replaced the `#fdcd0d` focus-ring fallbacks in `_base-elements.scss` and
  `_bootstrap-components.scss` with `2px solid #7F140E`.

### Verification done

`npx sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map` compiles with no errors
or warnings. Compiled values spot-checked (`--color-action`, `--radius-md: 3px`,
`--shadow-md: none`, `--h1-font-size`, `--color-link-default`).

**Not yet verified visually.** The Claude in Chrome extension was not connected, so no
screenshots were taken and the theme has not been opened in Xerte.

---

## Decisions already made

- **Fork rather than edit v2**, so live projects keep their current appearance.
- **Nothing below 16px.** The specification sets 16px as the minimum for labels,
  captions and controls, so `--font-size-xs` and `--font-size-sm` now both resolve to
  16px. Badges, small buttons and captions are noticeably larger than in v2. Revisit if
  any Xerte component breaks.
- **Overlay shadows kept.** `--shadow-lg`, `-xl` stay defined for Bootstrap dropdowns
  and modals, which the design system has not specified ("define and review overlay
  elevation separately"). Everything else is flat.
- **Filled charcoal `btn-secondary` left alone** for now. The design system's secondary
  button is v2's `btn-secondary-outline`. Decide in step 3 whether to swap them.
- **Breakpoints unchanged** at 640 / 768 / 1024px. The design system uses 480 / 800 /
  1100px, which shifts layouts, so it belongs with the layout work.
- **Visited links** use the default link colour, since the specification defines no
  separate visited state. Worth a second look for long reference pages.

## Open question — header banner

Needs a decision before step 2:

1. **Charcoal banner (recommended).** A solid charcoal `.jumbotron` with white title and
   light-grey subtitle. Uses the specification's optional dark panel, keeps a strong band
   at the top and suits a logo.
2. **White banner with a thin red top edge.** Closer to the reference guide's own header,
   quieter overall, less separation from the content below.

Either way: no gradient, no black overlay, no shadow.

---

## Step 2 — page layout (not started)

All in `scss/_layouts.scss` unless noted. Xerte's markup and JavaScript stay untouched;
the selectors below already exist.

| Xerte part | Selector | Change |
|---|---|---|
| Header banner | `.jumbotron`, `#pageTitle`, `#pageSubTitle` | Remove the grey gradient and the `::before` 50% black overlay. Apply the chosen option above. Title in the display font. |
| Top navbar | `.navbar`, `.navbar-inverse .navbar-inner` | White bar, 1px `--color-border-default` rule below, no shadow (`.navbar` still sets `--shadow-sm`). |
| Navbar hover and current page | `.navbar-inverse .nav > li > a:hover`, `.navbar .nav > li.activePage > a` | Charcoal text and a charcoal inset underline instead of red (lines 119, 128–129). |
| Sidebar contents list | `.bs-docs-sidenav`, `.nav-list > .active > a` | Square corners (drop the `--radius-md` corner rules), 1px rules between items, active item charcoal not red (line 145–146). Base template adds its own 6px radius and shadow in `modules/site/parent_templates/site/common/css/custom.css`, so override both. |
| Sections | `.evenSection`, `.oddSection` | Both white. Separate with a 1px top rule and section padding of 44 / 56 / 64px. |
| Section and content titles | `h2.sectionTitle`, `h3.contentTitle` in `_base-elements.scss` | Charcoal, display font, heading weight; drop the red and the light weight (line 158). |
| Footer | `.footer` | Charcoal, white text, 1px rule or a thin red top edge. |
| Back to top | `.top-round` in `_xerte-components.scss` | Action red, no shadow. |
| Feedback button | `#feedback_button` | Action red, drop the `box-shadow`, 3px radius. |
| Glossary tooltip | `.glossaryTip` in `_xerte-components.scss` | Charcoal background rather than brand red. |

## Step 3 — components (not started)

Mechanical part, measured in the current v3 tree:

- **20 hardcoded `border-radius` / `box-shadow` declarations** that tokens cannot reach:
  `_bootstrap-components.scss` (10), `_layouts.scss` (6), `_utilities.scss` (3),
  `_base-elements.scss` (1). A further 60 declarations already read tokens and are
  flat or 3px as a result.
- **24 colour codes written out by hand** outside the two token files.
- **29 references to `--color-brand-primary`** outside the token files. Each needs a
  decision: keep as a fine brand mark, change to `--color-action` for a primary action,
  or change to charcoal. Largest groups: `_base-elements.scss` (9),
  `_bootstrap-components.scss` (7), `_layouts.scss` (6), `_xerte-components.scss` (3).
  The aim is a small red footprint, roughly 5% of a viewport.

Components the design system does not define, so each needs a judgement call:
tabs and pills, accordions, alerts, breadcrumbs, badges, progress bars, tables,
carousels, and the custom components in `scss/components/` (boxes, callouts, cards,
quotes, details, dos-and-donts, project info, language).

Guidance to apply: flat, square panels, 3px on controls, 1px grey rules between repeated
rows instead of boxes, charcoal for selected states, red only for a primary action,
status colours only where the content carries that meaning.

## Step 4 — testing (not started)

- Docker: `docker compose up -d --build`, then http://localhost:8080.
- Demo pages: `themes/site/cardiffuni-v3/demos/` — `components.html`, `typography.html`,
  `forms.html`, `colors.html`, `base-elements-demo.html`, `lists-tables.html`,
  `patterns.html`, `images-media.html`, `flexbox.html`, `code-utilities.html`.
  Compare side by side with the v2 versions.
- A real Xerte site project switched to "Cardiff University v3": check the header,
  navbar, sidebar, section rules, tabs, accordions, tables and the footer.
- Check the 18px body text and the large h1 against Xerte's navigation, tables and
  interactive page types.
- Keyboard focus, 200% zoom, reduced motion, narrow widths, and Welsh labels (longer
  words need room to wrap).

## Step 5 — tidy up (not started)

- `README.md` and `THEMING-GUIDE.md` still describe v2 throughout.
- `themes/medr-theme.css` names v2 in its header comment and its usage example; its
  override values may also need revisiting against the new tokens.
- `cardiffuni-v3.jpg` is still v2's preview image. Regenerate once the look settles.
- `cardiff-design.json` holds v2's design tokens as JSON. Either update it from the new
  values or delete it if nothing reads it.
- Consider whether the design system's interactive patterns (guided activity, resource
  directory) belong here at all. `Implementation.md` in the vault suggests loading
  `components.css` and `components.js` per project inside a `.cu-resource` wrapper, with
  a `contentLoaded.cuResource` adapter — keeping them out of the theme.
- Note for the vault: `design-system/v1/conversation.html` and `discovery.html` are
  empty (0 bytes) although the documentation describes them as example fragments.

## Commands

```bash
# compile after editing SCSS (run in the theme folder)
npx sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map

# find work left in step 3
grep -rn -E '(border-radius|box-shadow)\s*:' scss --include='*.scss' | grep -v 'var(--'
grep -rn 'color-brand-primary' scss --include='*.scss' | grep -v '_allvariables\|_tokens'
grep -rn -E '#[0-9a-fA-F]{3,8}\b' scss --include='*.scss' | grep -v '_tokens.scss\|_allvariables.scss'
```
