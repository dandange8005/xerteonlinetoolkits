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

## Relationship to the original `cardiffuni` theme

This theme is a separate copy of `themes/site/cardiffuni`, not an update to it. Both themes are installed and enabled, and projects are using each of them.

**Timeline:** `cardiffuni` was built between October 2025 and January 2026. `cardiffuni-v2` was branched from it on 23 January 2026 and developed until April 2026. Since the branch, `cardiffuni` has had no styling changes.

**Why a copy rather than an update:** v2 renames classes and CSS variables that pages built on v1 already use, so upgrading in place would have changed the look of published projects. Copying kept v1 stable for existing content while v2 was reworked.

### What changed in v2

| | `cardiffuni` (v1) | `cardiffuni-v2` |
|---|---|---|
| CSS variables | `--cu-*` (e.g. `--cu-blue`, `--cu-gray-40`) | `--color-*` (e.g. `--color-brand-primary`, `--color-accent-blue`) |
| Colour utilities | Per-brand-colour classes (`.bg-cu-blue`, `.text-cu-stone`, `.bg-gray-50`) | Role-based classes (`.bg-brand`, `.bg-light`, `.bg-dark`, `.bg-white`) |
| Forms | Not styled without classes | Zero-config styling for inputs, selects and textareas |
| Bootstrap coverage | Tabs, accordions and core components | Adds alerts, badges, labels, breadcrumbs and progress bars |
| Components | Single `_custom-components.scss` | Split into `scss/components/` (buttons, boxes, callouts, cards, details, dos-and-donts, language toggle, links, project info, quotes) |
| Accessibility | Basic | Visible focus states, 44px touch targets, underlined links |
| Re-branding | Recompile the SCSS | Override CSS variables at runtime — see `themes/medr-theme.css` |
| Legacy support | n/a | `_legacy.scss` keeps the older `.flexContainer` / `.flexItem` layout classes working |

### Which one to use

- **New projects:** use `cardiffuni-v2`.
- **Existing v1 projects:** leave them on `cardiffuni` unless you can check the pages afterwards. Switching a project to v2 will drop any `--cu-*` variables, `.bg-cu-*` / `.text-cu-*` colour classes, and `.flex-initial`, `.flex-wrap-reverse` or `.image-*` classes the pages rely on, because v2 does not define them.

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
│   ├── _webkitCustoms.scss     # WebKit-specific fixes
│   ├── _legacy.scss            # Older .flexContainer / .flexItem support
│   └── components/             # Individual components
│       ├── _boxes.scss
│       ├── _buttons.scss
│       ├── _callout.scss
│       ├── _cards.scss
│       ├── _details.scss
│       ├── _dosanddonts.scss
│       ├── _language.scss      # Language toggle
│       ├── _links.scss
│       ├── _projectInfo.scss
│       └── _quotes.scss
├── themes/
│   └── medr-theme.css          # Medr re-brand, loaded after the theme CSS
└── demos/                      # Component demonstrations
    ├── index.html
    ├── typography.html
    ├── base-elements-demo.html
    ├── lists-tables.html
    ├── forms.html
    ├── components.html
    ├── colors.html
    ├── code-utilities.html
    ├── flexbox.html
    ├── images-media.html
    └── patterns.html
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
