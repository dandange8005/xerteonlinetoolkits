# Cardiff University v2 - Theming Guide

This guide explains how to customize the Cardiff University v2 theme for your own branding or project needs.

---

## Table of Contents

1. [Token Architecture](#token-architecture)
2. [Changing Brand Colors](#changing-brand-colors)
3. [Typography Customization](#typography-customization)
4. [Component Customization](#component-customization)
5. [Creating Theme Variants](#creating-theme-variants)
6. [Adding Custom Components](#adding-custom-components)
7. [Development Workflow](#development-workflow)

---

## Token Architecture

This theme uses a **hybrid two-layer architecture**:

| Layer | File | Purpose |
|-------|------|---------|
| **Primitives** | `_tokens.scss` | Raw brand values (SCSS variables) |
| **Semantics** | `_allvariables.scss` | Runtime tokens (CSS custom properties) |

### Why Two Layers?

- **Primitives** are compile-time values — perfect for Sass functions and breakpoints
- **Semantics** are runtime values — can be changed without recompiling, great for theming

### Token Flow

```
_tokens.scss (primitives)
    ↓
$token-color-brand-primary: #E4251B;
    ↓
_allvariables.scss (semantics)
    ↓
--color-brand-primary: #{t.$token-color-brand-primary};
    ↓
Components use: var(--color-brand-primary)
```

---

## Changing Brand Colors

### Option 1: CSS Override (No Recompile)

Add a `<style>` block or separate CSS file:

```css
:root {
  /* Primary brand color */
  --color-brand-primary: #0066CC;
  
  /* Secondary/dark color */
  --color-brand-secondary: #003366;
  
  /* Accent colors */
  --color-accent-green: #228B22;
  --color-accent-blue: #1E90FF;
}
```

This immediately affects all components using these variables.

### Option 2: Edit Primitive Tokens (Recompile Required)

Edit `scss/_tokens.scss`:

```scss
// Change these values to your brand colors
$token-color-brand-primary: #0066CC;    // Your primary color
$token-color-brand-secondary: #003366;  // Your secondary color
$token-color-brand-white: #FFFFFF;
$token-color-brand-light: #f9fafb;
```

Then recompile:

```bash
sass cardiffuni-v2.scss cardiffuni-v2.css --source-map
```

---

## Typography Customization

### Font Families

**Option 1: CSS Override**

```css
:root {
  --font-family-primary: "Your Sans Font", -apple-system, sans-serif;
  --font-family-secondary: "Your Serif Font", Georgia, serif;
}
```

**Option 2: Edit Tokens**

In `_tokens.scss`:

```scss
$token-font-family-primary: "Your Font", -apple-system, sans-serif;
$token-font-family-secondary: "Your Serif", Georgia, serif;
```

Don't forget to load your custom font:

```scss
// In cardiffuni-v2.scss, update the Google Fonts import:
@import url('https://fonts.googleapis.com/css2?family=Your+Font:wght@300;400;500;600;700&display=swap');
```

### Font Sizes

The theme uses fluid typography with `clamp()`. To adjust:

```css
:root {
  /* Base size (affects all relative sizes) */
  --font-size-base: clamp(0.9375rem, 0.85rem + 0.4vw, 1.0625rem);
  
  /* Individual sizes */
  --font-size-lg: clamp(1.125rem, 1.00rem + 0.625vw, 1.25rem);
  --font-size-xl: clamp(1.25rem, 1.10rem + 0.75vw, 1.5rem);
}
```

---

## Component Customization

### Buttons

Button tokens are centralized in `_allvariables.scss`:

```css
:root {
  /* Primary button */
  --btn-primary-bg: var(--color-brand-primary);
  --btn-primary-text: var(--color-white);
  --btn-primary-hover-bg: color-mix(in srgb, var(--color-brand-primary) 85%, black);
  
  /* Button sizing */
  --btn-padding-x: var(--spacing-4);
  --btn-padding-y: var(--spacing-2);
  --btn-border-radius: var(--radius-md);
}
```

### Links

```css
:root {
  --color-link-default: #0645AD;
  --color-link-hover: color-mix(in srgb, var(--color-link-default) 70%, black);
  --color-link-visited: #551A8B;
}
```

### Alerts

Override alert colors via status tokens:

```css
:root {
  --color-status-success: #07873E;
  --color-status-warning: #E9761E;
  --color-status-error: #E4251B;
  --color-status-info: #1E90FF;
}
```

---

## Creating Theme Variants

### Dark Mode

Add to your CSS or create a separate file:

```css
[data-theme="dark"] {
  --color-bg-body: #1a1a1a;
  --color-bg-page: #121212;
  --color-bg-subtle: #2a2a2a;
  
  --color-text-primary: #ffffff;
  --color-text-secondary: #b0b0b0;
  --color-text-inverse: #121212;
  
  --color-link-default: #6DB3F2;
  --color-link-hover: #8CC4F5;
  
  --color-border-default: #404040;
}
```

Apply with:

```html
<html data-theme="dark">
```

Or toggle with JavaScript:

```javascript
document.documentElement.setAttribute('data-theme', 'dark');
```

### High Contrast Mode

```css
[data-theme="high-contrast"] {
  --color-bg-body: #000000;
  --color-bg-page: #000000;
  --color-text-primary: #FFFFFF;
  
  --color-brand-primary: #FFFF00;
  --color-link-default: #00FFFF;
  
  --focus-ring-width: 4px;
  --border-width-1: 2px;
}
```

### Alternative Institution

```css
[data-theme="swansea"] {
  --color-brand-primary: #003B5C;    /* Swansea blue */
  --color-brand-secondary: #00263E;
  --font-family-primary: "Raleway", sans-serif;
}
```

---

## Adding Custom Components

### Step 1: Create Component File

Create `scss/components/_mycomponent.scss`:

```scss
/**
 * My Custom Component
 */

.my-component {
  padding: var(--spacing-md);
  background: var(--color-bg-subtle);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--color-brand-primary);
  
  &__title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    margin-bottom: var(--spacing-sm);
  }
  
  &__content {
    font-size: var(--font-size-base);
    line-height: var(--line-height-relaxed);
  }
  
  // Variant
  &--highlight {
    background: color-mix(in srgb, var(--color-brand-primary) 10%, white);
  }
}
```

### Step 2: Import in _custom-components.scss

```scss
@use "components/mycomponent";
```

### Step 3: Recompile

```bash
sass cardiffuni-v2.scss cardiffuni-v2.css --source-map
```

---

## Development Workflow

### Watch Mode

Auto-compile on save:

```bash
sass --watch cardiffuni-v2.scss:cardiffuni-v2.css --source-map
```

### VS Code Live Sass Compiler

Configure in `.vscode/settings.json`:

```json
{
  "liveSassCompile.settings.formats": [
    {
      "format": "expanded",
      "extensionName": ".css",
      "savePath": null
    }
  ],
  "liveSassCompile.settings.generateMap": true
}
```

### Testing Changes

1. Open demo pages in browser: `demos/index.html`
2. Use browser DevTools to test CSS variable changes in real-time
3. Once satisfied, update tokens and recompile

### Production Build

Minified output:

```bash
sass cardiffuni-v2.scss cardiffuni-v2.min.css --style=compressed --no-source-map
```

---

## Key CSS Variables Reference

### Colors

| Variable | Purpose |
|----------|---------|
| `--color-brand-primary` | Main brand color |
| `--color-brand-secondary` | Secondary/dark color |
| `--color-text-primary` | Main text color |
| `--color-text-inverse` | Text on dark backgrounds |
| `--color-bg-body` | Page background |
| `--color-bg-page` | Content area background |
| `--color-link-default` | Link color |

### Typography

| Variable | Purpose |
|----------|---------|
| `--font-family-primary` | Main font |
| `--font-family-secondary` | Accent/heading font |
| `--font-size-base` | Base text size |
| `--font-size-lg` through `--font-size-4xl` | Larger sizes |
| `--line-height-normal` | Standard line height (1.5) |

### Spacing

| Variable | Value |
|----------|-------|
| `--spacing-1` | 4px |
| `--spacing-2` | 8px |
| `--spacing-4` | 16px |
| `--spacing-6` | 24px |
| `--spacing-8` | 32px |

### Borders & Shadows

| Variable | Purpose |
|----------|---------|
| `--radius-sm` | Small corners (4px) |
| `--radius-md` | Medium corners (8px) |
| `--radius-lg` | Large corners (12px) |
| `--shadow-sm` | Subtle shadow |
| `--shadow-md` | Medium shadow |

---

## Troubleshooting

### Colors Not Updating

1. Check browser cache — hard refresh (Cmd+Shift+R)
2. Verify CSS is recompiled if editing SCSS
3. Check for typos in variable names
4. Ensure CSS file is loading after Bootstrap

### `color-mix()` Not Working

Requires modern browsers. Check [caniuse.com/color-mix](https://caniuse.com/mdn-css_types_color_color-mix).

For legacy support, define fallback values:

```scss
.button {
  background: #E4251B; /* Fallback */
  background: var(--btn-primary-bg);
}
```

### Fonts Not Loading

1. Check Google Fonts URL is correct
2. Verify font weights match what you're using
3. Check network tab for 404 errors

---

## Need Help?

- Review demo pages for usage examples
- Check `XERTE_THEME_STANDARDIZATION_GUIDE.md` for architectural details
- Contact: [@dandange8005](https://github.com/dandange8005)
