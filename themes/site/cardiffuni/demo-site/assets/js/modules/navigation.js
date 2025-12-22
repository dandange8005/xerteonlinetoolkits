/**
 * Navigation Module
 * Multi-page navigation with active page highlighting and sticky nav
 */

export default class Navigation {
    constructor() {
        this.nav = null;
        this.currentPage = null;
    }

    init() {
        // Wait for page layout to load navigation
        setTimeout(() => {
            this.nav = document.querySelector('.demo-nav');

            if (!this.nav) {
                console.warn('Navigation element not found');
                return;
            }

            // Get current page from URL
            this.currentPage = this.getCurrentPage();

            // Highlight active page in navigation
            this.highlightActivePage();

            // Setup sticky nav behavior
            this.setupStickyNav();

            console.log('Navigation initialized for page:', this.currentPage);
        }, 100); // Small delay to ensure DOM is ready
    }

    /**
     * Extract current page name from URL
     * @returns {string} Current page name (e.g., "components", "design-tokens")
     */
    getCurrentPage() {
        const path = window.location.pathname;
        const page = path.split('/').pop().replace('.html', '');

        // Return 'index' for root or empty page
        return page || 'index';
    }

    /**
     * Highlight the active page in navigation
     */
    highlightActivePage() {
        if (!this.nav) return;

        const navLinks = this.nav.querySelectorAll('a');

        navLinks.forEach(link => {
            link.classList.remove('active');

            const href = link.getAttribute('href');
            if (!href) return;

            // Extract page name from href
            const linkPage = href.replace('.html', '').replace('./', '');

            // Match current page
            if (linkPage === this.currentPage ||
                (this.currentPage === 'index' && (linkPage === '' || linkPage === 'index'))) {
                link.classList.add('active');
            }
        });
    }

    /**
     * Setup sticky navigation behavior
     * Shows/hides nav based on scroll direction
     */
    setupStickyNav() {
        let lastScrollY = window.scrollY;

        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;

            // Add sticky class when scrolling down past header
            if (currentScrollY > 200) {
                this.nav.classList.add('is-sticky');
            } else {
                this.nav.classList.remove('is-sticky');
            }

            // Hide/show on scroll direction
            if (currentScrollY > lastScrollY && currentScrollY > 300) {
                this.nav.classList.add('is-hidden');
            } else {
                this.nav.classList.remove('is-hidden');
            }

            lastScrollY = currentScrollY;
        });
    }
}
