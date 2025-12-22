/**
 * Code Snippets Module
 * Copy-to-clipboard functionality for code examples
 */

export default class CodeSnippets {
    constructor() {
        this.init();
    }

    init() {
        // Find all copy buttons
        const copyButtons = document.querySelectorAll('.code-copy-btn, .copy-btn');

        copyButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.copyCode(e.currentTarget);
            });
        });

        console.log(`Code snippets initialized (${copyButtons.length} copy buttons)`);
    }

    copyCode(button) {
        // Find the code element
        let codeText;

        if (button.classList.contains('code-copy-btn')) {
            // Component demo code - next sibling is the pre/code block
            const codeBlock = button.nextElementSibling || button.closest('.component-demo__code, .code-example')?.querySelector('code');
            codeText = codeBlock?.textContent;
        } else if (button.classList.contains('copy-btn')) {
            // Token/utility copy - data attribute or nearby code element
            const parent = button.closest('[data-code]') || button.closest('.token-card');

            if (parent?.dataset.code) {
                codeText = parent.dataset.code;
            } else {
                const codeElement = parent?.querySelector('code');
                codeText = codeElement?.textContent;
            }
        }

        if (codeText) {
            this.copyToClipboard(codeText);
            this.showCopyFeedback(button);
        } else {
            console.warn('No code found to copy');
        }
    }

    copyToClipboard(text) {
        // Modern clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).catch(err => {
                console.error('Failed to copy:', err);
                this.fallbackCopy(text);
            });
        } else {
            // Fallback for older browsers
            this.fallbackCopy(text);
        }
    }

    fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();

        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('Fallback copy failed:', err);
        }

        document.body.removeChild(textarea);
    }

    showCopyFeedback(button) {
        const originalHTML = button.innerHTML;

        // Change button text
        button.innerHTML = '<span class="copy-icon">✓</span><span class="copy-text">Copied!</span>';
        button.classList.add('copied');

        // Reset after 2 seconds
        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.classList.remove('copied');
        }, 2000);
    }
}
