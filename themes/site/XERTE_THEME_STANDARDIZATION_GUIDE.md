# Xerte Bootstrap Sites - Theme Creation Guide

**Version:** 1.1
**Last Updated:** January 25, 2026
**Author:** Based on analysis of `cardiffuni-v2`, `cardiffuni`, and `diged` themes
**Scope:** This guide is specifically for **Xerte Bootstrap sites**. A separate guide will be created for Xerte XOT sites.

> **Reference Implementation:** The `cardiffuni-v2` theme is the canonical example of this guide's architecture.

## Executive Summary

This guide provides a **standard procedure for creating new themes** for Xerte Bootstrap sites. It's based on analyzing existing themes (`cardiffuni`, `diged`, `blackgrey`, etc.) to establish best practices, folder structures, and required components.

### Core Design Principles

All Xerte themes must adhere to these fundamental principles:

1. **Bootstrap 2 Foundation** - Themes sit on top of the Bootstrap 2.3.2 framework
2. **Accessibility First** - Follow NHS Design System and GOV.UK Design System accessibility standards
3. **Text-Heavy Content** - Optimized for guidance, resources, and documentation
4. **Clean & Professional** - Minimal, clear, professional aesthetic
5. **Zero-Config Styling** - Base elements styled by default, no classes required for basic use
6. **Advanced Component Library** - Optional components and utilities for power users
7. **Theme Designer Tool** - Visual designer to accommodate different schools/departments with unique branding (e.g., 23 schools with different requirements)

---

## 1. Bootstrap 2 Framework Foundation

### 1.1 Overview

**All Xerte themes are built on Bootstrap 2.3.2**, the last version of Bootstrap 2. This is a critical architectural decision that affects all theming work.

#### Key Characteristics of Bootstrap 2

- **Released:** July 2013
- **Grid System:** 12-column grid with `.span*` classes
- **Responsive:** Mobile-first with responsive utilities
- **Components:** Rich set of UI components
- **CSS Framework:** Less-based (we use Sass for our themes)

#### Bootstrap 2 vs Modern Bootstrap

| Feature | Bootstrap 2 | Bootstrap 4/5 |
|---------|-------------|---------------|
| Grid | `.row > .span6` | `.row > .col-md-6` |
| Buttons | `.btn.btn-primary` | Same |
| Utilities | Limited | Extensive |
| Flexbox | No | Yes |
| Cards | No (use `.well`) | Yes |

### 1.2 Bootstrap 2 Pre-loaded

**Important:** Bootstrap 2.3.2 is **already included** in all Xerte Bootstrap sites. You do NOT need to include it in your theme.

The Xerte platform automatically loads:
- Bootstrap 2.3.2 CSS
- jQuery 1.x (Bootstrap 2 compatible)
- Bootstrap 2.3.2 JavaScript

Your theme CSS will be loaded **after** Bootstrap, allowing you to override Bootstrap's default styles.

### 1.3 Bootstrap 2 Components - Required vs Optional

**Required Components** (Must be styled):

These components are commonly used in Xerte Bootstrap sites and should be styled in every theme:

**Navigation:**
- Navbar (`.navbar`) - Site navigation
- Nav tabs (`.nav-tabs`) - Tabbed interfaces
- Breadcrumbs (`.breadcrumb`) - Navigation trail

**Content:**
- Typography (headings, paragraphs, lists) - All text content
- Tables (`.table`) - Data presentation
- Forms (`.form-*`) - User input
- Buttons (`.btn`, `.btn-primary`, etc.) - Actions

**Optional Components** (Style if needed):

These components may be used in some sites but are not always required:

**Visual Components:**
- Alerts (`.alert`, `.alert-success`, etc.) - Notifications
- Wells (`.well`) - Content containers
- Labels (`.label`) - Inline labels
- Badges (`.badge`) - Notification badges
- Progress bars (`.progress`, `.bar`) - Loading indicators
- Images (`.img-rounded`, `.img-circle`, `.img-polaroid`) - Image styling

**JavaScript Components:**
- Modals (`.modal`) - Dialog boxes
- Dropdowns (`.dropdown`) - Menu dropdowns
- Tooltips (`.tooltip`) - Hover information
- Popovers (`.popover`) - Click information
- Collapse (`.collapse`) - Expandable content
- Carousel (`.carousel`) - Image slideshows
- Nav pills (`.nav-pills`) - Alternative navigation style
- Pagination (`.pagination`) - Page navigation

### 1.4 Custom Flexbox Grid System

**Important:** We are **NOT using** Bootstrap 2's grid system (`.span*` classes). Instead, we're creating our own modern **flexbox-based grid system**.

#### Why Replace Bootstrap 2 Grid?

- Bootstrap 2 grid uses floats (outdated)
- `.span*` classes are inflexible
- No flexbox alignment/distribution features
- Poor responsive control

#### Custom Flexbox Grid Pattern

> **Note:** Detailed flexbox system specification will be provided separately.

**Placeholder Example Pattern:**

```html
<div class="container">
  <div class="flex flex-wrap">
    <div class="w-md-50">50% width column</div>
    <div class="w-md-50">50% width column</div>
  </div>

  <div class="flex flex-wrap gap-lg">
    <div class="w-md-33">33% width</div>
    <div class="w-md-33">33% width</div>
    <div class="w-md-33">33% width</div>
  </div>
</div>
```

**Expected Benefits:**
- Modern flexbox features (gap, alignment, distribution)
- Simpler class names (`.w-md-50` vs `.span6`)
- Better responsive control
- Auto-handles gutters with `gap`
- Easy to understand and maintain

---

## 2. Accessibility Standards

### 2.1 Reference Design Systems

Xerte themes **must meet the accessibility standards** established by:

1. **[NHS Design System](https://service-manual.nhs.uk/)** - Healthcare accessibility
2. **[GOV.UK Design System](https://design-system.service.gov.uk/)** - Government digital services
3. **[WCAG 2.1 Level AA](https://www.w3.org/WAI/WCAG21/quickref/)** - Web Content Accessibility Guidelines

### 2.2 Typography Accessibility

#### Font Size

```scss
// Base font size MUST be at least 16px
$token-font-size-base: 16px;

// For better readability, consider 18px for text-heavy content
$token-font-size-base: 18px;

// Line height for optimal readability
$token-line-height-base: 1.5;  // Minimum
$token-line-height-base: 1.6;  // Recommended for long-form text
```

#### Font Choices

```scss
// Use clear, readable fonts
// Avoid decorative fonts for body text
$token-font-primary-body:
  -apple-system,
  BlinkMacSystemFont,
  "Segoe UI",
  Roboto,
  "Helvetica Neue",
  Arial,
  sans-serif;

// Headings can use brand fonts if readable
$token-font-primary-heading:
  "Brand Font",
  Arial,
  sans-serif;
```

#### Text Spacing

**NHS/GOV.UK Requirements:**
- Line height at least 1.5× font size
- Paragraph spacing at least 2× font size
- Letter spacing at least 0.12× font size
- Word spacing at least 0.16× font size

```scss
p {
  font-size: 1rem;           // 16px minimum
  line-height: 1.6;          // 25.6px (1.6 × 16px)
  margin-bottom: 1.5rem;     // Space between paragraphs
  letter-spacing: 0.01em;    // Subtle letter spacing
}
```

### 2.3 Color Accessibility

#### Contrast Ratios (WCAG AA)

- **Normal text (< 18px)**: Minimum 4.5:1 contrast ratio
- **Large text (≥ 18px or ≥ 14px bold)**: Minimum 3:1 contrast ratio
- **UI components & graphics**: Minimum 3:1 contrast ratio

```scss
// Example: Valid color combinations
:root {
  // Dark text on light background (7:1 ratio - AAA)
  --color-text-primary: #121212;     // Near-black
  --color-bg-body: #FFFFFF;          // White

  // Link color with sufficient contrast (4.8:1 ratio - AA)
  --color-link: #0066CC;             // Blue
  --color-bg-body: #FFFFFF;          // White

  // WARNING: #E4251B (red) on white is 3.9:1 - FAILS AA for normal text
  // Only use for large text or with background adjustment
}
```

#### NHS Color Palette

NHS approved colors with tested accessibility:

```scss
// NHS Blue (primary)
$nhs-blue: #005EB8;           // Safe on white (4.5:1+)

// Emergency red
$nhs-red: #DA291C;            // Use with caution, fails on white for small text

// Dark grey (text)
$nhs-dark-grey: #4C6272;      // Safe on white (7.5:1)

// Mid grey (secondary text)
$nhs-mid-grey: #768692;       // Safe on white (4.6:1)
```

#### GOV.UK Color Palette

```scss
// GOV.UK Blue
$govuk-blue: #1D70B8;         // Safe on white (4.5:1+)

// GOV.UK Green (success)
$govuk-green: #00703C;        // Safe on white (7.1:1)

// GOV.UK Red (error)
$govuk-red: #D4351C;          // Safe on white (4.6:1)

// Text color
$govuk-text: #0B0C0C;         // Near-black (19.4:1)
```

### 2.4 Focus States

**Critical for keyboard navigation:**

```scss
// All interactive elements MUST have visible focus indicators
a, button, input, select, textarea {
  &:focus {
    outline: 3px solid #FFDD00;    // Yellow outline (NHS standard)
    outline-offset: 0;

    // Alternative: GOV.UK style
    // outline: 3px solid #FFBF47;
    // box-shadow: inset 0 0 0 3px #0B0C0C;
  }

  // Never remove focus outlines completely!
  // &:focus { outline: none; } ❌ NEVER DO THIS
}
```

#### GOV.UK Focus Pattern

```scss
*:focus {
  outline: 3px solid #FFBF47;      // Yellow
  outline-offset: 0;
  box-shadow:
    inset 0 0 0 4px #0B0C0C;       // Inner black border
}
```

### 2.5 Interactive Elements

#### Minimum Touch Targets

- **Minimum size**: 44×44 CSS pixels (WCAG 2.1)
- **Recommended**: 48×48 CSS pixels (better for motor impairments)

```scss
button, .btn, a.clickable {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;

  // Add spacing between interactive elements
  & + & {
    margin-left: 8px;
  }
}
```

#### Link Styling

```scss
// Links MUST be distinguishable from text
a {
  color: #0066CC;
  text-decoration: underline;    // Always underline body links

  &:hover {
    color: #003D7A;
    text-decoration: none;       // Optional: remove on hover
  }

  &:visited {
    color: #551A8B;              // Distinct visited color
  }

  &:active {
    color: #C00E0E;
  }
}

// Exception: Navigation links can use other patterns
.nav a {
  text-decoration: none;         // OK in clear navigation context
}
```

### 2.6 Form Accessibility

```scss
// Labels MUST be associated with inputs
label {
  display: block;
  margin-bottom: 4px;
  font-weight: 600;

  // Minimum label font size
  font-size: 1rem;  // 16px
}

// Error states
.error {
  border: 2px solid #D4351C;    // Red border

  & + .error-message {
    color: #D4351C;
    font-weight: 600;
    margin-top: 4px;

    // Include icon for non-color indicators
    &::before {
      content: "⚠ ";
    }
  }
}

// Success states
.success {
  border: 2px solid #00703C;    // Green border
}
```

### 2.7 Status & Feedback

**Never rely on color alone** to convey status:

```scss
// ❌ BAD: Color only
.success { color: green; }
.error { color: red; }

// ✅ GOOD: Color + Icon + Text
.success {
  color: #00703C;
  &::before {
    content: "✓ ";
  }
}

.error {
  color: #D4351C;
  &::before {
    content: "✗ ";
  }
}
```

### 2.8 Accessibility Checklist

Every theme must meet these requirements:

- [ ] Color contrast meets WCAG AA (4.5:1 for normal text)
- [ ] Font size minimum 16px
- [ ] Line height minimum 1.5
- [ ] Focus indicators always visible
- [ ] Links underlined or clearly distinguishable
- [ ] Touch targets minimum 44×44px
- [ ] Status not conveyed by color alone
- [ ] Form labels properly associated
- [ ] Keyboard navigation fully supported
- [ ] Heading hierarchy logical (h1 → h2 → h3)
- [ ] Skip links provided for long navigation
- [ ] Images have alt text
- [ ] Tested with screen reader
- [ ] Tested with keyboard only (no mouse)
- [ ] Tested with 200% zoom
- [ ] Text can be resized without horizontal scrolling

---

## 3. Content Optimization for Text-Heavy Resources

### 3.1 Design Philosophy

Xerte sites are primarily used for:
- Educational resources
- Training documentation
- Policy guidance
- Reference materials
- Learning content

**Design priorities:**
1. **Readability** over visual flair
2. **Scannability** for quick information finding
3. **Focus** on content, not decoration
4. **Professional** appearance for institutional trust

### 3.2 Typography for Reading

```scss
// Optimized for long-form reading
body {
  font-size: 18px;           // Larger for less eye strain
  line-height: 1.6;          // Comfortable line spacing
  max-width: 65ch;           // Optimal line length (45-75 characters)
  color: #0B0C0C;           // True black for maximum readability
}

// Generous paragraph spacing
p {
  margin-bottom: 1.5em;      // Clear separation
}

// Hierarchy for scanning
h2 {
  margin-top: 2em;           // Clear section breaks
  margin-bottom: 0.5em;
}

h3 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}
```

### 3.3 Reading Line Length

```scss
// Contain text width for readability
.content {
  max-width: 65ch;           // Characters, not pixels
  margin: 0 auto;

  // On wide screens, don't stretch text
  @media (min-width: 1200px) {
    max-width: 750px;        // Absolute max
  }
}
```

### 3.4 Clean, Professional Aesthetic

```scss
// Minimal decoration
:root {
  --color-bg-body: #FFFFFF;          // Clean white
  --color-bg-subtle: #F9FAFB;        // Very subtle grey

  --spacing-section: 3rem;           // Generous whitespace

  --border-subtle: 1px solid #E5E7EB;  // Delicate borders
  --radius-subtle: 4px;              // Gentle corners

  --shadow-subtle: 0 1px 2px rgba(0, 0, 0, 0.05);  // Minimal shadows
}

// Avoid:
// ❌ Gradients
// ❌ Heavy shadows
// ❌ Bright colors everywhere
// ❌ Decorative fonts
// ❌ Busy backgrounds
```

---

## 4. Theme Structure Overview

### 4.1 Required Files (Root Level)

Every theme MUST have these files in the root theme directory:

| File | Purpose | Example |
|------|---------|---------|
| `{themename}.info` | Theme metadata and configuration | `cardiffuni.info` |
| `{themename}.scss` | Main SCSS entry point | `cardiffuni.scss` |
| `{themename}.css` | Compiled CSS output | `cardiffuni.css` |
| `{themename}.css.map` | Source map for debugging | `cardiffuni.css.map` |
| `{themename}.js` | Optional JavaScript enhancements | `cardiffuni.js` |
| `{themename}.jpg` or `.png` | Theme preview image (optional) | `cardiffuni.jpg` |

### 4.2 Recommended Folder Structure

**Recommended Folder Structure** (Modern Modular - Used by `cardiffuni-v2`):

```
themename/
├── themename.info
├── themename.scss          # Main entry point
├── themename.css           # Compiled output
├── themename.css.map
├── themename.js
├── design-tokens.json      # Optional: Design JSON for tooling
├── scss/                   # SCSS source files
│   ├── _tokens.scss        # Primitive tokens (SCSS variables, compile-time)
│   ├── _allvariables.scss  # Semantic tokens (CSS custom properties, runtime)
│   ├── _base-elements.scss # Base HTML element styles
│   ├── _bootstrap-components.scss # Bootstrap component overrides (tabs, accordions, alerts)
│   ├── _layouts.scss       # Page structure (header, nav, footer, jumbotron)
│   ├── _xerte-components.scss # Xerte-specific components
│   ├── _custom-components.scss # Custom component imports
│   ├── _utilities.scss     # Utility classes
│   ├── _editorstyles.scss  # CKEditor styles
│   ├── _enhancements.scss  # Modern CSS features
│   ├── _webkitCustoms.scss # Browser-specific overrides
│   └── components/         # Individual custom components
│       ├── _buttons.scss
│       ├── _boxes.scss
│       ├── _callout.scss
│       ├── _cards.scss
│       ├── _details.scss
│       ├── _links.scss
│       └── _quotes.scss
├── demos/                  # Component demonstrations
│   ├── index.html          # Demo homepage
│   ├── typography.html
│   ├── base-elements-demo.html
│   ├── lists-tables.html
│   ├── forms.html
│   ├── components.html
│   ├── colors.html
│   └── assets/             # Demo-specific assets
│       └── demo-styles.css
└── docs/                   # Documentation (optional)
    ├── THEMING-GUIDE.md
    └── README.md
```

> **Note:** The Modern Modular Structure above is the recommended and adopted approach for all new themes. See `cardiffuni-v2` for the reference implementation.

---

## 5. Theme Configuration File (`.info`)

The `.info` file is a **required configuration file** that Xerte uses to identify and display the theme.

### 5.1 Required Format

```ini
name: themename
display name: Your Theme Display Name
description: A brief description of your theme
enabled: yes
preview: themename.jpg
```

### 5.2 Example from Cardiff University Theme

```ini
name: cardiffuni
display name: Cardiff University
description: Cardiff University branded theme with official colors
enabled: yes
preview: cardiffuni.jpg
```

### 5.3 Important Notes

- **`name`**: Must match your theme folder name and file names
- **`display name`**: Human-readable name shown in Xerte UI
- **`description`**: Brief explanation (1-2 sentences)
- **`enabled`**: Set to `yes` to make theme available
- **`preview`**: Optional preview image filename

---

## 6. Main SCSS Entry Point

### 6.1 Structure Pattern (Modern Approach)

```scss
/**
 * [Theme Name] - Main Entry Point
 *
 * This file orchestrates the theme by importing modular SCSS components.
 */

/* 1. Design Tokens & Variables */
@use "scss/_allvariables" as *;   // Semantic tokens (imports primitives internally)

/* 2. Base Styles */
@use "scss/enhancements";          // Modern CSS enhancements
@use "scss/base-elements";         // HTML element styles

/* 3. Component Styles */
@use "scss/bootstrap-components";  // Bootstrap component overrides (tabs, accordions, alerts)
@use "scss/layouts";               // Page structure (header, nav, footer, jumbotron)
@use "scss/xerte-components";      // Xerte-specific components
@use "scss/custom-components";     // Custom components (imports from components/ folder)

/* 4. Utilities & Layout */
@use "scss/utilities";             // Utility classes

/* 5. Editor Styles */
@use "scss/editorstyles";          // CKEditor custom styles

/* 6. External Resources */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
```

### 6.2 Key Principles

1. **Use `@use` over `@import`** for SCSS modules (modern Sass syntax)
2. **Import order matters**: Variables → Base → Components → Utilities
3. **Keep it modular**: Each `@use` should import a focused concern
4. **Document the purpose**: Comment each section clearly

---

## 7. Design Tokens - Hybrid Architecture

The `cardiffuni-v2` theme uses a **hybrid token architecture** with two layers:

| Layer | File | Purpose | Format |
|-------|------|---------|--------|
| **Primitives** | `_tokens.scss` | Raw brand values (source of truth) | SCSS variables (`$token-*`) |
| **Semantics** | `_allvariables.scss` | Runtime-configurable tokens | CSS custom properties (`--*`) |

### 7.1 Primitive Tokens (_tokens.scss)

Primitive tokens are **immutable brand values** that define your design foundation. They are SCSS variables used at compile-time.

```scss
/**
 * PRIMITIVE TOKENS - Raw, immutable brand values.
 * These are the foundation that semantic tokens build upon.
 */

// =============================================================================
// BRAND COLORS
// =============================================================================

// Primary Brand Colors
$token-color-brand-primary: #E4251B;    // Cardiff Red - PMS 485 C
$token-color-brand-secondary: #121212;  // Cardiff Black
$token-color-brand-white: #FFFFFF;
$token-color-brand-light: #f9fafb;      // Off-white for backgrounds

// Grayscale (10% increments)
$token-color-gray-10: #F2F2F2;
$token-color-gray-20: #E5E5E5;
$token-color-gray-30: #CCCCCC;
// ... through gray-90

// Accent Colors
$token-color-accent-forest-green: #07873E;
$token-color-accent-light-blue: #1E90FF;
$token-color-accent-orange: #E9761E;
$token-color-accent-yellow: #FFB300;

// =============================================================================
// TYPOGRAPHY
// =============================================================================

$token-font-family-primary: "Marr Sans", "Inter", -apple-system, sans-serif;
$token-font-family-secondary: "Darby Serif", Georgia, serif;

$token-font-weight-regular: 400;
$token-font-weight-medium: 500;
$token-font-weight-semibold: 600;
$token-font-weight-bold: 700;

$token-font-size-base: 16px;
$token-font-size-lg: 20px;
$token-font-size-xl: 24px;
// ...

// =============================================================================
// SPACING (8px base unit)
// =============================================================================

$token-spacing-1: 4px;
$token-spacing-2: 8px;
$token-spacing-4: 16px;
$token-spacing-6: 24px;
$token-spacing-8: 32px;
// ...

// =============================================================================
// ACCESSIBILITY
// =============================================================================

$token-focus-ring-width: 2px;
$token-min-touch-target: 44px;
```

### 7.2 Token Naming Convention

- **Prefix all tokens** with `$token-`
- **Use brand-neutral names** where possible: `$token-color-brand-primary` not `$token-color-cardiff-red`
- **Group by category**: colors, typography, spacing, borders, shadows, animation
- **Document Pantone/official codes** in comments for brand colors

---

## 8. Semantic Tokens (_allvariables.scss)

Semantic tokens convert primitive SCSS variables to **CSS custom properties** for runtime theming.

### 8.1 Import Pattern

```scss
/**
 * Semantic Design Tokens
 * Uses @use to import primitives and generates CSS custom properties
 */

@use "tokens" as t;  // Import primitive tokens with namespace

:root {
    // =========================================================================
    // BRAND COLORS (from primitives)
    // =========================================================================
    
    --color-brand-primary: #{t.$token-color-brand-primary};
    --color-brand-secondary: #{t.$token-color-brand-secondary};
    
    // =========================================================================
    // SEMANTIC COLORS (derived)
    // =========================================================================
    
    --color-text-primary: var(--color-brand-secondary);
    --color-text-inverse: var(--color-white);
    --color-bg-body: var(--color-light);
    --color-bg-page: var(--color-white);
    
    // Links (traditional blue, not brand color)
    --color-link-default: #0645AD;
    --color-link-hover: color-mix(in srgb, var(--color-link-default) 70%, black);
    --color-link-visited: #551A8B;
}
```

### 8.2 Modern CSS Techniques

#### Using `color-mix()` for State Variations

Generate hover, active, and disabled states dynamically:

```scss
:root {
    // Button states using color-mix()
    --btn-primary-bg: var(--color-brand-primary);
    --btn-primary-hover-bg: color-mix(in srgb, var(--color-brand-primary) 85%, black);
    --btn-primary-active-bg: color-mix(in srgb, var(--color-brand-primary) 80%, black);
    --btn-primary-disabled-bg: color-mix(in srgb, var(--color-brand-primary) 60%, white);
    
    // Auto-generated color scales
    --color-brand-primary-light: color-mix(in srgb, var(--color-brand-primary) 70%, white);
    --color-brand-primary-dark: color-mix(in srgb, var(--color-brand-primary) 70%, black);
}
```

#### Fluid Typography with `clamp()`

Responsive font sizes without media queries:

```scss
:root {
    // Fluid font sizes (min, preferred, max)
    --font-size-base: clamp(0.875rem, 0.80rem + 0.375vw, 1rem);
    --font-size-lg: clamp(1.125rem, 1.00rem + 0.625vw, 1.25rem);
    --font-size-xl: clamp(1.25rem, 1.10rem + 0.75vw, 1.5rem);
    --font-size-2xl: clamp(1.5rem, 1.30rem + 1vw, 1.75rem);
    --font-size-3xl: clamp(1.875rem, 1.60rem + 1.375vw, 2.25rem);
    --font-size-4xl: clamp(2.25rem, 1.90rem + 1.75vw, 3rem);
}
```

#### Heading Style Tokens

Pre-composed heading styles for consistency:

```scss
:root {
    --h1-font-size: var(--font-size-4xl);
    --h1-font-weight: var(--font-weight-bold);
    --h1-line-height: var(--line-height-snug);
    --h1-letter-spacing: var(--letter-spacing-tighter);
    
    --h2-font-size: var(--font-size-3xl);
    --h2-font-weight: var(--font-weight-bold);
    // ... and so on for h3-h6
}
```

### 8.3 Theme Variants

Override CSS variables for different themes:

```scss
// Dark mode
[data-theme="dark"] {
    --color-bg-body: #1a1a1a;
    --color-bg-page: #121212;
    --color-text-primary: #ffffff;
    --color-link-default: #6DB3F2;
}

// High contrast
[data-theme="high-contrast"] {
    --color-bg-body: #000000;
    --color-text-primary: #FFFFFF;
    --color-brand-primary: #FFFF00;
    --focus-ring-width: 4px;
}

// Alternative institution
[data-theme="other-uni"] {
    --color-brand-primary: #0066CC;
    --color-brand-secondary: #003366;
}
```

### 8.4 Benefits

- **Runtime customization**: Change colors without recompiling SCSS
- **JavaScript API**: Modify design values dynamically via `element.style.setProperty()`
- **Theme variants**: Dark mode, high contrast, institution-specific branding
- **Reduced code**: `color-mix()` eliminates need for manually calculated shades

---

## 9. Essential Components to Customize

Based on analyzing existing themes, here are the **minimum components you must style**:

### 9.1 Base HTML Elements (_base-elements.scss)

```scss
// Typography
h1, h2, h3, h4, h5, h6 { }
p { }
a { }
strong, em { }
code, pre { }

// Lists
ul, ol { }
dl, dt, dd { }

// Tables
table { }
thead, tbody, tr, th, td { }

// Forms
input, textarea, select { }
button { }

// Media
img, figure, figcaption { }

// Other
blockquote { }
hr { }
```

### 9.2 Bootstrap Components (_bootstrap-components.scss)

If using Bootstrap, override these:

```scss
// Alerts
.alert { }
.alert-success, .alert-info, .alert-warning, .alert-danger { }

// Buttons
.btn { }
.btn-primary, .btn-secondary, .btn-success { }

// Cards
.card { }
.card-header, .card-body, .card-footer { }

// Navigation
.nav { }
.navbar { }
.breadcrumb { }

// Forms
.form-group { }
.form-control { }

// Modal
.modal { }

// Progress
.progress { }
.progress-bar { }

// Badges
.badge { }

// List Group
.list-group { }
.list-group-item { }
```

### 9.3 Xerte-Specific Components (_xerte-components.scss)

These are Xerte Online Toolkits specific components:

```scss
// Page layouts
.page-header { }
.page-footer { }

// Content containers
.xerte-page { }
.xerte-content { }

// Navigation
.page-navigation { }
.toc { }  // Table of contents

// Interactive elements
.interactive-element { }
.quiz-question { }
.feedback { }

// Media players
.video-container { }
.audio-player { }
```

### 9.4 Utility Classes (_utilities.scss)

Provide helpful utility classes:

```scss
// Spacing
.mt-1, .mt-2, .mt-3 { }  // Margin top
.mb-1, .mb-2, .mb-3 { }  // Margin bottom
.p-1, .p-2, .p-3 { }     // Padding

// Flexbox
.flex { }
.flex-wrap { }
.justify-between, .justify-center { }
.items-center { }
.gap-sm, .gap-md, .gap-lg { }

// Grid
.w-md-50 { }  // Width 50% on medium+
.w-md-33 { }  // Width 33% on medium+

// Images
.image-full { }        // Full width image
.pull-left, .pull-right { }

// Lists
.list-none { }        // No bullets
.list-icon { }        // Custom icons
```

---

## 10. JavaScript File (Optional)

### 10.1 Purpose

Use `{themename}.js` for:
- Theme-specific interactions
- Dynamic theme switching
- Accessibility enhancements
- Custom event handlers

### 10.2 Example Structure

```javascript
/**
 * Theme Name - JavaScript Enhancements
 */

(function() {
  'use strict';

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    // Initialize theme features
    initDarkMode();
    initAccessibility();
    initInteractiveElements();
  }

  function initDarkMode() {
    // Dark mode toggle logic
  }

  function initAccessibility() {
    // Accessibility enhancements
  }

  function initInteractiveElements() {
    // Custom interactions
  }

})();
```

---

## 11. Documentation Requirements

### 11.1 Minimum Documentation

Every theme should include:

1. **README.md** - Overview, installation, usage
2. **THEMING-GUIDE.md** - Customization instructions
3. **CHANGELOG.md** - Version history (optional but recommended)

### 11.2 README.md Template

```markdown
# [Theme Name]

Brief description of the theme.

## Installation

1. Copy the theme folder to `themes/site/`
2. Compile SCSS: `sass themename.scss themename.css`
3. Enable in Xerte settings

## Features

- List key features
- Responsive design
- Accessible components
- etc.

## Customization

See [THEMING-GUIDE.md](docs/THEMING-GUIDE.md) for details.

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Credits

Author, contributors, licenses, etc.
```

### 11.3 Demo Files

Include demo HTML files to showcase components:

- `base-elements-demo.html` - All base HTML elements
- `bootstrap-components-demo.html` - Bootstrap components
- `component-showcase.html` - Custom components

---

## 12. Build & Compilation

### 12.1 SCSS Compilation

#### Option 1: Live Sass Compiler (VS Code Extension)

**Recommended for ease of use:**

1. Install the [Live Sass Compiler](https://marketplace.visualstudio.com/items?itemName=ritwickdey.live-sass) extension in VS Code
2. Configure in `.vscode/settings.json`:

```json
{
  "liveSassCompile.settings.formats": [
    {
      "format": "expanded",
      "extensionName": ".css",
      "savePath": null
    }
  ],
  "liveSassCompile.settings.generateMap": true,
  "liveSassCompile.settings.autoprefix": ["> 1%", "last 2 versions"]
}
```

3. Click "Watch Sass" in VS Code status bar
4. Edit `.scss` files and see automatic compilation

#### Option 2: Dart Sass CLI

**For command-line workflows:**

```bash
# Install Dart Sass
npm install -g sass

# Compile with source maps
sass themename.scss themename.css --source-map

# Watch for changes during development
sass --watch themename.scss:themename.css

# Production build (compressed)
sass themename.scss themename.css --style=compressed --no-source-map
```

### 12.2 Recommended npm Scripts

Add to `package.json` (if using npm):

```json
{
  "scripts": {
    "build": "sass themename.scss themename.css --style=compressed",
    "watch": "sass --watch themename.scss:themename.css",
    "dev": "sass --watch themename.scss:themename.css --source-map"
  }
}
```

---

## 13. Zero-Config Styling Philosophy

**Core Principle:** The bare-bones theme should make content look professional and accessible **without requiring end users to add any classes to HTML**.

### 13.1 Design Approach

```
Basic User          Intermediate User        Advanced User
     ↓                     ↓                       ↓
No classes needed    Optional utilities      Full component library
     ↓                     ↓                       ↓
Just HTML tags →    Add .btn, .alert  →    Custom components
```

### 13.2 Base Elements Must Be Self-Sufficient

All base HTML elements should be beautifully styled by default:

```html
<!-- User writes this simple HTML -->
<h1>Welcome to the Course</h1>
<p>This is a paragraph with a <a href="#">link</a> in it.</p>
<ul>
  <li>First item</li>
  <li>Second item</li>
</ul>

<!-- It looks professional immediately, no classes needed -->
```

### 13.3 Implementation Strategy

#### Level 1: Zero-Config (Base Elements)

Style ALL HTML tags to look great by default:

```scss
// _base-elements.scss
h1 {
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.2;
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
  font-weight: 700;
}

p {
  font-size: 1.125rem;        // 18px by default
  line-height: 1.6;
  margin-bottom: 1.5em;
  max-width: 65ch;
}

a {
  color: var(--color-link);
  text-decoration: underline;

  &:hover {
    color: var(--color-link-hover);
  }
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;

  th, td {
    padding: 12px 16px;
    border: 1px solid var(--border-color);
    text-align: left;
  }

  th {
    background-color: var(--color-bg-subtle);
    font-weight: 600;
  }
}

// Forms look good without classes
input[type="text"],
input[type="email"],
textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;

  &:focus {
    outline: 3px solid var(--focus-color);
    outline-offset: 0;
  }
}

button {
  background: var(--color-primary);
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  min-height: 44px;

  &:hover {
    background: var(--color-primary-dark);
  }
}
```

#### Level 2: Bootstrap Enhancement (Optional Classes)

Bootstrap classes work when users want more control:

```html
<!-- User can optionally add Bootstrap classes -->
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-success">Success Button</button>

<div class="alert alert-warning">
  This is a warning message
</div>
```

#### Level 3: Advanced Components (Power Users)

See section 14 below for the component library.

### 13.4 Styling Priority

```scss
/* 1. Base elements (highest priority - always applied) */
p { ... }
a { ... }

/* 2. Bootstrap 2 components (when classes are used) */
.btn { ... }
.alert { ... }

/* 3. Utility classes (when explicitly added) */
.mt-3 { ... }
.text-center { ... }

/* 4. Custom components (advanced usage) */
.card-feature { ... }
.callout-box { ... }
```

### 13.5 Testing Zero-Config

Create test HTML with NO classes:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="stylesheet" href="themename.css">
</head>
<body>
  <h1>Main Heading</h1>
  <p>A paragraph with <a href="#">a link</a> and <strong>bold text</strong>.</p>

  <h2>Subheading</h2>
  <ul>
    <li>List item one</li>
    <li>List item two</li>
  </ul>

  <table>
    <thead>
      <tr><th>Column 1</th><th>Column 2</th></tr>
    </thead>
    <tbody>
      <tr><td>Data 1</td><td>Data 2</td></tr>
    </tbody>
  </table>

  <form>
    <label>Name</label>
    <input type="text" placeholder="Enter name">
    <button>Submit</button>
  </form>
</body>
</html>
```

**Success Criteria:** This page should look professional, accessible, and complete without adding a single class.

---

## 14. Advanced Component Library

For power users who want more sophisticated components beyond basic HTML.

### 14.1 Library Structure

```
scss/
├── components/
│   ├── _buttons.scss          # Advanced button variants
│   ├── _cards.scss            # Card components
│   ├── _callouts.scss         # Callout/note boxes
│   ├── _tabs.scss             # Tab interfaces
│   ├── _accordions.scss       # Accordion/collapse
│   ├── _modals.scss           # Modal dialogs
│   ├── _tooltips.scss         # Tooltips
│   ├── _breadcrumbs.scss      # Breadcrumb navigation
│   ├── _pagination.scss       # Pagination
│   └── _custom.scss           # Institution-specific components
```

### 14.2 Component Documentation

Each component should have:

1. **Purpose** - What it's for
2. **HTML Example** - Copy-paste ready code
3. **Variants** - Available options
4. **Accessibility** - ARIA attributes, keyboard support
5. **Browser Support** - Any limitations

#### Example: Callout Component

**Purpose:** Highlight important information

**HTML:**
```html
<div class="callout callout-info">
  <h4>Did you know?</h4>
  <p>Additional information goes here.</p>
</div>
```

**Variants:**
- `.callout-info` - Information (blue)
- `.callout-success` - Success (green)
- `.callout-warning` - Warning (yellow)
- `.callout-danger` - Danger (red)

**SCSS:**
```scss
.callout {
  padding: 1.5rem;
  margin: 2rem 0;
  border-left: 4px solid;
  border-radius: 4px;
  background: var(--color-bg-subtle);

  h4 {
    margin-top: 0;
    font-weight: 600;
  }

  &.callout-info {
    border-color: var(--color-info);
    background: var(--color-info-bg);
  }

  &.callout-success {
    border-color: var(--color-success);
    background: var(--color-success-bg);
  }

  &.callout-warning {
    border-color: var(--color-warning);
    background: var(--color-warning-bg);
  }

  &.callout-danger {
    border-color: var(--color-danger);
    background: var(--color-danger-bg);
  }
}
```

### 14.3 Component Showcase

Create `component-showcase.html` with ALL components:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Component Library - Theme Name</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap.min.css">
  <link rel="stylesheet" href="themename.css">
</head>
<body>
  <div class="container">
    <h1>Component Library</h1>

    <!-- Buttons -->
    <section>
      <h2>Buttons</h2>
      <button class="btn">Default</button>
      <button class="btn btn-primary">Primary</button>
      <button class="btn btn-success">Success</button>
    </section>

    <!-- Callouts -->
    <section>
      <h2>Callouts</h2>
      <div class="callout callout-info">
        <h4>Information</h4>
        <p>This is an informational callout.</p>
      </div>
    </section>

    <!-- Add all other components... -->
  </div>
</body>
</html>
```

### 14.4 Utility Classes Library

Create comprehensive utilities in `_utilities.scss`:

```scss
// =============================================================================
// SPACING UTILITIES
// =============================================================================

// Margin top
.mt-0 { margin-top: 0 !important; }
.mt-1 { margin-top: 0.25rem !important; }  // 4px
.mt-2 { margin-top: 0.5rem !important; }   // 8px
.mt-3 { margin-top: 1rem !important; }     // 16px
.mt-4 { margin-top: 1.5rem !important; }   // 24px
.mt-5 { margin-top: 2rem !important; }     // 32px

// Margin bottom (same pattern)
.mb-0 { margin-bottom: 0 !important; }
.mb-1 { margin-bottom: 0.25rem !important; }
// ...

// Padding (same pattern)
.p-0 { padding: 0 !important; }
.p-1 { padding: 0.25rem !important; }
// ...

// =============================================================================
// FLEXBOX UTILITIES
// =============================================================================

.flex { display: flex !important; }
.flex-column { flex-direction: column !important; }
.flex-wrap { flex-wrap: wrap !important; }

.justify-start { justify-content: flex-start !important; }
.justify-center { justify-content: center !important; }
.justify-between { justify-content: space-between !important; }
.justify-end { justify-content: flex-end !important; }

.items-start { align-items: flex-start !important; }
.items-center { align-items: center !important; }
.items-end { align-items: flex-end !important; }

.gap-sm { gap: 0.5rem !important; }
.gap-md { gap: 1rem !important; }
.gap-lg { gap: 1.5rem !important; }

// =============================================================================
// WIDTH/HEIGHT UTILITIES
// =============================================================================

.w-25 { width: 25% !important; }
.w-50 { width: 50% !important; }
.w-75 { width: 75% !important; }
.w-100 { width: 100% !important; }

.w-auto { width: auto !important; }

// Responsive widths
@media (min-width: 768px) {
  .w-md-25 { width: 25% !important; }
  .w-md-33 { width: 33.333% !important; }
  .w-md-50 { width: 50% !important; }
  .w-md-66 { width: 66.666% !important; }
  .w-md-75 { width: 75% !important; }
  .w-md-100 { width: 100% !important; }
}

// =============================================================================
// TEXT UTILITIES
// =============================================================================

.text-left { text-align: left !important; }
.text-center { text-align: center !important; }
.text-right { text-align: right !important; }

.text-small { font-size: 0.875rem !important; }
.text-large { font-size: 1.25rem !important; }

.font-bold { font-weight: 700 !important; }
.font-normal { font-weight: 400 !important; }

// =============================================================================
// DISPLAY UTILITIES
// =============================================================================

.d-none { display: none !important; }
.d-block { display: block !important; }
.d-inline { display: inline !important; }
.d-inline-block { display: inline-block !important; }

// Responsive display
@media (min-width: 768px) {
  .d-md-none { display: none !important; }
  .d-md-block { display: block !important; }
}

// =============================================================================
// BACKGROUND/BORDER UTILITIES
// =============================================================================

.bg-light { background-color: var(--color-bg-light) !important; }
.bg-dark { background-color: var(--color-bg-dark) !important; }
.bg-primary { background-color: var(--color-primary) !important; }

.border { border: 1px solid var(--border-color) !important; }
.border-0 { border: 0 !important; }
.rounded { border-radius: 4px !important; }
.rounded-lg { border-radius: 8px !important; }
```

---

## 15. Theme Designer Tool (Standalone Project)

**Goal:** Create a visual designer inspired by [v0.app Design Systems](https://v0.app/chat/design-systems/v0example--base) that allows users to customize themes and export CSS custom properties.

> **Note:** This will be developed as a **standalone project**, separate from the core theme files. The theme architecture must be designed to support easy customization through CSS custom properties.

### 15.1 Design Vision

**Inspired by v0.app Design Systems interface** - A simplified version with clean layout and intuitive controls.

**Key Customization Areas:**
1. **Colors** - Brand colors, backgrounds, text, accents
2. **Typography** - Font families, sizes, weights, line heights
3. **Corners** - Border radius values
4. **Borders** - Border widths and styles
5. **Shadows** - Shadow depths and styles

### 15.2 User Workflow

Users should be able to:
1. **Adjust design tokens** via intuitive controls (color pickers, sliders, dropdowns)
2. **Preview changes** in real-time across multiple components
3. **See accessibility warnings** if colors fail WCAG standards
4. **Export CSS variables** to paste into their project
5. **Save/load theme presets** for different schools/departments

### 15.3 Tool Structure

```
theme-designer/
├── index.html              # Main designer interface
├── designer.css            # Designer UI styles
├── designer.js             # Designer logic
├── preview-iframe.html     # Live preview iframe
└── presets/               # Pre-made themes
    ├── default.json
    ├── dark-mode.json
    ├── high-contrast.json
    └── nhs-style.json
```

### 15.4 Designer Interface (Mockup)

```
┌─────────────────────────────────────────────────────────────┐
│  Xerte Theme Designer                    [ Reset ] [ Export ]│
├─────────────────────┬───────────────────────────────────────┤
│                     │                                       │
│  📦 Base Colors     │  PREVIEW                             │
│  ├─ Primary         │  ┌─────────────────────────────────┐ │
│  │  [#E4251B] 🎨   │  │ <h1>Heading Level 1</h1>        │ │
│  │  ⚠ Fails WCAG   │  │ <p>This is a paragraph with     │ │
│  │                  │  │ <a href="#">a link</a>.</p>      │ │
│  ├─ Background      │  │                                  │ │
│  │  [#FFFFFF] 🎨   │  │ <button>Click Me</button>        │ │
│  │  ✓ Passes WCAG  │  │                                  │ │
│  │                  │  │ <div class="alert">Alert box</div│ │
│  └─ Text            │  └─────────────────────────────────┘ │
│     [#121212] 🎨   │                                       │
│     ✓ Passes WCAG  │                                       │
│                     │                                       │
│  📏 Typography      │                                       │
│  ├─ Base Size       │                                       │
│  │  [18px] ─────•  │                                       │
│  ├─ Line Height     │                                       │
│  │  [1.6] ──────•  │                                       │
│  └─ Font Family     │                                       │
│     [Inter] ▼       │                                       │
│                     │                                       │
│  🎨 Accent Colors   │                                       │
│  ├─ Success         │                                       │
│  │  [#00703C] 🎨   │                                       │
│  ├─ Warning         │                                       │
│  │  [#FFBF47] 🎨   │                                       │
│  └─ Danger          │                                       │
│     [#D4351C] 🎨   │                                       │
│                     │                                       │
│  📐 Spacing         │                                       │
│  └─ Scale           │                                       │
│     [8px base] ──•  │                                       │
│                     │                                       │
│  💾 Presets         │                                       │
│  ├─ Default         │                                       │
│  ├─ Dark Mode       │                                       │
│  ├─ High Contrast   │                                       │
│  └─ NHS Style       │                                       │
│                     │                                       │
└─────────────────────┴───────────────────────────────────────┘
```

### 15.5 Implementation Approach

#### HTML Structure (designer.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Xerte Theme Designer</title>
  <link rel="stylesheet" href="designer.css">
</head>
<body>
  <div class="designer-layout">
    <!-- Left Panel: Controls -->
    <aside class="designer-controls">
      <h1>Theme Designer</h1>

      <!-- Base Colors -->
      <section class="control-section">
        <h2>Base Colors</h2>
        <div class="color-picker-group">
          <label>Primary Color
            <input type="color" id="color-primary" value="#E4251B">
            <span class="wcag-status" id="wcag-primary"></span>
          </label>
          <label>Background Color
            <input type="color" id="color-bg" value="#FFFFFF">
          </label>
          <label>Text Color
            <input type="color" id="color-text" value="#121212">
          </label>
        </div>
      </section>

      <!-- Typography -->
      <section class="control-section">
        <h2>Typography</h2>
        <label>Base Font Size
          <input type="range" id="font-size" min="14" max="22" value="18">
          <output id="font-size-output">18px</output>
        </label>
        <label>Line Height
          <input type="range" id="line-height" min="1.2" max="2" step="0.1" value="1.6">
          <output id="line-height-output">1.6</output>
        </label>
      </section>

      <!-- Accent Colors -->
      <section class="control-section">
        <h2>Accent Colors</h2>
        <label>Success <input type="color" id="color-success" value="#00703C"></label>
        <label>Warning <input type="color" id="color-warning" value="#FFBF47"></label>
        <label>Danger <input type="color" id="color-danger" value="#D4351C"></label>
      </section>

      <!-- Actions -->
      <div class="designer-actions">
        <button id="btn-reset">Reset to Default</button>
        <button id="btn-export" class="btn-primary">Export CSS</button>
      </div>
    </aside>

    <!-- Right Panel: Live Preview -->
    <main class="designer-preview">
      <iframe id="preview-frame" src="preview-iframe.html"></iframe>
    </main>
  </div>

  <!-- Export Modal -->
  <dialog id="export-modal">
    <h2>Export Theme CSS</h2>
    <p>Copy this CSS and add it to your project:</p>
    <textarea id="export-css" readonly rows="20"></textarea>
    <button id="btn-copy">Copy to Clipboard</button>
    <button id="btn-close-modal">Close</button>
  </dialog>

  <script src="designer.js"></script>
</body>
</html>
```

#### JavaScript Logic (designer.js)

```javascript
/**
 * Xerte Theme Designer
 * Allows visual customization and export of theme CSS variables
 */

class ThemeDesigner {
  constructor() {
    this.iframe = document.getElementById('preview-frame');
    this.controls = this.getControls();
    this.init();
  }

  getControls() {
    return {
      colorPrimary: document.getElementById('color-primary'),
      colorBg: document.getElementById('color-bg'),
      colorText: document.getElementById('color-text'),
      fontSize: document.getElementById('font-size'),
      lineHeight: document.getElementById('line-height'),
      colorSuccess: document.getElementById('color-success'),
      colorWarning: document.getElementById('color-warning'),
      colorDanger: document.getElementById('color-danger'),
    };
  }

  init() {
    // Add event listeners to all controls
    Object.entries(this.controls).forEach(([key, control]) => {
      control.addEventListener('input', () => this.updatePreview());
    });

    // Export button
    document.getElementById('btn-export').addEventListener('click', () => {
      this.showExportModal();
    });

    // Reset button
    document.getElementById('btn-reset').addEventListener('click', () => {
      this.resetToDefaults();
    });

    // Initial update
    this.updatePreview();
  }

  updatePreview() {
    const cssVars = this.generateCSSVariables();

    // Apply to preview iframe
    const iframeDoc = this.iframe.contentDocument;
    if (iframeDoc) {
      const root = iframeDoc.documentElement;
      Object.entries(cssVars).forEach(([key, value]) => {
        root.style.setProperty(key, value);
      });
    }

    // Check accessibility
    this.checkAccessibility();
  }

  generateCSSVariables() {
    return {
      '--color-primary': this.controls.colorPrimary.value,
      '--color-bg': this.controls.colorBg.value,
      '--color-text': this.controls.colorText.value,
      '--font-size-base': this.controls.fontSize.value + 'px',
      '--line-height-base': this.controls.lineHeight.value,
      '--color-success': this.controls.colorSuccess.value,
      '--color-warning': this.controls.colorWarning.value,
      '--color-danger': this.controls.colorDanger.value,
    };
  }

  checkAccessibility() {
    // Check contrast ratio for primary color on background
    const primary = this.controls.colorPrimary.value;
    const bg = this.controls.colorBg.value;
    const ratio = this.getContrastRatio(primary, bg);

    const status = document.getElementById('wcag-primary');
    if (ratio >= 4.5) {
      status.textContent = '✓ Passes WCAG AA';
      status.className = 'wcag-status pass';
    } else {
      status.textContent = '⚠ Fails WCAG AA';
      status.className = 'wcag-status fail';
    }
  }

  getContrastRatio(color1, color2) {
    // Simplified contrast calculation
    // In production, use proper WCAG formula
    const l1 = this.getLuminance(color1);
    const l2 = this.getLuminance(color2);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }

  getLuminance(hexColor) {
    // Convert hex to RGB and calculate relative luminance
    const rgb = parseInt(hexColor.slice(1), 16);
    const r = ((rgb >> 16) & 0xff) / 255;
    const g = ((rgb >> 8) & 0xff) / 255;
    const b = (rgb & 0xff) / 255;

    const [rs, gs, bs] = [r, g, b].map(c => {
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });

    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
  }

  showExportModal() {
    const cssVars = this.generateCSSVariables();
    const css = this.generateExportCSS(cssVars);

    document.getElementById('export-css').value = css;
    document.getElementById('export-modal').showModal();
  }

  generateExportCSS(vars) {
    let css = '/* Paste this into your custom-theme.css */\n\n:root {\n';
    Object.entries(vars).forEach(([key, value]) => {
      css += `  ${key}: ${value};\n`;
    });
    css += '}\n';
    return css;
  }

  resetToDefaults() {
    // Reset to default values
    this.controls.colorPrimary.value = '#E4251B';
    this.controls.colorBg.value = '#FFFFFF';
    this.controls.colorText.value = '#121212';
    this.controls.fontSize.value = '18';
    this.controls.lineHeight.value = '1.6';
    this.controls.colorSuccess.value = '#00703C';
    this.controls.colorWarning.value = '#FFBF47';
    this.controls.colorDanger.value = '#D4351C';

    this.updatePreview();
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new ThemeDesigner();
  });
} else {
  new ThemeDesigner();
}
```

### 15.6 Export Format

When users click "Export", they get:

```css
/* Paste this into your custom-theme.css or add to your HTML */

:root {
  /* Brand Colors */
  --color-primary: #E4251B;
  --color-bg: #FFFFFF;
  --color-text: #121212;

  /* Typography */
  --font-size-base: 18px;
  --line-height-base: 1.6;

  /* Accent Colors */
  --color-success: #00703C;
  --color-warning: #FFBF47;
  --color-danger: #D4351C;
}

/*
 * Usage Instructions:
 * 1. Create a file called 'custom-theme.css'
 * 2. Paste this code into it
 * 3. Load it AFTER your main theme CSS:
 *    <link rel="stylesheet" href="themename.css">
 *    <link rel="stylesheet" href="custom-theme.css">
 */
```

### 15.7 Accessibility Validation

The designer should:

1. **Real-time contrast checking** - Show WCAG pass/fail for all color combinations
2. **Warnings for small text** - Alert if font size < 16px
3. **Line height validation** - Warn if < 1.5
4. **Touch target size** - Ensure buttons meet 44×44px minimum

### 15.8 Preset Themes

Include pre-made accessible themes:

```javascript
const PRESETS = {
  default: {
    colorPrimary: '#E4251B',
    colorBg: '#FFFFFF',
    colorText: '#121212',
    fontSize: '18',
    lineHeight: '1.6',
  },
  darkMode: {
    colorPrimary: '#FF6B5B',
    colorBg: '#1a1a1a',
    colorText: '#FFFFFF',
    fontSize: '18',
    lineHeight: '1.6',
  },
  highContrast: {
    colorPrimary: '#FFFF00',
    colorBg: '#000000',
    colorText: '#FFFFFF',
    fontSize: '20',
    lineHeight: '1.8',
  },
  nhsStyle: {
    colorPrimary: '#005EB8',
    colorBg: '#FFFFFF',
    colorText: '#212B32',
    fontSize: '19',
    lineHeight: '1.5',
  },
};
```

---

## 16. Step-by-Step Theme Creation Checklist

### Phase 1: Setup & Planning

- [ ] Gather brand guidelines (colors, fonts, logos)
- [ ] Choose folder structure (Option A or B)
- [ ] Create theme directory: `themes/site/{themename}/`
- [ ] Create `.info` file with theme metadata

### Phase 2: Design Tokens

- [ ] Create `_tokens.scss` with brand colors
- [ ] Define typography tokens (fonts, sizes, weights)
- [ ] Define spacing scale (4px, 8px, 16px, etc.)
- [ ] Define border radii and shadows
- [ ] Define animation timings

### Phase 3: CSS Variables

- [ ] Create `_allvariables.scss`
- [ ] Convert SCSS tokens to CSS custom properties
- [ ] Add semantic color aliases
- [ ] Add auto-generated color scales (optional)

### Phase 4: Base Styles

- [ ] Style all base HTML elements in `_base-elements.scss`
- [ ] Set global typography styles
- [ ] Style links with all states (default, hover, visited, active)
- [ ] Style lists (ul, ol, dl)
- [ ] Style tables
- [ ] Style forms and inputs

### Phase 5: Component Styles

- [ ] Bootstrap components (if applicable)
  - [ ] Buttons (all variants and sizes)
  - [ ] Alerts
  - [ ] Cards
  - [ ] Navigation (navbar, tabs, breadcrumbs)
  - [ ] Forms
  - [ ] Modals
  - [ ] Progress bars
  - [ ] Badges
- [ ] Xerte-specific components
  - [ ] Page layouts
  - [ ] Navigation
  - [ ] Interactive elements
  - [ ] Media players
- [ ] Custom components (project-specific)

### Phase 6: Utilities & Layout

- [ ] Create utility classes (_utilities.scss)
- [ ] Create layout helpers (_layouts.scss)
- [ ] Add responsive breakpoints
- [ ] Add flexbox/grid utilities

### Phase 7: Testing & Documentation

- [ ] Create demo HTML files
- [ ] Test on all target browsers
- [ ] Test responsive behavior
- [ ] Test accessibility (keyboard navigation, screen readers)
- [ ] Write README.md
- [ ] Write THEMING-GUIDE.md
- [ ] Document customization options

### Phase 8: Deployment

- [ ] Compile production CSS
- [ ] Minify assets
- [ ] Test in Xerte environment
- [ ] Create preview image
- [ ] Set `enabled: yes` in .info file

---

## 17. Best Practices

### 17.1 Code Organization

✅ **DO:**
- Use a consistent naming convention (BEM, SMACSS, or similar)
- Keep files focused on a single concern
- Document complex styles with comments
- Use SCSS variables and mixins to reduce repetition
- Group related styles together

❌ **DON'T:**
- Put all styles in one massive file
- Use overly specific selectors (`.page > .container > .content > p`)
- Use `!important` unless absolutely necessary
- Hard-code values - use tokens/variables instead

### 17.2 Accessibility

✅ **MUST:**
- Maintain WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Provide focus indicators for all interactive elements
- Support keyboard navigation
- Use semantic HTML
- Test with screen readers

### 17.3 Performance

✅ **OPTIMIZE:**
- Minimize CSS file size (use compression)
- Remove unused styles
- Use efficient selectors
- Limit use of expensive properties (box-shadow, animations)
- Load web fonts efficiently

### 17.4 Maintainability

✅ **ENSURE:**
- Code is well-documented
- Variables are semantic and descriptive
- Styles are modular and reusable
- Breaking changes are documented
- Version numbers follow semantic versioning

---

## 18. Common Customization Scenarios

### Scenario 1: Different Organization Branding

**Goal:** Create a theme for Swansea University using Cardiff theme as base.

**Steps:**
1. Copy `cardiffuni` theme folder → `swansea`
2. Update `swansea.info` with new metadata
3. Update `_tokens.scss` with Swansea brand colors
4. Update fonts if different
5. Update preview image
6. Compile and test

### Scenario 2: Dark Mode Variant

**Goal:** Add dark mode to existing theme.

**Steps:**
1. Add dark mode CSS custom properties in `_allvariables.scss`:
   ```scss
   [data-theme="dark"] {
     --color-bg-body: #1a1a1a;
     --color-text-primary: #ffffff;
     // ... etc
   }
   ```
2. Add JavaScript toggle in `themename.js`
3. Test all components in dark mode
4. Update documentation

### Scenario 3: Project-Specific Theme

**Goal:** Create a one-off theme for a specific project within an organization.

**Steps:**
1. Use base organization theme
2. Create custom CSS file: `project-overrides.css`
3. Override specific CSS variables:
   ```css
   :root {
     --color-brand-primary: #custom-color;
   }
   ```
4. Load after main theme CSS

---

## 19. Troubleshooting

### Issue: Styles not applying

**Causes & Solutions:**
- SCSS not compiled → Run `sass themename.scss themename.css`
- CSS specificity conflict → Check if other styles override yours
- File not loaded → Verify file path in Xerte config
- Browser cache → Hard refresh (Cmd+Shift+R / Ctrl+Shift+F5)

### Issue: Colors look wrong

**Causes & Solutions:**
- Color token typo → Double-check variable names
- CSS variable not defined → Check `:root` definitions
- Color mixing not supported → Update to modern browser or use fallbacks

### Issue: Layout broken on mobile

**Causes & Solutions:**
- Missing responsive breakpoints → Add media queries
- Fixed widths → Use relative units (%, rem, em)
- Viewport meta tag missing → Add to HTML

---

## 20. Resources & References

### Official Documentation
- Xerte Online Toolkits: https://xerte.org.uk/
- Sass Documentation: https://sass-lang.com/documentation
- CSS Custom Properties: https://developer.mozilla.org/en-US/docs/Web/CSS/--*
- CSS color-mix(): https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix

### Theming Examples
- **Cardiff University v2** (Reference): `/themes/site/cardiffuni-v2/` — Modern implementation with hybrid tokens
- Cardiff University v1: `/themes/site/cardiffuni/`
- DigEd Theme: `/themes/site/diged/`
- Black Grey Theme: `/themes/site/blackgrey/`

### Tools
- Dart Sass Compiler: https://sass-lang.com/install
- Color Contrast Checker: https://webaim.org/resources/contrastchecker/
- Browser DevTools: Chrome, Firefox, Safari, Edge

---

## 21. Conclusion

This standardization guide provides a comprehensive framework for creating consistent, maintainable, and accessible themes for Xerte Online Toolkits. By following these guidelines, you'll ensure:

✅ **Consistency** across all themes
✅ **Maintainability** for long-term support
✅ **Flexibility** for customization
✅ **Quality** through best practices
✅ **Accessibility** for all users

For questions or suggestions, refer to existing theme documentation or consult with the development team.

---

**Document Version History:**
- v1.1 (2026-01-25): Updated to align with `cardiffuni-v2` reference implementation
  - Added hybrid token architecture (primitives + semantics)
  - Updated folder structure (`_layouts.scss`, `components/` subfolder)
  - Added modern CSS techniques (`color-mix()`, `clamp()`, heading tokens)
  - Removed `--cu-` prefix for generic token naming
  - Updated demo pages structure
- v1.0 (2026-01-22): Initial standardization guide created based on `cardiffuni` and `diged` theme analysis
