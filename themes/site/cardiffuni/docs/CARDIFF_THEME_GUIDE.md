# Cardiff University Theme Development Guide

This guide explains how to work with the Cardiff University theme for Xerte Online Toolkits (Bootstrap/Site templates).

## Table of Contents

1. [Brand Colors](#1-brand-colors)
2. [Typography](#2-typography)
3. [Component Styling](#3-component-styling)
4. [Development Workflow](#4-development-workflow)
5. [Accessibility Guidelines](#5-accessibility-guidelines)

---

## 1. Brand Colors

### Primary Colors

The theme uses Cardiff University's official brand colors:

| Color | Hex | Variable | Usage |
|---|---|---|---|
| **Primary Red** | `#E4251B` | `$cu-primary-red` | Primary actions, links, highlights |
| **White** | `#FFFFFF` | `$cu-white` | Backgrounds, text on dark |
| **Black** | `#121212` | `$cu-black` | Text, dark backgrounds |

### Grey Scale

Cardiff's grey scale uses 10% increments from black:

| Color | Hex | Variable |
|---|---|---|
| **10% Grey** | `#F2F2F2` | `$cu-gray-10` |
| **20% Grey** | `#E5E5E5` | `$cu-gray-20` |
| **30% Grey** | `#CCCCCC` | `$cu-gray-30` |
| **40% Grey** | `#B3B3B3` | `$cu-gray-40` |
| **50% Grey** | `#999999` | `$cu-gray-50` |
| **60% Grey** | `#808080` | `$cu-gray-60` |
| **70% Grey** | `#666666` | `$cu-gray-70` |
| **80% Grey** | `#4C4C4C` | `$cu-gray-80` |
| **90% Grey** | `#333333` | `$cu-gray-90` |

### Accent Colors

**Use sparingly!** These colors should only be used for specific purposes:

| Color | Hex | Variable | Contrast |
|---|---|---|---|
| **Forest Green** | `#07873E` | `$cu-forest-green` | Black and white |
| **Cadet** | `#5EB99B` | `$cu-cadet` | Black |
| **Stone** | `#C9C2BA` | `$cu-stone` | Black and white |
| **Light Blue** | `#1E90FF` | `$cu-light-blue` | Black |
| **Royal Blue** | `#4A42FF` | `$cu-royal-blue` | White |
| **Midnight Blue** | `#273573` | `$cu-midnight-blue` | White |
| **Midnight Purple** | `#26192C` | `$cu-midnight-purple` | White |
| **Orange** | `#E9761E` | `$cu-orange` | White |
| **Yellow** | `#FFB300` | `$cu-yellow` | Black |
| **Yellow Green** | `#85C041` | `$cu-yellow-green` | Black |
| **Indigo** | `#570185` | `$cu-indigo` | White |
| **Dark Violet** | `#D401C5` | `$cu-dark-violet` | Black and White |

### Color Contrast Rules

Following Cardiff University guidelines:

- **Red background** → Use white or black text
- **White background** → Use black or red text
- **Black background** → Use white text only (never red)

---

## 2. Typography

### Font Families

This theme prioritizes **readability** over brand-specific fonts, using:

**Primary Font (Body Text & Headings):**
```scss
$mainfonts: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

**Secondary Font (Quotes, Emphasis):**
```scss
$secondaryfonts: Georgia, "Times New Roman", Times, serif;
```

> **Note:** The official Cardiff brand fonts (Marr Sans and Darby Serif) are not used in this theme to ensure accessibility and readability for learning materials.

### Font Sizes

Following Cardiff University's digital typography guidelines:

| Element | Size | Variable | Line Height |
|---|---|---|---|
| **Base body copy** | 18px | `$font-size-base` | 1.5 (27px) |
| **Small text** | 16px | `$font-size-small` | 1.5 (24px) |
| **Small heading** | 24px | `$font-size-heading-sm` | 1.2 (28.8px) |
| **Medium heading** | 30px | `$font-size-heading-md` | 1.2 (36px) |
| **Large heading** | 36px | `$font-size-heading-lg` | 1.2 (43.2px) |
| **XL heading** | 48px | `$font-size-heading-xl` | 1.2 (57.6px) |

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
   - Maintain minimum 18px for body text
   - Use adequate line spacing (1.5 for body, 1.2 for headings)
   - Keep line length between 50-75 characters for optimal readability

---

## 3. Component Styling

### Buttons

#### Primary Buttons
```scss
background: $cu-primary-red (#E4251B)
color: $cu-white
hover: darken($cu-primary-red, 10%)
```

#### Secondary Buttons
```scss
background: $cu-white
border: 2px solid $cu-primary-red
color: $cu-primary-red
hover: background changes to light red
```

### Navigation

The navbar uses:
```scss
background: $cu-black (#121212)
link color: $cu-white
hover/active: $cu-primary-red background
```

### Panels & Cards

```scss
background: $cu-primary-red
text: $cu-white
border-radius: 4px
```

### Tables

Striped tables use:
```scss
odd rows: $cu-forest-green (accent color)
text on accent: black for contrast
```

### Footer

```scss
background: $cu-black
text: $cu-white
links: $cu-white
```

---

## 4. Development Workflow

### File Structure

```
themes/site/cardiffuni/
├── cardiffuni.scss          # Main SCSS file
├── cardiffuni.css           # Compiled CSS (auto-generated)
├── cardiffuni.css.map       # Source map (auto-generated)
├── cardiffuni.js            # Optional JavaScript
├── cardiffuni.info          # Theme metadata
├── cardiffuni.jpg           # Preview image
├── CARDIFF_THEME_GUIDE.md   # This file
└── scss/
    ├── _allvariables.scss   # All color and typography variables
    ├── _editorstyles.scss   # CKEditor styling
    └── _webkitCustoms.scss  # Custom scrollbar styles
```

### Editing the Theme

1. **Edit SCSS files** in the `scss/` folder or the main `cardiffuni.scss` file
2. **Save** - Live Sass Compiler will auto-compile
3. **Add Google Fonts import** to compiled CSS if it was stripped:
   ```css
   @import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap");
   ```
   Add this at the very top of `cardiffuni.css` if missing after compilation

### Customizing Colors

All colors are defined in `scss/_allvariables.scss`:

```scss
// Official Cardiff colors
$cu-primary-red: #E4251B;
$cu-black: #121212;
// ... etc

// Theme mappings
$brightcolor: $cu-primary-red;
$contrastcolor: $cu-black;
// ... etc
```

To change a color:
1. Edit the variable in `_allvariables.scss`
2. Save and let it compile
3. Check the preview

### Customizing Typography

Font settings are in `scss/_allvariables.scss`:

```scss
$mainfonts: "Inter", -apple-system, ...;
$font-size-base: 18px;
$line-height-normal: 1.5;
```

---

## 5. Accessibility Guidelines

### Color Contrast

Always ensure sufficient contrast ratios:

- **Normal text:** Minimum 4.5:1
- **Large text (18pt+):** Minimum 3:1
- **UI components:** Minimum 3:1

Use the contrast guidelines in Section 1 for Cardiff brand colors.

### Text Readability

1. **Minimum font sizes:**
   - Body text: 18px (1.125rem)
   - Small text: 16px (1rem)
   - Never go below 16px

2. **Line spacing:**
   - Body text: 1.5
   - Headings: 1.2
   - Never use line-height below 1.2

3. **Line length:**
   - Optimal: 50-75 characters per line
   - Maximum: 90 characters per line

### Focus States

Ensure all interactive elements have visible focus states using Cardiff Red:

```scss
:focus {
  outline: 2px solid $cu-primary-red;
  outline-offset: 2px;
}
```

### Icon Usage

- Use [Ionicons (sharp set)](https://ionic.io/ionicons) as per Cardiff guidelines
- Always provide text labels alongside icons
- Ensure icons have sufficient contrast

---

## Quick Reference

### Common Variables

```scss
// Colors
$cu-primary-red        // #E4251B
$cu-black              // #121212
$cu-white              // #FFFFFF
$cu-gray-10 to 90      // Grey scale

// Typography
$mainfonts             // Inter + system fonts
$secondaryfonts        // Georgia + serif fonts
$font-size-base        // 18px
$line-height-normal    // 1.5

// Spacing
$defaultpagepadding    // 2%
$contentmargin         // 2%
```

### File to Edit for...

- **Colors:** `scss/_allvariables.scss`
- **Typography:** `scss/_allvariables.scss`
- **Main styles:** `cardiffuni.scss`
- **Editor styles:** `scss/_editorstyles.scss`
- **Scrollbars:** `scss/_webkitCustoms.scss`

---

## Support

For Cardiff University brand guidelines, visit: https://brand.cardiff.ac.uk/

For Xerte development questions, see: [CLAUDE.md](../../../CLAUDE.md)
