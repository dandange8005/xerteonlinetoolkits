# Variable Migration Guide

This document outlines the migration from legacy cryptic variable names to semantic, meaningful names in the Cardiff University theme.

## Migration Date
October 1, 2025

## Overview

All theme variables have been renamed to follow a clear, semantic naming convention that makes the codebase more maintainable and easier to understand. The new naming system uses prefixes to indicate the type of property (color, spacing, border, shadow, etc.) and descriptive names that clearly indicate purpose.

## Variable Naming Convention

The new naming convention follows these patterns:

- **Color variables**: `$color-{category}-{variant}`
  - Examples: `$color-text-primary`, `$color-brand-primary`, `$color-bg-body`

- **Spacing variables**: `$spacing-{size}` or `$spacing-{context}-{purpose}`
  - Examples: `$spacing-md`, `$spacing-page-padding`

- **Border variables**: `$border-{property}-{variant}` or `$radius-{size}`
  - Examples: `$border-color-default`, `$radius-md`

- **Shadow variables**: `$shadow-{size}` or `$shadow-{context}`
  - Examples: `$shadow-md`, `$shadow-interface`

## Complete Variable Mapping

### Text Colors

| Old Variable | New Variable | Value/Token | Description |
|-------------|--------------|-------------|-------------|
| `$darkestcolor` | `$color-text-primary` | `t.$token-text-primary` | Main body text color |
| `$mainfontcolour` | `$color-text-on-light` | `t.$token-text-primary` | Text on light backgrounds |
| `$fontcolorfordarkestcolor` | `$color-text-on-dark` | `t.$token-text-inverted` | Text on dark backgrounds |
| `$fontcolorforlightestcolor` | `$color-text-on-light` | `t.$token-text-primary` | Text on light backgrounds |
| `$fontcolorfobrightcolor` | `$color-text-on-brand` | `t.$token-text-inverted` | Text on brand color backgrounds |
| `$fontcolorforcontrastcolor` | `$color-text-on-dark` | `t.$token-text-inverted` | Text on contrast/dark backgrounds |
| `$fontcolorformainhovercolor` | `$color-text-on-brand` | `t.$token-text-inverted` | Text on hover state backgrounds |
| `$hintcolor` | `$color-text-hint` | `t.$token-color-primary-red` | Hint text color |
| `$alertcolor` | `$color-text-alert` | `t.$token-color-primary-red` | Alert/error text color |

### Brand Colors

| Old Variable | New Variable | Value/Token | Description |
|-------------|--------------|-------------|-------------|
| `$brightcolor` | `$color-brand-primary` | `t.$token-color-primary-red` (#E4251B) | Primary brand color (Cardiff Red) |
| `$contrastcolor` | `$color-brand-secondary` | `t.$token-bg-dark` | Secondary brand color (black) |
| `$mainhovercolor` | `$color-brand-primary-hover` | `t.$token-btn-primary-hover` | Primary color hover state |
| `$whiteorlightest` | `$cu-white` | `t.$token-color-primary-white` (#FFFFFF) | White color |
| `$blackordarkest` | `$cu-black` | `t.$token-color-primary-black` (#121212) | Black color |

### Link Colors

| Old Variable | New Variable | Value | Description |
|-------------|--------------|-------|-------------|
| `$linkcolor` | `$color-link-default` | `#045bc6` | Default link color (blue) |
| `$linkhovercolor` | `$color-link-hover` | `#033a8a` | Link hover state (darker blue) |
| `$linkvisitedcolor` | `$color-link-visited` | `#551A8B` | Visited link color (purple) |

### Background Colors

| Old Variable | New Variable | Value/Token | Description |
|-------------|--------------|-------------|-------------|
| `$lightestcolor` | `$color-bg-body` | `t.$token-bg-secondary` | Body background color |
| `$bodybackgroundcolor` | `$color-bg-body` | `t.$token-bg-secondary` | Body background (same as above) |
| `$defaultpagebackground` | `$color-bg-page` | `t.$token-bg-primary` | Page background color |
| `$panelcolor` | `$color-bg-panel` | `t.$token-color-gray-70` | Panel background color |

### Accent Colors

| Old Variable | New Variable | Value/Token | Description |
|-------------|--------------|-------------|-------------|
| `$accent1` | `$color-accent-green` | `t.$token-color-accent-forest-green` | First accent color (forest green) |
| `$accent2` | `$color-accent-blue` | `t.$token-color-accent-light-blue` | Second accent color (light blue) |
| `$accent3` | `$color-accent-orange` | `t.$token-color-accent-orange` | Third accent color (orange) |

### Spacing Variables

| Old Variable | New Variable | Value/Token | Description |
|-------------|--------------|-------------|-------------|
| `$contentmargin` | `$spacing-content-margin` | `2%` | Content margin percentage |
| `$defaultpagepadding` | `$spacing-page-padding` | `t.$token-spacing-lg` | Default page padding |

### Border Radius Variables

| Old Variable | New Variable | Value/Token | Description |
|-------------|--------------|-------------|-------------|
| `$largeroundedcorners` | *(use `$radius-lg`)* | `t.$token-radius-lg` | Large border radius |
| `$mediumroundedcorners` | *(use `$radius-md`)* | `t.$token-radius-md` | Medium border radius |
| `$smallroundedcorners` | *(use `$radius-sm`)* | `t.$token-radius-sm` | Small border radius |
| `$imageroundedcorners` | `$radius-image` | `t.$token-radius-md` | Image border radius |

### Shadow Variables

| Old Variable | New Variable | Value/Token | Description |
|-------------|--------------|-------------|-------------|
| `$interfaceboxshadow` | `$shadow-interface` | `t.$token-shadow-md` | Interface element shadow |

## Files Updated

The following files were updated during the migration:

### 1. `scss/_allvariables.scss`
**Purpose**: Variable definitions and token mappings

**Changes**:
- Replaced all legacy variable names with semantic names
- Removed backward compatibility mappings
- Consolidated duplicate variables (e.g., `$lightestcolor` and `$bodybackgroundcolor` both became `$color-bg-body`)
- Simplified font color variables to three main categories: `on-light`, `on-dark`, `on-brand`

### 2. `cardiffuni.scss`
**Purpose**: Main theme stylesheet

**Changes**:
- Updated all variable references in body styles
- Updated heading color references
- Updated link color references (default, hover, visited)
- Updated jumbotron gradient colors
- Updated navbar background and text colors
- Updated accordion, table, panel, and footer styles
- Updated glossary and navigation pill styles

### 3. `scss/_base-elements.scss`
**Purpose**: Base HTML element styles

**Changes**:
- Updated `h2.sectionTitle` color reference
- Updated iframe caption color reference
- All other elements used Cardiff University token variables directly (`$cu-*`)

### 4. `scss/_utilities.scss`
**Purpose**: Utility classes

**Changes**:
- Updated `.list-icon` color reference
- Updated link hover color reference

## Migration Impact

### Breaking Changes
⚠️ **All legacy variable names have been removed.** If you have custom SCSS files that reference the old variable names, they will break and need to be updated.

### No Breaking Changes For
✅ **Compiled CSS output remains the same** - All color values, spacing, and visual appearance are unchanged.
✅ **Design tokens remain unchanged** - All Cardiff University brand values in `_tokens.scss` are untouched.

## How to Update Custom Code

If you have custom SCSS files or theme variants that use the old variable names, follow these steps:

### Step 1: Identify Usage
Search your custom SCSS files for any of the old variable names listed in this document.

```bash
# Example: Search for old variable names
grep -r "\$brightcolor\|\$darkestcolor\|\$linkcolor" your-custom-theme/
```

### Step 2: Replace Variables
Use the mapping tables above to replace old variables with new ones.

**Example - Before:**
```scss
.custom-header {
  background: $brightcolor;
  color: $fontcolorfobrightcolor;
  border: 1px solid $darkestcolor;
}

a.custom-link {
  color: $linkcolor;

  &:hover {
    color: $linkhovercolor;
  }
}
```

**Example - After:**
```scss
.custom-header {
  background: $color-brand-primary;
  color: $color-text-on-brand;
  border: 1px solid $color-text-primary;
}

a.custom-link {
  color: $color-link-default;

  &:hover {
    color: $color-link-hover;
  }
}
```

### Step 3: Test Compilation
After updating variable names, compile your SCSS to ensure no errors:

```bash
# Watch for compilation errors in Live Sass Compiler output
# Or manually compile if using command line tools
sass your-custom-theme.scss your-custom-theme.css
```

## Benefits of New Naming System

### 1. **Self-Documenting Code**
The new names clearly indicate what the variable is for:
- `$color-brand-primary` is obviously the primary brand color
- `$color-text-on-dark` clearly indicates text color for dark backgrounds
- Much easier to understand than `$brightcolor` or `$fontcolorfordarkestcolor`

### 2. **Better IDE Autocomplete**
Typing `$color-` gives you all color-related variables grouped together.
Typing `$spacing-` shows all spacing variables.

### 3. **Easier Onboarding**
New developers can understand the variable purpose without referencing documentation.

### 4. **Consistent with Modern CSS Practices**
Follows naming conventions similar to CSS custom properties and design systems like Tailwind, Material Design, etc.

### 5. **Easier Theme Variants**
When creating theme variants, the semantic names make it clear which variables to change:
- Want a different primary color? Change `$color-brand-primary`
- Want different link colors? Change `$color-link-default`, `$color-link-hover`, `$color-link-visited`

## Quick Reference Card

Common old → new mappings for quick reference:

```scss
// Brand Colors
$brightcolor          → $color-brand-primary
$contrastcolor        → $color-brand-secondary
$mainhovercolor       → $color-brand-primary-hover

// Text Colors
$darkestcolor         → $color-text-primary
$whiteorlightest      → $cu-white
$blackordarkest       → $cu-black

// Link Colors
$linkcolor            → $color-link-default
$linkhovercolor       → $color-link-hover
$linkvisitedcolor     → $color-link-visited

// Background Colors
$lightestcolor        → $color-bg-body
$panelcolor           → $color-bg-panel
$defaultpagebackground → $color-bg-page

// Text on Backgrounds
$fontcolorfobrightcolor     → $color-text-on-brand
$fontcolorfordarkestcolor   → $color-text-on-dark
$fontcolorforlightestcolor  → $color-text-on-light
```

## Related Documentation

- [CARDIFF_THEME_GUIDE.md](../CARDIFF_THEME_GUIDE.md) - Complete theme usage guide
- [CREATING_THEME_VARIANTS.md](../CREATING_THEME_VARIANTS.md) - How to create theme variants
- [scss/_tokens.scss](../scss/_tokens.scss) - Cardiff University design tokens
- [scss/_allvariables.scss](../scss/_allvariables.scss) - All theme variables

## Questions or Issues?

If you encounter any issues with the variable migration or need help updating custom code, please:

1. Check this migration guide for the correct variable mapping
2. Review the theme files to see examples of the new variable usage
3. Ensure your Live Sass Compiler is recompiling after changes
4. Check for typos in variable names (SCSS will error on undefined variables)

---

**Last Updated**: October 1, 2025
**Migration Version**: 2.0
**Theme**: Cardiff University (cardiffuni)
