# Adding Custom Styles to CKEditor

This guide explains how to add custom styles to the CKEditor WYSIWYG editor for use in the Cardiff University theme (and other Xerte Online Toolkits projects).

## Overview

CKEditor custom styles appear in the **Styles** dropdown menu in the editor toolbar. These styles allow content creators to apply pre-defined formatting to their content without writing CSS directly.

Custom styles consist of two parts:
1. **Style definition** - JavaScript configuration that registers the style with CKEditor
2. **CSS styling** - The actual visual styling that gets applied

## File Locations

### 1. CKEditor Style Definitions
**File:** `editor/js/vendor/ckeditor/styles.js`

This file contains the **shared** style definitions used across all project types (Xerte, Site/Bootstrap, Decision tree projects).

### 2. Theme CSS Styling

For the Cardiff University Bootstrap theme:
- **SCSS Source:** `themes/site/cardiffuni/scss/_editorstyles.scss`
- **Main SCSS:** `themes/site/cardiffuni/cardiffuni.scss`
- **Compiled CSS:** `themes/site/cardiffuni/cardiffuni.css`

**Note:** For Xerte projects, CSS would be defined in the appropriate Xerte template CSS files (e.g., `modules/xerte/parent_templates/Nottingham/`).

## Step-by-Step Guide

### Step 1: Add Style Definition to CKEditor

Open `editor/js/vendor/ckeditor/styles.js` and add your style definition to the array:

```javascript
CKEDITOR.stylesSet.add( 'default', [
    // ... existing styles ...

    // Your new style
    {
        name: 'My Custom Style',           // Display name in dropdown
        element: 'div',                    // HTML element (div, span, p, blockquote, etc.)
        wrap: true,                        // Wrap existing content (for block elements)
        attributes: {
            'class': 'my-custom-style'     // CSS class name
        }
    },

    // ... more styles ...
]);
```

**Style Definition Properties:**

| Property | Required | Description | Example |
|----------|----------|-------------|---------|
| `name` | Yes | Display name in the Styles dropdown | `'Highlight Box'` |
| `element` | Yes | HTML element to apply | `'div'`, `'span'`, `'p'`, `'blockquote'` |
| `attributes` | Optional | HTML attributes (usually CSS class) | `{ 'class': 'highlight-box' }` |
| `styles` | Optional | Inline CSS styles | `{ 'color': '#ff0000' }` |
| `wrap` | Optional | Wrap existing content (for blocks) | `true` or `false` |

**Common Element Types:**
- **Block elements:** `div`, `p`, `blockquote`, `h1`-`h6`
- **Inline elements:** `span`, `strong`, `em`, `code`

### Step 2: Create CSS Styling

For the Cardiff University theme, add your styles to `themes/site/cardiffuni/scss/_editorstyles.scss`:

```scss
/* My Custom Style */
.my-custom-style {
  padding: var(--spacing-md, 1rem);
  background: var(--cu-primary-red, #E4251B);
  color: var(--cu-white, #FFFFFF);
  border-left: 4px solid var(--cu-forest-green, #07873E);
  border-radius: var(--radius-sm, 4px);
  margin: var(--spacing-md, 1rem) 0;
}
```

**Best Practices:**
- Use CSS custom properties (variables) with fallback values
- Reference Cardiff University design tokens from `_allvariables.scss`
- Provide meaningful class names that describe the style's purpose

### Step 3: Ensure SCSS Import

Verify that `_editorstyles.scss` is imported in `cardiffuni.scss`:

```scss
// In cardiffuni.scss
@use "scss/editorstyles";          // CKEditor custom styles
```

### Step 4: Compile SCSS to CSS

Compile your SCSS to CSS using one of these methods:

**Option 1: Using Sass CLI**
```bash
cd themes/site/cardiffuni
sass cardiffuni.scss cardiffuni.css
```

**Option 2: Using npm script** (if configured)
```bash
npm run build
```

**Option 3: Watch mode** (auto-compile on changes)
```bash
sass --watch cardiffuni.scss:cardiffuni.css
```

### Step 5: Test the Style

1. **Clear browser cache** (Ctrl+Shift+R or Cmd+Shift+R)
2. **Open the editor** in a Xerte project
3. **Click the Styles dropdown** in the toolbar
4. **Select your custom style**
5. **Verify** the styling appears correctly

## Example: Cardiff Test Style

Here's a complete example of the "Cardiff Test Style" created for this theme:

**1. Style Definition** (`editor/js/vendor/ckeditor/styles.js`):
```javascript
{
    name: 'Cardiff Test Style',
    element: 'div',
    wrap: true,
    attributes: { 'class': 'cardiff-test-style' }
}
```

**2. CSS Styling** (`themes/site/cardiffuni/scss/_editorstyles.scss`):
```scss
/* Cardiff Test Style - CKEditor custom style */
.cardiff-test-style {
  padding: var(--spacing-md, 1rem);
  background: var(--cu-primary-red, #E4251B);
  color: var(--cu-white, #FFFFFF);
  border-left: 4px solid var(--cu-forest-green, #07873E);
  border-radius: var(--radius-sm, 4px);
  margin: var(--spacing-md, 1rem) 0;
}
```

## Available Cardiff University Design Tokens

Reference these CSS custom properties in your styles:

### Colors
- `--cu-primary-red` - Cardiff Red (#E4251B)
- `--cu-forest-green` - Forest Green (#07873E)
- `--cu-cadet` - Cadet Green (#5EB99B)
- `--cu-orange` - Orange (#E9761E)
- `--cu-yellow` - Yellow (#FFB300)
- `--cu-white` - White (#FFFFFF)
- `--cu-black` - Black (#121212)
- `--cu-gray-10` through `--cu-gray-90` - Gray scale

### Spacing
- `--spacing-xs` (4px)
- `--spacing-sm` (8px)
- `--spacing-md` (16px)
- `--spacing-lg` (24px)
- `--spacing-xl` (32px)
- `--spacing-2xl` (48px)

### Border Radius
- `--radius-sm` (2px)
- `--radius-md` (4px)
- `--radius-lg` (8px)

See `scss/_allvariables.scss` for the complete list of available design tokens.

## Troubleshooting

### Style not appearing in dropdown

1. **Check syntax** - Verify your JavaScript syntax in `styles.js`
2. **Clear browser cache** - Hard refresh (Ctrl+Shift+R)
3. **Check browser console** - Look for JavaScript errors (F12)
4. **Verify styles dropdown is enabled** - Check CKEditor toolbar configuration

### Style appears but has no visual effect

1. **Compile SCSS** - Ensure you've run the Sass compiler
2. **Check CSS class name** - Verify the class in `styles.js` matches your CSS
3. **Inspect element** - Use browser DevTools to check if CSS is loaded
4. **Check CSS specificity** - Your style might be overridden by other CSS

### Style works in editor but not in published content

- CKEditor uses `config.contentsCss` to load styles in the editor
- Published content uses the theme's main CSS file
- Ensure your styles are in the theme's compiled CSS, not just editor-specific CSS

## Additional Resources

- [CKEditor 4 Styles Documentation](https://ckeditor.com/docs/ckeditor4/latest/guide/dev_styles.html)
- [CKEditor 4 API - stylesSet](https://ckeditor.com/docs/ckeditor4/latest/api/CKEDITOR_config.html#cfg-stylesSet)
- Cardiff Theme Guide: `docs/CARDIFF_THEME_GUIDE.md`
- Theming Guide: `docs/THEMING-GUIDE.md`

---

**Last Updated:** 2025-10-07
**Version:** 1.0
