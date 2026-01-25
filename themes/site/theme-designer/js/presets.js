/**
 * Theme Presets
 * Pre-configured themes for quick application
 */

const ThemePresets = {
    cardiff: {
        name: 'Cardiff University',
        tokens: {
            'color-primary': '#E4251B',
            'color-secondary': '#121212',
            'color-accent': '#07873E',
            'color-link': '#0645AD',
            'color-focus': '#fdcd0d',
            'font-family': "'Inter', -apple-system, sans-serif",
            'font-size': '16',
            'line-height': '1.5',
            'border-radius': '8'
        }
    },

    medr: {
        name: 'Medr (Welsh Government)',
        tokens: {
            'color-primary': '#00703C',
            'color-secondary': '#0B0C0C',
            'color-accent': '#1D70B8',
            'color-link': '#1D70B8',
            'color-focus': '#FFBF47',
            'font-family': "'GDS Transport', Arial, sans-serif",
            'font-size': '19',
            'line-height': '1.6',
            'border-radius': '0'
        }
    },

    dark: {
        name: 'Dark Mode',
        tokens: {
            'color-primary': '#6366f1',
            'color-secondary': '#e5e7eb',
            'color-accent': '#22c55e',
            'color-link': '#818cf8',
            'color-focus': '#fbbf24',
            'font-family': "'Inter', -apple-system, sans-serif",
            'font-size': '16',
            'line-height': '1.5',
            'border-radius': '8'
        },
        // Dark mode also needs background overrides
        darkMode: true
    }
};

// Export for use in other modules
window.ThemePresets = ThemePresets;
