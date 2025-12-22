/**
 * Demo Site Main Controller
 * Coordinates all interactive features
 */

import PageLayout from './modules/page-layout.js';
import ThemeCustomizer from './modules/theme-customizer.js';
import CodeSnippets from './modules/code-snippets.js';
import Navigation from './modules/navigation.js';

class DemoSite {
    constructor() {
        this.pageLayout = null;
        this.customizer = null;
        this.codeSnippets = null;
        this.navigation = null;
    }

    async init() {
        console.log('Initializing Cardiff University Demo Site...');

        // Initialize page layout first (injects shared header/nav/footer)
        this.pageLayout = new PageLayout();
        await this.pageLayout.init();

        // Initialize all modules
        this.customizer = new ThemeCustomizer();
        this.codeSnippets = new CodeSnippets();
        this.navigation = new Navigation();
        this.navigation.init();

        // Setup event listeners
        this.setupEventListeners();

        // Load saved preferences
        this.loadPreferences();

        console.log('Demo site initialized successfully!');
    }

    setupEventListeners() {
        // Wait for page layout to inject elements
        setTimeout(() => {
            // Toggle customizer
            const customizerBtn = document.getElementById('toggle-customizer');
            if (customizerBtn) {
                customizerBtn.addEventListener('click', () => {
                    this.customizer.toggle();
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
        }, 150); // Delay to ensure DOM elements are injected
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
