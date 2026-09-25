# Cardiff Learning Resource UI — Design System
<!-- v1.0 | 2026-09-17 -->

The reusable visual language Nan approved in the Assessment Menu landing-page review. Apply it to future Codex-generated assessment and learning-resource interfaces. This is a project UI system, not a replacement for Cardiff University's corporate brand guidelines.

**Accepted:** colour roles, typography, buttons, spacing, horizontal rules, restrained red and purposeful icons. **Still open:** landing-page composition and list versus grid. The six-question conversation is a component to retain and assess for Xerte integration.

Organisation: keep Codex-generated outputs in this `codex/` folder. Other-model prototypes and original assets remain in the parent folder. See [[2-lane Assessment/Outputs/assessment-menu/codex/README|Codex output index]].

Canonical implementation: `design-system/v1/tokens.css`, `components.css` and `components.js`. Visual reference: [[2026-09-17_assessment-menu-design-system-v1.html]]. The original three landing pages are the extraction sources; their page layouts are not mandatory templates.

## 1. Visual Theme & Atmosphere

Clear, institutional and content-led. White space, strong charcoal typography and fine horizontal rules carry the hierarchy. Controls look precise and useful. Red is an occasional signal for a primary action or a brand edge, rather than a background treatment for whole sections.

Keep content easy to scan without turning every paragraph into a card. Quiet grey panels group a working area. Lists and grids use the same typography, border language and link treatment. A restrained dark panel is an optional composition device, not a second theme.

The system must work for staff reading guidance and discussing assessment design. It should feel recognisably Cardiff while allowing different page structures. It does not depend on animation, stock imagery or decorative illustrations.

## 2. Color Palette & Roles

All values are extracted from the reviewed prototypes. Tokens are scoped to `.cu-resource` to avoid changing the surrounding Xerte player.

| Token prefix `--cu-` | Value | Role and intent |
| --- | --- | --- |
| `bg` | `#FFFFFF` | Main paper and button text on dark fills. |
| `surface` | `#F2F2F2` | Quiet grouping, input hover and working areas. |
| `ink` | `#121212` | Main text, selected filters/steps, strong boundaries. Never substitute pure black. |
| `muted` | `#666666` | Supporting text, captions and field borders. |
| `border` | `#CCCCCC` | Standard 1px rules and control boundaries. |
| `line` | `#E5E5E5` | Subtle internal divisions; not the sole boundary of an essential input. |
| `red` | `#E4251B` | Cardiff brand mark and occasional fine top rules. |
| `action` | `#C21F16` | Primary button fill, providing stronger small-text contrast than bright brand red. |
| `action-hover` | `#A11A12` | Primary hover; error text where paired with an explanation. |
| `tint` | `#F8DADA` | Optional restrained red highlight. Not the default surface. |
| `link` | `#045bc6` | Underlined body links on light surfaces. |
| `focus` | `#7F140E` | Keyboard outline on light surfaces. |
| `success` | `#07873E` | Success cue with text or a check; not a new decorative accent. |
| `warning`, `warning-bg` | `#65501c`, `#faf3dd` | Proposed/draft label, with explicit wording. |
| `lane1`, `lane1-bg` | `#1d5c8f`, `#e8f1f8` | Lane 1 identity, always accompanied by its name. |
| `lane2`, `lane2-bg` | `#276c44`, `#e9f5ee` | Lane 2 identity, always accompanied by its name. |
| `on-dark`, `on-dark-muted` | `#FFFFFF`, `#CCCCCC` | Text on charcoal. Focus rings and links become white there. |

**Red discipline:** aim for a small accent footprint, approximately 5% or less of a typical viewport. This is a design heuristic, not a measured brand rule. Prefer one clear primary action per task area. Avoid red-filled banners, red body links, red text on charcoal, or red on every divider. Selected categories and steps are charcoal, not red.

## 3. Typography Rules

- Display: `'Franklin Gothic Heavy', 'Franklin Gothic', system-ui, sans-serif`.
- Body/UI: `system-ui, -apple-system, 'Segoe UI', sans-serif`.
- Rare numerical accent: `ui-serif, Georgia, 'Times New Roman', serif`.

These are the html-it Cardiff theme's substitutes for Marr Sans and Darby Serif. They are not the licensed brand fonts. Font availability changes rendering between devices; preserve the stack unless the actual licensed assets are supplied.

| Role | Size | Weight | Line height / tracking |
| --- | --- | --- | --- |
| Display title | `clamp(44px, 5.5vw, 76px)` | 850 | 1.1 / −0.035em |
| Section heading | `clamp(30px, 3.2vw, 44px)` | 800 | 1.1 / −0.035em |
| Component heading | 30px | 750 | 1.1 / −0.035em |
| Current design question | `clamp(30px, 3vw, 42px)` | 750 | 1.1 / −0.035em |
| Entry name | 20px | 700 | 1.35 / normal, body stack |
| Lead paragraph | 20px | 400 | 1.55 / normal |
| Body, labels, captions | 16px minimum | 400; labels 700 | 1.6 / normal |
| Button | 16px | 700 | 1.6 / normal |
| Occasional step numeral | 32–60px | 400, serif | 1–1.2 / normal |

The original Editorial hero used up to 88px and −0.05em. Treat that as an optional large-title variant, not the default of every page. The v1 component guide standardises on the quieter Studio scale above. Do not shrink body copy to make a layout fit. Keep prose at about 45–68 characters per line where space permits. Use upright headings and tabular numerals for aligned counts.

## 4. Component Stylings

### Buttons and interaction states

Primary: 1px `action` border/fill, white text, 3px radius, 12px × 20px padding, 48px minimum height, 12px icon gap. Secondary: white fill, charcoal text and 1px charcoal border, same geometry. Do not apply gradients, shadows or pill shapes.

| State | Treatment |
| --- | --- |
| Default | As above. Native button or anchor with a real destination. |
| Hover | Primary becomes `action-hover`; secondary becomes `surface`. |
| Active | 1px downward translation for enabled buttons; removed under reduced motion. |
| Keyboard focus | Instant 2px `focus` outline, offset 4px; white outline in a dark panel. No animated focus. |
| Disabled | Native `disabled`, opacity .5, not-allowed cursor; use only when the action is actually unavailable. |
| Busy, if a future operation needs it | Preserve width and label, add `aria-busy`, prevent duplicate submission. No fake loading on immediate local actions. |
| Export success | Concise adjacent live status, “Copied.” No celebratory animation. |
| Export failure | Visible labelled textarea, focus and select its contents, plus manual-copy instructions. Do not claim clipboard success. |

Icon-only control: 48px square, 1px neutral border, white fill, 24px symbol, accessible name. The label always identifies the action.

### Fields

Visible bold label above the field with an 8px gap. Inputs: 56px minimum height, 12px × 16px padding, 1px `muted` border, 3px radius, white background. Textareas: 112px minimum height and vertical resize. Hover uses `surface`; focus uses the same outline as buttons. Keep border thickness unchanged between states.

Error: `aria-invalid="true"`, 1px action-red border and specific text connected with `aria-describedby`. Disabled fields use native `disabled` and opacity .5. Do not invent validation on optional discussion notes. A completed field's value normally provides enough feedback without a success badge.

### Rules, groups, labels and icons

- Repeated entry: 1px neutral top rule, 20px vertical padding; no card border/shadow.
- Major boundary: 2px charcoal rule. Quiet section: 1px neutral rule and larger spacing.
- Grey workspace/panel: square edges, 24–40px internal padding.
- Question panel: white, optional 4px brand-red top rule. This is one focal mark, not a rule for every panel.
- Draft label: warning colours, 4px × 8px padding, 16px text, wording that states the status.
- Prototypes use small `→`, `←`, `↓`, `↗` and `✓` symbols. Keep their meaning consistent. `↗` means leaving the current page; it does not promise a new browser tab.
- Decorative icons next to visible text use `aria-hidden="true"`. Icon-only actions need an accessible name. Never use icons as the only indication of a state.
- Additional pictograms should use **Ionicons Sharp**, as specified in the vault's [[06 Elements]]. Do not describe the existing glyphs as an installed icon library; no icon dependency is bundled here.

### Six-question conversation

The question wording and authoring content stay in HTML. The reusable script handles navigation, temporary notes, current-step labels, note marks and copy fallback. Each instance needs a stable, unique `data-cu-conversation` key. Reuse that key for the same component when Xerte recreates its page; use a new key for a different question set.

Keep the navigation and note-taking controls keyboard-operable. Focus the new question heading after a deliberate step change. Without JavaScript, all six questions and their labelled note fields remain visible; enhancement-only controls remain hidden. Temporary state survives page reinsertion within the same open player, but not a reload or close. Do not add storage, analytics, model calls or server submission without a separate requirement.

### Assessment discovery

Keep a labelled search field, category buttons, result count, reset and useful empty state. Grid and list are **equal variants**, not separate content sets. Switching view must preserve the search query and category selection. Grid: three columns above 1100px, two to 480px, one below. List: one column throughout. Both use the same 17 records and direct entry links. The final product default remains undecided.

## 5. Layout Principles

Use a 4px base: **4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 80, 96px**. The token suffix denotes multiples of four, so `space-7` is 28px.

| Situation | Typical spacing |
| --- | --- |
| Icon/label and related controls | 8–12px |
| Within a content group | 16–24px |
| Entry grid gutters | 28px |
| Split content / question navigator | 28–40px |
| Major paired sections | 64px |
| Section padding | 44px narrow, 56px medium, 64px desktop; 80px for spacious landing sections |
| Desktop container | max 1240px; width `calc(100% - 96px)` |

Only radius tokens needed in v1: **0** for structural panels and **3px** for controls. Use `minmax(0,1fr)` for flexible grid tracks. Let long headings wrap inside their container. A page may be editorial, a directory, or a workbench while retaining this system.

## 6. Depth & Elevation

| Level | CSS | Use |
| --- | --- | --- |
| Flat | `box-shadow:none` | All v1 panels, buttons and entries. |
| Ambient / Standard / Elevated / Deep | Not defined | Do not invent these styles to fill a generic component catalogue. |

Depth comes from a subtle surface change, a boundary and spacing. The reviewed pages do not need floating cards. Define and review overlay elevation separately if a future product actually needs a dialog or popover.

## 7. Do's and Don'ts

**Do** preserve the restrained Cardiff palette; use blue underlined text links; separate repeated entries with hairlines; keep body text at 16px or larger; use labelled controls with visible focus; preserve source/status boundaries; scope portable styles to `.cu-resource`; let users compare list/grid without changing the data.

**Don't** rotate to another theme on the next page; flood the page with red; turn every section into a rounded card; invent shadows, icons, testimonials or assessment ratings; hide policy caveats inside a tooltip; treat a proposed D1 statement as agreed; promise persistent notes; present the English specimen as an approved bilingual publication; apply the component stylesheet globally to Xerte.

For Assessment Menu outputs, retain the six questions, guidance-not-policy statement, 17-type discovery and links to wider guidance. Welsh translations need language review. The previous Xerte Option C guide suggested omitting draft labels; Nan's latest instruction takes precedence: **keep D1 visibly proposed until agreed**.

## 8. Responsive Behavior

| Range | Behaviour |
| --- | --- |
| Above 1100px | 48px outer margins; 3-column discovery grid; 250px question navigation rail. |
| 801–1100px | 32px margins; 2-column grid; 220px navigation rail and 24px workspace gap. |
| 481–800px | 20px margins; paired sections stack; question steps wrap into rows; search controls stack. |
| 480px and below | 16px margins; 1-column discovery; 16px workspace padding; button rows wrap. |

Keep touch controls at least 44px, primary/secondary buttons at least 48px. Avoid horizontal overflow by fixing widths and wrapping layouts, not by clipping the host Xerte page. Reduce animation and remove the press translation when reduced motion is requested. The standalone showcase is an English component guide; allow additional space when adapting the interface for Welsh.

## 9. Agent Prompt Guide

Quick palette: paper `#FFFFFF` · surface `#F2F2F2` · ink `#121212` · muted `#666666` · rule `#CCCCCC` · brand `#E4251B` · action `#C21F16` · link `#045bc6` · focus `#7F140E`.

1. **New resource:** “Read `codex/DESIGN.md`. Create a Cardiff learning-resource page using its tokens and component styles. Use a structure that suits the content; keep the shared visual system.”
2. **Landing-page composition:** “Combine the six-question conversation with simple assessment discovery. Keep list and grid available for review; do not infer a chosen default.”
3. **Xerte adaptation:** “Use the portable v1 HTML/CSS/JS and the Xerte integration note. Scope the component, initialise on `contentLoaded`, preserve notes across page recreation, and test editor save/reload.”
4. **Content update:** “Change the supplied wording while preserving the design system, exact six-question framing, draft policy status and wider-guidance links.”
5. **New component:** “Add this component using the existing tokens. Document new states and responsive behaviour; introduce no new palette, shadow or icon family without a reason.”
6. **Audit:** “Check this output against DESIGN.md: colours by role, text sizes, spacing, rule hierarchy, focus, narrow-screen layout, export failure handling and content provenance.”

## Sources and exports

- [[2026-09-17 Assessment Menu Design Review]] — Nan's accepted visual preferences, open layout choices and Codex-folder instruction.
- The three `2026-09-16_assessment-menu-landing-…-v1.html` files and [[2026-09-16_landing-design-notes-v3]] — implementation and provenance.
- html-it theme 12, Cardiff University; [[Cardiff Design Tokens]]; [[06 Elements]].
- [[Assessment Menu - Xerte Build Guide (Home Page, Option C)]] — existing local integration context, checked against the source code on 17 September.
- `design-system/v1/tokens.css` — canonical scoped token values.
- `design-system/v1/components.css` — scoped reusable visual implementation.
- `design-system/v1/components.js` — conversation and discovery enhancement.
- `design-system/v1/conversation.html`, `discovery.html` — editable HTML fragments; discovery URLs must be adapted for the destination player.
- `design-system/v1/Xerte Integration.md` — exact installation steps, evidence and remaining checks.

Future changes should deliberately version this system. Do not silently change the accepted visual language to accommodate a new layout.
