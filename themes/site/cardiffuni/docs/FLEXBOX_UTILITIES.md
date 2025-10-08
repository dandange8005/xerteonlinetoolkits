# Flexbox Utility System

This enhanced flexbox system combines the best of both utility-first and component-based approaches, providing maximum flexibility with minimal markup.

## Overview

The system includes:
- **Modern utility classes** for granular control (like Tailwind CSS)
- **Responsive width utilities** with mobile-first approach
- **Legacy compatibility** for existing `.flexContainer` markup
- **Design token integration** using Cardiff University spacing scale

## Basic Usage

### Simple Two-Column Layout

**Flex-Basis Approach (Recommended - Simplest!):**
```html
<div class="flex flex-wrap gap-lg">
    <div class="flex-300">Column 1</div>
    <div class="flex-300">Column 2</div>
</div>
```
✅ Auto-responsive, gap-friendly, minimal markup

**Percentage Approach (When you need exact widths):**
```html
<div class="flex flex-wrap gap-md">
    <div class="w-full w-md-50">Column 1</div>
    <div class="w-full w-md-50">Column 2</div>
</div>
```
⚠️ Use with `gap-md` only (calculations optimized for 16px gap)

**Legacy Approach (Still Supported):**
```html
<div class="flexContainer">
    <div class="flexItem c50">Column 1</div>
    <div class="flexItem c50">Column 2</div>
</div>
```

## Flex Container Classes

### Display & Wrap
- `.flex` - Creates flex container with default gap
- `.flex-wrap` - Allow items to wrap
- `.flex-nowrap` - Prevent wrapping
- `.flex-wrap-reverse` - Wrap in reverse

### Direction
- `.flex-row` - Horizontal layout (default)
- `.flex-row-reverse` - Horizontal, reversed
- `.flex-col` - Vertical layout
- `.flex-col-reverse` - Vertical, reversed

### Justify Content (Horizontal Alignment)
- `.justify-start` - Align to start
- `.justify-end` - Align to end
- `.justify-center` - Center items
- `.justify-between` - Space between items
- `.justify-around` - Space around items
- `.justify-evenly` - Even spacing

### Align Items (Vertical Alignment)
- `.items-start` - Align to top
- `.items-end` - Align to bottom
- `.items-center` - Center vertically
- `.items-baseline` - Align to baseline
- `.items-stretch` - Stretch to fill

### Gap (Spacing Between Items)
- `.gap-0` - No gap
- `.gap-xs` - 4px
- `.gap-sm` - 8px
- `.gap-md` - 16px (default)
- `.gap-lg` - 24px
- `.gap-xl` - 32px
- `.gap-2xl` - 48px

## Flex Item Classes

### Flex Behavior
- `.flex-1` - Grow and shrink equally, ignore initial size
- `.flex-auto` - Grow and shrink, respect initial size
- `.flex-initial` - Only shrink, respect initial size
- `.flex-none` - No grow or shrink

### Flex Basis (Minimum Width)
- `.flex-100` - Min 100px, can grow
- `.flex-200` - Min 200px, can grow
- `.flex-300` - Min 300px, can grow
- `.flex-400` - Min 400px, can grow
- `.flex-500` - Min 500px, can grow
- `.flex-600` - Min 600px, can grow

### Align Self (Override Container Alignment)
- `.self-auto` - Use container alignment
- `.self-start` - Align to top
- `.self-end` - Align to bottom
- `.self-center` - Center vertically
- `.self-stretch` - Stretch to fill
- `.self-baseline` - Align to baseline

## Width Utilities (Mobile-First)

### Fixed Widths (All Breakpoints)
- `.w-full` - 100%
- `.w-auto` - Auto width
- `.w-10` - 10%
- `.w-20` - 20%
- `.w-25` - 25%
- `.w-30` - 30%
- `.w-33` - 33.333%
- `.w-40` - 40%
- `.w-50` - 50%
- `.w-60` - 60%
- `.w-70` - 70%
- `.w-80` - 80%

### Responsive Widths (806px and up)
Add `-md` suffix for desktop-only widths:
- `.w-md-10` through `.w-md-80`
- `.w-md-full`
- `.w-md-auto`

## Common Layout Patterns

### Three Equal Columns (Flex-Basis - Recommended)
```html
<div class="flex flex-wrap gap-lg">
    <div class="flex-300">Column 1</div>
    <div class="flex-300">Column 2</div>
    <div class="flex-300">Column 3</div>
</div>
```
✅ Automatically wraps and grows to fill space

### Three Equal Columns (Percentage - Exact widths)
```html
<div class="flex flex-wrap gap-lg">
    <div class="w-full w-md-33">Column 1</div>
    <div class="w-full w-md-33">Column 2</div>
    <div class="w-full w-md-33">Column 3</div>
</div>
```

### Sidebar + Main Content (Flex-Basis - Recommended)
```html
<div class="flex flex-wrap gap-lg">
    <aside class="flex-200">Sidebar</aside>
    <main class="flex-400">Main Content</main>
</div>
```
✅ Sidebar min 200px, main min 400px, both grow to fill space

### Sidebar + Main Content (Percentage - Exact 30/70)
```html
<div class="flex flex-wrap gap-lg">
    <aside class="w-full w-md-30">Sidebar</aside>
    <main class="w-full w-md-70">Main Content</main>
</div>
```

### Centered Card with Max Width
```html
<div class="flex justify-center">
    <div class="flex-600">Card content</div>
</div>
```

### Vertical Centering
```html
<div class="flex items-center justify-center" style="min-height: 400px;">
    <div>Centered content</div>
</div>
```

### Auto-Flowing Cards (Flex-Basis - Best for Grids!)
```html
<div class="flex flex-wrap gap-lg">
    <div class="flex-300">Card 1</div>
    <div class="flex-300">Card 2</div>
    <div class="flex-300">Card 3</div>
    <div class="flex-300">Card 4</div>
</div>
```
✅ Cards automatically flow and wrap based on container width

### Product Grid (Different Sizes)
```html
<div class="flex flex-wrap gap-md">
    <div class="flex-200">Small Card</div>
    <div class="flex-200">Small Card</div>
    <div class="flex-400">Featured Card (Larger)</div>
    <div class="flex-200">Small Card</div>
</div>
```

### Dashboard Layout
```html
<div class="flex flex-wrap gap-lg">
    <div class="flex-300">Widget 1</div>
    <div class="flex-300">Widget 2</div>
    <div class="flex-600">Large Widget</div>
</div>
```

### Header with Space Between
```html
<header class="flex items-center justify-between">
    <h1>Site Title</h1>
    <nav>Navigation</nav>
</header>
```

## Migration Guide

### From Legacy System 2

**Before:**
```html
<div class="flexContainer">
    <div class="flexItem c50">Column 1</div>
    <div class="flexItem c50">Column 2</div>
</div>
```

**After (Recommended):**
```html
<div class="flex flex-wrap gap-md">
    <div class="w-full w-md-50">Column 1</div>
    <div class="w-full w-md-50">Column 2</div>
</div>
```

**After (Minimal Change):**
```html
<!-- No change needed! Legacy classes still work -->
<div class="flexContainer">
    <div class="flexItem c50">Column 1</div>
    <div class="flexItem c50">Column 2</div>
</div>
```

## Advantages of New System

### ✅ Pros
1. **More Control** - Granular utilities for any layout scenario
2. **Mobile-First** - Explicit responsive behavior
3. **Design Token Integration** - Uses Cardiff spacing scale
4. **Modern** - Aligns with industry standards (Tailwind, Bootstrap 5)
5. **Composable** - Mix and match utilities as needed
6. **No Box-Sizing Issues** - Uses modern CSS gap instead of padding
7. **Backward Compatible** - Legacy classes still work

### 📋 When to Use What

**Use `.flex` system when:**
- Building custom layouts
- Need precise control
- Creating reusable components
- Working on new features

**Use `.flexContainer` system when:**
- Maintaining existing code
- Quick prototyping
- Simple column layouts
- Minimizing markup changes

## Tips & Best Practices

### 🎯 Recommended Approach

1. **Use flex-basis for most layouts** (`.flex-300`, `.flex-400`, etc.)
   - Simpler markup
   - Gap-friendly (no calc needed)
   - Automatically responsive
   - Great for cards, grids, and adaptive layouts

2. **Use percentages only when you need exact widths** (`.w-md-50`, `.w-md-33`)
   - Precise control (exact 50/50, 30/70 splits)
   - Traditional page layouts
   - When design requires exact percentages

3. **Use gap over padding** - Cleaner spacing with `.gap-*` utilities

4. **Combine utilities** - Mix flex, width, and spacing utilities

5. **Keep it semantic** - Use HTML5 elements (`<main>`, `<aside>`, `<article>`)

6. **Test responsively** - Always check layouts at 806px breakpoint

### 💡 Quick Decision Guide

**Choose `.flex-300` style when:**
- Building card grids
- Creating adaptive dashboards
- Want simplicity
- Don't need exact percentages
- **Using any gap size** (gap-sm, gap-lg, gap-xl, etc.)

**Choose `.w-md-50` style when:**
- Need exact percentage splits
- Building traditional layouts (sidebars)
- Design specifies exact widths
- **Only using gap-md (16px)** - other gap sizes may cause wrapping

## Browser Support

All modern browsers support these utilities:
- Chrome/Edge 84+
- Firefox 63+
- Safari 14.1+

The `gap` property is used instead of padding for cleaner layouts and better browser support.

## Examples in Context

### Image Gallery
```html
<div class="flex flex-wrap gap-lg">
    <figure class="w-full w-md-25">
        <img src="..." class="w-full">
        <figcaption>Image 1</figcaption>
    </figure>
    <figure class="w-full w-md-25">
        <img src="..." class="w-full">
        <figcaption>Image 2</figcaption>
    </figure>
    <figure class="w-full w-md-25">
        <img src="..." class="w-full">
        <figcaption>Image 3</figcaption>
    </figure>
    <figure class="w-full w-md-25">
        <img src="..." class="w-full">
        <figcaption>Image 4</figcaption>
    </figure>
</div>
```

### Feature List with Icons
```html
<div class="flex flex-col gap-md">
    <div class="flex gap-sm items-center">
        <span class="flex-none">✓</span>
        <p class="flex-1">Feature description</p>
    </div>
    <div class="flex gap-sm items-center">
        <span class="flex-none">✓</span>
        <p class="flex-1">Another feature</p>
    </div>
</div>
```

### Responsive Navigation
```html
<nav class="flex flex-col flex-md-row gap-md justify-between items-center">
    <a href="/" class="flex-none">Logo</a>
    <ul class="flex gap-md">
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
</nav>
```

## Reference

For spacing values, see `_allvariables.scss`:
- `--spacing-xs`: 4px
- `--spacing-sm`: 8px
- `--spacing-md`: 16px
- `--spacing-lg`: 24px
- `--spacing-xl`: 32px
- `--spacing-2xl`: 48px
- `--spacing-3xl`: 64px
- `--spacing-4xl`: 80px

Breakpoint: 806px (matches existing Cardiff theme)
