# Dev Summary: Inclusive Prehabilitation for People with Cancer

A personal reference documenting the development process, platform learnings, and design decisions from building the I-Prehab Xerte learning resource (March 2026).

---

## Project Timeline

The project converted an existing HEIW learning platform course into a Xerte Online Toolkits resource, using the Modern XOT1 theme as a base with extensive custom styling and interactive components.

| Date | Milestone |
|------|-----------|
| 2026-03-06 | Project kickoff. Set up custom.css with design tokens from design.json. Wrote the Xerte custom CSS developer reference guide after investigating the CSS loading pipeline. |
| 2026-03-08 | Added layout utility classes (flex, grid, alignment, gap) with a reference HTML page. |
| 2026-03-09 | Built a full set of Tailwind-style atomic utility classes (40+ classes across backgrounds, text, spacing, borders, shadows). Created atomic-utilities.html reference page with live previews. |
| 2026-03-14 | Added blockquote styling. Set up components/ and specs/ directories. |
| 2026-03-15 | Built the audio player and flexible card components. Separated JS into custom.js. |
| 2026-03-16 | Built the slider/carousel component with keyboard navigation and ARIA support. |
| 2026-03-17 | Built document link and banner card components. Refactored CSS selectors (removed unnecessary `#x_pageDiv` prefixes). Applied text-wrap globally. Scoped grid layout to `.x_text_page` only. |
| 2026-03-23 | Handed over to academic team. Cleaned up project docs. |

### How the work evolved

The first few days were spent understanding Xerte's internals rather than writing visible features. That investigation (the CSS loading pipeline, the accessibility theme issue, the `@import` constraint) turned out to be the most valuable part of the project, because it shaped every CSS decision that followed. Without it, I would have written high-specificity selectors everywhere and broken accessibility modes.

The design system came next: tokens, then utilities, then components. Each layer built on the previous one. By the time I was building components, I had a vocabulary of utility classes that made it quick to compose layouts without writing new CSS for every variation.

The interactive components (audio player, slider) came last and required the least iteration, because the visual language was already established.

---

## Xerte Platform Learnings

These are the non-obvious things I learned about developing custom styles and scripts within Xerte Online Toolkits.

### CSS loading pipeline

Xerte's `xenith.js` builds the stylesheet chain in a specific order:

1. Framework CSS (jQuery UI, FontAwesome, etc.)
2. `#theme_css` (active theme, e.g. xot1.css)
3. **`#lo_css`** (your custom CSS, from the Styles field in project properties)
4. `#special_theme_css` (accessibility theme, disabled until user selects one)

Because `#lo_css` loads after the theme, you don't need `!important` for overrides. But you do need to be careful about specificity relative to the accessibility themes that load after you.

### The `@import` constraint

Custom CSS is injected as an inline `<style>` tag. The `@import` rule (e.g. for Google Fonts) **must be the absolute first line** of the stylesheet. Any comment or whitespace before it causes a silent failure. This is easy to forget when reorganising the CSS.

### The accessibility theme problem

This was the single biggest learning. Xerte's accessibility themes (darkmode, highcontrast, etc.) use low-specificity element selectors like `p { color: #E0E0E0 }`. If your custom CSS uses ID-prefixed selectors for colour properties (e.g. `#x_pageDiv h1 { color: #0f6b99 }`), your rule wins the cascade even though the accessibility theme loads later.

Worse: for headings, the accessibility themes don't even set explicit `color` rules. They rely on inheritance from `body { color }`. But CSS inheritance always loses to any explicit rule on the element, regardless of specificity or source order. So even a bare `h1 { color: teal }` in your custom CSS will persist in dark mode.

**The fix I adopted:** Separate structure from colour. Use high-specificity selectors for layout properties (font-size, margin, padding, grid), but low-specificity element or class selectors for colour properties. This way the accessibility themes can override colours via source order while your layout stays intact.

**The fix Xerte itself needs:** I filed a GitHub issue proposing two changes: (1) add explicit `h1-h6 { color }` rules to each accessibility theme CSS file, and (2) extend `disableBespokeCSS()` in xenith.js to also disable `#lo_css` when an accessibility theme is active (currently it only does this for the xhibit theme).

### Font Awesome icon preservation

The XOT1 footer buttons use Font Awesome icons via `font-family: "Font Awesome 5 Free"` on button elements. If you override `font-family` on `#x_footerBlock button`, the icons break. Only override `color` on those buttons. I caught this by accident and it took a while to diagnose.

### CSS Grid breakout pattern

The Xerte content DOM nests content inside `#x_pageDiv > .innerPage > #pageContents`. The grid goes on `#pageContents`, not on the outer wrappers. You also need `.innerPage { width: 100% }` because without it, the inner page defaults to a fixed pixel width and the grid's `1fr` columns resolve to 0px.

### Preview vs publish

Custom CSS only appears in the published output (`data.xml`), not in editor preview (`preview.xml`). You must publish to test your styles via `play.php`. This tripped me up early on.

### Content DOM targeting

Not all Xerte pages have the same wrapper classes. I initially applied the grid layout broadly, then had to scope it to `.x_text_page` only, because media pages and other page types have different DOM structures that broke under the grid.

---

## Design System Approach

### Why a design system for a single project?

The academic team will continue editing content after handover. A design system with documented tokens and utility classes means they can compose new layouts by combining existing classes, without needing to write or modify CSS. The reference HTML pages (design-tokens.html, utility-classes.html, atomic-utilities.html) serve as a visual catalogue they can browse and copy from.

### Token architecture

Tokens are defined in `design.json` (the source of truth) and exported as CSS custom properties at the top of `custom.css`. The token categories are: colours (primary, accent, interactive, highlight, neutrals, semantic states), typography (family, scale, weights, line heights), spacing (8px base unit), border radius, and shadows.

Using CSS custom properties rather than hardcoded values means a future rebrand only requires updating the token values in one place.

### Three layers of CSS

1. **Design tokens** (CSS custom properties): the raw values
2. **Base styles**: applied to Xerte's existing elements (headings, paragraphs, header, sidebar, footer) using the tokens
3. **Utility classes**: Tailwind-style atomic classes for composing layouts in HTML without writing new CSS

The utility layer was the most impactful for handover. The academic team can style content by adding classes like `bg-surface p-lg rounded-md shadow-card` directly in the Xerte HTML editor.

### Component HTML snippets

Each component (audio player, slider, card variants, document link, banner card) has a reference HTML file in `components/` with copy-paste snippets and usage notes. The idea is that content editors can drop these into Xerte's HTML editor without understanding the underlying CSS or JS.

---

## Things I'd Do Differently

### Start with the accessibility investigation, not after

I spent the first day writing CSS with `#x_pageDiv` prefixes everywhere, which is the natural instinct when working inside a large application. When I later discovered the accessibility theme issue, I had to go back and refactor all the colour-related selectors to lower specificity. If I'd investigated the CSS pipeline first, I would have structured the CSS correctly from the start.

*In practice, I did course-correct fairly quickly, and this investigation became the Xerte custom CSS developer reference guide, which is probably the most reusable artefact from the project.*

### Use a CSS preprocessor

The project uses plain CSS. For a project of this size (~1500 lines), a preprocessor like Sass would have helped with organisation (partials, nesting, mixins for the utility class generation). I avoided it because the final CSS needs to be pasted into Xerte's Styles field as a single block, and I didn't want to add a build step. In hindsight, a simple Sass setup with a concat/minify step would have been worth the overhead.

### Document the component API more formally

The component HTML snippets in `components/` show how to use each component, but they don't document the available modifiers or explain which parts are required vs optional. A more structured API reference (like a mini pattern library) would make it easier for someone unfamiliar with the code to use the components confidently.

### Consider a simpler slider

The slider component works well but required a fair amount of JavaScript (100+ lines) for something that could potentially have been handled with a CSS-only approach (scroll-snap) or by using Xerte's built-in carousel page type. The custom slider was justified because the content structure didn't fit Xerte's built-in options, but I should have evaluated those options more thoroughly first.

---

## Known Limitations

1. **Heading colours in accessibility modes**: Content headings remain teal in dark mode/high contrast. This is a Xerte platform issue (filed as GitHub issue). The contrast ratio (3.3:1) passes for large text but fails WCAG AA for normal text.

2. **No build pipeline**: CSS and JS are maintained as single flat files. Changes require manually pasting the full CSS into Xerte's Styles field after each edit.

3. **`#lo_css` not disabled in accessibility modes**: Xerte only disables custom CSS for the xhibit theme. For all other themes (including XOT1), your custom CSS remains active. This is acknowledged in the Xerte source code with a TODO comment but hasn't been addressed.

4. **Single-page audio constraint**: The audio player's "pause other players" logic works within a single page but doesn't account for page transitions in Xerte. If a user navigates away while audio is playing, the audio stops naturally (the DOM is replaced), but there's no explicit cleanup.
