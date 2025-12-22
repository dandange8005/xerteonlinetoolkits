/**
 * Theme Customizer Module
 * Live editing of CSS custom properties
 */

export default class ThemeCustomizer {
    constructor() {
        this.panel = document.getElementById('theme-customizer');
        this.controls = {};
        this.currentTheme = {};
        this.init();
    }

    init() {
        if (!this.panel) {
            console.warn('Theme customizer panel not found');
            return;
        }

        // Setup color pickers
        this.setupColorControls();

        // Setup typography controls
        this.setupTypographyControls();

        // Setup spacing controls
        this.setupSpacingControls();

        // Setup action buttons
        this.setupActions();

        console.log('Theme customizer initialized');
    }

    setupColorControls() {
        // Get all color inputs
        const colorInputs = this.panel.querySelectorAll('input[type="color"]');

        colorInputs.forEach(input => {
            const varName = input.dataset.cssVar; // e.g., --cu-primary-red

            // Sync color picker with text input
            const textInput = input.nextElementSibling;

            input.addEventListener('input', (e) => {
                const color = e.target.value;
                this.updateCSSVariable(varName, color);
                if (textInput && textInput.classList.contains('customizer-hex')) {
                    textInput.value = color;
                }
            });

            if (textInput && textInput.classList.contains('customizer-hex')) {
                textInput.addEventListener('input', (e) => {
                    const color = e.target.value;
                    if (this.isValidColor(color)) {
                        this.updateCSSVariable(varName, color);
                        input.value = color;
                    }
                });
            }

            this.controls[varName] = { input, textInput };
        });
    }

    setupTypographyControls() {
        // Font size sliders
        const fontSizeInputs = this.panel.querySelectorAll('[data-type="font-size"]');

        fontSizeInputs.forEach(input => {
            const varName = input.dataset.cssVar;
            const valueDisplay = input.nextElementSibling;

            input.addEventListener('input', (e) => {
                const value = `${e.target.value}px`;
                this.updateCSSVariable(varName, value);
                if (valueDisplay && valueDisplay.classList.contains('customizer-value')) {
                    valueDisplay.textContent = value;
                }
            });

            this.controls[varName] = { input, valueDisplay };
        });

        // Line height sliders
        const lineHeightInputs = this.panel.querySelectorAll('[data-type="line-height"]');

        lineHeightInputs.forEach(input => {
            const varName = input.dataset.cssVar;
            const valueDisplay = input.nextElementSibling;

            input.addEventListener('input', (e) => {
                const value = e.target.value;
                this.updateCSSVariable(varName, value);
                if (valueDisplay && valueDisplay.classList.contains('customizer-value')) {
                    valueDisplay.textContent = value;
                }
            });

            this.controls[varName] = { input, valueDisplay };
        });
    }

    setupSpacingControls() {
        // Spacing inputs
        const spacingInputs = this.panel.querySelectorAll('[data-type="spacing"]');

        spacingInputs.forEach(input => {
            const varName = input.dataset.cssVar;
            const valueDisplay = input.nextElementSibling;

            input.addEventListener('input', (e) => {
                const value = `${e.target.value}px`;
                this.updateCSSVariable(varName, value);
                if (valueDisplay && valueDisplay.classList.contains('customizer-value')) {
                    valueDisplay.textContent = value;
                }
            });

            this.controls[varName] = { input, valueDisplay };
        });
    }

    setupActions() {
        // Export CSS button
        const exportBtn = document.getElementById('export-css');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportCSS();
            });
        }

        // Reset button
        const resetBtn = document.getElementById('reset-theme');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.resetTheme();
            });
        }

        // Close button
        const closeBtn = this.panel.querySelector('.demo-customizer__close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.close();
            });
        }
    }

    updateCSSVariable(varName, value) {
        // Update the CSS variable on :root
        document.documentElement.style.setProperty(varName, value);

        // Track changes
        this.currentTheme[varName] = value;

        // Save to localStorage
        this.saveTheme();
    }

    saveTheme() {
        localStorage.setItem('cardiff-theme-customizations', JSON.stringify(this.currentTheme));
    }

    applyTheme(theme) {
        Object.entries(theme).forEach(([varName, value]) => {
            document.documentElement.style.setProperty(varName, value);
        });
        this.currentTheme = { ...theme };
    }

    resetTheme() {
        // Clear all custom properties
        Object.keys(this.currentTheme).forEach(varName => {
            document.documentElement.style.removeProperty(varName);
        });

        this.currentTheme = {};
        localStorage.removeItem('cardiff-theme-customizations');

        // Reset all form inputs to defaults
        Object.entries(this.controls).forEach(([varName, control]) => {
            if (control.input) {
                const defaultValue = control.input.dataset.default;
                if (defaultValue) {
                    control.input.value = defaultValue;
                    if (control.textInput) {
                        control.textInput.value = defaultValue;
                    }
                    if (control.valueDisplay) {
                        control.valueDisplay.textContent = defaultValue + (control.input.dataset.type === 'font-size' || control.input.dataset.type === 'spacing' ? 'px' : '');
                    }
                }
            }
        });

        this.showNotification('Theme reset to default');
    }

    exportCSS() {
        // Generate CSS code from current theme
        let css = ':root {\n';

        Object.entries(this.currentTheme).forEach(([varName, value]) => {
            css += `  ${varName}: ${value};\n`;
        });

        css += '}';

        // Copy to clipboard
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(css).then(() => {
                this.showNotification('CSS copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy CSS:', err);
            });
        }

        // Also trigger download
        this.downloadCSS(css);
    }

    downloadCSS(css) {
        const blob = new Blob([css], { type: 'text/css' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'custom-cardiff-theme.css';
        a.click();
        URL.revokeObjectURL(url);
    }

    toggle() {
        const isOpen = this.panel.hasAttribute('hidden');

        if (isOpen) {
            this.panel.removeAttribute('hidden');
            // Small delay for smooth animation
            setTimeout(() => {
                this.panel.classList.add('is-open');
            }, 10);
        } else {
            this.close();
        }

        // Update button state
        const toggleBtn = document.getElementById('toggle-customizer');
        if (toggleBtn) {
            toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        }
    }

    close() {
        this.panel.classList.remove('is-open');

        // Wait for animation to complete before hiding
        setTimeout(() => {
            this.panel.setAttribute('hidden', '');
        }, 300);
    }

    showNotification(message) {
        // Simple toast notification
        const toast = document.createElement('div');
        toast.className = 'demo-toast';
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('show');
        }, 10);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    isValidColor(color) {
        // Simple color validation (hex, rgb, hsl)
        const hexPattern = /^#[0-9A-F]{6}$/i;
        const hexShortPattern = /^#[0-9A-F]{3}$/i;
        const rgbPattern = /^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$/;
        const hslPattern = /^hsl\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*\)$/;

        return hexPattern.test(color) || hexShortPattern.test(color) || rgbPattern.test(color) || hslPattern.test(color);
    }
}
