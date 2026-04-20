# XOT Dev Workflow

A personal reference for developing custom styles and components in Xerte Online Toolkits using the XOT project template (Modern Nottingham / XOT1 theme). Use as an onboarding checklist at project start and a platform reference during development.

**Scope:** XOT template only. Bootstrap template has a different file and DOM structure and is not covered here.

---

## Contents

- [Section 1: Project Setup Checklist](#section-1-project-setup-checklist)
  - [Phase 1: Platform Investigation](#phase-1-platform-investigation)
  - [Phase 2: Design System Setup](#phase-2-design-system-setup)
  - [Phase 3: Component Development](#phase-3-component-development)
  - [Phase 4: Handover and Cleanup](#phase-4-handover-and-cleanup)
- [Section 2: Platform Reference](#section-2-platform-reference)
  - [1. CSS Loading Pipeline](#1-css-loading-pipeline)
  - [2. The @import Constraint](#2-the-import-constraint)
  - [3. Accessibility Theme Problem](#3-accessibility-theme-problem)
  - [4. Colour vs Structure Rule](#4-colour-vs-structure-rule)
  - [5. Font Awesome Preservation](#5-font-awesome-preservation)
  - [6. CSS Grid Breakout Pattern](#6-css-grid-breakout-pattern)
  - [7. Preview vs Publish](#7-preview-vs-publish)
  - [8. Content DOM Targeting](#8-content-dom-targeting)
  - [9. Known Xerte Gaps](#9-known-xerte-gaps)

---

## Section 1: Project Setup Checklist

Work through these phases top-to-bottom at the start of every XOT project. Each phase has an entry condition — do not start a phase until its condition is met.

---

### Phase 1: Platform Investigation

**Entry condition:** None — this is always the first phase, before writing any CSS or JS.

> Skipping this phase means refactoring colour selectors later. The investigation shapes every CSS decision that follows.

- [ ] Identify the active theme (e.g. Modern Nottingham / XOT1)
- [ ] Open DevTools on a live XOT project and inspect the `<head>` stylesheet order: confirm the sequence is framework CSS → `#theme_css` → `#lo_css` → `#special_theme_css`
- [ ] Open the accessibility theme CSS files (`darkmode.css`, `highcontrast.css`, `lightmode.css`, `blackonyellow.css`) and note which selectors they use for colour properties — specifically whether `h1–h6` have explicit `color` rules or rely on inheritance from `body`
- [ ] Map the content DOM for the page types you will use. The standard XOT text page nests as: `#x_pageDiv > .innerPage > #pageContents`. Confirm this holds for your theme.
- [ ] Note which Xerte page type classes are present on the `<body>` for each page type you will use (e.g. `.x_text_page`, `.x_media_page`) — these are needed to scope CSS safely (see Section 2.8)

---

### Phase 2: Design System Setup

**Entry condition:** Phase 1 complete.

- [ ] Create project directory structure:
  ```
  PROJECT-NAME/
  ├── design.json        ← token source of truth
  ├── custom.css         ← paste into Xerte Styles field
  ├── custom.js          ← paste into Xerte Scripts field
  ├── changelog.md
  ├── docs/              ← dev notes, guides, component specs
  ├── components/        ← copy-paste HTML snippets
  └── demos/             ← standalone reference HTML pages
  ```
- [ ] Create `design.json` with token categories: colours (primary, accent, interactive, highlight, neutrals, semantic states, text, background), typography (font families, scale, weights, line heights, letter spacing), spacing (8px base unit + named scale), border radius, shadows, components
- [ ] Scaffold `custom.css`:
  - If using Google Fonts, line 1 must be `@import` — no preceding comment or whitespace (see Section 2.2)
  - Define CSS custom properties from `design.json` in `:root {}`
  - Write base styles (typography, spacing) using low-specificity selectors for colour (see Section 2.3 and 2.4)
  - Add atomic utility classes last
- [ ] Scaffold `custom.js` with an empty `DOMContentLoaded` wrapper:
  ```js
  document.addEventListener('DOMContentLoaded', function () {
    // components
  });
  ```
- [ ] Create `changelog.md` with today's date and an "Initial setup" entry
- [ ] Paste `custom.css` into the Xerte project Styles field, publish, and verify it loads without errors in `play.php`

---

### Phase 3: Component Development

**Entry condition:** Phase 2 complete — design tokens and utility classes are in `custom.css`.

Repeat the following cycle for each component:

- [ ] Write a component design spec in `docs/` before building. Include: layout description, which utility classes to use, which properties need inline styles (and why), any JS behaviour, ARIA requirements. See `docs/2026-03-12-audio-player-component-design.md` in the I-Prehab project as a template.
- [ ] Build the component as a self-contained HTML snippet in `components/` using utility classes from `custom.css`
- [ ] Add any required JS to `custom.js`
- [ ] Create a demo/reference HTML page in `demos/` with live previews and copy-paste snippets — content editors use this as their visual catalogue
- [ ] Paste updated `custom.css` and `custom.js` into Xerte and publish; verify the component renders correctly in `play.php`
- [ ] Update `changelog.md` with a dated entry describing what was added

---

### Phase 4: Handover and Cleanup

**Entry condition:** All content is complete and published.

- [ ] Verify every component in `components/` has a matching demo page in `demos/`
- [ ] Write a `docs/dev-summary.md` documenting platform learnings, design decisions, and any known limitations discovered during the project
- [ ] Do a final publish and verify the complete resource in `play.php`
- [ ] Add a final dated entry to `changelog.md`
- [ ] Remove any draft or temporary files

---

## Section 2: Platform Reference

Named topics you can jump to directly. Each covers one non-obvious aspect of Xerte's CSS/JS environment.

---

### 1. CSS Loading Pipeline

`xenith.js` builds the stylesheet chain in this fixed order:

| Position | Element | Source |
|---|---|---|
| 1–n | Framework CSS | jQuery UI, FontAwesome, etc. |
| n+1 | `#theme_css` | Active theme (e.g. `xot1.css`) |
| n+2 | `#lo_css` | Your custom CSS (from the Styles field) |
| n+3 | `#special_theme_css` | Accessibility theme (disabled until user selects one) |

Because `#lo_css` loads after the theme, you do not need `!important` for overrides. Because the accessibility themes load after `#lo_css`, high-specificity colour rules in your CSS will override them — even when the user has switched to dark mode.

---

### 2. The @import Constraint

Custom CSS is delivered as an inline `<style>` tag. The `@import` rule only works if it is the absolute first statement — no preceding comments, no whitespace.

```css
/* Correct */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Broken — comment before @import causes a silent failure */
/* My project styles */
@import url('...');
```

Failure is silent: no console error, fonts simply do not load.

---

### 3. Accessibility Theme Problem

Xerte's accessibility themes (`darkmode.css`, `highcontrast.css`, etc.) use low-specificity element selectors:

```css
/* darkmode.css — specificity 0-0-1 */
body { background: #121212; color: #E0E0E0; }
p    { color: #E0E0E0; }
```

**Specificity trap:** If your custom CSS uses ID-prefixed selectors for colour properties (e.g. `#x_pageDiv h1 { color: #0f6b99 }`), your rule has higher specificity (1-0-1) and wins the cascade even though `darkmode.css` loads later. Your brand colour persists in dark mode.

**Inheritance trap:** Accessibility themes do not set explicit `color` rules on `h1–h6`. They rely on inheritance from `body { color }`. But any explicit `color` rule on the element — even at 0-0-1 specificity — beats inheritance regardless of source order. So even a bare `h1 { color: teal }` in your custom CSS will persist in dark mode.

**Fix:** See Section 2.4.

---

### 4. Colour vs Structure Rule

Use high-specificity selectors (`#x_pageDiv p`, `#x_pageContent h1`) **only** for layout and structural properties. Use bare element or class selectors for colour properties so accessibility themes can override via source order.

**Safe at high specificity:**
- `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`
- `margin`, `padding`
- `display`, `grid-*`, `flex-*`
- `width`, `max-width`, `height`, `border-radius`
- `box-shadow` (structural depth, not state indicators)

**Avoid high specificity for:**
- `color`
- `background`, `background-color`
- `border-color`
- `opacity` on text

```css
/* Correct — structure at high specificity, colour at low specificity */
#x_pageDiv p,
#x_pageContent p {
  font-family: var(--font-family-base);
  line-height: 1.7;
  margin-bottom: 16px;
  /* no color here */
}

p { color: var(--color-text-primary); }   /* 0-0-1 — accessibility theme wins */
h1, h2, h3 { color: var(--color-heading); } /* 0-0-3 — accessibility theme wins */
```

---

### 5. Font Awesome Preservation

The XOT1 footer navigation buttons use Font Awesome icons via `font-family: "Font Awesome 5 Free"` on `#x_footerBlock button`. Overriding `font-family` on those buttons replaces the icons with blank squares or Unicode codepoints. Only override `color`.

```css
/* Safe */
#x_footerBlock button { color: var(--color-primary); }

/* Breaks icons */
#x_footerBlock button { font-family: 'Inter', sans-serif; }
```

---

### 6. CSS Grid Breakout Pattern

The Xerte content DOM nests as:

```
#x_pageDiv
  └── .innerPage
        └── #pageContents      ← direct parent of p, h3, .panel, iframe, etc.
```

Apply the grid to `#pageContents`, not to `#x_pageDiv` or `.innerPage`. Also set `.innerPage { width: 100% }` — without it, `.innerPage` defaults to a fixed pixel width and `1fr` columns resolve to `0px`.

```css
.x_text_page #x_pageDiv .innerPage { width: 100%; }

.x_text_page #pageContents {
  display: grid;
  grid-template-columns:
    [full-start]    1fr
    [content-start] min(720px, 100%)
    [content-end]   1fr
    [full-end];
}

.x_text_page #pageContents > *       { grid-column: content; }
.x_text_page #pageContents > .panel,
.x_text_page #pageContents > figure,
.x_text_page #pageContents > table,
.x_text_page #pageContents > iframe  { grid-column: full; }
```

Note the `.x_text_page` scope prefix — see Section 2.8.

---

### 7. Preview vs Publish

The Styles field content is written to `data.xml` only when you publish. Editor preview uses `preview.xml` and will not reflect your custom CSS.

| Action | File written | Seen in |
|---|---|---|
| Save in editor | `preview.xml` | Editor preview only |
| Publish | `data.xml` | `play.php` (public URL) |

Always publish to test custom styles. Do not trust the editor preview for CSS verification.

---

### 8. Content DOM Targeting

Not all Xerte page types share the same wrapper structure. Applying the CSS Grid layout broadly will break media pages and other page types. Scope layout rules to the specific page type class that appears on `<body>`.

```css
/* Scoped — only applies to text pages */
.x_text_page #pageContents { display: grid; /* ... */ }

/* Unscoped — breaks media pages */
#pageContents { display: grid; /* ... */ }
```

Check the page type class in DevTools by inspecting `<body>` on each page type you intend to use, before writing any layout CSS.

---

### 9. Known Xerte Gaps

These are platform-level issues in Xerte itself, not fixable in `custom.css` alone.

**`#lo_css` not disabled in accessibility modes**
`xenith.js` only disables custom CSS for the `xhibit` theme. For XOT1, `#lo_css` remains active when the user selects dark mode, high contrast, or any other accessibility theme. There is a TODO comment in `disableBespokeCSS()` in `xenith.js` acknowledging this gap. The workaround is Section 2.4 (colour vs structure rule).

**Heading colour in accessibility modes**
Content headings remain in the brand colour in all accessibility modes because the accessibility theme CSS files do not set explicit `color` rules on `h1–h6` — they rely on body inheritance. Contrast ratio for teal `#0f6b99` on darkmode's `#121212` background is ~3.3:1, which passes WCAG AA for large text (≥18px bold) but fails for normal-weight body-size text. Filed as a GitHub issue against Xerte with two proposed fixes: (1) add explicit `h1–h6 { color }` to each accessibility theme file, and (2) extend `disableBespokeCSS()` to also disable `#lo_css`.

**No build pipeline**
`custom.css` and `custom.js` are single flat files. After each edit, you must manually paste the full file contents into the Xerte project Styles/Scripts fields and publish to see the result.
