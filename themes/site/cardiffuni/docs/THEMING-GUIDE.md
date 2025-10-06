# Cardiff University Theme - Customization Guide

**Last Updated:** October 6, 2025

This theme uses CSS Custom Properties (CSS Variables) for easy runtime customization without needing to recompile SCSS.

## Quick Start: Customizing Colors

### Option 1: Inline Styles (Quick Testing)

```html
<style>
  :root {
    --color-brand-primary: #0066CC;
    --spacing-lg: 32px;
  }
</style>
```

### Option 2: External Stylesheet (Recommended)

Create a file `custom-theme.css`:

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
  --font-size-base: 18px;
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

## Available Color Scales

All color scales auto-update when you change the base color:

```css
:root {
  /* Change this */
  --color-brand-primary: #0066CC;

  /* These update automatically */
  --color-brand-primary-lighter  /* 30% lighter */
  --color-brand-primary-light    /* 15% lighter */
  --color-brand-primary-dark     /* 15% darker */
  --color-brand-primary-darker   /* 30% darker */
}
```

## Creating Project-Specific Themes

### Method 1: Override in HTML

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

### Method 2: Dark Mode

```css
[data-theme="dark"] {
  --color-bg-body: #1a1a1a;
  --color-bg-page: #121212;
  --color-text-primary: #ffffff;
  --color-text-inverse: #121212;
  --color-brand-primary: #FF6B5B; /* Brighter for dark mode */
}
```

Toggle with JavaScript:
```javascript
// Toggle dark mode
const isDark = document.body.getAttribute('data-theme') === 'dark';
document.body.setAttribute('data-theme', isDark ? '' : 'dark');
```

### Method 3: Per-Project Branding

For completely different organizations:

```css
/* Swansea University */
[data-theme="swansea"] {
  --color-brand-primary: #660066;
  --color-brand-secondary: #FFD700;
  --cu-primary-red: #660066; /* Override Cardiff red */
}

/* Cardiff Met University */
[data-theme="cardiffmet"] {
  --color-brand-primary: #C41E3A;
  --color-accent-green: #FFB81C;
}
```

## Available Variables

### Colors

#### Cardiff University Brand Colors (Fixed)
- `--cu-primary-red`, `--cu-white`, `--cu-black`
- `--cu-gray-10` through `--cu-gray-90` (10% increments)
- `--cu-forest-green`, `--cu-cadet`, `--cu-stone`, etc.

#### Semantic Colors (Customizable)
- `--color-text-primary`, `--color-text-inverse`, `--color-text-alert`
- `--color-brand-primary`, `--color-brand-secondary`
- `--color-link-default`, `--color-link-hover`, `--color-link-visited`
- `--color-accent-green`, `--color-accent-blue`, `--color-accent-orange`
- `--color-bg-body`, `--color-bg-page`, `--color-bg-panel`

#### Auto-Generated Scales
- `--color-brand-primary-lighter/light/dark/darker`
- `--color-brand-secondary-lighter/light/dark/darker`
- `--color-accent-*-light/dark`
- `--color-bg-subtle/muted/elevated`
- `--color-text-subtle/muted`

### Typography
- Font families: `--font-primary-body`, `--font-primary-heading`, `--font-secondary`
- Font sizes: `--font-size-xs` through `--font-size-4xl`
- Line heights: `--line-height-tight/normal/loose`
- Font weights: `--font-weight-light/regular/medium/bold`

### Spacing
- `--spacing-xs` through `--spacing-4xl` (4px, 8px, 16px, 24px, 32px, 48px, 64px, 80px)

### Borders
- Radius: `--radius-none/sm/md/lg/xl/pill`
- Width: `--border-width-sm/md/lg`
- Colors: `--border-color-default/light/dark`

### Shadows
- `--shadow-none/sm/md/lg`

### Animation
- Duration: `--animation-fast/medium/slow`
- Easing: `--animation-easing/easing-in/easing-out`

## Examples

### Example 1: Green Environmental Project

```css
:root {
  --color-brand-primary: #2E7D32;
  --color-brand-secondary: #689F38;
  --color-accent-green: #558B2F;
  --color-bg-body: #F1F8E9;
}
```

### Example 2: Medical/Health Theme

```css
:root {
  --color-brand-primary: #1976D2;
  --color-accent-blue: #42A5F5;
  --color-bg-body: #E3F2FD;
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem); /* Larger for accessibility */
}
```

### Example 3: High Contrast (Accessibility)

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

## Browser Support

CSS Custom Properties are supported in all modern browsers:
- Chrome/Edge 49+
- Firefox 31+
- Safari 9.1+
- Opera 36+

`color-mix()` requires:
- Chrome/Edge 111+
- Firefox 113+
- Safari 16.2+

For older browsers, the base colors will still work (color scales won't auto-update).

## Tips

1. **Test in Dev Tools**: Use browser dev tools to live-edit CSS variables and see changes instantly
2. **Keep Cardiff Branding**: Don't override `--cu-*` colors unless creating a completely different theme
3. **Use Semantic Variables**: Override `--color-brand-primary` instead of `--cu-primary-red` for flexibility
4. **Accessibility**: Maintain sufficient color contrast when customizing
5. **Document Your Theme**: Keep a record of which variables you've overridden

## Need Help?

- Check `_allvariables.scss` for all available variables
- See commented theme examples in `_allvariables.scss`
- Test your theme with the browser's accessibility inspector
