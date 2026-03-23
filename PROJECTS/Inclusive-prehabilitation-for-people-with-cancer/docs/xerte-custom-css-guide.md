# Xerte Custom CSS — Developer Reference Guide

A practical reference for writing custom CSS that works correctly with Xerte's theme system, accessibility modes, and CSS loading pipeline.

---

## 1. How Xerte loads CSS

Understanding the load order is essential. Xerte's `xenith.js` builds the stylesheet chain in this sequence:

| Position | Element | Source |
|----------|---------|--------|
| 1–n | Framework CSS | jQuery UI, mainStyles, fonts, FontAwesome, etc. |
| n+1 | `#theme_css` | Active theme (e.g. `xot1.css`) |
| n+2 | **`#lo_css`** | **Your custom CSS** (from the Styles field in project properties) |
| n+3 | `#special_theme_css` | Accessibility theme CSS (disabled until user selects one) |
| n+4 | `#special_theme_responsive_css` | Accessibility responsive text CSS |

**Key points:**
- Your `#lo_css` is injected as an inline `<style>` tag, loaded *after* the theme but *before* the accessibility theme
- The `@import` rule (e.g. Google Fonts) **must be the very first line** of `#lo_css` to work inside an inline style tag
- You do **not** need `!important` — your CSS loads after the theme CSS, so cascade order handles overrides naturally
- When an accessibility theme is selected, `xenith.js` enables `#special_theme_css` (which sits after `#lo_css` in the DOM) and disables `#theme_css`

---

## 2. The accessibility theme override problem

### Symptom
When a user selects Dark mode, High contrast, or another accessibility theme, some of your custom styles persist and break the theme — most commonly:
- Body text remains dark on a dark background (nearly invisible)
- Heading colours don't change
- Elements retain your brand colours instead of the accessibility theme's colours

### Root cause: specificity mismatch

Xerte's built-in accessibility themes (e.g. `darkmode.css`, `highcontrast.css`) use **low-specificity element selectors**:

```css
/* darkmode.css — specificity 0-0-1 */
p    { color: #E0E0E0; }
h1   { color: #E0E0E0; }
body { background: #121212; color: #E0E0E0; }
```

If your custom CSS uses **ID-prefixed selectors** for colour properties, your specificity is higher and you win the cascade — even though `darkmode.css` loads later:

```css
/* custom.css — specificity 1-0-1 — BEATS darkmode regardless of order */
#x_pageDiv p    { color: #333333; }   /* wins over darkmode's p { color } */
#x_pageDiv h1   { color: #0f6b99; }   /* wins over darkmode's h1 { color } */
```

### The heading colour inheritance trap

Darkmode.css sets `body { color: #E0E0E0 }` and expects headings to **inherit** that colour. If your custom CSS has an explicit `h1, h2, h3 { color: ... }` rule — even a low-specificity one — it beats inheritance regardless of source order, because **explicit rules always win over inherited values in CSS**.

```css
/* darkmode.css relies on this cascading to h1/h2/h3 via inheritance */
body { color: #E0E0E0; }
h1   { font-size: 1em; margin: 0; }  /* no color set — expects inherit */

/* your custom.css — even with spec 0-0-1, this explicit rule BEATS inheritance */
h1, h2, h3 { color: #0f6b99; }  /* still teal in dark mode! */
```

**Fix:** Add explicit `color: #E0E0E0` to the h1–h6 rules in `darkmode.css` itself. The file is at `themes/Nottingham/darkmode/darkmode.css`. This is the only reliable fix since CSS has no way to "opt out" of overriding inheritance without modifying the accessibility theme file.

Do the same for `highcontrast.css`, `lightmode.css`, and `blackonyellow.css` if you use custom heading colours.

### What Xerte disables (and doesn't)

When an accessibility theme is activated, `xenith.js` calls `disableBespokeCSS()`:

```javascript
function disableBespokeCSS() {
    // Disables the custom header colour style tag
    $("#customHeaderStyle").prop('disabled', XENITH.ACCESSIBILITY.specialTheme !== false);

    // Only disables lo_css for the "xhibit" theme — NOT for other themes
    // Comment in source: "perhaps we should always do this... & possibly also for #lo_css"
    if (x_params.theme == "xhibit") {
        $("#lo_sheet_css").prop('disabled', XENITH.ACCESSIBILITY.specialTheme !== false);
    }
}
```

**`#lo_css` is never disabled for non-xhibit themes.** This is a known gap in Xerte's code. Your custom CSS remains active during all accessibility modes.

---

## 3. The fix: separate structure from colour

The principle: **use high-specificity selectors for layout/structure/typography, but low-specificity selectors for colour**.

### Do this

```css
/* HIGH specificity — structure only, no colour */
#x_pageDiv p,
#x_pageContent p {
  font-family: var(--font-family-base);
  line-height: 1.7;
  margin-bottom: 16px;
  /* ✗ do NOT put color: here */
}

#x_pageDiv h1, #x_pageContent h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-top: 48px;
  /* ✗ do NOT put color: here */
}

/* LOW specificity — colour only, accessibility themes can override */
p           { color: #333333; }
h1, h2, h3  { color: #0f6b99; }
```

### Why it works

| Rule | Specificity | Position | Winner in default mode | Winner in dark mode |
|------|-------------|----------|----------------------|---------------------|
| `#x_pageDiv p { font-family }` | 1-0-1 | `#lo_css` | Your font ✓ | Your font ✓ (structure preserved) |
| `p { color: #333 }` | 0-0-1 | `#lo_css` | Your dark text ✓ | — |
| `p { color: #E0E0E0 }` (darkmode) | 0-0-1 | `#special_theme_css` (later) | — | Darkmode light text ✓ |

Because both colour rules have **equal specificity**, source order decides — and darkmode.css loads after `#lo_css`, so it wins when active.

---

## 4. Rules for safe custom CSS

### Safe to use high-specificity selectors for:
- `font-family`
- `font-size`, `font-weight`, `line-height`, `letter-spacing`
- `margin`, `padding`
- `display`, `grid-*`, `flex-*`
- `width`, `max-width`, `height`
- `border-radius`
- `box-shadow` (structural shadows like card depth)

### Avoid high-specificity selectors for:
- `color`
- `background`, `background-color`
- `border-color`
- `box-shadow` used for focus/state indicators
- `opacity` on text

For these properties, either:
- Use bare element selectors (`p`, `h1`, `a`)
- Or use class-only selectors (`.x_textPage`, `.panel`)
- Avoid ID-prefixed element selectors (`#x_pageDiv p`, `#x_pageContent h1`)

---

## 5. Font Awesome icon preservation

The XOT1 theme's footer navigation buttons use Font Awesome icons via CSS `content` on `:before` pseudo-elements. The icon rendering depends on a specific `font-family`:

```css
/* From xot1.css */
#x_footerBlock button {
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
}
```

**Never override `font-family` on `#x_footerBlock button`** — it will replace the icons with blank squares or Unicode codepoints. Override only `color`:

```css
/* Safe */
#x_footerBlock button { color: var(--color-primary); }

/* Breaks icons */
#x_footerBlock button { font-family: 'Inter', sans-serif; }
```

---

## 6. The `@import` rule constraint

When CSS is delivered via an inline `<style>` tag (as `#lo_css` is), the `@import` rule only works if it is the **absolute first statement** in the stylesheet. Any comment, whitespace, or rule before it will cause the import to be silently ignored.

```css
/* ✓ Correct */
@import url('https://fonts.googleapis.com/css2?...');

/* ✗ Breaks the import — comment must come AFTER */
/* My styles */
@import url('...');
```

---

## 7. CSS Grid breakout pattern in Xerte

When using a CSS Grid reading-column layout, target `#pageContents` — not `#x_pageDiv` or `.innerPage`. The Xerte content DOM is:

```
#x_pageDiv
  └── .innerPage
        └── #pageContents      ← direct parent of p, h3, .panel, iframe, etc.
              ├── <p>
              ├── <h3>
              └── <div class="panel">
```

Also set `.innerPage { width: 100% }` — without it, `.innerPage` defaults to a fixed pixel width and the grid's `1fr` columns resolve to `0px`.

```css
#x_pageDiv .innerPage { width: 100%; }

#pageContents {
  display: grid;
  grid-template-columns:
    [full-start]    1fr
    [content-start] min(720px, 100%)
    [content-end]   1fr
    [full-end];
}

#pageContents > *                { grid-column: content; }
#pageContents > .panel,
#pageContents > figure,
#pageContents > table,
#pageContents > iframe           { grid-column: full; }
```

---

## 8. Responsive iframes

YouTube and other embeds are inserted with hardcoded `width` and `height` HTML attributes (e.g. `width="832" height="468"`). CSS attributes override HTML attributes, so this fixes overflow without `!important`:

```css
#pageContents iframe,
#x_pageDiv iframe {
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 9;
  max-width: 100%;
  display: block;
}
```

---

## 9. Preview vs publish

| Action | File written | Viewed by |
|--------|-------------|-----------|
| Save in editor | `preview.xml` | Editor preview only |
| **Publish** | `data.xml` | `play.php` (public URL) |

Custom CSS in the Styles field is only applied to `play.php` after **publishing**. Always publish to test final output.

---

## 10. Quick diagnosis checklist

When custom styles break an accessibility theme, work through this list:

1. **Check source order** — open DevTools > Elements, inspect `<head>`. Confirm `#lo_css` appears before `#special_theme_css`.
2. **Check specificity** — use DevTools > Styles panel. If your rule shows as overriding the accessibility theme rule, compare the selectors. Your rule likely has a higher-specificity ID prefix.
3. **Move colour to lower-specificity rule** — strip `color` / `background` from the ID-prefixed rule and add a bare element selector rule.
4. **Verify `#lo_css` is not disabled** — Xerte only disables it for the xhibit theme. For all other themes it stays active.
5. **Check `@import`** — if Google Fonts aren't loading, ensure the `@import` is the very first line with no preceding comments or rules.
