# Changelog — Inclusive Prehabilitation for People with Cancer
## Custom CSS Development Log

---

## 2026-03-06

### Initial setup
- Created `custom.css` in the project folder
- Established CSS custom properties (design tokens) sourced from `design.json`, covering colours, typography, spacing, border radius, and shadows
- Added Google Fonts `@import` for Inter (must remain first line for inline `<style>` delivery)

### How CSS is delivered
- Xerte loads CSS via `xenith.js`: base CSS → theme CSS (xot1.css) → inline `<style id="lo_css">` tag
- Custom CSS is pasted into the **Styles** field in Xerte project properties and published via `data.xml`
- `@import` must be the very first rule; no `!important` needed as custom styles load after the theme

---

### Typography
- Applied Inter font family globally to body, content area, sidebar, header, and footer
- Set body font size to `1.125rem` with `line-height: 1.7` (relaxed) for readability
- Styled headings h1–h4 with brand accent colour (`#0f6b99`), appropriate sizes, and generous top margins
- Added `text-wrap: pretty` on paragraphs and `text-wrap: balance` on headings
- Added `overflow-wrap: break-word` to prevent long words breaking layout
- Applied `-webkit-font-smoothing: antialiased` for crisper Inter rendering on macOS

### Spacing & readability
- Added `margin-bottom: 16px` on paragraphs and generous margins above headings
- Fixed double-gap between a lead-in paragraph and the list that follows it (`p + ul/ol` negative margin)
- Tightened list item spacing (`line-height: normal`, `margin-bottom: 4px`)
- Added padding top/bottom on `#x_pageDiv`

### Layout — CSS Grid breakout
- Applied CSS Grid to `#pageContents` (the actual direct parent of page content elements)
- Three named zones: `full-start/end` and `content-start/end`
- Default: all direct children sit in the 720px reading column
- Full-width breakout for: `.panel`, `figure`, `table`, `iframe`, `video`, Xerte media page classes, `.wide`
- Set `#x_pageDiv .innerPage { width: 100% }` to allow the grid columns to resolve correctly

### Header
- Set header background to `--color-bg-hero` (`#256a91`, steel blue)
- Progress bar fill changed to `--color-highlight` (yellow `#f5c200`) for contrast on blue background
- Progress bar text (`.pbTxt`) set to `rgba(255,255,255,0.9)` — was invisible on blue
- Progress bar track set to `rgba(255,255,255,0.25)`
- Styled project title (h1) and page title (h2) with Inter and appropriate weights

### Footer
- Left `font-family` off `#x_footerBlock button` to preserve Font Awesome icon rendering
- Applied brand primary colour to nav button text only

### Responsive media
- **iframes**: overrode hardcoded `width`/`height` HTML attributes with `width: 100%; height: auto; aspect-ratio: 16/9` — fixes YouTube embeds overflowing the 720px content column
- **Images**: added `max-width: 100%; height: auto` to prevent overflow; `border-radius` for consistency; `figure`/`figcaption` styling; vertical breathing room for inline images

### Sidebar
- Set background to `--color-bg-page` (white)
- Menu items (`.menuItem`): colour-only overrides — `--color-text-primary` default, `--color-primary` on hover with `neutral-50` background
- Active/current item: soft pale blue background (`#deeef8`), `--color-primary-dark` text, jQuery UI focus border removed (`outline: none; box-shadow: none`)
- Visited checkmarks (`.viewTick`): `--color-primary` (blue)
- Unvisited checkmarks: `--color-neutral-300` (muted grey)
- Chapter headers (`.chapterItem`): `--color-accent` text, `neutral-50` background
- Fixed icon vertical alignment: added flexbox (`align-items: center; justify-content: space-between`) to `.ui-button-text` span so checkmark stays centred on multi-line items
- Fixed overflow scrollbars caused by `width: 100%` on the flex span — removed it

### Accessibility theme support

#### What works
- **Header background**: dark mode correctly overrides `#x_headerBlock { background }` — same specificity (1-0-0), darkmode.css loads later so it wins
- **Body text / paragraphs**: dark mode correctly overrides — darkmode.css sets `p { color: #E0E0E0 }` explicitly, matching our `p { color }` specificity; source order decides in darkmode's favour
- **Header headings (h1/h2)**: fixed by adding explicit `color: var(--color-text-on-dark)` (white) to `#x_headerBlock h1` and `#x_headerBlock h2` — white is readable on both the default steel blue and darkmode's black header

#### Known limitation — content heading colour in accessibility modes
Content headings (h1–h4 in the page body) remain in the brand teal (`#0f6b99`) when any accessibility theme is active. This is a structural gap in Xerte's accessibility theme CSS files.

**Root cause (CSS cascade):** All four accessibility theme files (`darkmode.css`, `highcontrast.css`, `lightmode.css`, `blackonyellow.css`) set `body { color }` and `p { color }` explicitly but do NOT set `color` on `h1`–`h6` — they rely on inheritance from `body`. In CSS, any explicit `color` rule on an element always beats an inherited value, regardless of specificity or source order. Our `h1, h2, h3, h4 { color: var(--color-text-heading) }` rule in `lo_css` therefore persists in all accessibility modes.

**Secondary cause:** `xenith.js` does not disable `#lo_css` when an accessibility theme is activated (it only does this for the `xhibit` theme). The source code contains a TODO comment acknowledging this gap.

**Contrast impact:** Teal `#0f6b99` on darkmode's `#121212` background = ~3.3:1 contrast ratio. Passes WCAG AA for large text (≥3:1) but fails for normal text (requires 4.5:1).

**Filed as GitHub issue:** See `../xerte-github-issue.md` — two fixes proposed to the Xerte project team:
1. Add explicit `h1–h6 { color }` to each accessibility theme CSS file
2. Extend `disableBespokeCSS()` in `xenith.js` to also disable `#lo_css`

---

## 2026-03-09

### Atomic utility classes (v2.0.0)
Added a full set of Tailwind-style single-purpose atomic utility classes to `custom.css`. All values are sourced from existing CSS custom properties — no new tokens introduced.

**Categories added:**

- **Backgrounds** — `.bg-page`, `.bg-surface`, `.bg-hero`, `.bg-primary`, `.bg-primary-light`, `.bg-primary-dark`, `.bg-accent`, `.bg-accent-dark`, `.bg-highlight`, `.bg-neutral-50/100/200/800/900`, `.bg-success-light`, `.bg-warning-light`, `.bg-error-light`, `.bg-info-light`
- **Text colour** — `.text-primary`, `.text-secondary`, `.text-muted`, `.text-on-dark`, `.text-link`, `.text-heading`, `.text-success`, `.text-warning`, `.text-error`, `.text-info`
- **Font size** — `.text-xs` through `.text-h1`
- **Font weight** — `.font-regular`, `.font-medium`, `.font-semibold`, `.font-bold`
- **Line height** — `.leading-tight`, `.leading-normal`, `.leading-relaxed`
- **Letter spacing** — `.tracking-wide`, `.tracking-wider`
- **Text transform** — `.uppercase`, `.capitalize`, `.lowercase`
- **Padding** — full (`p-*`), horizontal (`px-*`), vertical (`py-*`), top (`pt-*`), bottom (`pb-*`) — all spacing tokens
- **Margin** — full (`m-*`), top (`mt-*`), bottom (`mb-*`), vertical (`my-*`), horizontal (`mx-*`) — all spacing tokens, plus `*-0` resets
- **Border** — `.border`, `.border-top/bottom/left/right`, `.border-none`; colour modifiers `.border-primary/accent/success/warning/error/info` (combine with `.border`); left-accent strips `.border-l-primary/accent/success/warning/error/info` (4px, callout pattern)
- **Border radius** — `.rounded-none/sm/md/lg/xl/pill/full`
- **Shadow** — `.shadow-none`, `.shadow-sm`, `.shadow-md`, `.shadow-card`
- **Sizing** — `.w-full`, `.w-auto`, `.max-w-sm` (320px), `.max-w-md` (480px), `.max-w-lg` (640px), `.max-w-content` (720px)
- **Display** — `.block`, `.inline`, `.inline-block`, `.inline-flex`, `.hidden`
- **Overflow / position** — `.overflow-hidden`, `.relative`

### New demo page
Created `atomic-utilities.html` — a standalone reference page with live previews and copy-paste HTML snippets for every atomic class. Composition examples show how to build common components from atomics only (no custom CSS): plain card, elevated card with left accent, info/success/warning/error callouts, stat blocks, feature list rows, dark hero banner, pill badges, and module list rows.

---

## Files
| File | Purpose |
|------|---------|
| `custom.css` | Main custom stylesheet — paste into Xerte project Styles field and publish |
| `design.json` | Design token source — colours, typography, spacing, components |
| `utility-classes.html` | Reference for layout utility classes (flex, grid, alignment, gap) |
| `atomic-utilities.html` | Reference for atomic utility classes (bg, text, spacing, border, shadow, etc.) |
| `design-tokens.html` | Visual reference for all design tokens |
| `my-plan.md` | Project brief and localhost setup notes |
| `changelog.md` | This file |
