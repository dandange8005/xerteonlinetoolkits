/**
 * Page Layout Module
 * Injects shared header, navigation, and footer across all pages
 * Provides single source of truth for shared layout components
 */

export default class PageLayout {
    constructor() {
        this.header = null;
        this.nav = null;
        this.footer = null;
    }

    /**
     * Initialize page layout by injecting all shared components
     */
    async init() {
        this.loadHeader();
        this.loadNavigation();
        this.loadFooter();
        this.loadCustomizer();
    }

    /**
     * Load and inject header component
     */
    loadHeader() {
        const headerHTML = `
    <!-- HEADER / HERO -->
    <header class="demo-header" role="banner">
        <div class="demo-header__container">
            <img src="assets/images/logo-cardiff.svg" alt="Cardiff University" class="demo-header__logo">
            <h1 class="demo-header__title">Cardiff University Theme</h1>
            <p class="demo-header__subtitle">Interactive Demo & Documentation v2.0</p>

            <!-- Quick Actions -->
            <div class="demo-header__actions">
                <button class="button button-primary" id="toggle-customizer">
                    <span class="button__icon">🎨</span> Live Theme Customizer
                </button>
            </div>
        </div>
    </header>
        `;

        document.body.insertAdjacentHTML('afterbegin', headerHTML);
        this.header = document.querySelector('.demo-header');
    }

    /**
     * Load and inject navigation component
     */
    loadNavigation() {
        const navHTML = `
    <!-- STICKY NAVIGATION -->
    <nav class="demo-nav" role="navigation" aria-label="Main navigation">
        <div class="demo-nav__container">
            <ul class="demo-nav__menu">
                <li><a href="index.html">Home</a></li>
                <li><a href="design-tokens.html">Design Tokens</a></li>
                <li><a href="base-elements.html">Base Elements</a></li>
                <li><a href="components.html">Components</a></li>
                <li><a href="utilities.html">Utilities</a></li>
                <li><a href="bootstrap.html">Bootstrap</a></li>
                <li><a href="flex-layouts.html">Flex Layouts</a></li>
                <li><a href="grid-layouts.html">Grid Layouts</a></li>
                <li><a href="customization.html">Customization</a></li>
            </ul>

            <!-- Search -->
            <div class="demo-nav__search">
                <input type="search" placeholder="Search..." id="demo-search" aria-label="Search documentation">
            </div>
        </div>
    </nav>
        `;

        this.header.insertAdjacentHTML('afterend', navHTML);
        this.nav = document.querySelector('.demo-nav');
    }

    /**
     * Load and inject footer component
     */
    loadFooter() {
        const footerHTML = `
    <!-- FOOTER -->
    <footer class="demo-footer">
        <div class="demo-footer__container">
            <div class="footer-section">
                <h3>Resources</h3>
                <ul>
                    <li><a href="../docs/CARDIFF_THEME_GUIDE.md">Theme Guide</a></li>
                    <li><a href="../demos/">Reference Demos</a></li>
                    <li><a href="https://www.cardiff.ac.uk/public-information/about-us/our-brand">Cardiff Brand Guidelines</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <ul>
                    <li><a href="design-tokens.html">Design Tokens</a></li>
                    <li><a href="components.html">Components</a></li>
                    <li><a href="utilities.html">Utilities</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <p>Cardiff University Theme v2.0</p>
                <p>Built with modern CSS custom properties</p>
            </div>
        </div>
    </footer>
        `;

        document.body.insertAdjacentHTML('beforeend', footerHTML);
        this.footer = document.querySelector('.demo-footer');
    }

    /**
     * Load and inject theme customizer component
     */
    loadCustomizer() {
        const customizerHTML = `
    <!-- Side Panel: Live Theme Customizer (collapsible) -->
    <aside class="demo-customizer" id="theme-customizer" aria-label="Theme customizer" hidden>
        <div class="demo-customizer__header">
            <h2>Live Theme Customizer</h2>
            <button class="demo-customizer__close" aria-label="Close customizer">×</button>
        </div>

        <div class="demo-customizer__body">
            <!-- Color Controls -->
            <section class="customizer-section">
                <h3>Brand Colors</h3>
                <div class="customizer-control">
                    <label for="primary-color">Primary Brand Color</label>
                    <input type="color" id="primary-color" data-css-var="--cu-primary-red" value="#E4251B">
                    <input type="text" class="customizer-hex" value="#E4251B" data-default="#E4251B">
                </div>
                <div class="customizer-control">
                    <label for="forest-green">Forest Green</label>
                    <input type="color" id="forest-green" data-css-var="--cu-forest-green" value="#07873E">
                    <input type="text" class="customizer-hex" value="#07873E" data-default="#07873E">
                </div>
            </section>

            <!-- Typography Controls -->
            <section class="customizer-section">
                <h3>Typography</h3>
                <div class="customizer-control">
                    <label for="base-font-size">Base Font Size</label>
                    <input type="range" id="base-font-size" data-css-var="--font-size-base" data-type="font-size" min="14" max="20" value="16" data-default="16">
                    <span class="customizer-value">16px</span>
                </div>
            </section>

            <!-- Spacing Controls -->
            <section class="customizer-section">
                <h3>Spacing Scale</h3>
                <div class="customizer-control">
                    <label for="spacing-base">Spacing Base (MD)</label>
                    <input type="range" id="spacing-base" data-css-var="--spacing-md" data-type="spacing" min="12" max="24" value="16" data-default="16">
                    <span class="customizer-value">16px</span>
                </div>
            </section>

            <!-- Actions -->
            <div class="customizer-actions">
                <button class="button button-primary button--small" id="export-css">Export CSS</button>
                <button class="button button-secondary button--small" id="reset-theme">Reset</button>
            </div>
        </div>
    </aside>
        `;

        // Insert customizer after navigation
        if (this.nav) {
            this.nav.insertAdjacentHTML('afterend', customizerHTML);
        }
    }
}
