/**
 * Demo Site Main Controller
 * Coordinates all interactive features
 */

import ThemeCustomizer from './modules/theme-customizer.js';
import CodeSnippets from './modules/code-snippets.js';
import ResponsivePreview from './modules/responsive-preview.js';
import Navigation from './modules/navigation.js';

class DemoSite {
    constructor() {
        this.customizer = null;
        this.codeSnippets = null;
        this.responsivePreview = null;
        this.navigation = null;
    }

    init() {
        console.log('Initializing Cardiff University Demo Site...');

        // Initialize all modules
        this.customizer = new ThemeCustomizer();
        this.codeSnippets = new CodeSnippets();
        this.responsivePreview = new ResponsivePreview();
        this.navigation = new Navigation();

        // Setup event listeners
        this.setupEventListeners();

        // Load saved preferences
        this.loadPreferences();

        console.log('Demo site initialized successfully!');
    }

    setupEventListeners() {
        // Toggle customizer
        const customizerBtn = document.getElementById('toggle-customizer');
        if (customizerBtn) {
            customizerBtn.addEventListener('click', () => {
                this.customizer.toggle();
            });
        }

        // Toggle responsive preview
        const responsiveBtn = document.getElementById('toggle-responsive');
        if (responsiveBtn) {
            responsiveBtn.addEventListener('click', () => {
                this.responsivePreview.toggle();
            });
        }

        // Handle keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K: Open search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.getElementById('demo-search');
                if (searchInput) {
                    searchInput.focus();
                }
            }

            // Escape: Close customizer
            if (e.key === 'Escape') {
                this.customizer.close();
            }
        });
    }

    loadPreferences() {
        // Load user's saved theme customizations from localStorage
        const savedTheme = localStorage.getItem('cardiff-theme-customizations');
        if (savedTheme) {
            try {
                this.customizer.applyTheme(JSON.parse(savedTheme));
                console.log('Loaded saved theme customizations');
            } catch (error) {
                console.error('Error loading saved theme:', error);
            }
        }
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        const demoSite = new DemoSite();
        demoSite.init();
    });
} else {
    const demoSite = new DemoSite();
    demoSite.init();
}
