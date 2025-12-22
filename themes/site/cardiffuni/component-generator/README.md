# Xerte Component Generator

A visual tool for creating and customizing HTML components for Xerte Online Toolkits projects. This app allows users to select components, customize their properties, see live previews, and generate copy-ready HTML code.

## 📁 Project Structure

```
Apps/component-generator/
├── component-generator.html     # Main application file
├── component-generator.css      # Styles using Open Props design tokens
├── component-generator.js       # Application logic and functionality
└── README.md                   # This documentation
```

## 🚀 Features

### **Component Library**
- **8 Component Types**: Box, Card, Button, Callout, Accordion, Alert, Quote, Dos & Don'ts
- **Live Preview**: Real-time component rendering with your CSS themes
- **Visual Icon Picker**: 32+ categorized Font Awesome icons with search functionality
- **Form Controls**: Dynamic settings panels for each component type

### **User Interface**
- **Two-Column Layout**: 40% controls, 60% preview/code
- **Modern Toggle Switches**: Professional iOS/Material Design style toggles
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Cardiff University Branding**: Uses official colors and typography

### **Code Generation**
- **Syntax Highlighting**: Professional dark theme using Prism.js
- **Code Wrapping**: No horizontal overflow, proper line wrapping
- **Copy to Clipboard**: One-click copying with visual feedback
- **Clean HTML Output**: Properly formatted, indented code

## 🛠️ Technical Implementation

### **Architecture**
- **Vanilla JavaScript**: No frameworks, lightweight and fast
- **Open Props Design Tokens**: Consistent spacing, typography, and colors
- **Modular CSS**: Organized styles with semantic class names
- **Error Handling**: Comprehensive try-catch blocks and null checks

### **Design System**
- **CSS Custom Properties**: Cardiff University brand colors
- **Open Props Integration**: Semantic design tokens for spacing and typography
- **Responsive Grid**: CSS Grid layout with proper breakpoints
- **Accessibility**: Proper focus states, keyboard navigation, screen reader support

## 📋 Component Types & Features

### 1. **Box Component**
- **Features**: Title, content, optional icon
- **Controls**: Text inputs, toggle for icon inclusion, visual icon picker
- **Output**: Simple content container with optional Font Awesome icon

### 2. **Card Component**
- **Features**: Title, content, image, link, clickable option
- **Controls**: Text inputs, URL fields, clickable toggle
- **Output**: Card layout with optional image and call-to-action

### 3. **Button Component**
- **Features**: Multiple styles (primary, outline), sizes, block option
- **Controls**: Text input, style/size dropdowns, block toggle
- **Output**: Styled button following Cardiff University design system

### 4. **Callout Component**
- **Features**: Title, content, type (warning, success, danger, info), custom emoji
- **Controls**: Text inputs, type dropdown, emoji input
- **Output**: Alert-style callout with visual indicators

### 5. **Accordion Component**
- **Features**: Collapsible content with summary and details
- **Controls**: Summary text, hidden content textarea
- **Output**: HTML5 details/summary accordion

### 6. **Alert Component**
- **Features**: System notifications with different types
- **Controls**: Content textarea, type dropdown
- **Output**: Alert component with Font Awesome icons

### 7. **Quote Component**
- **Features**: Quote text with author attribution
- **Controls**: Quote content, author name, role/title
- **Output**: Blockquote with citation and role

### 8. **Dos and Don'ts Component**
- **Features**: Educational lists with visual indicators
- **Controls**: Multi-line textarea with DO:/DON'T: prefixes
- **Output**: List with checkmarks and crosses

## 🎨 Visual Icon Picker

### **Icon Categories**
- **Information** (8 icons): Info, question, warning, check, etc.
- **Learning** (8 icons): Book, graduation cap, teacher, certificate, etc.
- **Actions** (8 icons): Download, upload, play, search, settings, etc.
- **Communication** (8 icons): Email, phone, comments, bell, etc.

### **Features**
- **Visual Grid**: 45x45px icon preview boxes
- **Search Functionality**: Real-time filtering by name or CSS class
- **Click to Select**: Visual feedback with accent color highlighting
- **Tooltip Names**: Hover to see icon names

## 💻 Code Features

### **Syntax Highlighting**
- **Theme**: Prism Tomorrow (professional dark theme)
- **Language**: HTML with proper token highlighting
- **Line Numbers**: Optional line numbering for reference
- **Code Wrapping**: No horizontal scroll, text wraps properly

### **Generated HTML**
- **Clean Output**: Properly indented, semantic HTML
- **Escaped Content**: User input is safely escaped
- **Consistent Formatting**: 2-space indentation, proper line breaks
- **Copy Ready**: Can be directly pasted into Xerte projects

## 🔧 Installation & Setup

### **Requirements**
- Modern web browser with JavaScript enabled
- Internet connection for external dependencies:
  - Font Awesome 5.15.4
  - Prism.js 1.29.0
  - Open Props design tokens

### **File Dependencies**
```html
<!-- Main Xerte CSS -->
<link rel="stylesheet" href="../../css/bs_main.min.css">

<!-- External Dependencies -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.css">

<!-- Application Styles -->
<link rel="stylesheet" href="component-generator.css">
```

### **Usage**
1. Open `component-generator.html` in a web browser
2. Select a component type from the dropdown
3. Customize properties using the form controls
4. Preview the component in real-time
5. Copy the generated HTML code
6. Paste into your Xerte project

## 🎯 Design Decisions

### **Layout Choice: 40/60 Split**
- **Left Column (40%)**: Component selection and settings
- **Right Column (60%)**: Preview and code generation
- **Reasoning**: More space for preview and code, compact controls

### **Open Props Integration**
- **Benefits**: Consistent design tokens, maintainable CSS, semantic spacing
- **Tokens Used**: `--size-*` for spacing, `--font-*` for typography, `--gray-*` for colors
- **Custom Properties**: Cardiff University brand colors preserved

### **Error Handling Strategy**
- **Try-Catch Blocks**: Around all major functions to prevent crashes
- **Null Checks**: Before DOM manipulation to avoid errors
- **Console Logging**: For debugging and development insight
- **Graceful Fallbacks**: Alternative methods when primary approaches fail

## 🐛 Debugging & Troubleshooting

### **Common Issues**
1. **Mouse Freezing/Unresponsive Interface**
   - Check browser console for JavaScript errors
   - Ensure all external dependencies load successfully
   - Clear browser cache and reload

2. **Icons Not Displaying**
   - Verify Font Awesome CDN connection
   - Check for ad blockers blocking external resources
   - Ensure proper internet connection

3. **Code Not Highlighting**
   - Check Prism.js CDN resources
   - Verify language class is properly set
   - Check console for Prism initialization errors

### **Debug Mode**
- Open browser console (F12) to see initialization logs
- Look for error messages in console
- Check Network tab for failed resource loads

## 🚀 Future Enhancements

### **Potential Features**
1. **More Components**: Tables, forms, media players, navigation elements
2. **Theme Switching**: Toggle between Bootstrap, XOT, and Bristol themes
3. **Save/Load**: Local storage for component configurations
4. **Export Options**: Multiple format outputs (React, Vue, etc.)
5. **Component Library**: Pre-built component templates
6. **Accessibility Checker**: Built-in a11y validation
7. **CSS Custom Properties**: Live theme color customization

### **Technical Improvements**
1. **TypeScript**: Type safety and better developer experience
2. **Build Process**: Bundling, minification, optimization
3. **Testing**: Unit tests for component generation
4. **PWA**: Offline functionality and app installation
5. **API Integration**: Save components to cloud storage

## 📖 Code Examples

### **Adding a New Component**
```javascript
// 1. Add to componentConfigs
componentConfigs.newComponent = {
    title: 'Default Title',
    content: 'Default content'
};

// 2. Add to updateControls() switch statement
case 'newComponent':
    controlsHTML = `
        <div class="form-group">
            <label for="newTitle">Title</label>
            <input type="text" id="newTitle" value="${config.title}" 
                   onchange="updateConfig('title', this.value)">
        </div>
    `;
    break;

// 3. Add to updatePreview() switch statement
case 'newComponent':
    html = `<div class="new-component">
        <h3>${currentConfig.title}</h3>
        <p>${currentConfig.content}</p>
    </div>`;
    break;

// 4. Add to updateCode() switch statement
case 'newComponent':
    html = `<div class="new-component">
  <h3>${escapeHtml(currentConfig.title)}</h3>
  <p>${escapeHtml(currentConfig.content)}</p>
</div>`;
    break;
```

### **Adding New Icons**
```javascript
// Add to iconCategories object
iconCategories['New Category'] = [
    { class: 'fas fa-new-icon', name: 'New Icon' },
    { class: 'fas fa-another-icon', name: 'Another Icon' }
];
```

## 📄 License & Credits

### **Dependencies**
- **Font Awesome**: Icons (Free license)
- **Prism.js**: Syntax highlighting (MIT license)
- **Open Props**: Design tokens (MIT license)

### **Cardiff University**
- Brand colors and typography guidelines
- Franklin Gothic font family usage

### **Development**
Built with assistance from Claude Code (Anthropic) for Cardiff University's Xerte Online Toolkits theme system.

---

## 📞 Support

For questions, issues, or contributions to this component generator, please refer to the main Xerte Themes project documentation and Cardiff University's learning technology team.