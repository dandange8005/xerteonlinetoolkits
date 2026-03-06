# LTA-XOT Theme Restructuring Plan

## Overview

This document records the restructuring of the LTA-XOT theme from a nested SCSS folder structure to a flat, descriptive, single-level architecture similar to cardiffuni-v2.

## Completed: January 2026

---

## Previous Structure (37 files, 9 directories)

```
lta-xot/
├── lta-xot.scss
├── abstract/          (2 files)
│   ├── _cuColours.scss
│   └── _xibit.scss
├── base/              (9 files)
│   ├── _index.scss
│   ├── _customProperties.scss
│   ├── _overall-reset.scss
│   ├── _xot-reset.scss
│   ├── _base.scss
│   ├── _typography.scss
│   ├── _focused.scss
│   ├── _header.scss
│   └── _footer.scss
├── components/        (7 files)
│   ├── _index.scss
│   ├── _buttons.scss
│   ├── _forms.scss
│   ├── _alerts.scss
│   ├── _boxes.scss
│   ├── _cards.scss
│   └── _sidebar.scss
├── layouts/           (4 files)
│   ├── _index.scss
│   ├── _flex.scss
│   ├── _grid.scss
│   └── _contentMenu.scss
├── pages/             (12 files)
│   ├── _index.scss
│   ├── _textPage.scss
│   ├── _category.scss
│   ├── _graphicPage.scss
│   ├── _mediaPage.scss
│   ├── _navigatorPage.scss
│   ├── _tablePage.scss
│   ├── _hangmanPage.scss
│   ├── _documentation.scss
│   ├── _x_connectorMenu_page.scss
│   ├── _titlePage.scss (empty)
│   └── _quizPage.scss (empty)
├── utility/           (1 file)
│   └── _utilityClass.scss
├── vendors/           (3 files)
│   ├── _index.scss
│   ├── _jquery-ui.scss
│   └── _jquery-ui-theme.scss
└── assets/
```

---

## New Structure (8 files, 1 directory)

```
lta-xot/
├── lta-xot.scss              # Main entry point
├── scss/
│   ├── _tokens.scss          # Design tokens & CSS custom properties
│   ├── _base.scss            # Reset + typography + base elements
│   ├── _components.scss      # Buttons, forms, alerts, boxes, cards
│   ├── _layouts.scss         # Flex, grid, content layouts
│   ├── _xerte.scss           # XOT-specific: header, footer, page types
│   ├── _utilities.scss       # Helper classes
│   └── _vendors.scss         # jQuery UI overrides
├── assets/                   # Logos, images (unchanged)
├── CLAUDE.md
└── RESTRUCTURE-PLAN.md       # This file
```

---

## File Migration Map

### 1. `_tokens.scss`
Consolidated from:
- `base/_customProperties.scss` - CSS custom properties, color system
- `abstract/_cuColours.scss` - Cardiff University Sass variables (converted to CSS custom properties)

### 2. `_base.scss`
Consolidated from:
- `base/_overall-reset.scss` - CSS reset
- `base/_xot-reset.scss` - XOT-specific resets
- `base/_base.scss` - Base element styles
- `base/_typography.scss` - Typography rules
- `base/_focused.scss` - Focus states

### 3. `_components.scss`
Consolidated from:
- `components/_buttons.scss` - Button system
- `components/_forms.scss` - Form elements
- `components/_alerts.scss` - Alert variants
- `components/_boxes.scss` - Box containers
- `components/_cards.scss` - Card styles (mostly empty)
- `components/_sidebar.scss` - Sidebar styles (commented out)

### 4. `_layouts.scss`
Consolidated from:
- `layouts/_flex.scss` - Flexbox utilities
- `layouts/_grid.scss` - Grid utilities
- `layouts/_contentMenu.scss` - Content menu layout

### 5. `_xerte.scss`
Consolidated XOT-specific styles:
- `base/_header.scss` - Header block
- `base/_footer.scss` - Footer block
- `pages/_textPage.scss` - Text page styles
- `pages/_category.scss` - Category styles
- `pages/_graphicPage.scss` - Graphic page
- `pages/_mediaPage.scss` - Media page
- `pages/_navigatorPage.scss` - Navigator page
- `pages/_tablePage.scss` - Table page
- `pages/_hangmanPage.scss` - Hangman page
- `pages/_documentation.scss` - Documentation
- `abstract/_xibit.scss` - Xhibit footer/accessibility

**Note:** Empty page files (`_titlePage.scss`, `_quizPage.scss`, `_x_connectorMenu_page.scss`) were removed.

### 6. `_utilities.scss`
Direct migration from:
- `utility/_utilityClass.scss` - All utility classes

### 7. `_vendors.scss`
Consolidated from:
- `vendors/_jquery-ui.scss` - jQuery UI base
- `vendors/_jquery-ui-theme.scss` - jQuery UI theme

---

## External Dependencies (Unchanged)

- **Open Props** - CSS custom properties library (via CDN)
- **Animate.css** - Animation library (via CDN)
- **FontAwesome 5 Free** - Icons (loaded separately)

---

## Benefits of New Structure

1. **Simplified navigation** - All SCSS files in a single directory
2. **Descriptive naming** - File names clearly indicate their purpose
3. **Reduced imports** - Fewer index files and forward declarations
4. **Easier maintenance** - Related styles grouped logically
5. **Consistent with cardiffuni-v2** - Follows established patterns

---

## Verification Checklist

- [ ] SCSS compiles without errors
- [ ] Output CSS file size is similar to previous
- [ ] All styles render correctly in browser
- [ ] Theme works with Xerte Online Toolkits
