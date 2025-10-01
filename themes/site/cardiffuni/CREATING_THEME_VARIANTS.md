# Creating Theme Variants

This guide shows you how to create new theme variants from the Cardiff University base theme using the design token system.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Creating Your First Variant](#creating-your-first-variant)
3. [Common Customizations](#common-customizations)
4. [Example Variants](#example-variants)

---

## Architecture Overview

The theme uses a **three-layer architecture**:

```
┌─────────────────────────────────────────────┐
│  Layer 1: _tokens.scss                      │
│  Cardiff University Brand Design Tokens     │
│  (Official brand values - DO NOT EDIT)      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 2: _allvariables.scss                │
│  Theme Variable Mapping                     │
│  (Map tokens to theme - CUSTOMIZE HERE)     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 3: Component Styles                  │
│  (Uses variables from Layer 2)              │
└─────────────────────────────────────────────┘
```

### Benefits:

- **Consistency**: All themes use official Cardiff brand colors
- **Flexibility**: Easy to create variants by remapping tokens
- **Maintainability**: Brand updates happen in one place (_tokens.scss)
- **Scalability**: Create unlimited theme variants

---

## Creating Your First Variant

Let's create a "Cardiff Blue" theme variant as an example.

### Step 1: Copy the Theme Folder

```bash
cd themes/site
cp -r cardiffuni cardiffblue
```

### Step 2: Update Theme Metadata

Edit `cardiffblue/cardiffblue.info`:

```
name: cardiffblue
display name: Cardiff University - Blue Variant
description: Cardiff University theme with blue as primary color
enabled: yes
preview: cardiffblue.jpg
```

### Step 3: Rename Files

```bash
cd cardiffblue
mv cardiffuni.scss cardiffblue.scss
mv cardiffuni.js cardiffblue.js
```

### Step 4: Customize `_allvariables.scss`

Open `scss/_allvariables.scss` and change the color mappings:

```scss
// BEFORE (Cardiff Red theme):
$brightcolor: t.$token-color-primary-red;       // Primary brand color (red)

// AFTER (Cardiff Blue variant):
$brightcolor: t.$token-color-accent-royal-blue; // Primary brand color (blue)
```

That's it! The entire theme will now use blue instead of red for:
- Links
- Buttons
- Navigation highlights
- Accents

### Step 5: Compile

Run your SASS compiler or restart Live Sass Compiler.

---

## Common Customizations

### Change Primary Color

The `$brightcolor` variable controls the main accent color throughout the theme:

```scss
// Options:
$brightcolor: t.$token-color-primary-red;        // Cardiff Red (default)
$brightcolor: t.$token-color-accent-royal-blue;  // Royal Blue
$brightcolor: t.$token-color-accent-forest-green;// Forest Green
$brightcolor: t.$token-color-accent-midnight-blue;// Midnight Blue
$brightcolor: t.$token-color-accent-orange;      // Orange
```

### Change Background Colors

```scss
// Light background (body)
$bodybackgroundcolor: t.$token-bg-secondary;     // Light grey (default)
$bodybackgroundcolor: t.$token-bg-primary;       // White

// Page background
$defaultpagebackground: t.$token-bg-primary;     // White (default)
$defaultpagebackground: t.$token-color-gray-10;  // Light grey
```

### Change Dark/Header Color

```scss
// Dark contrast color (navigation, footer)
$contrastcolor: t.$token-bg-dark;                // Black (default)
$contrastcolor: t.$token-color-accent-midnight-blue; // Midnight Blue
$contrastcolor: t.$token-color-gray-90;          // Dark grey
```

### Change Accent Colors

```scss
// Accent colors for tables, panels, etc.
$accent1: t.$token-color-accent-forest-green;    // Default
$accent2: t.$token-color-accent-light-blue;      // Default
$accent3: t.$token-color-accent-orange;          // Default

// Try different combinations:
$accent1: t.$token-color-accent-cadet;
$accent2: t.$token-color-accent-stone;
$accent3: t.$token-color-accent-yellow;
```

### Change Font Stack

```scss
// Default (Cardiff brand fonts with Inter fallback):
$mainfonts: t.$token-font-primary-body;
$headingfonts: t.$token-font-primary-heading;

// Use only web-safe fonts:
$mainfonts: "Inter", -apple-system, sans-serif;
$headingfonts: "Inter", -apple-system, sans-serif;

// Use serif for body:
$mainfonts: t.$token-font-secondary;  // Georgia, serif
```

### Adjust Spacing

```scss
// Default page padding
$defaultpagepadding: t.$token-spacing-lg;  // 24px (default)
$defaultpagepadding: t.$token-spacing-xl;  // 32px (more spacious)
$defaultpagepadding: t.$token-spacing-md;  // 16px (compact)
```

### Adjust Border Radius

```scss
// Default rounded corners
$largeroundedcorners: t.$token-radius-lg;   // 8px (default)
$mediumroundedcorners: t.$token-radius-md;  // 4px (default)

// More rounded:
$largeroundedcorners: t.$token-radius-xl;   // 12px
$mediumroundedcorners: t.$token-radius-lg;  // 8px

// Less rounded (sharper):
$largeroundedcorners: t.$token-radius-md;   // 4px
$mediumroundedcorners: t.$token-radius-sm;  // 2px
```

---

## Example Variants

### Example 1: "Cardiff Night" (Dark Blue Theme)

**Color Scheme**: Midnight blue primary, dark backgrounds

```scss
// In _allvariables.scss
$brightcolor: t.$token-color-accent-midnight-blue;
$contrastcolor: t.$token-color-accent-midnight-purple;
$accent1: t.$token-color-accent-royal-blue;
$accent2: t.$token-color-accent-light-blue;
$accent3: t.$token-color-accent-cadet;
```

### Example 2: "Cardiff Nature" (Green Theme)

**Color Scheme**: Forest green primary, natural tones

```scss
// In _allvariables.scss
$brightcolor: t.$token-color-accent-forest-green;
$contrastcolor: t.$token-color-gray-90;
$accent1: t.$token-color-accent-yellow-green;
$accent2: t.$token-color-accent-cadet;
$accent3: t.$token-color-accent-stone;
```

### Example 3: "Cardiff Energy" (Orange/Yellow Theme)

**Color Scheme**: Orange primary, warm colors

```scss
// In _allvariables.scss
$brightcolor: t.$token-color-accent-orange;
$contrastcolor: t.$token-color-gray-90;
$accent1: t.$token-color-accent-yellow;
$accent2: t.$token-color-accent-yellow-green;
$accent3: t.$token-color-primary-red;
```

### Example 4: "Cardiff Professional" (Minimal Grey)

**Color Scheme**: Subdued greys with red accents

```scss
// In _allvariables.scss
$brightcolor: t.$token-color-gray-70;  // Subdued primary
$contrastcolor: t.$token-color-gray-90;
$accent1: t.$token-color-primary-red;   // Red for important items
$accent2: t.$token-color-gray-60;
$accent3: t.$token-color-gray-50;

// Increase contrast
$darkestcolor: t.$token-color-primary-black;
$lightestcolor: t.$token-color-primary-white;
```

### Example 5: "Cardiff High Contrast" (Accessibility Focus)

**Color Scheme**: Maximum contrast for accessibility

```scss
// In _allvariables.scss
$brightcolor: t.$token-color-primary-red;
$contrastcolor: t.$token-color-primary-black;
$darkestcolor: t.$token-color-primary-black;
$lightestcolor: t.$token-color-primary-white;
$bodybackgroundcolor: t.$token-bg-primary;  // Pure white

// Use less rounded corners for clarity
$largeroundedcorners: t.$token-radius-sm;
$mediumroundedcorners: t.$token-radius-sm;

// Increase font sizes
$font-size-base: t.$token-font-size-lg;  // 24px instead of 18px
```

---

## File Checklist for New Variants

When creating a new theme variant, make sure you have:

- [ ] Copied and renamed the theme folder
- [ ] Updated `.info` file with new theme name and metadata
- [ ] Renamed `.scss`, `.css`, and `.js` files to match theme name
- [ ] Customized `scss/_allvariables.scss` with your color mappings
- [ ] Updated `@use` statements if file names changed
- [ ] Compiled SCSS to CSS
- [ ] Added Google Fonts import to top of compiled CSS (if missing)
- [ ] Created preview image (`.jpg`) showing theme appearance
- [ ] Tested theme in Xerte bootstrap project

---

## Advanced Customization

### Using Custom Colors (Outside Design Tokens)

If you need a color not in the Cardiff palette:

```scss
// Define custom color first
$custom-teal: #008B8B;

// Then use it
$brightcolor: $custom-teal;
```

**Note**: Using non-Cardiff colors may not align with brand guidelines.

### Mixing Multiple Token Sets

You can create hybrid themes:

```scss
// Blue primary with green accents
$brightcolor: t.$token-color-accent-royal-blue;
$accent1: t.$token-color-accent-forest-green;
$accent2: t.$token-color-accent-yellow-green;
```

### Programmatic Color Adjustments

Use SASS color functions for variations:

```scss
@use "sass:color";

// Make primary color lighter for backgrounds
$brightcolor-light: color.scale(t.$token-color-primary-red, $lightness: 40%);

// Use it
.panel-light {
  background: $brightcolor-light;
}
```

---

## Tips & Best Practices

1. **Start with small changes**: Change one variable at a time to see effects
2. **Test contrast**: Use tools like WebAIM Contrast Checker
3. **Preview on devices**: Test on mobile, tablet, desktop
4. **Document your choices**: Add comments explaining color choices
5. **Keep accessibility in mind**: Maintain 4.5:1 contrast for text
6. **Use semantic names**: Name variants by purpose, not just color
7. **Version control**: Use git to track theme variants

---

## Troubleshooting

### Colors Not Changing

- Check if Live Sass Compiler is running
- Stop and restart the compiler
- Clear browser cache
- Verify token imports: `@use "tokens" as t;`

### Compilation Errors

- Ensure all `@use` statements are at the top of files
- Check for typos in token names (e.g., `t.$token-color-primary-red`)
- Verify file paths in `@use` statements

### Missing Fonts

- Add Google Fonts import at top of compiled CSS
- Check font family fallbacks are in place

---

## Need Help?

- Review [CARDIFF_THEME_GUIDE.md](CARDIFF_THEME_GUIDE.md) for base theme documentation
- Check [Cardiff University Style Guide](https://brand.cardiff.ac.uk/) for brand guidelines
- Review token values in `scss/_tokens.scss`
