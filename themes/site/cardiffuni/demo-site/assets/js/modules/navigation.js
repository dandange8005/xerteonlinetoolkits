/**
 * Navigation Module
 * Smooth scroll, active section tracking, sticky nav
 */

export default class Navigation {
    constructor() {
        this.nav = document.querySelector('.demo-nav');
        this.sections = [];
        this.currentSection = null;
        this.init();
    }

    init() {
        if (!this.nav) {
            console.warn('Navigation element not found');
            return;
        }

        // Get all sections
        this.sections = Array.from(document.querySelectorAll('.demo-section'));

        // Setup smooth scroll
        this.setupSmoothScroll();

        // Setup intersection observer for active section tracking
        this.setupSectionTracking();

        // Setup sticky nav on scroll
        this.setupStickyNav();

        console.log('Navigation initialized');
    }

    setupSmoothScroll() {
        const navLinks = this.nav.querySelectorAll('a[href^="#"]');

        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetSection = document.getElementById(targetId);

                if (targetSection) {
                    const offsetTop = targetSection.offsetTop - this.nav.offsetHeight - 20;

                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    setupSectionTracking() {
        const options = {
            root: null,
            rootMargin: `-${this.nav.offsetHeight + 50}px 0px -70% 0px`,
            threshold: 0
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.updateActiveSection(entry.target.id);
                }
            });
        }, options);

        this.sections.forEach(section => {
            observer.observe(section);
        });
    }

    updateActiveSection(sectionId) {
        // Remove active class from all links
        const navLinks = this.nav.querySelectorAll('a');
        navLinks.forEach(link => link.classList.remove('active'));

        // Add active class to current section link
        const activeLink = this.nav.querySelector(`a[href="#${sectionId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        this.currentSection = sectionId;
    }

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
