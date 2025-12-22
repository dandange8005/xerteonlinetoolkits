/**
 * Prism.js - Lightweight syntax highlighting
 * Minimal version for demo site
 */

(function() {
    if (typeof window === 'undefined') {
        return;
    }

    const Prism = {
        highlight: function(text, grammar) {
            return text; // Basic passthrough for now
        },

        highlightElement: function(element) {
            const code = element.textContent;
            const language = element.className.match(/language-(\w+)/)?.[1] || '';

            // Basic HTML escaping
            element.innerHTML = this.escapeHTML(code);
        },

        highlightAll: function() {
            const elements = document.querySelectorAll('code[class*="language-"]');
            elements.forEach(element => {
                this.highlightElement(element);
            });
        },

        escapeHTML: function(text) {
            return text
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }
    };

    window.Prism = Prism;

    // Auto-highlight on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => Prism.highlightAll());
    } else {
        Prism.highlightAll();
    }
})();
