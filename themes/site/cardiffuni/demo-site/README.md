# Cardiff University Theme - Demo Site

Interactive demonstration and documentation for the Cardiff University theme v2.0.

## Overview

This single-page demo site showcases all features of the Cardiff University theme, including:

- **150+ CSS Custom Properties**: Colors, typography, spacing, borders, shadows, animations
- **10 Custom Components**: Box, Card, Callout, Quote, Button (8 variants), Details, Language Toggle, Lists, Links
- **60+ Utility Classes**: Flexbox system, spacing, typography, colors
- **Bootstrap Overrides**: Tabs, Pills, Accordion, Carousel
- **Base Elements**: Typography, Lists, Tables, Code blocks, Forms

## Features

### Interactive Elements

1. **Live Theme Customizer**
   - Adjust CSS variables in real-time
   - Export customizations as CSS
   - Reset to defaults
   - Auto-saves to localStorage

2. **Code Snippets with Copy**
   - One-click copy to clipboard
   - Visual feedback on copy
   - Syntax highlighting

3. **Responsive Preview**
   - Toggle between device sizes (Mobile, Tablet, Desktop)
   - Test responsive behavior in iframe

4. **Smooth Navigation**
   - Sticky header with auto-hide
   - Active section tracking
   - Smooth scroll to sections

## File Structure

```
demo-site/
├── index.html                      # Main demo page
├── assets/
│   ├── css/
│   │   ├── demo-site.css          # Demo site styling
│   │   └── prism.css              # Syntax highlighting
│   ├── js/
│   │   ├── demo-site.js           # Main orchestrator (ES6)
│   │   ├── modules/
│   │   │   ├── theme-customizer.js
│   │   │   ├── code-snippets.js
│   │   │   ├── responsive-preview.js
│   │   │   └── navigation.js
│   │   └── vendor/
│   │       ├── prism.js
│   │       └── clipboard.min.js
│   ├── images/
│   │   └── logo-cardiff.svg
│   └── data/
│       └── theme-data.json (planned)
└── README.md
```

## Usage

1. **View the demo**: Open `index.html` in a web browser
2. **Customize theme**: Click "Live Theme Customizer" button
3. **Copy code**: Click copy buttons on code examples
4. **Test responsive**: Click "Preview Modes" button

## Keyboard Shortcuts

- `Ctrl/Cmd + K`: Focus search
- `Escape`: Close customizer panel

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Development

The demo site uses ES6 modules. For local development:

1. Serve via local web server (required for ES6 modules)
2. Edit JavaScript modules in `assets/js/modules/`
3. Customize styles in `assets/css/demo-site.css`

## Future Enhancements

- Migration to VitePress/Docusaurus documentation framework
- Enhanced search functionality
- More interactive examples
- Video tutorials
- Figma design tokens export

## License

Part of the Cardiff University Theme project.

---

**Version**: 2.0
**Last Updated**: December 22, 2025
