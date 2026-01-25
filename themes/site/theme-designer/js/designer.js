/**
 * Xerte Theme Designer - Main Application
 */

class ThemeDesigner {
    constructor() {
        this.iframe = document.getElementById('preview-frame');
        this.exportModal = document.getElementById('export-modal');
        this.currentPreset = null;

        // Current theme state
        this.theme = {
            'color-primary': '#E4251B',
            'color-secondary': '#121212',
            'color-accent': '#07873E',
            'color-link': '#0645AD',
            'color-focus': '#fdcd0d',
            'font-family': "'Inter', -apple-system, sans-serif",
            'font-size': '16',
            'line-height': '1.5',
            'border-radius': '8'
        };

        this.init();
    }

    init() {
        this.bindColorInputs();
        this.bindRangeInputs();
        this.bindSelectInputs();
        this.bindPresetButtons();
        this.bindActionButtons();
        this.bindModalButtons();
        this.bindPreviewTabs();

        // Initial update
        this.iframe.addEventListener('load', () => {
            this.updatePreview();
            this.updateContrastBadges();
        });
    }

    /**
     * Bind color picker and hex input events
     */
    bindColorInputs() {
        const colorInputs = [
            { picker: 'color-primary', hex: 'color-primary-hex', key: 'color-primary' },
            { picker: 'color-secondary', hex: 'color-secondary-hex', key: 'color-secondary' },
            { picker: 'color-accent', hex: 'color-accent-hex', key: 'color-accent' },
            { picker: 'color-link', hex: 'color-link-hex', key: 'color-link' },
            { picker: 'color-focus', hex: 'color-focus-hex', key: 'color-focus' }
        ];

        colorInputs.forEach(({ picker, hex, key }) => {
            const pickerEl = document.getElementById(picker);
            const hexEl = document.getElementById(hex);

            if (pickerEl && hexEl) {
                // Color picker change
                pickerEl.addEventListener('input', (e) => {
                    const value = e.target.value.toUpperCase();
                    hexEl.value = value;
                    this.theme[key] = value;
                    this.updatePreview();
                    this.updateContrastBadges();
                });

                // Hex input change
                hexEl.addEventListener('input', (e) => {
                    let value = e.target.value;
                    if (!value.startsWith('#')) {
                        value = '#' + value;
                    }
                    if (/^#[0-9A-Fa-f]{6}$/.test(value)) {
                        pickerEl.value = value;
                        this.theme[key] = value.toUpperCase();
                        this.updatePreview();
                        this.updateContrastBadges();
                    }
                });
            }
        });
    }

    /**
     * Bind range slider events
     */
    bindRangeInputs() {
        const ranges = [
            { id: 'font-size', output: 'font-size-output', key: 'font-size', unit: 'px' },
            { id: 'line-height', output: 'line-height-output', key: 'line-height', unit: '' },
            { id: 'border-radius', output: 'border-radius-output', key: 'border-radius', unit: 'px' }
        ];

        ranges.forEach(({ id, output, key, unit }) => {
            const rangeEl = document.getElementById(id);
            const outputEl = document.getElementById(output);

            if (rangeEl && outputEl) {
                rangeEl.addEventListener('input', (e) => {
                    const value = e.target.value;
                    outputEl.textContent = value + unit;
                    this.theme[key] = value;
                    this.updatePreview();
                });
            }
        });
    }

    /**
     * Bind select input events
     */
    bindSelectInputs() {
        const fontFamily = document.getElementById('font-family');
        if (fontFamily) {
            fontFamily.addEventListener('change', (e) => {
                this.theme['font-family'] = e.target.value;
                this.updatePreview();
            });
        }
    }

    /**
     * Bind preset buttons
     */
    bindPresetButtons() {
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const presetKey = e.target.dataset.preset;
                this.applyPreset(presetKey);

                // Update active state
                document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
            });
        });
    }

    /**
     * Bind action buttons (reset, export)
     */
    bindActionButtons() {
        document.getElementById('btn-reset')?.addEventListener('click', () => {
            this.applyPreset('cardiff');
            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
        });

        document.getElementById('btn-export')?.addEventListener('click', () => {
            this.showExportModal();
        });
    }

    /**
     * Bind modal buttons
     */
    bindModalButtons() {
        document.getElementById('btn-close-modal')?.addEventListener('click', () => {
            this.exportModal.close();
        });

        document.getElementById('btn-copy')?.addEventListener('click', () => {
            this.copyToClipboard();
        });

        document.getElementById('btn-download')?.addEventListener('click', () => {
            this.downloadCSS();
        });

        // Close on backdrop click
        this.exportModal?.addEventListener('click', (e) => {
            if (e.target === this.exportModal) {
                this.exportModal.close();
            }
        });
    }

    /**
     * Bind preview tab switching
     */
    bindPreviewTabs() {
        document.querySelectorAll('.preview-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;

                // Update active tab
                document.querySelectorAll('.preview-tab').forEach(t => t.classList.remove('active'));
                e.target.classList.add('active');

                // Send message to iframe
                this.iframe.contentWindow?.postMessage({ type: 'showSection', section: tabName }, '*');
            });
        });
    }

    /**
     * Apply a preset theme
     */
    applyPreset(presetKey) {
        const preset = window.ThemePresets?.[presetKey];
        if (!preset) return;

        this.currentPreset = presetKey;
        this.theme = { ...preset.tokens };

        // Update all controls
        this.updateControlsFromTheme();
        this.updatePreview();
        this.updateContrastBadges();
    }

    /**
     * Update all control inputs from current theme state
     */
    updateControlsFromTheme() {
        // Color inputs
        ['primary', 'secondary', 'accent', 'link', 'focus'].forEach(name => {
            const key = `color-${name}`;
            const pickerEl = document.getElementById(key);
            const hexEl = document.getElementById(`${key}-hex`);

            if (pickerEl && this.theme[key]) {
                pickerEl.value = this.theme[key];
            }
            if (hexEl && this.theme[key]) {
                hexEl.value = this.theme[key];
            }
        });

        // Range inputs
        const fontSizeEl = document.getElementById('font-size');
        const fontSizeOutput = document.getElementById('font-size-output');
        if (fontSizeEl && this.theme['font-size']) {
            fontSizeEl.value = this.theme['font-size'];
            fontSizeOutput.textContent = this.theme['font-size'] + 'px';
        }

        const lineHeightEl = document.getElementById('line-height');
        const lineHeightOutput = document.getElementById('line-height-output');
        if (lineHeightEl && this.theme['line-height']) {
            lineHeightEl.value = this.theme['line-height'];
            lineHeightOutput.textContent = this.theme['line-height'];
        }

        const borderRadiusEl = document.getElementById('border-radius');
        const borderRadiusOutput = document.getElementById('border-radius-output');
        if (borderRadiusEl && this.theme['border-radius']) {
            borderRadiusEl.value = this.theme['border-radius'];
            borderRadiusOutput.textContent = this.theme['border-radius'] + 'px';
        }

        // Font family
        const fontFamilyEl = document.getElementById('font-family');
        if (fontFamilyEl && this.theme['font-family']) {
            fontFamilyEl.value = this.theme['font-family'];
        }
    }

    /**
     * Update the preview iframe with current theme
     */
    updatePreview() {
        const iframeDoc = this.iframe.contentDocument;
        if (!iframeDoc) return;

        const root = iframeDoc.documentElement;

        // Apply CSS custom properties
        root.style.setProperty('--color-brand-primary', this.theme['color-primary']);
        root.style.setProperty('--color-brand-secondary', this.theme['color-secondary']);
        root.style.setProperty('--color-accent-green', this.theme['color-accent']);
        root.style.setProperty('--color-link-default', this.theme['color-link']);
        root.style.setProperty('--focus-ring-color', this.theme['color-focus']);
        root.style.setProperty('--font-family-primary', this.theme['font-family']);
        root.style.setProperty('--font-size-base', this.theme['font-size'] + 'px');
        root.style.setProperty('--line-height-normal', this.theme['line-height']);
        root.style.setProperty('--radius-md', this.theme['border-radius'] + 'px');
        root.style.setProperty('--btn-border-radius', this.theme['border-radius'] + 'px');

        // Generate derived colors using color-mix
        root.style.setProperty('--color-brand-primary-dark',
            `color-mix(in srgb, ${this.theme['color-primary']} 80%, black)`);
        root.style.setProperty('--color-brand-primary-light',
            `color-mix(in srgb, ${this.theme['color-primary']} 30%, white)`);
        root.style.setProperty('--btn-primary-bg', this.theme['color-primary']);
        root.style.setProperty('--btn-primary-hover-bg',
            `color-mix(in srgb, ${this.theme['color-primary']} 85%, black)`);
        root.style.setProperty('--color-link-hover',
            `color-mix(in srgb, ${this.theme['color-link']} 70%, black)`);
    }

    /**
     * Update contrast ratio badges
     */
    updateContrastBadges() {
        const white = '#FFFFFF';

        // Primary color contrast
        const primaryContrast = document.getElementById('contrast-primary');
        if (primaryContrast) {
            const result = ColorUtils.checkContrast(white, this.theme['color-primary']);
            primaryContrast.textContent = result.passesAA ? `✓ AA (${result.ratio}:1)` : `✗ Fail (${result.ratio}:1)`;
            primaryContrast.className = 'contrast-badge ' + (result.passesAA ? 'pass' : 'fail');
        }

        // Secondary color contrast
        const secondaryContrast = document.getElementById('contrast-secondary');
        if (secondaryContrast) {
            const result = ColorUtils.checkContrast(white, this.theme['color-secondary']);
            secondaryContrast.textContent = result.passesAA ? `✓ AA (${result.ratio}:1)` : `✗ Fail (${result.ratio}:1)`;
            secondaryContrast.className = 'contrast-badge ' + (result.passesAA ? 'pass' : 'fail');
        }

        // Link color contrast
        const linkContrast = document.getElementById('contrast-link');
        if (linkContrast) {
            const result = ColorUtils.checkContrast(this.theme['color-link'], white);
            linkContrast.textContent = result.passesAA ? `✓ AA (${result.ratio}:1)` : `✗ Fail (${result.ratio}:1)`;
            linkContrast.className = 'contrast-badge ' + (result.passesAA ? 'pass' : 'fail');
        }
    }

    /**
     * Generate export CSS
     */
    generateCSS() {
        const presetName = this.currentPreset
            ? window.ThemePresets[this.currentPreset]?.name || 'Custom'
            : 'Custom';

        return `/**
 * Custom Theme: ${presetName}
 * Generated by Xerte Theme Designer
 * Date: ${new Date().toISOString().split('T')[0]}
 * 
 * Usage: Load this CSS after cardiffuni-v2.css
 */

:root {
    /* Brand Colors */
    --color-brand-primary: ${this.theme['color-primary']};
    --color-brand-secondary: ${this.theme['color-secondary']};
    --color-accent-green: ${this.theme['color-accent']};
    
    /* Derived brand colors */
    --color-brand-primary-light: color-mix(in srgb, var(--color-brand-primary) 30%, white);
    --color-brand-primary-dark: color-mix(in srgb, var(--color-brand-primary) 80%, black);
    
    /* Links */
    --color-link-default: ${this.theme['color-link']};
    --color-link-hover: color-mix(in srgb, var(--color-link-default) 70%, black);
    
    /* Focus */
    --focus-ring-color: ${this.theme['color-focus']};
    --focus-ring: 3px solid ${this.theme['color-focus']};
    
    /* Typography */
    --font-family-primary: ${this.theme['font-family']};
    --font-size-base: ${this.theme['font-size']}px;
    --line-height-normal: ${this.theme['line-height']};
    
    /* Borders */
    --radius-md: ${this.theme['border-radius']}px;
    --btn-border-radius: ${this.theme['border-radius']}px;
    
    /* Buttons */
    --btn-primary-bg: var(--color-brand-primary);
    --btn-primary-hover-bg: color-mix(in srgb, var(--color-brand-primary) 85%, black);
    --btn-primary-active-bg: color-mix(in srgb, var(--color-brand-primary) 75%, black);
}
`;
    }

    /**
     * Show export modal with generated CSS
     */
    showExportModal() {
        const css = this.generateCSS();
        document.getElementById('export-css').value = css;
        this.exportModal.showModal();
    }

    /**
     * Copy CSS to clipboard
     */
    async copyToClipboard() {
        const css = document.getElementById('export-css').value;
        try {
            await navigator.clipboard.writeText(css);
            const btn = document.getElementById('btn-copy');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span class="btn-icon">✓</span> Copied!';
            setTimeout(() => {
                btn.innerHTML = originalText;
            }, 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    }

    /**
     * Download CSS as file
     */
    downloadCSS() {
        const css = this.generateCSS();
        const blob = new Blob([css], { type: 'text/css' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'custom-theme.css';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.themeDesigner = new ThemeDesigner();
    });
} else {
    window.themeDesigner = new ThemeDesigner();
}
