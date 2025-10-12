# Cardiff University Theme - Component Library

This document catalogs all available components in the Cardiff University Xerte theme.

## Component Organization

Components are organized into modular SCSS files in `scss/components/`:
- Each component has its own file for maintainability
- Components use Cardiff University design tokens from `_allvariables.scss`
- All components are imported via `_custom-components.scss`

---

## Implemented Custom Components

### ✅ Content Components

#### **Box** (`_boxes.scss`)
Simple container component with padding, borders, and shadows.
- `.box` - Base container style
- `.box-icon` - Flexbox layout with icon
- `.box__title` - Optional title element

**Usage:**
```html
<div class="box">Content here</div>
<div class="box box-icon">
  <i class="fas fa-user"></i>
  <div>Content with icon</div>
</div>
```

#### **Cards** (`_cards.scss`)
Content cards with images, headings, and descriptions.
- `.card` - Base card container
- `.card--clickable` - Interactive card with hover effects
- `.card__image`, `.card__content`, `.card__heading`, `.card__link`

**Usage:**
```html
<div class="card card--clickable">
  <div class="card__image"><img src="..." alt="..."></div>
  <div class="card__content">
    <h3><a href="#" class="card__link">Card Title</a></h3>
    <p class="card__description">Description text</p>
  </div>
</div>
```

#### **Callout** (`_callout.scss`)
Alert/notice boxes with semantic color variants.
- `.callout` - Base callout (neutral)
- `.callout.warning` - Yellow warning (⚠️)
- `.callout.success` - Green success (✅)
- `.callout.danger` - Red error (⛔)
- `.callout.info` - Blue information (ℹ️)

**Usage:**
```html
<div class="callout warning">
  <h4>Warning</h4>
  <p>This is a warning message.</p>
</div>
```

#### **Quotes** (`_quotes.scss`)
Styled blockquotes with optional author images.
- `.quote` - Base quote style
- `.quote.with-image` - Quote with author image
- `.quote-image`, `.quote-author`

---

### ✅ Interactive Components

#### **Buttons** (`_buttons.scss`)
Custom button styles for links and button elements.
- `.button` - Base button style
- `.button--outline` - Outlined button
- `.button--small` - Smaller size
- `.button--block` - Full width
- `.btn-mini` - Circular mini button (back to top)

**Usage:**
```html
<a href="#" class="button">Click me</a>
<button class="button button--outline">Outline button</button>
```

#### **Details** (`_details.scss`)
Native HTML `<details>` disclosure widget styling.
- `.details` - Container element
- `.details__summary` - Clickable toggle
- `.details__text` - Expanded content

**Usage:**
```html
<details class="details">
  <summary class="details__summary">Click to expand</summary>
  <div class="details__text">
    <p>Hidden content here</p>
  </div>
</details>
```

#### **Language Toggle** (`_language.scss`)
Language switcher positioned in header.
- `#language-toggle` - Positioned toggle button
- Responsive: hides text on small screens

---

### ✅ List Components

#### **Do's and Don'ts** (`_dosanddonts.scss`)
Visual lists showing best practices vs. things to avoid.
- `.do-dont-list` - Container box
- `.do-dont-list__label` - Colored label (Do/Don't)
- `.list--tick` - Checkmark list
- `.list--cross` - Cross/X list

**Usage:**
```html
<div class="do-dont-list">
  <h3 class="do-dont-list__label">Do</h3>
  <ul class="list--tick">
    <li>Use semantic HTML</li>
  </ul>
</div>
```

---

### ✅ Utility Components

#### **Links** (`_links.scss`)
Specialized link styles with icons.
- `.link-action` - Link with arrow icon
- `.link-external` - Link with external icon
- `.link-asset` - Styled file download link

**Usage:**
```html
<a href="#" class="link-action">Take action</a>
<a href="https://..." class="link-external">External link</a>
<a href="file.pdf" class="link-asset">
  <i class="fas fa-file-pdf link-asset__icon"></i>
  <div>
    <div class="link-asset__name">Document.pdf</div>
    <div class="link-asset__label">PDF, 2.5 MB</div>
  </div>
</a>
```

#### **Project Info** (`_projectInfo.scss`)
Project metadata display.
- `#project-info` - Flexbox metadata container

---

## Bootstrap Components (Implemented)

### ✅ Navigation Components
- **Tabs** (`_bootstrap-components.scss`) - `.nav-tabs`
- **Pills** (`_bootstrap-components.scss`) - `.nav-pills`
- **Accordion** (`_bootstrap-components.scss`) - `.accordion-group`
- **Carousel** (`_bootstrap-components.scss`) - Image slider with controls

### ✅ Other Bootstrap Components
- **Panel** - `.panel`
- **Well** - `.well`
- **Tables** - `.table-striped`
- **Lead Text** - `.lead`

---

## Planned Components (Not Yet Implemented)

- [ ] Alert (semantic alerts)
- [ ] Avatars
- [ ] Badge
- [ ] Breadcrumbs
- [ ] Checkboxes (custom styled)
- [ ] Collapse
- [ ] Expand all Button
- [ ] Highlight
- [ ] Icons (icon system)
- [ ] Labels
- [ ] Modal
- [ ] Pagination
- [ ] Progress Bar
- [ ] Stepper
- [ ] Switch (toggle)
- [ ] Timeline
- [ ] Tooltip
- [ ] Typography utilities
- [ ] Video player

---

## Design Token Reference

All components use Cardiff University design tokens:

**Colors:**
- `--color-brand-primary` / `--color-brand-secondary`
- `--color-text-primary` / `--color-link-default`
- `--cu-white`, `--cu-gray-*` (10-90)

**Spacing:**
- `--spacing-xs`, `--spacing-sm`, `--spacing-md`, `--spacing-lg`, `--spacing-xl`, `--spacing-2xl`, `--spacing-3xl`

**Typography:**
- `--font-size-xs` through `--font-size-3xl`
- `--font-weight-light`, `--font-weight-regular`, `--font-weight-medium`, `--font-weight-bold`

**Borders & Shadows:**
- `--radius-sm`, `--radius-md`, `--radius-lg`
- `--shadow-sm`, `--shadow-md`, `--shadow-lg`

---

## Adding New Components

To add a new component:

1. Create `scss/components/_componentname.scss`
2. Add component documentation header with usage examples
3. Use Cardiff Uni design tokens (not hardcoded values)
4. Add `@forward "components/componentname";` to `_custom-components.scss`
5. Document the component in this file