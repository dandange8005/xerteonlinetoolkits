# Cardiff University Theme - Demo Site Project Structure

**Plan Date**: December 22, 2025
**Status**: Planned for Future Implementation
**Version**: 1.0

---

## Overview

Create a comprehensive single-page demo site to showcase all features of the Cardiff University theme, with interactive features (live theme customizer, code snippets with copy, responsive preview) and future-proof structure for migration to a professional documentation framework.

## Project Requirements

- **Site Type**: Single-page HTML with smooth scroll navigation
- **Interactive Features**:
  - Live theme customizer (adjust CSS variables in real-time)
  - Code snippets with copy-to-clipboard
  - Responsive preview toggles (mobile/tablet/desktop)
- **Existing Demos**: Keep in `/demos` folder as reference
- **Future Goal**: Migrate to documentation framework (VitePress/Docusaurus)

## Theme Features to Showcase

- **150+ CSS Custom Properties**: Colors, typography, spacing, borders, shadows, animations
- **10 Custom Components**: Box, Card, Callout, Quote, Button (8 variants), Details, Language Toggle, Lists, Links
- **60+ Utility Classes**: Flexbox system, spacing, typography, colors
- **Bootstrap Overrides**: Tabs, Pills, Accordion, Carousel
- **Base Elements**: Typography, Lists, Tables, Code blocks, Forms

---

## Directory Structure

```
themes/site/cardiffuni/
├── demo-site/                          # NEW: Main demo site directory
│   ├── index.html                      # Single-page demo site
│   ├── assets/
│   │   ├── css/
│   │   │   ├── demo-site.css          # Demo site-specific styling
│   │   │   └── prism.css              # Syntax highlighting
│   │   ├── js/
│   │   │   ├── demo-site.js           # Main orchestrator (ES6 module)
│   │   │   ├── modules/
│   │   │   │   ├── theme-customizer.js    # Live CSS variable editor
│   │   │   │   ├── code-snippets.js       # Copy-to-clipboard
│   │   │   │   ├── responsive-preview.js  # Viewport toggle
│   │   │   │   └── navigation.js          # Smooth scroll, active tracking
│   │   │   └── vendor/
│   │   │       ├── prism.js               # Code syntax highlighting
│   │   │       └── clipboard.min.js       # Copy functionality
│   │   ├── images/
│   │   │   ├── logo-cardiff.svg           # Cardiff University logo
│   │   │   └── demo-*.jpg                 # Demo content images
│   │   └── data/
│   │       └── theme-data.json            # Structured theme data
│   └── README.md                       # Demo site documentation
├── demos/                              # EXISTING: Keep as reference
│   └── [existing demo files]
├── cardiffuni.css                      # Main theme CSS (used by demo)
├── scss/                               # Theme source files
└── docs/                               # Theme documentation
```

---

## HTML Structure (index.html)

### Main Sections

1. **Header/Hero**
   - Cardiff University branding
   - Title: "Cardiff University Theme - Interactive Demo & Documentation v2.0"
   - Quick action buttons (Toggle Customizer, Preview Modes)

2. **Sticky Navigation**
   - Links to: Overview, Design Tokens, Components, Utilities, Base Elements, Bootstrap, Customization
   - Optional search bar
   - Auto-highlights active section on scroll

3. **Main Content Area**
   - Side Panel: Theme Customizer (collapsible, fixed right)
   - Content Sections:
     - **Overview**: Stats (150+ variables, 10 components, 60+ utilities), key features
     - **Design Tokens**: Colors (brand, grayscale, accents), Typography, Spacing, Borders, Shadows, Animations
     - **Components**: 10 custom components with live previews, code snippets, CSS variable docs
     - **Utilities**: Flexbox, Spacing, Typography, Colors (60+ utilities)
     - **Base Elements**: Typography, Lists, Tables, Code, Forms
     - **Bootstrap**: Tabs, Pills, Accordion, Carousel
     - **Customization Guide**: Methods for overriding CSS variables

4. **Footer**
   - Resources links (Theme Guide, Reference Demos, Brand Guidelines)
   - Quick navigation links

---

## JavaScript Architecture (ES6 Modules)

### Main Orchestrator: `demo-site.js`
- Coordinates all modules
- Handles global event listeners
- Manages localStorage preferences
- Keyboard shortcuts (Ctrl/Cmd + K for search)

### Module 1: `theme-customizer.js`
**Features:**
- Color pickers for brand colors (synced with hex inputs)
- Sliders for typography (font size, line height)
- Spacing scale controls
- Real-time CSS variable updates via `document.documentElement.style.setProperty()`
- Export CSS button (copies to clipboard + downloads file)
- Reset button (clears all customizations)
- Auto-save to localStorage

**Key Methods:**
- `updateCSSVariable(varName, value)` - Updates CSS custom property
- `exportCSS()` - Generates CSS file with current customizations
- `resetTheme()` - Removes all custom properties
- `toggle()` - Shows/hides customizer panel

### Module 2: `code-snippets.js`
**Features:**
- Copy buttons for all code examples
- Visual feedback (button text changes to "Copied!" for 2s)
- Supports component demos, token/utility snippets
- Fallback for older browsers

**Key Methods:**
- `copyCode(button)` - Finds associated code and copies
- `copyToClipboard(text)` - Uses modern Clipboard API with fallback
- `showCopyFeedback(button)` - Visual confirmation

### Module 3: `responsive-preview.js`
**Features:**
- Device viewport buttons (Mobile 375px, Tablet 768px, Desktop 1440px, Responsive 100%)
- Clones demo content into iframe
- Syncs theme CSS with iframe
- Smooth width transitions

**Key Methods:**
- `show()` - Creates iframe with demo content
- `setPreviewWidth(width)` - Adjusts iframe width
- `toggle()` - Shows/hides preview frame

### Module 4: `navigation.js`
**Features:**
- Smooth scroll to sections
- Active section tracking with Intersection Observer
- Sticky nav on scroll
- Auto-hide nav on scroll down (shows on scroll up)

**Key Methods:**
- `setupSmoothScroll()` - Handles anchor link clicks
- `setupSectionTracking()` - Intersection Observer for active states
- `updateActiveSection(sectionId)` - Updates nav link highlighting

---

## CSS Organization (demo-site.css)

### Scope: Demo Site UI Only
**NOT included**: Theme styles (already in cardiffuni.css)

**Included**:
- Demo header/hero styling
- Sticky navigation (with sticky, hidden states)
- Theme customizer side panel (slide-in animation)
- Component demo cards (header, preview area, code blocks, props)
- Token/utility grids (responsive grid layouts)
- Responsive preview frame
- Footer styling
- Toast notifications
- Copy button states
- Responsive breakpoints

**Design Tokens (Demo-specific)**:
```css
:root {
    --demo-nav-height: 60px;
    --demo-sidebar-width: 320px;
    --demo-spacing: 2rem;
    --demo-transition: 0.3s ease;
}
```

---

## Component Demo Structure

Each component follows this pattern:

```html
<article class="component-demo" id="component-{name}">
    <!-- Header -->
    <div class="component-demo__header">
        <h4>{Component Name}</h4>
        <span class="component-badge">{Category}</span>
    </div>

    <!-- Live Preview -->
    <div class="component-demo__preview">
        <!-- Actual component markup -->
    </div>

    <!-- Code Snippet -->
    <div class="component-demo__code">
        <button class="code-copy-btn">📋 Copy</button>
        <pre><code class="language-html">...</code></pre>
    </div>

    <!-- CSS Variables Reference -->
    <div class="component-demo__props">
        <h5>CSS Variables</h5>
        <ul>
            <li><code>--{var-name}</code> - Description</li>
        </ul>
    </div>
</article>
```

---

## Accessibility Features

1. **Keyboard Navigation**
   - All interactive elements keyboard-accessible
   - Ctrl/Cmd + K for search focus
   - Tab order follows visual hierarchy
   - Visible focus indicators

2. **ARIA Labels**
   - `role="banner"` for header
   - `role="navigation"` for nav
   - `aria-label` for icon-only buttons
   - `aria-expanded` for collapsible panels
   - `aria-hidden` for decorative elements

3. **Screen Reader Support**
   - Semantic HTML (header, nav, main, section, article)
   - Descriptive link text
   - Alt text for images
   - Status announcements for copy actions

4. **Color Contrast**
   - WCAG 2.1 AA compliance
   - Focus indicators: 3:1 contrast ratio
   - Text: minimum 4.5:1 contrast

5. **Responsive Design**
   - Touch-friendly targets (min 44x44px)
   - Viewport meta tag
   - Mobile-first approach

---

## Performance Optimizations

1. **Code Splitting**: ES6 modules loaded on-demand
2. **Lazy Loading**: Prism.js deferred, images below fold lazy-loaded
3. **Caching**: localStorage for customizations
4. **CSS**: Single main theme file (83KB), lightweight demo-site.css
5. **Images**: SVG for logos/icons, optimized JPGs for demos

---

## Future Migration Path

### To VitePress/Docusaurus:
1. Each `<section>` → separate `.md` or `.mdx` file
2. JS modules → Vue/React components
3. Anchor links → routing
4. Sticky nav → sidebar navigation
5. Search → framework search integration

### File Mapping Example (VitePress):
```
Current                  →  Future
index.html              →  docs/index.md
#design-tokens          →  docs/design-tokens.md
#components             →  docs/components/
assets/js/modules/      →  .vitepress/theme/
assets/css/             →  .vitepress/theme/styles/
```

---

## Implementation Plan

### Phase 1: Foundation (Build Directory & HTML)
1. Create `/demo-site` directory structure
2. Build `index.html` with all section scaffolding
3. Create `demo-site.css` with layout styles
4. Add Cardiff University logo and placeholder images

**Files to Create**:
- `demo-site/index.html`
- `demo-site/assets/css/demo-site.css`
- `demo-site/assets/images/logo-cardiff.svg`
- `demo-site/README.md`

### Phase 2: Interactive Features (JavaScript Modules)
1. Create `demo-site.js` main orchestrator
2. Build `navigation.js` module (smooth scroll, active tracking)
3. Build `code-snippets.js` module (copy functionality)
4. Build `theme-customizer.js` module (CSS variable editor)
5. Build `responsive-preview.js` module (viewport toggle)
6. Add Prism.js vendor files

**Files to Create**:
- `demo-site/assets/js/demo-site.js`
- `demo-site/assets/js/modules/navigation.js`
- `demo-site/assets/js/modules/code-snippets.js`
- `demo-site/assets/js/modules/theme-customizer.js`
- `demo-site/assets/js/modules/responsive-preview.js`
- `demo-site/assets/js/vendor/prism.js`
- `demo-site/assets/js/vendor/clipboard.min.js`
- `demo-site/assets/css/prism.css`

### Phase 3: Content Population (Fill Sections)
1. **Design Tokens Section**:
   - All colors (brand, grayscale, accents) with swatches
   - Typography scale with visual previews
   - Spacing scale with visual bars
   - Borders, shadows, animations

2. **Components Section**:
   - All 10 components with live previews
   - Code snippets for each variant
   - CSS variable documentation

3. **Utilities Section**:
   - Flexbox utilities (60+ classes)
   - Spacing utilities
   - Typography utilities
   - Color utilities

4. **Base Elements Section**:
   - Typography (h1-h6, p, blockquote, etc.)
   - Lists (ul, ol, dl)
   - Tables
   - Code blocks
   - Forms

5. **Bootstrap Section**:
   - Tabs, Pills, Accordion, Carousel examples

6. **Customization Section**:
   - Methods for overriding CSS variables
   - Complete variable reference table

### Phase 4: Polish & Testing
1. Accessibility audit (keyboard nav, ARIA, contrast)
2. Mobile responsive testing
3. Browser compatibility testing (Chrome, Firefox, Safari, Edge)
4. Performance optimization
5. Write README documentation

---

## Critical Files

1. **index.html** - Main HTML structure with all sections, navigation, interactive elements
2. **demo-site.js** - Main orchestrator coordinating all modules
3. **theme-customizer.js** - Live CSS variable editor with export functionality
4. **demo-site.css** - Demo site-specific styling (layouts, component demos, UI)
5. **_allvariables.scss** - Reference for documenting all CSS custom properties

---

## Success Criteria

✅ Single-page site with all Cardiff theme features showcased
✅ Live theme customizer with real-time CSS variable editing
✅ Copy-to-clipboard for all code examples
✅ Responsive preview with mobile/tablet/desktop toggles
✅ Existing demos preserved in `/demos` folder
✅ Fully accessible (WCAG 2.1 AA)
✅ Mobile responsive
✅ Future-proof structure for documentation framework migration

---

## Estimated Timeline

**Phase 1**: 1-2 days
**Phase 2**: 2-3 days
**Phase 3**: 3-4 days
**Phase 4**: 1-2 days

**Total**: ~7-11 days of development

---

## Notes for Future Implementation

- This plan was created after comprehensive exploration of the Cardiff University theme
- All existing demo files (7 files) will be preserved in the `/demos` folder
- The design leverages ES6 modules for maintainability and future framework migration
- Structure is intentionally simple (single-page) for initial release, with clear migration path to documentation framework
- All interactive features use modern web APIs with fallbacks for browser compatibility
