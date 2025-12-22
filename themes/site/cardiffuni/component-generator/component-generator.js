// Component configurations
const componentConfigs = {
    box: {
        title: 'Box Title',
        content: 'Your content goes here. This is a simple box component.',
        icon: '',
        hasIcon: false
    },
    card: {
        title: 'Card Title',
        content: 'Card description goes here.',
        imageUrl: '',
        linkText: 'Read more',
        linkUrl: '#',
        clickable: false
    },
    button: {
        text: 'Button Text',
        url: '#',
        style: 'primary',
        size: 'normal',
        block: false
    },
    callout: {
        title: 'Callout Title',
        content: 'This is a callout message.',
        type: 'warning',
        emoji: '⚠️'
    },
    accordion: {
        title: 'Click to expand',
        content: 'Hidden content goes here when expanded.'
    },
    alert: {
        content: 'This is an alert message.',
        type: 'info'
    },
    quote: {
        content: 'This is a quote or testimonial.',
        author: 'Author Name',
        role: 'Their Role'
    },
    dosdonts: {
        title: 'Best Practices',
        items: ['Do this thing', 'Do that thing', "Don't do this", "Don't do that"],
        types: ['do', 'do', 'dont', 'dont']
    },
    flexSystem1: {
        numItems: 2,
        direction: 'row',
        wrap: 'wrap',
        alignItems: 'stretch',
        justifyContent: 'flex-start',
        gap: true,
        items: [
            { flexClass: 'flex-300', content: '<h3>Item 1</h3>\n<p>This item has a flex-basis of 300px and will grow/shrink as needed.</p>' },
            { flexClass: 'flex-300', content: '<h3>Item 2</h3>\n<p>This item has a flex-basis of 300px and will grow/shrink as needed.</p>' }
        ]
    },
    flexSystem2: {
        numColumns: 2,
        direction: 'row',
        wrap: 'wrap',
        alignItems: 'stretch',
        justifyContent: 'flex-start',
        gap: true,
        columns: [
            { width: 'c50', content: '<h3>Column 1</h3>\n<p>Content for first column goes here.</p>' },
            { width: 'c50', content: '<h3>Column 2</h3>\n<p>Content for second column goes here.</p>' }
        ]
    }
};

// Current component state
let currentComponent = 'box';
let currentConfig = JSON.parse(JSON.stringify(componentConfigs[currentComponent]));

// Common Font Awesome icons organized by category
const iconCategories = {
    'Information': [
        { class: 'fas fa-info-circle', name: 'Info Circle' },
        { class: 'fas fa-question-circle', name: 'Question Circle' },
        { class: 'fas fa-exclamation-triangle', name: 'Warning Triangle' },
        { class: 'fas fa-exclamation-circle', name: 'Exclamation Circle' },
        { class: 'fas fa-check-circle', name: 'Check Circle' },
        { class: 'fas fa-times-circle', name: 'Times Circle' },
        { class: 'fas fa-lightbulb', name: 'Lightbulb' },
        { class: 'fas fa-star', name: 'Star' }
    ],
    'Learning': [
        { class: 'fas fa-book', name: 'Book' },
        { class: 'fas fa-graduation-cap', name: 'Graduation Cap' },
        { class: 'fas fa-chalkboard-teacher', name: 'Teacher' },
        { class: 'fas fa-user-graduate', name: 'Graduate' },
        { class: 'fas fa-pencil-alt', name: 'Pencil' },
        { class: 'fas fa-clipboard-list', name: 'Clipboard List' },
        { class: 'fas fa-tasks', name: 'Tasks' },
        { class: 'fas fa-certificate', name: 'Certificate' }
    ],
    'Actions': [
        { class: 'fas fa-download', name: 'Download' },
        { class: 'fas fa-upload', name: 'Upload' },
        { class: 'fas fa-play', name: 'Play' },
        { class: 'fas fa-pause', name: 'Pause' },
        { class: 'fas fa-stop', name: 'Stop' },
        { class: 'fas fa-search', name: 'Search' },
        { class: 'fas fa-cog', name: 'Settings' },
        { class: 'fas fa-edit', name: 'Edit' }
    ],
    'Communication': [
        { class: 'fas fa-envelope', name: 'Email' },
        { class: 'fas fa-phone', name: 'Phone' },
        { class: 'fas fa-comments', name: 'Comments' },
        { class: 'fas fa-bell', name: 'Bell' },
        { class: 'fas fa-bullhorn', name: 'Announcement' },
        { class: 'fas fa-share', name: 'Share' },
        { class: 'fas fa-link', name: 'Link' },
        { class: 'fas fa-hashtag', name: 'Hashtag' }
    ]
};

// Initialize the app
function init() {
    try {
        console.log('Initializing component generator...');
        updateControls();
        updatePreview();
        updateCode();
        console.log('Component generator initialized successfully');
    } catch (error) {
        console.error('Error initializing app:', error);
    }
}

// Update the controls panel based on selected component
function updateControls() {
    const controlsContainer = document.getElementById('componentControls');
    const config = componentConfigs[currentComponent];
    
    let controlsHTML = '';
    
    switch(currentComponent) {
        case 'box':
            controlsHTML = `
                <div class="form-group">
                    <label for="boxTitle">Title</label>
                    <input type="text" id="boxTitle" value="${config.title}" onchange="updateConfig('title', this.value)">
                </div>
                <div class="form-group">
                    <label for="boxContent">Content</label>
                    <textarea id="boxContent" onchange="updateConfig('content', this.value)">${config.content}</textarea>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Include Icon</span>
                    <label class="toggle-switch">
                        <input type="checkbox" id="boxHasIcon" ${config.hasIcon ? 'checked' : ''} onchange="updateConfig('hasIcon', this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
                <div class="form-group" id="iconGroup" style="${config.hasIcon ? '' : 'display: none;'}">
                    <label for="boxIcon">Select Icon</label>
                    <input type="text" id="boxIcon" value="${config.icon}" placeholder="fas fa-info-circle" onchange="updateConfig('icon', this.value)" style="margin-bottom: 0.5rem;">
                    <div id="iconPicker" class="icon-picker-container">
                        ${generateIconPicker()}
                    </div>
                </div>
            `;
            break;
            
        case 'card':
            controlsHTML = `
                <div class="form-group">
                    <label for="cardTitle">Title</label>
                    <input type="text" id="cardTitle" value="${config.title}" onchange="updateConfig('title', this.value)">
                </div>
                <div class="form-group">
                    <label for="cardContent">Content</label>
                    <textarea id="cardContent" onchange="updateConfig('content', this.value)">${config.content}</textarea>
                </div>
                <div class="form-group">
                    <label for="cardImageUrl">Image URL (optional)</label>
                    <input type="url" id="cardImageUrl" value="${config.imageUrl}" onchange="updateConfig('imageUrl', this.value)">
                </div>
                <div class="form-group">
                    <label for="cardLinkText">Link Text</label>
                    <input type="text" id="cardLinkText" value="${config.linkText}" onchange="updateConfig('linkText', this.value)">
                </div>
                <div class="form-group">
                    <label for="cardLinkUrl">Link URL</label>
                    <input type="url" id="cardLinkUrl" value="${config.linkUrl}" onchange="updateConfig('linkUrl', this.value)">
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Clickable Card</span>
                    <label class="toggle-switch">
                        <input type="checkbox" id="cardClickable" ${config.clickable ? 'checked' : ''} onchange="updateConfig('clickable', this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
            `;
            break;
            
        case 'button':
            controlsHTML = `
                <div class="form-group">
                    <label for="buttonText">Button Text</label>
                    <input type="text" id="buttonText" value="${config.text}" onchange="updateConfig('text', this.value)">
                </div>
                <div class="form-group">
                    <label for="buttonUrl">URL</label>
                    <input type="url" id="buttonUrl" value="${config.url}" onchange="updateConfig('url', this.value)">
                </div>
                <div class="form-group">
                    <label for="buttonStyle">Style</label>
                    <select id="buttonStyle" onchange="updateConfig('style', this.value)">
                        <option value="primary" ${config.style === 'primary' ? 'selected' : ''}>Primary</option>
                        <option value="outline" ${config.style === 'outline' ? 'selected' : ''}>Outline</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="buttonSize">Size</label>
                    <select id="buttonSize" onchange="updateConfig('size', this.value)">
                        <option value="normal" ${config.size === 'normal' ? 'selected' : ''}>Normal</option>
                        <option value="small" ${config.size === 'small' ? 'selected' : ''}>Small</option>
                    </select>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Block Button (Full Width)</span>
                    <label class="toggle-switch">
                        <input type="checkbox" id="buttonBlock" ${config.block ? 'checked' : ''} onchange="updateConfig('block', this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
            `;
            break;
            
        case 'callout':
            controlsHTML = `
                <div class="form-group">
                    <label for="calloutTitle">Title</label>
                    <input type="text" id="calloutTitle" value="${config.title}" onchange="updateConfig('title', this.value)">
                </div>
                <div class="form-group">
                    <label for="calloutContent">Content</label>
                    <textarea id="calloutContent" onchange="updateConfig('content', this.value)">${config.content}</textarea>
                </div>
                <div class="form-group">
                    <label for="calloutType">Type</label>
                    <select id="calloutType" onchange="updateConfig('type', this.value)">
                        <option value="warning" ${config.type === 'warning' ? 'selected' : ''}>Warning</option>
                        <option value="success" ${config.type === 'success' ? 'selected' : ''}>Success</option>
                        <option value="danger" ${config.type === 'danger' ? 'selected' : ''}>Danger</option>
                        <option value="info" ${config.type === 'info' ? 'selected' : ''}>Info</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="calloutEmoji">Custom Emoji (optional)</label>
                    <input type="text" id="calloutEmoji" value="${config.emoji}" onchange="updateConfig('emoji', this.value)">
                </div>
            `;
            break;
            
        case 'accordion':
            controlsHTML = `
                <div class="form-group">
                    <label for="accordionTitle">Summary Text</label>
                    <input type="text" id="accordionTitle" value="${config.title}" onchange="updateConfig('title', this.value)">
                </div>
                <div class="form-group">
                    <label for="accordionContent">Hidden Content</label>
                    <textarea id="accordionContent" onchange="updateConfig('content', this.value)">${config.content}</textarea>
                </div>
            `;
            break;
            
        case 'alert':
            controlsHTML = `
                <div class="form-group">
                    <label for="alertContent">Alert Message</label>
                    <textarea id="alertContent" onchange="updateConfig('content', this.value)">${config.content}</textarea>
                </div>
                <div class="form-group">
                    <label for="alertType">Type</label>
                    <select id="alertType" onchange="updateConfig('type', this.value)">
                        <option value="info" ${config.type === 'info' ? 'selected' : ''}>Info</option>
                        <option value="success" ${config.type === 'success' ? 'selected' : ''}>Success</option>
                        <option value="warning" ${config.type === 'warning' ? 'selected' : ''}>Warning</option>
                        <option value="danger" ${config.type === 'danger' ? 'selected' : ''}>Danger</option>
                    </select>
                </div>
            `;
            break;
            
        case 'quote':
            controlsHTML = `
                <div class="form-group">
                    <label for="quoteContent">Quote Text</label>
                    <textarea id="quoteContent" onchange="updateConfig('content', this.value)">${config.content}</textarea>
                </div>
                <div class="form-group">
                    <label for="quoteAuthor">Author</label>
                    <input type="text" id="quoteAuthor" value="${config.author}" onchange="updateConfig('author', this.value)">
                </div>
                <div class="form-group">
                    <label for="quoteRole">Role/Title</label>
                    <input type="text" id="quoteRole" value="${config.role}" onchange="updateConfig('role', this.value)">
                </div>
            `;
            break;
            
        case 'dosdonts':
            controlsHTML = `
                <div class="form-group">
                    <label for="dosdontsTitle">Section Title</label>
                    <input type="text" id="dosdontsTitle" value="${config.title}" onchange="updateConfig('title', this.value)">
                </div>
                <div class="form-group">
                    <label>Items (one per line, prefix with DO: or DON'T:)</label>
                    <textarea id="dosdontsItems" placeholder="DO: Follow best practices&#10;DO: Use clear language&#10;DON'T: Ignore accessibility&#10;DON'T: Use complex jargon" onchange="updateDosdontsItems(this.value)">${config.items.map((item, i) => (config.types[i] === 'do' ? 'DO: ' : "DON'T: ") + item).join('\n')}</textarea>
                </div>
            `;
            break;

        case 'flexSystem1':
            controlsHTML = `
                <div class="form-group">
                    <label for="flexNumItems">Number of Items</label>
                    <select id="flexNumItems" onchange="updateFlexSystem1Items(this.value)">
                        <option value="1" ${config.numItems === 1 ? 'selected' : ''}>1 Item</option>
                        <option value="2" ${config.numItems === 2 ? 'selected' : ''}>2 Items</option>
                        <option value="3" ${config.numItems === 3 ? 'selected' : ''}>3 Items</option>
                        <option value="4" ${config.numItems === 4 ? 'selected' : ''}>4 Items</option>
                        <option value="5" ${config.numItems === 5 ? 'selected' : ''}>5 Items</option>
                        <option value="6" ${config.numItems === 6 ? 'selected' : ''}>6 Items</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="flexDirection">Direction</label>
                    <select id="flexDirection" onchange="updateConfig('direction', this.value)">
                        <option value="row" ${config.direction === 'row' ? 'selected' : ''}>Row</option>
                        <option value="row-reverse" ${config.direction === 'row-reverse' ? 'selected' : ''}>Row Reverse</option>
                        <option value="column" ${config.direction === 'column' ? 'selected' : ''}>Column</option>
                        <option value="column-reverse" ${config.direction === 'column-reverse' ? 'selected' : ''}>Column Reverse</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="flexWrap">Wrap</label>
                    <select id="flexWrap" onchange="updateConfig('wrap', this.value)">
                        <option value="wrap" ${config.wrap === 'wrap' ? 'selected' : ''}>Wrap</option>
                        <option value="nowrap" ${config.wrap === 'nowrap' ? 'selected' : ''}>No Wrap</option>
                        <option value="wrap-reverse" ${config.wrap === 'wrap-reverse' ? 'selected' : ''}>Wrap Reverse</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="flexAlignItems">Align Items (Vertical)</label>
                    <select id="flexAlignItems" onchange="updateConfig('alignItems', this.value)">
                        <option value="stretch" ${config.alignItems === 'stretch' ? 'selected' : ''}>Stretch</option>
                        <option value="flex-start" ${config.alignItems === 'flex-start' ? 'selected' : ''}>Start</option>
                        <option value="flex-end" ${config.alignItems === 'flex-end' ? 'selected' : ''}>End</option>
                        <option value="center" ${config.alignItems === 'center' ? 'selected' : ''}>Center</option>
                        <option value="baseline" ${config.alignItems === 'baseline' ? 'selected' : ''}>Baseline</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="flexJustifyContent">Justify Content (Horizontal)</label>
                    <select id="flexJustifyContent" onchange="updateConfig('justifyContent', this.value)">
                        <option value="flex-start" ${config.justifyContent === 'flex-start' ? 'selected' : ''}>Start</option>
                        <option value="flex-end" ${config.justifyContent === 'flex-end' ? 'selected' : ''}>End</option>
                        <option value="center" ${config.justifyContent === 'center' ? 'selected' : ''}>Center</option>
                        <option value="space-between" ${config.justifyContent === 'space-between' ? 'selected' : ''}>Space Between</option>
                        <option value="space-around" ${config.justifyContent === 'space-around' ? 'selected' : ''}>Space Around</option>
                        <option value="space-evenly" ${config.justifyContent === 'space-evenly' ? 'selected' : ''}>Space Evenly</option>
                    </select>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Include Gap Spacing</span>
                    <label class="toggle-switch">
                        <input type="checkbox" id="flexGap" ${config.gap ? 'checked' : ''} onchange="updateConfig('gap', this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
                <div id="flexItemSettings">
                    ${config.items.map((item, i) => `
                        <div class="form-group" style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #ddd;">
                            <label for="flexItemClass${i}">Item ${i + 1} Flex Class</label>
                            <select id="flexItemClass${i}" onchange="updateFlexSystem1ItemClass(${i}, this.value)">
                                <option value="flex-1" ${item.flexClass === 'flex-1' ? 'selected' : ''}>flex-1 (grow/shrink, no basis)</option>
                                <option value="flex-initial" ${item.flexClass === 'flex-initial' ? 'selected' : ''}>flex-initial (shrink only)</option>
                                <option value="flex-auto" ${item.flexClass === 'flex-auto' ? 'selected' : ''}>flex-auto (grow/shrink with basis)</option>
                                <option value="flex-none" ${item.flexClass === 'flex-none' ? 'selected' : ''}>flex-none (fixed size)</option>
                                <option value="flex-100" ${item.flexClass === 'flex-100' ? 'selected' : ''}>flex-100 (100px basis)</option>
                                <option value="flex-200" ${item.flexClass === 'flex-200' ? 'selected' : ''}>flex-200 (200px basis)</option>
                                <option value="flex-300" ${item.flexClass === 'flex-300' ? 'selected' : ''}>flex-300 (300px basis)</option>
                                <option value="flex-400" ${item.flexClass === 'flex-400' ? 'selected' : ''}>flex-400 (400px basis)</option>
                                <option value="flex-500" ${item.flexClass === 'flex-500' ? 'selected' : ''}>flex-500 (500px basis)</option>
                                <option value="flex-600" ${item.flexClass === 'flex-600' ? 'selected' : ''}>flex-600 (600px basis)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="flexItemContent${i}">Item ${i + 1} Content</label>
                            <textarea id="flexItemContent${i}" onchange="updateFlexSystem1ItemContent(${i}, this.value)">${item.content}</textarea>
                        </div>
                    `).join('')}
                </div>
            `;
            break;

        case 'flexSystem2':
            controlsHTML = `
                <div class="form-group">
                    <label for="flexNumColumns">Number of Columns</label>
                    <select id="flexNumColumns" onchange="updateFlexSystem2Columns(this.value)">
                        <option value="1" ${config.numColumns === 1 ? 'selected' : ''}>1 Column</option>
                        <option value="2" ${config.numColumns === 2 ? 'selected' : ''}>2 Columns</option>
                        <option value="3" ${config.numColumns === 3 ? 'selected' : ''}>3 Columns</option>
                        <option value="4" ${config.numColumns === 4 ? 'selected' : ''}>4 Columns</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="flexDirection">Direction</label>
                    <select id="flexDirection" onchange="updateConfig('direction', this.value)">
                        <option value="row" ${config.direction === 'row' ? 'selected' : ''}>Row</option>
                        <option value="row-reverse" ${config.direction === 'row-reverse' ? 'selected' : ''}>Row Reverse</option>
                        <option value="column" ${config.direction === 'column' ? 'selected' : ''}>Column</option>
                        <option value="column-reverse" ${config.direction === 'column-reverse' ? 'selected' : ''}>Column Reverse</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="flexWrap">Wrap</label>
                    <select id="flexWrap" onchange="updateConfig('wrap', this.value)">
                        <option value="wrap" ${config.wrap === 'wrap' ? 'selected' : ''}>Wrap</option>
                        <option value="nowrap" ${config.wrap === 'nowrap' ? 'selected' : ''}>No Wrap</option>
                        <option value="wrap-reverse" ${config.wrap === 'wrap-reverse' ? 'selected' : ''}>Wrap Reverse</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="flexAlignItems">Align Items (Vertical)</label>
                    <select id="flexAlignItems" onchange="updateConfig('alignItems', this.value)">
                        <option value="stretch" ${config.alignItems === 'stretch' ? 'selected' : ''}>Stretch</option>
                        <option value="flex-start" ${config.alignItems === 'flex-start' ? 'selected' : ''}>Start</option>
                        <option value="flex-end" ${config.alignItems === 'flex-end' ? 'selected' : ''}>End</option>
                        <option value="center" ${config.alignItems === 'center' ? 'selected' : ''}>Center</option>
                        <option value="baseline" ${config.alignItems === 'baseline' ? 'selected' : ''}>Baseline</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="flexJustifyContent">Justify Content (Horizontal)</label>
                    <select id="flexJustifyContent" onchange="updateConfig('justifyContent', this.value)">
                        <option value="flex-start" ${config.justifyContent === 'flex-start' ? 'selected' : ''}>Start</option>
                        <option value="flex-end" ${config.justifyContent === 'flex-end' ? 'selected' : ''}>End</option>
                        <option value="center" ${config.justifyContent === 'center' ? 'selected' : ''}>Center</option>
                        <option value="space-between" ${config.justifyContent === 'space-between' ? 'selected' : ''}>Space Between</option>
                        <option value="space-around" ${config.justifyContent === 'space-around' ? 'selected' : ''}>Space Around</option>
                        <option value="space-evenly" ${config.justifyContent === 'space-evenly' ? 'selected' : ''}>Space Evenly</option>
                    </select>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Include Gap Spacing</span>
                    <label class="toggle-switch">
                        <input type="checkbox" id="flexGap" ${config.gap ? 'checked' : ''} onchange="updateConfig('gap', this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
                <div id="flexColumnSettings">
                    ${config.columns.map((col, i) => `
                        <div class="form-group" style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #ddd;">
                            <label for="flexColWidth${i}">Column ${i + 1} Width</label>
                            <select id="flexColWidth${i}" onchange="updateFlexSystem2ColumnWidth(${i}, this.value)">
                                <option value="c10" ${col.width === 'c10' ? 'selected' : ''}>10%</option>
                                <option value="c20" ${col.width === 'c20' ? 'selected' : ''}>20%</option>
                                <option value="c25" ${col.width === 'c25' ? 'selected' : ''}>25%</option>
                                <option value="c30" ${col.width === 'c30' ? 'selected' : ''}>30%</option>
                                <option value="c33" ${col.width === 'c33' ? 'selected' : ''}>33.33%</option>
                                <option value="c40" ${col.width === 'c40' ? 'selected' : ''}>40%</option>
                                <option value="c50" ${col.width === 'c50' ? 'selected' : ''}>50%</option>
                                <option value="c60" ${col.width === 'c60' ? 'selected' : ''}>60%</option>
                                <option value="c70" ${col.width === 'c70' ? 'selected' : ''}>70%</option>
                                <option value="c80" ${col.width === 'c80' ? 'selected' : ''}>80%</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="flexColContent${i}">Column ${i + 1} Content</label>
                            <textarea id="flexColContent${i}" onchange="updateFlexSystem2ColumnContent(${i}, this.value)">${col.content}</textarea>
                        </div>
                    `).join('')}
                </div>
            `;
            break;
    }

    controlsContainer.innerHTML = controlsHTML;
}

// Update component configuration
function updateConfig(key, value) {
    try {
        currentConfig[key] = value;
        
        // Handle special cases
        if (currentComponent === 'box' && key === 'hasIcon') {
            const iconGroup = document.getElementById('iconGroup');
            if (iconGroup) {
                iconGroup.style.display = value ? '' : 'none';
            }
        }
        
        updatePreview();
        updateCode();
    } catch (error) {
        console.error('Error updating config:', error);
    }
}

// Special handler for dos/don'ts items
function updateDosdontsItems(text) {
    const lines = text.split('\n').filter(line => line.trim());
    const items = [];
    const types = [];

    lines.forEach(line => {
        if (line.startsWith('DO:')) {
            items.push(line.substring(3).trim());
            types.push('do');
        } else if (line.startsWith("DON'T:")) {
            items.push(line.substring(6).trim());
            types.push('dont');
        }
    });

    currentConfig.items = items;
    currentConfig.types = types;

    updatePreview();
    updateCode();
}

// Special handlers for Flex System 1 (flex-basis)
function updateFlexSystem1Items(numItems) {
    const num = parseInt(numItems);
    currentConfig.numItems = num;

    // Adjust items array based on number
    while (currentConfig.items.length < num) {
        const index = currentConfig.items.length + 1;
        currentConfig.items.push({
            flexClass: 'flex-300',
            content: `<h3>Item ${index}</h3>\n<p>This item has a flex-basis of 300px and will grow/shrink as needed.</p>`
        });
    }

    while (currentConfig.items.length > num) {
        currentConfig.items.pop();
    }

    updateControls();
    updatePreview();
    updateCode();
}

// Update flex system 1 item class
function updateFlexSystem1ItemClass(index, flexClass) {
    if (currentConfig.items[index]) {
        currentConfig.items[index].flexClass = flexClass;
        updatePreview();
        updateCode();
    }
}

// Update flex system 1 item content
function updateFlexSystem1ItemContent(index, content) {
    if (currentConfig.items[index]) {
        currentConfig.items[index].content = content;
        updatePreview();
        updateCode();
    }
}

// Special handlers for Flex System 2 (percentage-based)
function updateFlexSystem2Columns(numColumns) {
    const num = parseInt(numColumns);
    currentConfig.numColumns = num;

    // Adjust columns array based on number
    while (currentConfig.columns.length < num) {
        const index = currentConfig.columns.length + 1;
        const defaultWidth = num === 2 ? 'c50' : num === 3 ? 'c33' : 'c25';
        currentConfig.columns.push({
            width: defaultWidth,
            content: `<h3>Column ${index}</h3>\n<p>Content for column ${index} goes here.</p>`
        });
    }

    while (currentConfig.columns.length > num) {
        currentConfig.columns.pop();
    }

    updateControls();
    updatePreview();
    updateCode();
}

// Update flex system 2 column width
function updateFlexSystem2ColumnWidth(index, width) {
    if (currentConfig.columns[index]) {
        currentConfig.columns[index].width = width;
        updatePreview();
        updateCode();
    }
}

// Update flex system 2 column content
function updateFlexSystem2ColumnContent(index, content) {
    if (currentConfig.columns[index]) {
        currentConfig.columns[index].content = content;
        updatePreview();
        updateCode();
    }
}

// Update the preview
function updatePreview() {
    const previewContainer = document.getElementById('componentPreview');
    let html = '';
    
    switch(currentComponent) {
        case 'box':
            if (currentConfig.hasIcon) {
                html = `
                    <div class="box box-icon">
                        <i class="${currentConfig.icon}"></i>
                        <div>
                            <h3 class="box__title">${currentConfig.title}</h3>
                            <p>${currentConfig.content}</p>
                        </div>
                    </div>
                `;
            } else {
                html = `
                    <div class="box">
                        <h3 class="box__title">${currentConfig.title}</h3>
                        <p>${currentConfig.content}</p>
                    </div>
                `;
            }
            break;
            
        case 'card':
            const cardClasses = ['card'];
            if (currentConfig.clickable) cardClasses.push('card--clickable');
            
            html = `
                <div class="${cardClasses.join(' ')}">
                    ${currentConfig.imageUrl ? `<div class="card__image"><img src="${currentConfig.imageUrl}" alt="${currentConfig.title}"></div>` : ''}
                    <div class="card__content">
                        <h3 class="card__heading">${currentConfig.title}</h3>
                        <p class="card__description">${currentConfig.content}</p>
                        <a href="${currentConfig.linkUrl}" class="card__link">${currentConfig.linkText}</a>
                    </div>
                </div>
            `;
            break;
            
        case 'button':
            const buttonClasses = ['button'];
            if (currentConfig.style === 'outline') buttonClasses.push('button--outline');
            if (currentConfig.size === 'small') buttonClasses.push('button--small');
            if (currentConfig.block) buttonClasses.push('button--block');
            
            html = `<a href="${escapeHtml(currentConfig.url)}" class="${buttonClasses.join(' ')}">${escapeHtml(currentConfig.text)}</a>`;
            break;
            
        case 'callout':
            const calloutAttr = currentConfig.emoji ? ` emoji-data="${currentConfig.emoji}"` : '';
            html = `
                <div class="callout ${currentConfig.type}"${calloutAttr}>
                    <h4>${currentConfig.title}</h4>
                    <p>${currentConfig.content}</p>
                </div>
            `;
            break;
            
        case 'accordion':
            html = `
                <details class="details">
                    <summary class="details__summary">${currentConfig.title}</summary>
                    <div class="details__text">
                        <p>${currentConfig.content}</p>
                    </div>
                </details>
            `;
            break;
            
        case 'alert':
            html = `
                <div class="alert alert-${currentConfig.type}">
                    <p>${currentConfig.content}</p>
                </div>
            `;
            break;
            
        case 'quote':
            html = `
                <blockquote class="quote">
                    <p>${currentConfig.content}</p>
                    <footer class="quote__author">
                        <cite>${currentConfig.author}</cite>
                        <span class="quote__role">${currentConfig.role}</span>
                    </footer>
                </blockquote>
            `;
            break;
            
        case 'dosdonts':
            html = `
                <div class="dosdonts">
                    <h3>${currentConfig.title}</h3>
                    <ul class="dosdonts__list">
                        ${currentConfig.items.map((item, i) => `
                            <li class="dosdonts__item dosdonts__item--${currentConfig.types[i]}">
                                ${item}
                            </li>
                        `).join('')}
                    </ul>
                </div>
            `;
            break;

        case 'flexSystem1':
            const flex1Classes = ['flex'];
            if (currentConfig.direction !== 'row') {
                flex1Classes.push(`flex-${currentConfig.direction}`);
            }
            // Add wrap class
            if (currentConfig.wrap === 'wrap') {
                flex1Classes.push('flex-wrap');
            } else if (currentConfig.wrap === 'nowrap') {
                flex1Classes.push('flex-no-wrap');
            } else if (currentConfig.wrap === 'wrap-reverse') {
                flex1Classes.push('flex-wrap-reverse');
            }
            if (currentConfig.alignItems !== 'stretch') {
                if (currentConfig.alignItems === 'center') {
                    flex1Classes.push('flex-center-y');
                }
            }
            if (currentConfig.justifyContent !== 'flex-start') {
                if (currentConfig.justifyContent === 'center') {
                    flex1Classes.push('flex-center-x');
                }
            }

            html = `
                <div class="${flex1Classes.join(' ')}" style="align-items: ${currentConfig.alignItems}; justify-content: ${currentConfig.justifyContent};">
                    ${currentConfig.items.map(item => `
                        <div class="${item.flexClass}">
                            ${item.content}
                        </div>
                    `).join('')}
                </div>
            `;
            break;

        case 'flexSystem2':
            const flex2Classes = ['flexContainer'];
            if (currentConfig.direction !== 'row') {
                flex2Classes.push(`flex-${currentConfig.direction}`);
            }
            // Add wrap class
            if (currentConfig.wrap === 'wrap') {
                flex2Classes.push('flex-wrap');
            } else if (currentConfig.wrap === 'nowrap') {
                flex2Classes.push('flex-no-wrap');
            } else if (currentConfig.wrap === 'wrap-reverse') {
                flex2Classes.push('flex-wrap-reverse');
            }
            if (currentConfig.alignItems !== 'stretch') {
                if (currentConfig.alignItems === 'center') {
                    flex2Classes.push('flex-center-y');
                }
            }
            if (currentConfig.justifyContent !== 'flex-start') {
                if (currentConfig.justifyContent === 'center') {
                    flex2Classes.push('flex-center-x');
                }
            }

            html = `
                <div class="${flex2Classes.join(' ')}" style="align-items: ${currentConfig.alignItems}; justify-content: ${currentConfig.justifyContent};">
                    ${currentConfig.columns.map(col => `
                        <div class="flexItem ${col.width}">
                            ${col.content}
                        </div>
                    `).join('')}
                </div>
            `;
            break;
    }

    previewContainer.innerHTML = html;
}

// Update the generated code
function updateCode() {
    const codeContainer = document.getElementById('generatedCode');
    let html = '';
    
    switch(currentComponent) {
        case 'box':
            if (currentConfig.hasIcon) {
                html = `<div class="box box-icon">
  <i class="${currentConfig.icon}"></i>
  <div>
    <h3 class="box__title">${escapeHtml(currentConfig.title)}</h3>
    <p>${escapeHtml(currentConfig.content)}</p>
  </div>
</div>`;
            } else {
                html = `<div class="box">
  <h3 class="box__title">${escapeHtml(currentConfig.title)}</h3>
  <p>${escapeHtml(currentConfig.content)}</p>
</div>`;
            }
            break;
            
        case 'card':
            const cardClasses = ['card'];
            if (currentConfig.clickable) cardClasses.push('card--clickable');
            
            html = `<div class="${cardClasses.join(' ')}">`;
            if (currentConfig.imageUrl) {
                html += `\n  <div class="card__image">
    <img src="${escapeHtml(currentConfig.imageUrl)}" alt="${escapeHtml(currentConfig.title)}">
  </div>`;
            }
            html += `\n  <div class="card__content">
    <h3 class="card__heading">${escapeHtml(currentConfig.title)}</h3>
    <p class="card__description">${escapeHtml(currentConfig.content)}</p>
    <a href="${escapeHtml(currentConfig.linkUrl)}" class="card__link">${escapeHtml(currentConfig.linkText)}</a>
  </div>
</div>`;
            break;
            
        case 'button':
            const buttonClasses = ['button'];
            if (currentConfig.style === 'outline') buttonClasses.push('button--outline');
            if (currentConfig.size === 'small') buttonClasses.push('button--small');
            if (currentConfig.block) buttonClasses.push('button--block');
            
            html = `<a href="${escapeHtml(currentConfig.url)}" class="${buttonClasses.join(' ')}">${escapeHtml(currentConfig.text)}</a>`;
            break;
            
        case 'callout':
            const calloutAttr = currentConfig.emoji ? ` emoji-data="${currentConfig.emoji}"` : '';
            html = `<div class="callout ${currentConfig.type}"${calloutAttr}>
  <h4>${escapeHtml(currentConfig.title)}</h4>
  <p>${escapeHtml(currentConfig.content)}</p>
</div>`;
            break;
            
        case 'accordion':
            html = `<details class="details">
  <summary class="details__summary">${escapeHtml(currentConfig.title)}</summary>
  <div class="details__text">
    <p>${escapeHtml(currentConfig.content)}</p>
  </div>
</details>`;
            break;
            
        case 'alert':
            html = `<div class="alert alert-${currentConfig.type}">
  <p>${escapeHtml(currentConfig.content)}</p>
</div>`;
            break;
            
        case 'quote':
            html = `<blockquote class="quote">
  <p>${escapeHtml(currentConfig.content)}</p>
  <footer class="quote__author">
    <cite>${escapeHtml(currentConfig.author)}</cite>
    <span class="quote__role">${escapeHtml(currentConfig.role)}</span>
  </footer>
</blockquote>`;
            break;
            
        case 'dosdonts':
            html = `<div class="dosdonts">
  <h3>${escapeHtml(currentConfig.title)}</h3>
  <ul class="dosdonts__list">
${currentConfig.items.map((item, i) => `    <li class="dosdonts__item dosdonts__item--${currentConfig.types[i]}">${escapeHtml(item)}</li>`).join('\n')}
  </ul>
</div>`;
            break;

        case 'flexSystem1':
            const flex1CodeClasses = ['flex'];
            if (currentConfig.direction !== 'row') {
                flex1CodeClasses.push(`flex-${currentConfig.direction}`);
            }
            // Add wrap class
            if (currentConfig.wrap === 'wrap') {
                flex1CodeClasses.push('flex-wrap');
            } else if (currentConfig.wrap === 'nowrap') {
                flex1CodeClasses.push('flex-no-wrap');
            } else if (currentConfig.wrap === 'wrap-reverse') {
                flex1CodeClasses.push('flex-wrap-reverse');
            }
            if (currentConfig.alignItems !== 'stretch') {
                if (currentConfig.alignItems === 'center') {
                    flex1CodeClasses.push('flex-center-y');
                }
            }
            if (currentConfig.justifyContent !== 'flex-start') {
                if (currentConfig.justifyContent === 'center') {
                    flex1CodeClasses.push('flex-center-x');
                }
            }

            const style1Attr = [];
            if (currentConfig.alignItems !== 'stretch' && currentConfig.alignItems !== 'center') {
                style1Attr.push(`align-items: ${currentConfig.alignItems}`);
            }
            if (currentConfig.justifyContent !== 'flex-start' && currentConfig.justifyContent !== 'center') {
                style1Attr.push(`justify-content: ${currentConfig.justifyContent}`);
            }
            const style1String = style1Attr.length > 0 ? ` style="${style1Attr.join('; ')}"` : '';

            html = `<div class="${flex1CodeClasses.join(' ')}"${style1String}>
${currentConfig.items.map(item => `  <div class="${item.flexClass}">
    ${escapeHtml(item.content).replace(/\n/g, '\n    ')}
  </div>`).join('\n')}
</div>`;
            break;

        case 'flexSystem2':
            const flex2CodeClasses = ['flexContainer'];
            if (currentConfig.direction !== 'row') {
                flex2CodeClasses.push(`flex-${currentConfig.direction}`);
            }
            // Add wrap class
            if (currentConfig.wrap === 'wrap') {
                flex2CodeClasses.push('flex-wrap');
            } else if (currentConfig.wrap === 'nowrap') {
                flex2CodeClasses.push('flex-no-wrap');
            } else if (currentConfig.wrap === 'wrap-reverse') {
                flex2CodeClasses.push('flex-wrap-reverse');
            }
            if (currentConfig.alignItems !== 'stretch') {
                if (currentConfig.alignItems === 'center') {
                    flex2CodeClasses.push('flex-center-y');
                }
            }
            if (currentConfig.justifyContent !== 'flex-start') {
                if (currentConfig.justifyContent === 'center') {
                    flex2CodeClasses.push('flex-center-x');
                }
            }

            const style2Attr = [];
            if (currentConfig.alignItems !== 'stretch' && currentConfig.alignItems !== 'center') {
                style2Attr.push(`align-items: ${currentConfig.alignItems}`);
            }
            if (currentConfig.justifyContent !== 'flex-start' && currentConfig.justifyContent !== 'center') {
                style2Attr.push(`justify-content: ${currentConfig.justifyContent}`);
            }
            const style2String = style2Attr.length > 0 ? ` style="${style2Attr.join('; ')}"` : '';

            html = `<div class="${flex2CodeClasses.join(' ')}"${style2String}>
${currentConfig.columns.map(col => `  <div class="flexItem ${col.width}">
    ${escapeHtml(col.content).replace(/\n/g, '\n    ')}
  </div>`).join('\n')}
</div>`;
            break;
    }

    codeContainer.textContent = html;

    // Re-run Prism syntax highlighting
    if (window.Prism) {
        Prism.highlightElement(codeContainer);
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Generate icon picker HTML
function generateIconPicker() {
    let html = '<input type="text" class="icon-search" placeholder="Search icons..." onkeyup="filterIcons(this.value)">';
    html += '<div class="icon-picker" id="iconGrid">';
    
    Object.entries(iconCategories).forEach(([category, icons]) => {
        html += `<div class="icon-category">
            <div class="icon-category-title">${category}</div>
            <div class="icon-category-grid">`;
        
        icons.forEach(icon => {
            html += `<div class="icon-option" data-icon="${icon.class}" title="${icon.name}" onclick="selectIcon('${icon.class}')">
                <i class="${icon.class}"></i>
            </div>`;
        });
        
        html += '</div></div>';
    });
    
    html += '</div>';
    return html;
}

// Select an icon from the picker
function selectIcon(iconClass) {
    try {
        currentConfig.icon = iconClass;
        const iconInput = document.getElementById('boxIcon');
        if (iconInput) {
            iconInput.value = iconClass;
        }
        
        // Update visual selection
        document.querySelectorAll('.icon-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        const selectedIcon = document.querySelector(`[data-icon="${iconClass}"]`);
        if (selectedIcon) {
            selectedIcon.classList.add('selected');
        }
        
        updatePreview();
        updateCode();
    } catch (error) {
        console.error('Error selecting icon:', error);
    }
}

// Filter icons based on search
function filterIcons(searchTerm) {
    try {
        const categories = document.querySelectorAll('.icon-category');
        
        if (!searchTerm) {
            searchTerm = '';
        }
        searchTerm = searchTerm.toLowerCase();
        
        categories.forEach(category => {
            const categoryIcons = category.querySelectorAll('.icon-option');
            let hasVisibleIcons = false;
            
            categoryIcons.forEach(icon => {
                const iconName = icon.getAttribute('title')?.toLowerCase() || '';
                const iconClass = icon.getAttribute('data-icon')?.toLowerCase() || '';
                
                if (iconName.includes(searchTerm) || iconClass.includes(searchTerm)) {
                    icon.style.display = 'flex';
                    hasVisibleIcons = true;
                } else {
                    icon.style.display = 'none';
                }
            });
            
            category.style.display = hasVisibleIcons ? 'block' : 'none';
        });
    } catch (error) {
        console.error('Error filtering icons:', error);
    }
}

// Handle component type change
document.addEventListener('DOMContentLoaded', function() {
    const componentSelector = document.getElementById('componentType');
    componentSelector.addEventListener('change', function() {
        currentComponent = this.value;
        currentConfig = JSON.parse(JSON.stringify(componentConfigs[currentComponent]));
        updateControls();
        updatePreview();
        updateCode();
    });

    init();
});

// Copy to clipboard function
function copyToClipboard() {
    try {
        const codeElement = document.getElementById('generatedCode');
        if (!codeElement) {
            console.error('Code element not found');
            return;
        }
        
        const code = codeElement.textContent;
        const button = document.querySelector('.copy-button');
        
        if (!button) {
            console.error('Copy button not found');
            return;
        }
        
        navigator.clipboard.writeText(code).then(function() {
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
                button.innerHTML = originalText;
            }, 2000);
        }).catch(function(error) {
            console.log('Clipboard API failed, using fallback:', error);
            // Fallback for older browsers
            try {
                const textArea = document.createElement('textarea');
                textArea.value = code;
                textArea.style.position = 'fixed';
                textArea.style.opacity = '0';
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    button.innerHTML = originalText;
                }, 2000);
            } catch (fallbackError) {
                console.error('Copy fallback failed:', fallbackError);
                alert('Copy failed. Please manually select and copy the code.');
            }
        });
    } catch (error) {
        console.error('Error in copyToClipboard:', error);
    }
}