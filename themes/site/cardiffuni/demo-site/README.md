# Cardiff University Theme - Demo Site

Interactive demonstration and documentation for the Cardiff University theme v2.0.

## Overview

This multi-page demo site showcases all features of the Cardiff University theme across 9 organized pages:

- **150+ CSS Custom Properties**: Colors, typography, spacing, borders, shadows, animations
- **10 Custom Components**: Box, Card, Callout, Quote, Button (8 variants), Details, Language Toggle, Lists, Links
- **60+ Utility Classes**: Flexbox system, spacing, typography, colors
- **Bootstrap Overrides**: Tabs, Pills, Accordion, Carousel
- **Base Elements**: Typography, Lists, Tables, Code blocks, Forms
- **Layout Patterns**: Flexbox and CSS Grid layout examples

## Pages

1. **Home** (`index.html`) - Welcome page with feature cards and quick start guide
2. **Design Tokens** (`design-tokens.html`) - Colors, typography, spacing, borders, shadows, animations, z-index, aspect ratios
3. **Base Elements** (`base-elements.html`) - Styled HTML elements
4. **Components** (`components.html`) - 10 custom components with live previews
5. **Utilities** (`utilities.html`) - 60+ utility classes reference
6. **Bootstrap** (`bootstrap.html`) - Cardiff-branded Bootstrap overrides
7. **Flex Layouts** (`flex-layouts.html`) - Flexbox patterns and utilities
8. **Grid Layouts** (`grid-layouts.html`) - CSS Grid patterns and utilities
9. **Customization** (`customization.html`) - Guide to customizing the theme

## Features

### Interactive Elements

1. **Live Theme Customizer**
   - Available on all pages via sticky navigation
   - Adjust CSS variables in real-time
   - Export customizations as CSS
   - Reset to defaults
   - Auto-saves to localStorage (persists across pages)

2. **Code Snippets with Copy**
   - One-click copy to clipboard
   - Visual feedback on copy
   - Syntax highlighting with Prism.js

3. **Multi-Page Navigation**
   - Shared navigation across all pages
   - Active page highlighting
   - Sticky header with auto-hide on scroll down

## File Structure

```
demo-site/
├── index.html                      # Home page
├── design-tokens.html              # Design Tokens page
├── base-elements.html              # Base Elements page
├── components.html                 # Components page
├── utilities.html                  # Utilities page
├── bootstrap.html                  # Bootstrap page
├── flex-layouts.html               # Flex Layouts page
├── grid-layouts.html               # Grid Layouts page
├── customization.html              # Customization page
├── assets/
│   ├── css/
│   │   ├── demo-site.css          # Demo site styling
│   │   └── prism.css              # Syntax highlighting
│   ├── js/
│   │   ├── demo-site.js           # Main orchestrator (ES6)
│   │   ├── modules/
│   │   │   ├── page-layout.js     # Shared header/nav/footer injection
│   │   │   ├── theme-customizer.js # Live CSS variable editor
│   │   │   ├── code-snippets.js   # Copy-to-clipboard functionality
│   │   │   └── navigation.js      # Multi-page navigation & active state
│   │   └── vendor/
│   │       ├── prism.js
│   │       └── clipboard.min.js
│   ├── images/
│   │   └── logo-cardiff.svg
│   └── data/
│       └── theme-data.json (planned)
└── README.md
```

## Architecture

### JavaScript Module System (ES6)

**PageLayout Module** (`page-layout.js`):
- Injects shared header, navigation, footer, and customizer on all pages
- Single source of truth for shared layout components
- Template-based HTML injection

**Navigation Module** (`navigation.js`):
- Multi-page navigation with URL-based active state
- Sticky navigation with auto-hide on scroll
- Active page highlighting

**ThemeCustomizer Module** (`theme-customizer.js`):
- Live CSS custom property editing
- localStorage persistence (works globally across all pages)
- Export and reset functionality

**CodeSnippets Module** (`code-snippets.js`):
- Copy-to-clipboard for all code examples
- Visual feedback on copy actions

## Usage

### Viewing the Demo

1. **Local Development**: Serve via local web server (required for ES6 modules)
   ```bash
   # Example with Python
   cd demo-site
   python3 -m http.server 8000
   # Visit http://localhost:8000
   ```

2. **XAMPP/Apache**: Access via your web server
   ```
   http://localhost/xertetoolkits/themes/site/cardiffuni/demo-site/
   ```

### Navigation

- Click any page link in the navigation to explore different sections
- Use the Live Theme Customizer button (top right) to customize colors, typography, and spacing
- Theme customizations persist across all pages via localStorage

### Customization

1. **Live Customizer**: Click "Live Theme Customizer" button and adjust controls
2. **Export CSS**: Click "Export CSS" to download your customizations
3. **Reset**: Click "Reset" to restore default theme

## Keyboard Shortcuts

- `Ctrl/Cmd + K`: Focus search input
- `Escape`: Close customizer panel

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

Requires ES6 module support and CSS custom properties.

## Development

### Adding New Pages

1. Create new HTML file in `demo-site/` directory
2. Include standard page structure:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Page Title - Cardiff University Theme</title>
       <link rel="stylesheet" href="../cardiffuni.css">
       <link rel="stylesheet" href="assets/css/prism.css">
       <link rel="stylesheet" href="assets/css/demo-site.css">
   </head>
   <body>
       <main class="demo-main">
           <div class="demo-content">
               <!-- Your content here -->
           </div>
       </main>
       <script src="assets/js/vendor/prism.js" defer></script>
       <script src="assets/js/vendor/clipboard.min.js" defer></script>
       <script src="assets/js/demo-site.js" type="module"></script>
   </body>
   </html>
   ```
3. Add page link to navigation in `page-layout.js`

### Modifying Shared Layout

Edit `assets/js/modules/page-layout.js` to update:
- Header content
- Navigation links
- Footer content
- Theme customizer controls

Changes will automatically apply to all pages.

### Customizing Styles

- **Theme styles**: Edit SCSS files in `../scss/` and recompile
- **Demo site styles**: Edit `assets/css/demo-site.css`
- **Page-specific styles**: Add inline styles or create new CSS files

## Technical Details

### How Shared Layout Works

1. Each page loads `demo-site.js` as an ES6 module
2. `demo-site.js` initializes `PageLayout` module first
3. `PageLayout` injects shared header, navigation, footer, and customizer into the page
4. Other modules (Navigation, ThemeCustomizer, CodeSnippets) initialize
5. Navigation module detects current page and highlights active link

### Theme Customization Persistence

- Customizations saved to `localStorage` under key `cardiff-theme-customizations`
- On page load, saved theme automatically applied via `document.documentElement.style.setProperty()`
- Works globally across all pages without additional configuration

## Future Enhancements

- Migration to VitePress/Docusaurus documentation framework
- Enhanced search functionality across all pages
- More interactive layout examples
- Video tutorials for each section
- Figma design tokens export
- Component playground with live editing

## Contributing

When adding new content or pages:
1. Maintain consistent HTML structure
2. Use existing CSS classes and design tokens
3. Add copy buttons to all code examples
4. Test theme customizer on new pages
5. Verify keyboard navigation works
6. Check mobile responsiveness

## License

Part of the Cardiff University Theme project.

---

**Version**: 2.0
**Architecture**: Multi-Page
**Last Updated**: December 22, 2025
