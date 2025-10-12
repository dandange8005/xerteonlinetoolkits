# Development Log - Cardiff University Theme

This document tracks major development milestones and architectural decisions for the Cardiff University Xerte theme.

---

## 2025-10-12: Modular Component System Implementation

### Overview
Implemented a comprehensive modular component system, migrating 10 custom components from a previous project into the Cardiff University theme with proper design token integration.

### Architecture Changes

#### Directory Structure Created
```
themes/site/cardiffuni/
├── cardiffuni.scss                    (updated - imports custom components)
├── scss/
│   ├── _custom-components.scss        (NEW - forwards all components)
│   └── components/                    (NEW - component modules)
│       ├── _boxes.scss               ✅ Box component
│       ├── _buttons.scss             ✅ Button styles
│       ├── _callout.scss             ✅ Alert/notice boxes
│       ├── _cards.scss               ✅ Content cards
│       ├── _details.scss             ✅ Disclosure widget
│       ├── _dosanddonts.scss         ✅ Best practice lists
│       ├── _language.scss            ✅ Language toggle
│       ├── _links.scss               ✅ Specialized links
│       ├── _projectInfo.scss         ✅ Metadata display
│       └── _quotes.scss              ✅ Styled blockquotes
└── docs/
    ├── Components.md                  (updated - full documentation)
    └── DevLog.md                      (NEW - this file)
```

#### Import Chain Updated
Modified `cardiffuni.scss` to include custom components:
```scss
@use "scss/_allvariables" as *;
@use "scss/enhancements";
@use "scss/base-elements";
@use "scss/bootstrap-components";
@use "scss/xerte-components";
@use "scss/custom-components";     // ← NEW
@use "scss/utilities";
@use "scss/layouts";
@use "scss/editorstyles";
```

### Components Migrated

| Component | File | Purpose | Key Classes |
|-----------|------|---------|-------------|
| **Boxes** | `_boxes.scss` | Simple containers with borders/shadows | `.box`, `.box-icon`, `.box__title` |
| **Buttons** | `_buttons.scss` | Custom button styles with variants | `.button`, `.button--outline`, `.button--small`, `.button--block`, `.btn-mini` |
| **Callout** | `_callout.scss` | Semantic alert boxes | `.callout`, `.callout.warning`, `.callout.success`, `.callout.danger`, `.callout.info` |
| **Cards** | `_cards.scss` | Content cards with images/metadata | `.card`, `.card--clickable`, `.card__image`, `.card__content`, `.card__link` |
| **Details** | `_details.scss` | HTML5 disclosure widget styling | `.details`, `.details__summary`, `.details__text` |
| **Do's & Don'ts** | `_dosanddonts.scss` | Best practice comparison lists | `.do-dont-list`, `.list--tick`, `.list--cross` |
| **Language** | `_language.scss` | Header language switcher | `#language-toggle`, `.language-toggle-text` |
| **Links** | `_links.scss` | Action, external, asset links | `.link-action`, `.link-external`, `.link-asset` |
| **Project Info** | `_projectInfo.scss` | Project metadata display | `#project-info` |
| **Quotes** | `_quotes.scss` | Enhanced blockquotes | `.quote`, `.quote.with-image`, `.quote-author` |

### Design Token Migration

All components were updated to use Cardiff University design tokens for consistency:

#### Color Tokens
- `--clr-accent` → `--color-brand-secondary`
- `--clr-link` → `--color-link-default`
- `--clr-body` → `--color-text-primary`
- `--clr-border` → `--border-color-default`
- `--cu-white` → `--cu-white` (unchanged)

#### Spacing Tokens
- `--size-1` through `--size-8` → `--spacing-xs` through `--spacing-3xl`
- `--size-fluid-1`, `--size-fluid-2` → `--spacing-sm`, `--spacing-md`
- `--gap` → `--spacing-md`

#### Typography Tokens
- `--fs-base` → `--font-size-base`
- `--fs-sm` → `--font-size-sm`
- `--fs-lg` → `--font-size-lg`
- `--font-weight-7` → `--font-weight-bold`

#### Border & Shadow Tokens
- `--radius-2` → `--radius-md`
- `--shadow-1`, `--shadow-2`, `--shadow-3` → `--shadow-sm`, `--shadow-md`, `--shadow-lg`

### Design Decisions

#### Why Modular Approach?
1. **Maintainability** - Each component in its own file for easier updates
2. **Scalability** - Can grow to 50+ components without file chaos
3. **Collaboration** - Reduces Git merge conflicts
4. **Selective Loading** - Ability to import only needed components
5. **Industry Standard** - Follows CSS architecture best practices (ITCSS, SMACSS)

#### Naming Convention
Adopted BEM (Block Element Modifier) methodology:
- **Block**: `.box`, `.card`, `.button`
- **Element**: `.box__title`, `.card__content`, `.link-asset__name`
- **Modifier**: `.box-icon`, `.button--outline`, `.card--clickable`

Note: Using single dash for modifiers (`.box-icon`) instead of strict BEM double dash (`.box--icon`) for consistency with existing codebase patterns.

#### Component Organization Categories
Components are categorized in `_custom-components.scss`:
1. **Content Components** - boxes, cards, callout, quotes
2. **Interactive Components** - buttons, details, language toggle
3. **List Components** - dos and donts lists
4. **Utility Components** - specialized links, project info

### Documentation Updates

#### Components.md
Completely restructured with:
- Component organization explanation
- Usage examples for each component
- Design token reference guide
- Instructions for adding new components
- Clear distinction between implemented and planned components

#### In-File Documentation
Each component SCSS file includes:
- Purpose statement
- Usage examples (HTML)
- List of variants and elements
- Feature descriptions where relevant

### Technical Implementation

#### @forward System
Used Sass `@forward` directive for clean module exports:
```scss
// _custom-components.scss
@forward "components/boxes";
@forward "components/cards";
// ... etc
```

This approach:
- Maintains module encapsulation
- Creates single import point
- Supports namespacing if needed in future
- Follows modern Sass module system (@use/@forward vs @import)

#### Accessibility Considerations
- Focus states on all interactive components
- Screen reader patterns (language toggle text hiding)
- Semantic HTML support (details/summary)
- ARIA-compatible markup examples

### Future Enhancements

#### Planned Components (Not Yet Implemented)
- Alert (semantic alerts)
- Avatars
- Badge
- Breadcrumbs
- Checkboxes (custom styled)
- Collapse
- Expand all Button
- Highlight
- Icons (icon system)
- Labels
- Modal
- Pagination
- Progress Bar
- Stepper
- Switch (toggle)
- Timeline
- Tooltip
- Typography utilities
- Video player

#### Potential Improvements
1. Add component variants as needed (size, color options)
2. Consider CSS custom property overrides for component customization
3. Add utility classes for component composition
4. Create component playground/demo page
5. Add unit tests for component styles (if applicable)

### Migration Notes

#### Breaking Changes
None - this is additive only. All existing styles remain unchanged.

#### Compatibility
- Works with existing Bootstrap components
- No conflicts with Xerte-specific components
- Compatible with current utility class system

#### Browser Support
Components use modern CSS features:
- CSS Custom Properties (variables)
- Flexbox
- CSS Grid (in some utilities)
- aspect-ratio (with fallbacks where needed)

### References
- Source components: https://github.com/dandange8005/CU-Xerte-Themes/tree/master/Bootstrap/components
- Cardiff Uni theme: `/themes/site/cardiffuni/`
- Design system: `scss/_allvariables.scss`

---

## Development Standards

### Adding New Components

When adding new components, follow these guidelines:

1. **Create Component File**
   - Location: `scss/components/_componentname.scss`
   - Naming: lowercase, hyphenated, underscore prefix

2. **Document the Component**
   ```scss
   /**
    * Component Name
    *
    * PURPOSE: Brief description
    *
    * USAGE:
    * <example HTML>
    *
    * VARIANTS:
    * - List of modifier classes
    */
   ```

3. **Use Design Tokens**
   - Always use CSS custom properties from `_allvariables.scss`
   - Never hardcode colors, spacing, or typography values
   - Reference: See "Design Token Reference" in Components.md

4. **Follow BEM Naming**
   - Block: `.component-name`
   - Element: `.component-name__element`
   - Modifier: `.component-name--modifier` or `.component-name-modifier`

5. **Register Component**
   - Add `@forward` statement to `_custom-components.scss`
   - Document in `Components.md` with usage examples

6. **Test Responsiveness**
   - Ensure mobile-first approach
   - Test on various screen sizes
   - Consider touch targets (min 44px)

### Git Commit Messages
Use semantic commit format:
- `feat: add [component name] component`
- `fix: correct [issue] in [component]`
- `docs: update [documentation file]`
- `refactor: restructure [component] styles`
- `style: format [file] with prettier`

---

## Changelog

### [Unreleased]

### [2025-10-12] - Component System Implementation
#### Added
- Modular component directory structure (`scss/components/`)
- 10 custom components with Cardiff Uni design tokens
- `_custom-components.scss` index file
- Comprehensive component documentation in `Components.md`
- This development log

#### Changed
- Updated `cardiffuni.scss` to import custom components
- Migrated design tokens from old variable system to Cardiff Uni tokens

#### Documentation
- Created `DevLog.md` with architecture decisions
- Updated `Components.md` with full component catalog

---

*This log tracks significant architectural changes and design decisions. For component usage documentation, see Components.md.*
