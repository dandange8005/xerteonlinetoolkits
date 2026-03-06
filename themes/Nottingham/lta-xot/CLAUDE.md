# LTA XOT Theme

**Purpose:** Xerte Online Toolkits theme with Cardiff University branding. Features a flat, descriptive SCSS architecture.

## Structure

```
lta-xot/
├── lta-xot.scss              # Main entry point
├── scss/
│   ├── _tokens.scss          # Design tokens & CSS custom properties
│   ├── _base.scss            # Reset, typography, base elements
│   ├── _components.scss      # Buttons, forms, alerts, boxes
│   ├── _layouts.scss         # Flex, grid, content layouts
│   ├── _xerte.scss           # XOT-specific: header, footer, pages
│   ├── _utilities.scss       # Helper classes
│   └── _vendors.scss         # jQuery UI overrides
├── assets/                   # Logos, images
├── CLAUDE.md                 # This file
└── RESTRUCTURE-PLAN.md       # Migration documentation
```

## Key Reference Points

- **Color System:** Defined in `scss/_tokens.scss` using CSS custom properties
- **Design Tokens:** All in `scss/_tokens.scss` (colors, typography, spacing)
- **External Dependencies:** Open Props, Animate.css, FontAwesome 5 Free (via CDN)

## File Purposes

| File | Purpose |
|------|---------|
| `_tokens.scss` | CSS variables for colors, fonts, spacing |
| `_base.scss` | CSS reset, typography, focus states, accessibility filters |
| `_components.scss` | Button variants, forms, alerts, boxes |
| `_layouts.scss` | Flexbox, CSS Grid utilities, dialog styles |
| `_xerte.scss` | Header, footer, page-specific styles (text, category, media, etc.) |
| `_utilities.scss` | Helper classes (text, colors, spacing, visibility) |
| `_vendors.scss` | jQuery UI theme overrides |

## Notes

- Theme uses `@use` module syntax (not `@import`)
- Compiles with Live Sass Compile or any modern Sass compiler
- Restructured from nested 7-folder structure to flat single-folder architecture (Jan 2026)
