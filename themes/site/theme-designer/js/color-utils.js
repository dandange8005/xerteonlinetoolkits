/**
 * Color Utility Functions
 * Handles color manipulation and WCAG contrast checking
 */

const ColorUtils = {
    /**
     * Convert hex color to RGB object
     */
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    },

    /**
     * Convert RGB to hex
     */
    rgbToHex(r, g, b) {
        return '#' + [r, g, b].map(x => {
            const hex = x.toString(16);
            return hex.length === 1 ? '0' + hex : hex;
        }).join('');
    },

    /**
     * Calculate relative luminance for WCAG
     * @see https://www.w3.org/TR/WCAG20/#relativeluminancedef
     */
    getLuminance(hex) {
        const rgb = this.hexToRgb(hex);
        if (!rgb) return 0;

        const [rs, gs, bs] = [rgb.r, rgb.g, rgb.b].map(c => {
            c = c / 255;
            return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        });

        return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
    },

    /**
     * Calculate contrast ratio between two colors
     * @see https://www.w3.org/TR/WCAG20/#contrast-ratiodef
     */
    getContrastRatio(color1, color2) {
        const l1 = this.getLuminance(color1);
        const l2 = this.getLuminance(color2);
        const lighter = Math.max(l1, l2);
        const darker = Math.min(l1, l2);
        return (lighter + 0.05) / (darker + 0.05);
    },

    /**
     * Check if contrast passes WCAG thresholds
     */
    checkContrast(foreground, background) {
        const ratio = this.getContrastRatio(foreground, background);
        return {
            ratio: ratio.toFixed(2),
            passesAA: ratio >= 4.5,
            passesAAA: ratio >= 7,
            passesAALarge: ratio >= 3,
        };
    },

    /**
     * Darken a color by percentage
     */
    darken(hex, percent) {
        const rgb = this.hexToRgb(hex);
        if (!rgb) return hex;
        
        const factor = 1 - (percent / 100);
        return this.rgbToHex(
            Math.round(rgb.r * factor),
            Math.round(rgb.g * factor),
            Math.round(rgb.b * factor)
        );
    },

    /**
     * Lighten a color by percentage
     */
    lighten(hex, percent) {
        const rgb = this.hexToRgb(hex);
        if (!rgb) return hex;
        
        const factor = percent / 100;
        return this.rgbToHex(
            Math.round(rgb.r + (255 - rgb.r) * factor),
            Math.round(rgb.g + (255 - rgb.g) * factor),
            Math.round(rgb.b + (255 - rgb.b) * factor)
        );
    },

    /**
     * Check if a color is light or dark
     */
    isLight(hex) {
        return this.getLuminance(hex) > 0.179;
    }
};

// Export for use in other modules
window.ColorUtils = ColorUtils;
