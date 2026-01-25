# Cardiff University Theme v2

A modern, accessible theme for Xerte Online Toolkits featuring Cardiff University branding, a hybrid design token architecture, and zero-config styling.

## Features

- ✅ **Zero-Config Styling** — Beautiful styling for all HTML elements without adding classes
- ✅ **Hybrid Token Architecture** — Primitive SCSS tokens + semantic CSS custom properties
- ✅ **Modern CSS** — Uses `color-mix()`, `clamp()`, and CSS custom properties
- ✅ **Accessibility First** — WCAG AA compliant, visible focus states, 44px touch targets
- ✅ **Bootstrap 2 Compatible** — Styled overrides for tabs, accordions, alerts, and more
- ✅ **Custom Components** — Boxes, callouts, cards, quotes, and more
- ✅ **Fluid Typography** — Responsive font sizes without media queries
- ✅ **Runtime Theming** — Change colors via CSS variables without recompiling

## Quick Start

### Installation

1. Copy the `cardiffuni-v2` folder to `themes/site/` in your Xerte installation
2. Compile SCSS (if making changes):
   ```bash
   sass cardiffuni-v2.scss cardiffuni-v2.css --source-map
   ```
3. Enable the theme in Xerte settings

### Using the Theme

The theme works immediately with plain HTML — no classes required:

```html
<h1>Welcome to the Course</h1>
<p>This paragraph is automatically styled with proper typography.</p>
<a href="#">Links are accessible blue with underlines</a>

<ul>
  <li>Lists look great by default</li>
  <li>No classes needed</li>
</ul>
```

For advanced styling, use Bootstrap classes or custom components:

```html
<button class="btn btn-primary">Primary Button</button>
<div class="callout callout-info">Important information here</div>
```

## File Structure

```
cardiffuni-v2/
├── cardiffuni-v2.info          # Theme metadata
├── cardiffuni-v2.scss          # Main entry point
├── cardiffuni-v2.css           # Compiled CSS
├── cardiffuni-v2.css.map       # Source map
├── cardiffuni-v2.jpg           # Preview image
├── cardiff-design.json         # Design tokens JSON
├── scss/
│   ├── _tokens.scss            # Primitive tokens (SCSS)
│   ├── _allvariables.scss      # Semantic tokens (CSS custom properties)
│   ├── _base-elements.scss     # Base HTML element styles
│   ├── _bootstrap-components.scss  # Bootstrap overrides
│   ├── _layouts.scss           # Page structure (header, footer, nav)
│   ├── _xerte-components.scss  # Xerte-specific styles
│   ├── _custom-components.scss # Custom component imports
│   ├── _utilities.scss         # Utility classes
│   ├── _enhancements.scss      # Modern CSS features
│   ├── _editorstyles.scss      # CKEditor styles
│   └── components/             # Individual components
│       ├── _buttons.scss
│       ├── _boxes.scss
│       ├── _callout.scss
│       ├── _cards.scss
│       ├── _details.scss
│       ├── _links.scss
│       └── _quotes.scss
└── demos/                      # Component demonstrations
    ├── index.html
    ├── typography.html
    ├── base-elements-demo.html
    ├── lists-tables.html
    ├── forms.html
    ├── components.html
    └── colors.html
```

## Customization

See [THEMING-GUIDE.md](THEMING-GUIDE.md) for detailed customization instructions.

### Quick Customization

Override CSS variables without recompiling:

```css
:root {
  --color-brand-primary: #0066CC;    /* Change primary color */
  --color-brand-secondary: #003366;  /* Change secondary color */
  --font-family-primary: "Your Font", sans-serif;
}
```

## Browser Support

- Chrome/Edge 111+ (for `color-mix()`)
- Firefox 113+
- Safari 16.4+

## Credits

- **Author:** Dan Dange ([@dandange8005](https://github.com/dandange8005))
- **Organization:** Cardiff University Digital Education
- **Based on:** Xerte Online Toolkits Bootstrap Sites

## License

For internal Cardiff University use. Part of the Xerte Online Toolkits ecosystem.
