# Improving Your Color Scale with OKLCH and Relative Color Syntax

Looking at your Cardiff University theme variables, I can definitely help improve the color scale using OKLCH and relative color syntax. This will give you more consistent and perceptually uniform color variations.

## Updated CSS Variables with OKLCH

Here's how you can enhance your color system:

```css
:root {
    // =========================================================================
    // CARDIFF UNIVERSITY BRAND COLORS (OKLCH Version)
    // =========================================================================

    // Primary Colors in OKLCH format
    --cu-primary-red-oklch: oklch(0.55 0.22 29);      /* #e4251b converted to OKLCH */
    --cu-white-oklch: oklch(1 0 0);                    /* Pure white */
    --cu-black-oklch: oklch(0.06 0 0);                 /* #121212 converted to OKLCH */

    // Accent Colors in OKLCH format
    --cu-forest-green-oklch: oklch(0.48 0.18 157);     /* #07873E converted to OKLCH */
    --cu-cadet-oklch: oklch(0.68 0.12 177);            /* #5EB99B converted to OKLCH */
    --cu-stone-oklch: oklch(0.81 0.05 65);             /* #C9C2BA converted to OKLCH */
    --cu-light-blue-oklch: oklch(0.6 0.18 245);        /* #1E90FF converted to OKLCH */
    --cu-royal-blue-oklch: oklch(0.5 0.22 263);       /* #4A42FF converted to OKLCH */
    --cu-midnight-blue-oklch: oklch(0.3 0.12 251);     /* #273573 converted to OKLCH */
    --cu-midnight-purple-oklch: oklch(0.2 0.08 299);   /* #26192C converted to OKLCH */
    --cu-orange-oklch: oklch(0.65 0.17 50);            /* #E9761E converted to OKLCH */
    --cu-yellow-oklch: oklch(0.85 0.18 95);            /* #FFB300 converted to OKLCH */
    --cu-yellow-green-oklch: oklch(0.75 0.15 135);     /* #85C041 converted to OKLCH */
    --cu-indigo-oklch: oklch(0.3 0.2 300);             /* #570185 converted to OKLCH */
    --cu-dark-violet-oklch: oklch(0.55 0.25 320);      /* #D401C5 converted to OKLCH */

    // =========================================================================
    // OKLCH COLOR SCALES (Using Relative Color Syntax)
    // =========================================================================

    // Lightness steps for consistent scales
    --lightness-step-50: 0.98;
    --lightness-step-100: 0.94;
    --lightness-step-200: 0.88;
    --lightness-step-300: 0.78;
    --lightness-step-400: 0.68;
    --lightness-step-500: 0.58;
    --lightness-step-600: 0.48;
    --lightness-step-700: 0.38;
    --lightness-step-800: 0.28;
    --lightness-step-900: 0.18;
    --lightness-step-950: 0.08;

    // Chroma adjustments for different contexts
    --chroma-boost: 1.2;  /* For vibrant states */
    --chroma-normal: 1;   /* Default */
    --chroma-muted: 0.6;  /* For subtle backgrounds */
    --chroma-faded: 0.3;  /* For very subtle accents */

    // Primary Brand Scale (OKLCH with relative color syntax)
    --color-brand-primary-50: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-50) c h);
    --color-brand-primary-100: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-100) c h);
    --color-brand-primary-200: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-200) c h);
    --color-brand-primary-300: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-300) c h);
    --color-brand-primary-400: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-400) c h);
    --color-brand-primary-500: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-500) c h);
    --color-brand-primary-600: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-600) c h);
    --color-brand-primary-700: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-700) c h);
    --color-brand-primary-800: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-800) c h);
    --color-brand-primary-900: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-900) c h);
    --color-brand-primary-950: oklch(from var(--cu-primary-red-oklch) var(--lightness-step-950) c h);

    // Secondary Brand Scale (using black)
    --color-brand-secondary-50: oklch(from var(--cu-black-oklch) var(--lightness-step-50) c h);
    --color-brand-secondary-100: oklch(from var(--cu-black-oklch) var(--lightness-step-100) c h);
    --color-brand-secondary-200: oklch(from var(--cu-black-oklch) var(--lightness-step-200) c h);
    --color-brand-secondary-300: oklch(from var(--cu-black-oklch) var(--lightness-step-300) c h);
    --color-brand-secondary-400: oklch(from var(--cu-black-oklch) var(--lightness-step-400) c h);
    --color-brand-secondary-500: oklch(from var(--cu-black-oklch) var(--lightness-step-500) c h);
    --color-brand-secondary-600: oklch(from var(--cu-black-oklch) var(--lightness-step-600) c h);
    --color-brand-secondary-700: oklch(from var(--cu-black-oklch) var(--lightness-step-700) c h);
    --color-brand-secondary-800: oklch(from var(--cu-black-oklch) var(--lightness-step-800) c h);
    --color-brand-secondary-900: oklch(from var(--cu-black-oklch) var(--lightness-step-900) c h);
    --color-brand-secondary-950: oklch(from var(--cu-black-oklch) var(--lightness-step-950) c h);

    // Accent Color Scales (OKLCH)
    --color-accent-green-50: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-50) c h);
    --color-accent-green-100: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-100) c h);
    --color-accent-green-200: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-200) c h);
    --color-accent-green-300: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-300) c h);
    --color-accent-green-400: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-400) c h);
    --color-accent-green-500: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-500) c h);
    --color-accent-green-600: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-600) c h);
    --color-accent-green-700: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-700) c h);
    --color-accent-green-800: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-800) c h);
    --color-accent-green-900: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-900) c h);
    --color-accent-green-950: oklch(from var(--cu-forest-green-oklch) var(--lightness-step-950) c h);

    --color-accent-blue-50: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-50) c h);
    --color-accent-blue-100: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-100) c h);
    --color-accent-blue-200: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-200) c h);
    --color-accent-blue-300: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-300) c h);
    --color-accent-blue-400: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-400) c h);
    --color-accent-blue-500: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-500) c h);
    --color-accent-blue-600: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-600) c h);
    --color-accent-blue-700: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-700) c h);
    --color-accent-blue-800: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-800) c h);
    --color-accent-blue-900: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-900) c h);
    --color-accent-blue-950: oklch(from var(--cu-light-blue-oklch) var(--lightness-step-950) c h);

    --color-accent-orange-50: oklch(from var(--cu-orange-oklch) var(--lightness-step-50) c h);
    --color-accent-orange-100: oklch(from var(--cu-orange-oklch) var(--lightness-step-100) c h);
    --color-accent-orange-200: oklch(from var(--cu-orange-oklch) var(--lightness-step-200) c h);
    --color-accent-orange-300: oklch(from var(--cu-orange-oklch) var(--lightness-step-300) c h);
    --color-accent-orange-400: oklch(from var(--cu-orange-oklch) var(--lightness-step-400) c h);
    --color-accent-orange-500: oklch(from var(--cu-orange-oklch) var(--lightness-step-500) c h);
    --color-accent-orange-600: oklch(from var(--cu-orange-oklch) var(--lightness-step-600) c h);
    --color-accent-orange-700: oklch(from var(--cu-orange-oklch) var(--lightness-step-700) c h);
    --color-accent-orange-800: oklch(from var(--cu-orange-oklch) var(--lightness-step-800) c h);
    --color-accent-orange-900: oklch(from var(--cu-orange-oklch) var(--lightness-step-900) c h);
    --color-accent-orange-950: oklch(from var(--cu-orange-oklch) var(--lightness-step-950) c h);

    // Chroma variations for different contexts
    --color-brand-primary-muted: oklch(from var(--cu-primary-red-oklch) l calc(c * var(--chroma-muted)) h);
    --color-brand-primary-faded: oklch(from var(--cu-primary-red-oklch) l calc(c * var(--chroma-faded)) h);
    --color-brand-primary-vibrant: oklch(from var(--cu-primary-red-oklch) l calc(c * var(--chroma-boost)) h);

    // Grayscale in OKLCH (more perceptually uniform)
    --cu-gray-10-oklch: oklch(0.98 0 0);
    --cu-gray-20-oklch: oklch(0.95 0 0);
    --cu-gray-30-oklch: oklch(0.88 0 0);
    --cu-gray-40-oklch: oklch(0.78 0 0);
    --cu-gray-50-oklch: oklch(0.68 0 0);
    --cu-gray-60-oklch: oklch(0.58 0 0);
    --cu-gray-70-oklch: oklch(0.48 0 0);
    --cu-gray-80-oklch: oklch(0.38 0 0);
    --cu-gray-90-oklch: oklch(0.28 0 0);

    // =========================================================================
    // SEMANTIC DESIGN TOKENS (Updated to use OKLCH)
    // =========================================================================

    // Text Colors
    --color-text-primary: var(--cu-black-oklch);
    --color-text-inverse: var(--cu-white-oklch);
    --color-text-hint: var(--cu-primary-red-oklch);
    --color-text-alert: var(--cu-primary-red-oklch);
    --color-text-on-light: var(--cu-black-oklch);
    --color-text-on-dark: var(--cu-white-oklch);
    --color-text-on-brand: var(--cu-white-oklch);

    // Brand Colors
    --color-brand-primary: var(--cu-primary-red-oklch);
    --color-brand-secondary: var(--cu-black-oklch);

    // Link Colors (converted to OKLCH)
    --color-link-default: oklch(0.55 0.15 250);      /* #045bc6 converted to OKLCH */
    --color-link-hover: oklch(0.45 0.15 250);       /* #033a8a converted to OKLCH */
    --color-link-visited: oklch(0.35 0.15 310);     /* #551A8B converted to OKLCH */

    // Accent Colors
    --color-accent-green: var(--cu-forest-green-oklch);
    --color-accent-blue: var(--cu-light-blue-oklch);
    --color-accent-orange: var(--cu-orange-oklch);

    // Background Colors
    --color-bg-body: oklch(0.98 0.01 210);           /* #f9fafb converted to OKLCH */
    --color-bg-page: var(--cu-white-oklch);
    --color-bg-panel: var(--cu-gray-70-oklch);

    // =========================================================================
    // BACKWARD COMPATIBILITY
    // Keep original hex values for browsers without OKLCH support
    // =========================================================================

    @supports not (color: oklch(0 0 0)) {
        /* Fallback to original hex values */
        --cu-primary-red-oklch: var(--cu-primary-red);
        --cu-white-oklch: var(--cu-white);
        --cu-black-oklch: var(--cu-black);
        
        /* Other color fallbacks... */
        
        /* Use color-mix for scales */
        --color-brand-primary-50: color-mix(in srgb, var(--cu-primary-red) 10%, white);
        --color-brand-primary-100: color-mix(in srgb, var(--cu-primary-red) 20%, white);
        --color-brand-primary-200: color-mix(in srgb, var(--cu-primary-red) 30%, white);
        --color-brand-primary-300: color-mix(in srgb, var(--cu-primary-red) 40%, white);
        --color-brand-primary-400: color-mix(in srgb, var(--cu-primary-red) 60%, white);
        --color-brand-primary-500: var(--cu-primary-red);
        --color-brand-primary-600: color-mix(in srgb, var(--cu-primary-red) 80%, black);
        --color-brand-primary-700: color-mix(in srgb, var(--cu-primary-red) 90%, black);
        --color-brand-primary-800: color-mix(in srgb, var(--cu-primary-red) 95%, black);
        --color-brand-primary-900: color-mix(in srgb, var(--cu-primary-red) 98%, black);
        --color-brand-primary-950: color-mix(in srgb, var(--cu-primary-red) 99%, black);
    }
}
```

## Benefits of This Approach

1. **Perceptually Uniform**: OKLCH provides more consistent lightness perception across different hues, making your color scales more balanced.

2. **Simplified Maintenance**: With relative color syntax, you only need to define the base color, and all variations are generated automatically.

3. **Flexible Chroma Control**: You can easily adjust the saturation of colors for different contexts (muted, faded, vibrant).

4. **Better Grayscale**: The OKLCH grayscale is more perceptually uniform than simple hex values.

5. **Backward Compatibility**: The `@supports` query ensures your site still works in browsers without OKLCH support.

## Implementation Example

Here's how you might use these new variables in your components:

```css
.card {
    background-color: var(--color-bg-page);
    border: 1px solid var(--cu-gray-30-oklch);
    box-shadow: var(--shadow-md);
}

.card-header {
    background-color: var(--color-brand-primary-100);
    color: var(--color-brand-primary-700);
    padding: var(--spacing-md);
}

.card-body {
    padding: var(--spacing-md);
    color: var(--color-text-primary);
}

.button-primary {
    background-color: var(--color-brand-primary-500);
    color: var(--color-text-on-brand);
}

.button-primary:hover {
    background-color: var(--color-brand-primary-600);
}

.button-primary:active {
    background-color: var(--color-brand-primary-700);
}

.button-secondary {
    background-color: var(--color-brand-primary-100);
    color: var(--color-brand-primary-700);
}

.alert-success {
    background-color: var(--color-accent-green-100);
    color: var(--color-accent-green-700);
    border-left: 4px solid var(--color-accent-green-500);
}
```

This approach gives you a much more systematic and maintainable color system while preserving your existing design tokens and naming conventions.