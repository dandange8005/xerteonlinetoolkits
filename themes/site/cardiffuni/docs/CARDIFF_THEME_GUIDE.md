# Cardiff University Theme Guide

**Last Updated:** October 6, 2025
**Version:** 2.0 (CSS Custom Properties)

This comprehensive guide covers both development and customization of the Cardiff University theme for Xerte Online Toolkits (Bootstrap/Site templates).

## Table of Contents

1. [Overview](#overview)
2. [Quick Start: Customization](#quick-start-customization)
3. [Brand Colors](#brand-colors)
4. [Typography](#typography)
5. [CSS Custom Properties Reference](#css-custom-properties-reference)
6. [Theme Variants & Customization](#theme-variants--customization)
7. [Component Styling](#component-styling)
8. [Development Workflow](#development-workflow)
9. [Accessibility Guidelines](#accessibility-guidelines)
10. [Browser Support](#browser-support)

---

## Overview

### What's New in Version 2.0

This theme now uses **CSS Custom Properties (CSS Variables)** instead of SCSS variables, enabling:

- ✅ **Runtime customization** - Change colors without recompiling SCSS
- ✅ **Live theming** - Switch themes dynamically with JavaScript
- ✅ **Auto-generated color scales** - Lighter/darker variants update automatically
- ✅ **Per-project branding** - Easy customization for different projects
- ✅ **Simplified architecture** - No intermediate SCSS variables

### Architecture

```
CSS Custom Properties in :root
    ↓
Components use var() to reference properties
    ↓
Users override properties at runtime (no compilation needed)
```

---

## Quick Start: Customization

### Option 1: Inline Styles (Quick Testing)

```html
<style>
  :root {
    --color-brand-primary: #0066CC;
    --spacing-lg: 32px;
    --font-size-base: 18px;
  }
</style>
```

### Option 2: External Stylesheet (Recommended)

Create `custom-theme.css`:

```css
:root {
  /* Change primary brand color */
  --color-brand-primary: #2E7D32;

  /* Change accent colors */
  --color-accent-green: #00A86B;

  /* Adjust spacing */
  --spacing-lg: 28px;
  --spacing-xl: 40px;

  /* Modify typography */
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --line-height-normal: 1.6;
}
```

Load it after the main theme CSS:
```html
<link rel="stylesheet" href="cardiffuni.css">
<link rel="stylesheet" href="custom-theme.css">
```

### Option 3: JavaScript (Dynamic Theming)

```javascript
// Change theme dynamically
document.documentElement.style.setProperty('--color-brand-primary', '#0066CC');

// Toggle between themes
function setTheme(themeName) {
  document.body.setAttribute('data-theme', themeName);
}
```

---

## Brand Colors

### Primary Colors

The theme uses Cardiff University's official brand colors:

| Color | Hex | CSS Variable | Usage |
|---|---|---|---|
| **Primary Red** | `#E4251B` | `--cu-primary-red` | Primary actions, links, highlights |
| **White** | `#FFFFFF` | `--cu-white` | Backgrounds, text on dark |
| **Black** | `#121212` | `--cu-black` | Text, dark backgrounds |

### Grey Scale

Cardiff's grey scale uses 10% increments:

| Color | Hex | CSS Variable | Usage |
|---|---|---|---|
| **10% Grey** | `#F2F2F2` | `--cu-gray-10` | Subtle backgrounds |
| **20% Grey** | `#E5E5E5` | `--cu-gray-20` | Borders, dividers |
| **30% Grey** | `#CCCCCC` | `--cu-gray-30` | Default borders |
| **40% Grey** | `#B3B3B3` | `--cu-gray-40` | Muted text |
| **50% Grey** | `#999999` | `--cu-gray-50` | Placeholder text |
| **60% Grey** | `#808080` | `--cu-gray-60` | Secondary text |
| **70% Grey** | `#666666` | `--cu-gray-70` | Dark text |
| **80% Grey** | `#4C4C4C` | `--cu-gray-80` | Very dark backgrounds |
| **90% Grey** | `#333333` | `--cu-gray-90` | Near-black backgrounds |

### Accent Colors

**Use sparingly!** These colors should only be used for specific purposes:

| Color | Hex | CSS Variable | Contrast |
|---|---|---|---|
| **Forest Green** | `#07873E` | `--cu-forest-green` | Black and white |
| **Cadet** | `#5EB99B` | `--cu-cadet` | Black |
| **Stone** | `#C9C2BA` | `--cu-stone` | Black and white |
| **Light Blue** | `#1E90FF` | `--cu-light-blue` | Black |
| **Royal Blue** | `#4A42FF` | `--cu-royal-blue` | White |
| **Midnight Blue** | `#273573` | `--cu-midnight-blue` | White |
| **Midnight Purple** | `#26192C` | `--cu-midnight-purple` | White |
| **Orange** | `#E9761E` | `--cu-orange` | White |
| **Yellow** | `#FFB300` | `--cu-yellow` | Black |
| **Yellow Green** | `#85C041` | `--cu-yellow-green` | Black |
| **Indigo** | `#570185` | `--cu-indigo` | White |
| **Dark Violet** | `#D401C5` | `--cu-dark-violet` | Black and White |

### Auto-Generated Color Scales

When you change a base color, all scale variants update automatically:

```css
/* Change this */
--color-brand-primary: #0066CC;

/* These auto-update using color-mix() */
--color-brand-primary-lighter  /* 30% lighter */
--color-brand-primary-light    /* 15% lighter */
--color-brand-primary-dark     /* 15% darker */
--color-brand-primary-darker   /* 30% darker */
```

Available auto-generated scales:
- Primary brand scale: `--color-brand-primary-{lighter|light|dark|darker}`
- Secondary brand scale: `--color-brand-secondary-{lighter|light|dark|darker}`
- Accent scales: `--color-accent-{green|blue|orange}-{light|dark}`
- Background scale: `--color-bg-{subtle|muted|elevated}`
- Text scale: `--color-text-{subtle|muted}`

### Color Contrast Rules

Following Cardiff University guidelines:

- **Red background** → Use white or black text
- **White background** → Use black or red text
- **Black background** → Use white text only (never red)

---

## Typography

### Font Families

This theme prioritizes **readability** over brand-specific fonts:

**Primary Font (Body Text):**
```css
--font-primary-body: "Marr Sans Regular", "Franklin Gothic Book", "Franklin Gothic",
                     "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI",
                     Roboto, Helvetica, Arial, sans-serif;
```

**Primary Font (Headings):**
```css
--font-primary-heading: "Marr Sans Bold", "Franklin Gothic Heavy", "Franklin Gothic",
                        "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI",
                        Roboto, Helvetica, Arial, sans-serif;
```

**Secondary Font (Quotes, Emphasis):**
```css
--font-secondary: "Darby Serif", Georgia, "Times New Roman", Times, serif;
```

> **Note:** The theme includes Cardiff brand fonts (Marr Sans, Darby Serif) with fallbacks to ensure accessibility and readability.

### Font Sizes (Fluid/Responsive)

All font sizes use `clamp()` for fluid typography that scales with viewport:

| Element | CSS Variable | Min → Max | Line Height Variable |
|---|---|---|---|
| **Extra Small** | `--font-size-xs` | 12px → 13px | - |
| **Small** | `--font-size-sm` | 13px → 14px | - |
| **Base (Body)** | `--font-size-base` | 14px → 16px | `--line-height-normal` (1.5) |
| **Medium** | `--font-size-md` | 16px → 18px | - |
| **Large** | `--font-size-lg` | 18px → 20px | `--line-height-normal` (1.5) |
| **Extra Large** | `--font-size-xl` | 20px → 24px | `--line-height-tight` (1.2) |
| **2X Large** | `--font-size-2xl` | 24px → 30px | `--line-height-tight` (1.2) |
| **3X Large** | `--font-size-3xl` | 30px → 36px | `--line-height-tight` (1.2) |
| **4X Large** | `--font-size-4xl` | 36px → 48px | `--line-height-tight` (1.2) |

### Font Weights

| Weight | CSS Variable | Value | Usage |
|---|---|---|---|
| **Light** | `--font-weight-light` | 300 | Subtle emphasis |
| **Regular** | `--font-weight-regular` | 400 | Body text |
| **Medium** | `--font-weight-medium` | 500 | UI elements |
| **Bold** | `--font-weight-bold` | 700 | Headings, emphasis |

### Line Heights

| CSS Variable | Value | Usage |
|---|---|---|
| `--line-height-tight` | 1.2 | Headings, compact text |
| `--line-height-normal` | 1.5 | Body text (optimal) |
| `--line-height-loose` | 1.75 | Relaxed reading |

### Typography Best Practices

1. **Alignment**
   - Headings should be left-aligned for accessibility
   - Center alignment only when absolutely necessary
   - Never right-align headings
   - Never justify text

2. **Hierarchy**
   - Use consistent heading levels (h1 → h2 → h3)
   - Don't skip heading levels
   - Ensure sufficient contrast between heading levels

3. **Readability**
   - Maintain minimum 14px for body text (scales to 16px on larger screens)
   - Use adequate line spacing (1.5 for body, 1.2 for headings)
   - Keep line length between 50-75 characters for optimal readability

---

## CSS Custom Properties Reference

### Semantic Colors (Customizable)

```css
/* Text Colors */
--color-text-primary      /* Main text color */
--color-text-inverse      /* Text on dark backgrounds */
--color-text-hint         /* Hint/helper text */
--color-text-alert        /* Alert/error text */
--color-text-on-light     /* Text on light backgrounds */
--color-text-on-dark      /* Text on dark backgrounds */
--color-text-on-brand     /* Text on brand color backgrounds */
--color-text-subtle       /* Reduced contrast text */
--color-text-muted        /* Highly muted text */

/* Brand Colors */
--color-brand-primary           /* Main brand color */
--color-brand-primary-hover     /* Hover state */
--color-brand-secondary         /* Secondary brand color */

/* Link Colors */
--color-link-default      /* Default link color */
--color-link-hover        /* Link hover state */
--color-link-visited      /* Visited link color */

/* Accent Colors */
--color-accent-green
--color-accent-blue
--color-accent-orange

/* Background Colors */
--color-bg-body           /* Main page background */
--color-bg-page           /* Content area background */
--color-bg-panel          /* Panel/card backgrounds */
--color-bg-subtle         /* Subtle background variation */
--color-bg-muted          /* Muted background */
--color-bg-elevated       /* Elevated surface (cards) */
```

### Spacing

```css
--spacing-xs      /* 4px */
--spacing-sm      /* 8px */
--spacing-md      /* 16px */
--spacing-lg      /* 24px */
--spacing-xl      /* 32px */
--spacing-2xl     /* 48px */
--spacing-3xl     /* 64px */
--spacing-4xl     /* 80px */
```

### Borders

```css
/* Border Radius */
--radius-none     /* 0 */
--radius-sm       /* 2px */
--radius-md       /* 4px */
--radius-lg       /* 8px */
--radius-xl       /* 12px */
--radius-pill     /* 999px */

/* Border Width */
--border-width-sm /* 1px */
--border-width-md /* 2px */
--border-width-lg /* 4px */

/* Border Colors */
--border-color-default
--border-color-light
--border-color-dark
```

### Shadows

```css
--shadow-none     /* No shadow */
--shadow-sm       /* Subtle elevation */
--shadow-md       /* Medium elevation */
--shadow-lg       /* High elevation */
```

### Buttons

```css
--btn-primary-bg
--btn-primary-text
--btn-primary-hover
--btn-primary-disabled

--btn-secondary-bg
--btn-secondary-text
--btn-secondary-border
--btn-secondary-hover
```

### Animation

```css
/* Duration */
--animation-fast      /* 150ms */
--animation-medium    /* 300ms */
--animation-slow      /* 500ms */

/* Easing */
--animation-easing           /* ease-in-out */
--animation-easing-in        /* ease-in */
--animation-easing-out       /* ease-out */
```

### Z-Index

```css
--z-index-sticky      /* 100 */
--z-index-dropdown    /* 200 */
--z-index-overlay     /* 300 */
--z-index-modal       /* 400 */
```

---

## Theme Variants & Customization

### Creating Project-Specific Themes

#### Method 1: Data Attribute Theming

```html
<body data-theme="project-blue">
  <!-- Your content -->
</body>
```

Add to your CSS:
```css
[data-theme="project-blue"] {
  --color-brand-primary: #0066CC;
  --color-brand-secondary: #00A86B;
  --color-accent-green: #2E7D32;
}
```

#### Method 2: Dark Mode

```css
[data-theme="dark"] {
  --color-bg-body: #1a1a1a;
  --color-bg-page: #121212;
  --color-text-primary: #ffffff;
  --color-text-inverse: #121212;
  --color-brand-primary: #FF6B5B; /* Brighter for dark mode */
  --cu-gray-10: #2a2a2a;
  --cu-gray-20: #3a3a3a;
  --cu-gray-90: #e0e0e0;
  --cu-gray-80: #d0d0d0;
}
```

Toggle with JavaScript:
```javascript
const isDark = document.body.getAttribute('data-theme') === 'dark';
document.body.setAttribute('data-theme', isDark ? '' : 'dark');
```

#### Method 3: Per-Organization Branding

```css
/* Swansea University */
[data-theme="swansea"] {
  --color-brand-primary: #660066;
  --color-brand-secondary: #FFD700;
}

/* Cardiff Met University */
[data-theme="cardiffmet"] {
  --color-brand-primary: #C41E3A;
  --color-accent-green: #FFB81C;
}
```

### Real-World Examples

#### Example 1: Green Environmental Project

```css
:root {
  --color-brand-primary: #2E7D32;
  --color-brand-secondary: #689F38;
  --color-accent-green: #558B2F;
  --color-bg-body: #F1F8E9;
}
```

#### Example 2: Medical/Health Theme

```css
:root {
  --color-brand-primary: #1976D2;
  --color-accent-blue: #42A5F5;
  --color-bg-body: #E3F2FD;
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
}
```

#### Example 3: High Contrast (Accessibility)

```css
[data-theme="high-contrast"] {
  --color-bg-body: #000000;
  --color-bg-page: #000000;
  --color-text-primary: #FFFFFF;
  --color-brand-primary: #FFFF00;
  --color-link-default: #00FFFF;
  --border-width-md: 3px;
  --font-size-base: 18px;
}
```

---

## Component Styling

### Buttons

#### Primary Buttons
```css
background: var(--btn-primary-bg)      /* Cardiff Red */
color: var(--btn-primary-text)         /* White */
hover: var(--btn-primary-hover)        /* Darker red */
```

#### Secondary Buttons
```css
background: var(--btn-secondary-bg)         /* White */
border: 2px solid var(--btn-secondary-border) /* Red */
color: var(--btn-secondary-text)            /* Red */
hover: var(--btn-secondary-hover)           /* Light red bg */
```

### Navigation

The navbar uses:
```css
background: var(--cu-gray-20)
link color: var(--cu-gray-80)
hover/active: var(--cu-white) background with var(--color-brand-primary) text
active indicator: 2px bottom border in var(--color-brand-primary)
```

### Panels & Cards

```css
background: var(--color-brand-primary)
text: var(--cu-white)
border-radius: var(--radius-md)
padding: var(--spacing-lg)
```

#### Panel Enhancement Features
- Auto-removes top margin from first child
- Auto-removes bottom margin from last child
- Uppercase labels with letter-spacing for ::after pseudo-elements

### Tables

```css
background: var(--cu-white)
shadow: var(--shadow-sm)
font-size: var(--font-size-sm)

/* Header */
thead background: var(--cu-midnight-blue)
thead color: var(--cu-white)

/* Striped rows */
even rows: var(--cu-gray-10)
```

### Alerts

Using auto-generated color scales:
```css
/* Success */
background: var(--color-accent-green-light)
border: var(--color-accent-green)
text: var(--color-accent-green-dark)

/* Info */
background: var(--color-accent-blue-light)
border: var(--color-accent-blue)
text: var(--color-accent-blue-dark)

/* Warning */
background: var(--color-accent-orange-light)
border: var(--color-accent-orange)
text: var(--color-accent-orange-dark)
```

### Lead Text

Large introductory text:
```css
font-size: var(--font-size-xl)
color: var(--cu-gray-60)
line-height: var(--line-height-tight)
font-weight: var(--font-weight-light)
```

### Footer

```css
background: var(--cu-gray-80)
text: var(--cu-white)
links: var(--cu-white)
padding: var(--spacing-xl) vertical
```

---

## Development Workflow

### File Structure

```
themes/site/cardiffuni/
├── cardiffuni.scss              # Main SCSS file (imports only)
├── cardiffuni.css               # Compiled CSS (auto-generated)
├── cardiffuni.css.map           # Source map (auto-generated)
├── cardiffuni.js                # Optional JavaScript
├── cardiffuni.info              # Theme metadata
├── cardiffuni.jpg               # Preview image
├── test-theme.html              # Test page for CSS variables
├── docs/
│   └── CARDIFF_THEME_GUIDE.md   # This file
└── scss/
    ├── _allvariables.scss       # CSS Custom Properties definitions
    ├── _enhancements.scss       # Modern CSS improvements (portable)
    ├── _base-elements.scss      # HTML element styles
    ├── _bootstrap-components.scss # Bootstrap overrides
    ├── _xerte-components.scss   # Xerte-specific components
    ├── _utilities.scss          # Utility classes
    └── _layouts.scss            # Layout components
```

### Module Architecture

The theme follows a modular structure:

1. **`_allvariables.scss`** - Pure CSS custom properties (no SCSS variables)
2. **`_enhancements.scss`** - Theme-agnostic modern CSS (portable to other themes)
3. **`_base-elements.scss`** - Cardiff-branded HTML element styles
4. **`_bootstrap-components.scss`** - Bootstrap component overrides
5. **`_xerte-components.scss`** - Xerte Online Toolkits specific components
6. **`_utilities.scss`** - Helper classes
7. **`_layouts.scss`** - Page layout and structural components

### Editing the Theme

1. **Edit SCSS files** in the `scss/` folder or the main `cardiffuni.scss` file
2. **Save** - Live Sass Compiler will auto-compile to `cardiffuni.css`
3. **Test** - Open `test-theme.html` in your browser to test all CSS variables
4. **Verify** - Check that all variables are working correctly

### Customizing Colors

All colors are defined in `scss/_allvariables.scss` as CSS custom properties:

```scss
:root {
    // Cardiff brand colors
    --cu-primary-red: #E4251B;
    --cu-black: #121212;

    // Semantic mappings
    --color-brand-primary: var(--cu-primary-red);
    --color-text-primary: var(--cu-black);
}
```

To change a color:
1. Edit the CSS custom property in `_allvariables.scss`
2. Save and let it compile
3. Or override at runtime (no compilation needed!)

### Adding New Components

Add component styles to the appropriate module:

- **Bootstrap components** → `_bootstrap-components.scss`
- **Xerte components** → `_xerte-components.scss`
- **Base HTML elements** → `_base-elements.scss`
- **Layout structures** → `_layouts.scss`

Always use CSS custom properties with `var()`:
```scss
.my-component {
    color: var(--color-text-primary);
    background: var(--color-brand-primary);
    padding: var(--spacing-md);
}
```

### Testing Your Changes

Use the included `test-theme.html` page:

1. Open in browser
2. Use live color customizer
3. Test theme switcher
4. Verify all components render correctly
5. Check color scales update automatically

---

## Accessibility Guidelines

### Color Contrast

Always ensure sufficient contrast ratios:

- **Normal text:** Minimum 4.5:1
- **Large text (18pt/24px+):** Minimum 3:1
- **UI components:** Minimum 3:1

Use the contrast guidelines in the Brand Colors section for Cardiff brand colors.

### Text Readability

1. **Minimum font sizes:**
   - Body text: 14px (scales to 16px on larger screens)
   - Small text: 13px (scales to 14px)
   - Never go below 12px

2. **Line spacing:**
   - Body text: 1.5 (`--line-height-normal`)
   - Headings: 1.2 (`--line-height-tight`)
   - Never use line-height below 1.2

3. **Line length:**
   - Optimal: 50-75 characters per line
   - Maximum: 90 characters per line
   - Use `max-inline-size: 70ch` for long-form content

### Focus States

Ensure all interactive elements have visible focus states:

```css
:focus {
  outline: 2px solid var(--color-brand-primary);
  outline-offset: 2px;
}

/* Or for better visibility */
:focus-visible {
  outline: 3px solid var(--color-brand-primary);
  outline-offset: 2px;
}
```

### Reduced Motion

The theme respects user preferences for reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Icon Usage

- Use [Ionicons (sharp set)](https://ionic.io/ionicons) as per Cardiff guidelines
- Always provide text labels alongside icons
- Ensure icons have sufficient contrast
- Use `aria-label` for icon-only buttons

---

## Browser Support

### CSS Custom Properties
Supported in all modern browsers:
- Chrome/Edge 49+
- Firefox 31+
- Safari 9.1+
- Opera 36+

### color-mix() Function
Required for auto-generated color scales:
- Chrome/Edge 111+
- Firefox 113+
- Safari 16.2+

**Fallback behavior:** For older browsers, the base colors will still work. Auto-generated color scales won't update dynamically, but the theme remains functional.

---

## Tips & Best Practices

1. **Test in Dev Tools**
   Use browser dev tools to live-edit CSS variables and see changes instantly

2. **Keep Cardiff Branding**
   Don't override `--cu-*` colors unless creating a completely different theme

3. **Use Semantic Variables**
   Override `--color-brand-primary` instead of `--cu-primary-red` for flexibility

4. **Accessibility First**
   Maintain sufficient color contrast when customizing

5. **Document Your Theme**
   Keep a record of which variables you've overridden

6. **Leverage Auto-Scales**
   Use auto-generated color scales (`-light`, `-dark` variants) instead of hardcoding shades

7. **Test Responsively**
   Fluid typography scales with viewport - test on multiple screen sizes

---

## Quick Reference

### Common CSS Variables

```css
/* Colors */
--cu-primary-red           /* #E4251B - Cardiff Red */
--cu-black                 /* #121212 - Near black */
--cu-white                 /* #FFFFFF - White */
--cu-gray-10 to --cu-gray-90  /* Grey scale (10% increments) */

/* Semantic Colors */
--color-brand-primary      /* Main brand color */
--color-text-primary       /* Main text color */
--color-bg-body            /* Page background */
--color-link-default       /* Link color */

/* Typography */
--font-primary-body        /* Body text font stack */
--font-primary-heading     /* Heading font stack */
--font-size-base           /* 14px → 16px (fluid) */
--line-height-normal       /* 1.5 */
--font-weight-regular      /* 400 */

/* Spacing */
--spacing-xs               /* 4px */
--spacing-sm               /* 8px */
--spacing-md               /* 16px */
--spacing-lg               /* 24px */
--spacing-xl               /* 32px */
```

### File to Edit for...

- **CSS Variables:** `scss/_allvariables.scss`
- **HTML Elements:** `scss/_base-elements.scss`
- **Bootstrap Components:** `scss/_bootstrap-components.scss`
- **Xerte Components:** `scss/_xerte-components.scss`
- **Layout:** `scss/_layouts.scss`
- **Utilities:** `scss/_utilities.scss`
- **Modern CSS Features:** `scss/_enhancements.scss`

---

## Support & Resources

### Cardiff University Resources
- **Brand Guidelines:** https://brand.cardiff.ac.uk/
- **Digital Accessibility:** https://www.cardiff.ac.uk/public-information/policies-and-procedures/accessible-digital-content

### Xerte Resources
- **Development Guide:** See [CLAUDE.md](../../../CLAUDE.md) in repository root
- **Test Page:** `test-theme.html` in theme folder
- **Theming Guide:** This document

### Testing Tools
- **Color Contrast:** https://webaim.org/resources/contrastchecker/
- **WAVE Accessibility:** https://wave.webaim.org/
- **Browser DevTools:** Built-in CSS variable inspector

---

**Document Version:** 2.0
**Last Updated:** October 6, 2025
**Maintained by:** Cardiff University Xerte Theme Team
