/**
 * Responsive Preview Module
 * Device viewport preview toggle
 */

export default class ResponsivePreview {
    constructor() {
        this.previewFrame = document.getElementById('preview-frame');
        this.iframe = this.previewFrame?.querySelector('.demo-preview-iframe');
        this.isActive = false;
        this.currentWidth = '100%';
        this.init();
    }

    init() {
        if (!this.previewFrame) {
            console.warn('Preview frame not found');
            return;
        }

        // Setup preview control buttons
        const previewButtons = this.previewFrame.querySelectorAll('.preview-btn');

        previewButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const width = e.currentTarget.dataset.width;
                this.setPreviewWidth(width);

                // Update active state
                previewButtons.forEach(btn => btn.classList.remove('active'));
                e.currentTarget.classList.add('active');
            });
        });

        console.log('Responsive preview initialized');
    }

    toggle() {
        this.isActive = !this.isActive;

        if (this.isActive) {
            this.show();
        } else {
            this.hide();
        }
    }

    show() {
        // Clone the demo content into iframe
        const demoContent = document.querySelector('.demo-content');

        if (demoContent && this.iframe) {
            this.previewFrame.removeAttribute('hidden');

            // Create iframe document
            const iframeDoc = this.iframe.contentDocument || this.iframe.contentWindow.document;

            // Copy theme CSS
            const themeCSS = Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
                .map(link => `<link rel="stylesheet" href="${link.href}">`)
                .join('\n');

            // Build iframe content
            iframeDoc.open();
            iframeDoc.write(`
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    ${themeCSS}
                    <style>
                        body { margin: 2rem; background: #f9fafb; }
                    </style>
                </head>
                <body>
                    ${demoContent.innerHTML}
                </body>
                </html>
            `);
            iframeDoc.close();

            console.log('Preview mode activated');
        }
    }

    hide() {
        if (this.previewFrame) {
            this.previewFrame.setAttribute('hidden', '');
            console.log('Preview mode deactivated');
        }
    }

    setPreviewWidth(width) {
        if (this.iframe) {
            if (width === '100%') {
                this.iframe.style.width = '100%';
                this.iframe.style.maxWidth = '100%';
            } else {
                this.iframe.style.width = width + 'px';
                this.iframe.style.maxWidth = width + 'px';
                this.iframe.style.margin = '0 auto';
            }

            this.currentWidth = width;
        }
    }
}
