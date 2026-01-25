# Xerte Theme Designer

A visual theme customization tool for Xerte Online Toolkits.

## Features

- 🎨 **Visual Controls** — Color pickers, sliders, and dropdowns
- 👁️ **Live Preview** — See changes in real-time
- ✅ **WCAG Checking** — Contrast ratio validation
- 📦 **Presets** — Cardiff University, Medr (Welsh Gov), Dark Mode
- 📋 **Export CSS** — Copy or download generated CSS

## Usage

1. Open `index.html` in your browser
2. Adjust colors, typography, and borders using the sidebar controls
3. Preview changes in the right panel
4. Click **Export CSS** to get your custom theme
5. Load the exported CSS after `cardiffuni-v2.css`

## File Structure

```
theme-designer/
├── index.html              # Main interface
├── css/
│   └── designer.css        # UI styles
├── js/
│   ├── designer.js         # Application logic
│   ├── color-utils.js      # Color/contrast utilities
│   └── presets.js          # Theme presets
└── preview/
    └── components.html     # Preview samples
```

## Presets

| Preset | Primary Color | Style |
|--------|--------------|-------|
| Cardiff University | #E4251B | Modern, rounded |
| Medr (Welsh Gov) | #00703C | GOV.UK style, sharp |
| Dark Mode | #6366f1 | Dark background |

## Browser Support

Requires modern browser with `color-mix()` support:
- Chrome/Edge 111+
- Firefox 113+
- Safari 16.4+
