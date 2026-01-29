# Fork Changelog - Cardiff University / DigEd Customizations

> **Maintainer:** Dan Dange ([@dandange8005](https://github.com/dandange8005))
> **Fork of:** [thexerteproject/xerteonlinetoolkits](https://github.com/thexerteproject/xerteonlinetoolkits)
> **Purpose:** Custom themes and templates for Cardiff University Digital Education
> **Note:** This fork is for internal use only and will not submit pull requests to the upstream repository.

This changelog tracks all customizations made to this fork that differ from the upstream Xerte Online Toolkits repository.

---

## Overview

This fork maintains custom themes for Cardiff University's Digital Education team while staying in sync with upstream Xerte releases.

### Custom Assets (Not in Upstream)

| Asset | Location | Description |
|-------|----------|-------------|
| Cardiff Uni Theme | `themes/site/cardiffuni/` | Full theme with SCSS architecture, design tokens, and custom components |
| Cardiff Uni Theme v2 | `themes/site/cardiffuni-v2/` | Refactored theme with design token architecture and Bootstrap 2 integration |
| DigEd Bootstrap Theme | `themes/site/diged/` | Modern Bootstrap-based theme with modular SCSS |
| CKEditor Styles | `editor/js/vendor/ckeditor/styles.js` | Custom editor styles for Cardiff branding |
| Project Docs | `CLAUDE.md` | AI assistant context for development |

---

## Changelog

### [Unreleased]

#### Notes
- Featherlight lightbox applies `overflow:hidden` to html, which causes scroll reset - needs investigation

---

### [2026-01-29] - Demo Pages Enhancement

#### Changed
- **Demo Pages Refactor** (`themes/site/cardiffuni-v2/demos/`)
  - Updated color palette demo to use semantic design tokens
  - Expanded components demo with alerts, badges, progress bars, and more UI elements
  - Refactored demo styles to use new CSS custom properties
  - Updated navigation links and titles across all demo pages

#### Added
- **FontAwesome 6.6.0 Integration**
  - Comprehensive icon system for demo pages
  - Icon examples in components showcase

#### Files Modified
- 11 demo HTML files updated with new color system and icons
- `demo-styles.css` refactored for CSS custom properties

---

### [2026-01-28] - Navigation Color System Decoupling

#### Added
- **Independent Navigation Colors** (`scss/_allvariables.scss`)
  - New CSS variables: `--color-nav-accent` and `--color-nav-accent-dark`
  - Separates navigation styling from brand colors for greater customization flexibility

#### Changed
- Updated Bootstrap component styles to use new navigation color tokens
- Regenerated compiled CSS with new color system

#### Configuration
- Updated `.gitignore` with additional exclusions
- Refined VS Code settings for Live Sass Compiler
- Updated autoprefixer configuration to exclude Internet Explorer
  - Settings: `["defaults", "not IE > 0"]`
  - Removes unnecessary vendor prefixes (`-webkit-box-sizing`, `-ms-flexbox`, etc.)

---

### [2026-01-26] - Utility Classes Refactor & Flexbox Demo

#### Changed
- **Utilities SCSS Reorganization** (`scss/_utilities.scss`)
  - Refactored with modern SCSS loops for spacing, flexbox, and utilities
  - Reduced from 802 lines to more maintainable structure
  - Moved legacy utilities to separate `_legacy.scss` file (104 lines)

#### Added
- **Flexbox Demo Page** (`demos/flexbox.html`)
  - Comprehensive flexbox utility demonstrations (847 lines)
  - Interactive examples of flex layouts and utilities
  - Added to navigation across all demo pages

- **Legacy Utilities Module** (`scss/_legacy.scss`)
  - Backward-compatible utilities from System 2
  - Legacy flexbox system (`.flexContainer`, `.flexItem`)
  - Responsive column classes (`.c10` through `.c80`)
  - Old image helpers and color naming classes
  - All mapped to modern design tokens

#### Fixed
- **Button Component Styles** (`scss/components/_buttons.scss`)
  - Prevented Bootstrap link hover color overrides
  - Improved button state management

#### Files Modified
- 18 files changed, 3,447 insertions, 1,513 deletions
- Created backup: `_utilities.scss.bak`

---

### [2026-01-25] - Theme Designer Tool & Theme Variants

#### Added
- **Theme Designer Tool** (`themes/site/theme-designer/`)
  - Interactive web-based theme customization tool
  - Real-time color palette editor with live preview
  - Color utility functions for shade generation
  - Preset theme configurations
  - Files:
    - `index.html` - Main designer interface (218 lines)
    - `css/designer.css` - Designer UI styles (534 lines)
    - `js/designer.js` - Core designer logic (426 lines)
    - `js/color-utils.js` - Color manipulation utilities (109 lines)
    - `js/presets.js` - Theme presets (56 lines)
    - `preview/components.html` - Component preview page
    - `README.md` - Tool documentation

- **Medr Theme** (`themes/site/cardiffuni-v2/themes/medr-theme.css`)
  - Complete theme variant for Medr branding (391 lines)
  - Custom color palette and typography

- **ASDA Theme** (`themes/site/cardiffuni-v2/themes/asda-theme.css`)
  - Theme variant for ASDA project (184 lines)
  - Alternative color scheme and styling

- **Medr Design System** (`themes/site/Medr/Medr Design System.json`)
  - JSON design token specification for Medr theme

#### Documentation
- **Cardiff Uni v2 README** (`themes/site/cardiffuni-v2/README.md`)
  - Comprehensive theme overview (118 lines)
  - Quick start guide and feature documentation

- **Theming Guide** (`themes/site/cardiffuni-v2/THEMING-GUIDE.md`)
  - Detailed customization instructions (417 lines)
  - Token architecture explanation
  - Component customization examples
  - Theme variant creation guide

- **Standardization Guide Relocation**
  - Moved `XERTE_THEME_STANDARDIZATION_GUIDE.md` from `cardiffuni/` to `themes/site/` root
  - Updated with Cardiff Uni v2 theme documentation (300 lines)
  - Added 205 new lines, removed 95 outdated lines

#### Files Added
- 10 new files, 2,502 total lines added

---

### [2026-01-25] - CSS Variable Naming Standardization

#### Changed
- **CSS Variable Prefix Refactor**
  - Renamed all `--cu-*` prefixes to `--color-*` for generic reusability
  - Updated animation variable names for consistency
  - Applied across all components and SCSS modules

#### Files Modified
- 20 files updated across theme components
- `_base-elements.scss`, `_bootstrap-components.scss`, `_editorstyles.scss`
- `_layouts.scss`, `_utilities.scss`, `_xerte-components.scss`
- All 10 component SCSS files updated

#### Impact
- 1,014 insertions, 938 deletions
- Improved theme portability and reusability
- Cleaner, more semantic variable naming

---

### [2026-01-24] - Cardiff Uni v2 Design System Refactor

#### Changed
- **Design Token Architecture** (`themes/site/cardiffuni-v2/scss/`)
  - Restructured `_tokens.scss` as primitive-only tokens (SCSS variables, compile-time)
  - Updated `_allvariables.scss` to use hybrid approach:
    - Imports tokens via `@use "tokens" as t;`
    - Generates CSS custom properties using SCSS interpolation `#{t.$token-*}`
    - Single semantic layer for easy runtime theming
  - Removed `--cu-` prefix for generic, reusable token names
  - Updated `cardiff-design.json` colors to match official brand tokens

- **Button System Consolidation**
  - Centralized all button tokens in `_allvariables.scss`
  - Updated `_buttons.scss` to reference centralized `--btn-*` tokens
  - Added ghost button variant (`.button-ghost`)
  - Added size variants (`.button-sm`, `.button-lg`)
  - Uses `color-mix()` for hover/active/disabled states

- **Link Colors**
  - Changed to traditional blue (`#0645AD`) instead of brand primary
  - Uses `color-mix()` for hover and active states

- **Typography & Spacing**
  - Updated font size scale to match design JSON
  - Added heading style tokens (h1-h6)
  - Numeric spacing scale (1, 2, 4, 8...) with semantic aliases

#### Files Modified
- `themes/site/cardiffuni-v2/scss/_tokens.scss` - Primitive tokens only
- `themes/site/cardiffuni-v2/scss/_allvariables.scss` - Semantic tokens with CSS custom properties
- `themes/site/cardiffuni-v2/scss/components/_buttons.scss` - References centralized tokens
- `themes/site/cardiffuni-v2/cardiff-design.json` - Updated color values

#### Backup Files Created
- `_tokens.scss.bak` - Original tokens file
- `_allvariables.scss.bak` - Original variables file

---

### [2026-01-23] - Bootstrap 2 Demo Pages

#### Added
- **Demo Pages Suite** (`themes/site/cardiffuni-v2/demos/`)
  - `index.html` - Demo homepage with navigation
  - `typography.html` - Typography showcase
  - `lists-tables.html` - Lists and tables examples
  - `images-media.html` - Images and media components
  - `forms.html` - Form elements and inputs
  - `components.html` - UI component library
  - `code-utilities.html` - Code blocks and utility classes
  - `colors.html` - Color palette documentation
  - `patterns.html` - Design patterns
  - `base-elements-demo.html` - Base HTML elements showcase

- **Local Bootstrap 2 Assets** (`demos/assets/`)
  - Self-contained Bootstrap 2 CSS/JS for demo pages
  - `demo-styles.css` - Demo-specific styling

- **Additional SCSS Files**
  - `_bootstrap-components.scss` - Bootstrap 2 component integrations
  - `_editorstyles.scss` - Editor-specific styles
  - `_enhancements.scss` - Visual enhancements
  - `_layouts.scss` - Layout utilities
  - `_utilities.scss` - Utility classes
  - `_webkitCustoms.scss` - WebKit-specific fixes
  - `_xerte-components.scss` - Xerte-specific components
  - `_custom-components.scss` - Custom component imports

---

### [2026-01-22] - Fork Sync & AI Features Setup

#### Changed
- Synced fork with upstream `develop` branch (994 new commits)
- Major upstream additions include:
  - AI integration (OpenAI, Anthropic, Mistral support)
  - Security fixes (RCE vulnerability #1505, SSRF bypass #1504)
  - Interactive Video improvements (#1513, #1510)
  - Graph library for analytics
  - Quiz/MCQ button display options
  - Accessibility improvements (#922 Bullets page)

#### Added
- `vendor_config.php` - AI vendor API key configuration
  - Configured OpenAI API keys for:
    - AI content generation (GPT)
    - Transcription (Whisper)
    - Embeddings/RAG (OpenAI encoding)
    - Image generation (DALL-E 2, DALL-E 3, GPT Image 1)

#### Database
- Ran `upgrade.php` to create AI-related tables:
  - `management_helper` - Stores AI vendor settings and preferences
  - `ai_request_logs` - Tracks AI API usage and costs

#### Configuration
- Enabled AI vendors in Management → AI Settings admin panel

---

### [2024-11-23] - Fork Sync & DigEd Theme

#### Changed
- Rebased fork onto upstream `develop` branch
- Resolved `.gitignore` conflict (merged upstream's `openai_config.php` ignores with local `.DS_Store`)

#### Added
- `themes/site/diged/` - New DigEd Bootstrap theme
- OKLCH color documentation for improved color scales

---

### [2024-10-12] - Cardiff University Theme v2.0

#### Added
- Modular component system with 10 custom components:
  - Boxes, Buttons, Callout, Cards, Details
  - Do's & Don'ts lists, Language toggle, Links, Project Info, Quotes
- Design token system (`scss/_tokens.scss`)
- CSS custom properties for runtime customization
- Component showcase page
- Flexbox utility system
- CKEditor custom styles

#### Changed
- Migrated from monolithic CSS to modular SCSS architecture
- Updated all components to use Cardiff design tokens
- Restructured theme documentation

#### Documentation
- `CARDIFF_THEME_GUIDE.md` - Complete theming guide
- `Components.md` - Component catalog and usage
- `DevLog.md` - Development decisions log
- `THEMING-GUIDE.md` - Customization instructions

---

### [2024-09] - Initial Cardiff Theme

#### Added
- `themes/site/cardiffuni/` - Initial Cardiff University theme
- Custom SCSS variables for Cardiff branding
- Base editor styles integration

---

## Syncing with Upstream

To sync this fork with the latest upstream changes:

```bash
# Fetch upstream
git fetch upstream

# Rebase onto upstream/develop
git rebase upstream/develop

# Resolve any conflicts, then force push
git push --force-with-lease origin develop
```

## File Inventory

### Files Modified from Upstream
- `.gitignore` - Added `.DS_Store`
- `editor/js/vendor/ckeditor/styles.js` - Custom editor styles

### Files Added (Not in Upstream)
```
CLAUDE.md
FORK_CHANGELOG.md (this file)
.vscode/settings.json
vendor_config.php                                  (AI API keys - do not commit to public repos)
themes/site/cardiffuni/                            (entire directory)
themes/site/cardiffuni-v2/                         (entire directory)
  ├── themes/medr-theme.css                        (Medr theme variant)
  ├── themes/asda-theme.css                        (ASDA theme variant)
  ├── README.md                                    (Theme overview)
  ├── THEMING-GUIDE.md                             (Customization guide)
  └── demos/flexbox.html                           (Flexbox utilities demo)
themes/site/diged/                                 (entire directory)
themes/site/theme-designer/                        (Interactive theme designer tool)
themes/site/Medr/                                  (Medr design system)
themes/site/XERTE_THEME_STANDARDIZATION_GUIDE.md   (Relocated from cardiffuni/)
```

---

## Contact

For questions about these customizations:
- GitHub: [@dandange8005](https://github.com/dandange8005)
- Organisation: Cardiff University Digital Education
