# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About Xerte Online Toolkits

Xerte Online Toolkits is a PHP-based e-learning content creation platform that allows users to create interactive learning objects. This is the open-source version maintained by The Xerte Project.

## Development Commands

### Testing
- **PHP Unit Tests**: Download `phpunit.phar` and run:
  ```bash
  php phpunit.phar
  ```
  Configuration is in `tests/phpunit.xml`

### Build Commands (for Popcorn.js component)
The `src/popcorn-js` directory contains a JavaScript media framework with its own build system:
```bash
cd src/popcorn-js
make all          # Build all components
make check        # Run JSLint on all files
make lint         # Lint core popcorn.js
make clean        # Clean build artifacts
```

### Setup and Installation
- Initial setup wizard: Visit `/setup` in your web browser
- File system test: `setup/file_system_test.php`
- PHP modules test: `setup/php_modules_test.php`

## Architecture Overview

### Core Structure
- **Root PHP files**: Main application entry points (`index.php`, `play.php`, `edit.php`, etc.)
- **website_code/**: Core application logic and utilities
- **modules/**: Three main module types:
  - `xerte/`: Xerte-specific templates and functionality
  - `site/`: Site-building templates and functionality  
  - `decision/`: Decision tree templates and functionality
- **editor/**: Rich text and media editing functionality
- **library/**: Third-party libraries (Zend Framework, SAML2, etc.)

### Template System
Templates are located in `modules/{module_type}/parent_templates/` and define different content types that can be created. Each template includes:
- XML configuration files defining the template structure
- HTML/JavaScript files for rendering
- Icon and preview assets

### Key Directories
- **USER-FILES/**: User-generated content and uploads
- **themes/**: UI themes and styling
- **languages/**: Internationalization files
- **plugins/**: Plugin system for extensibility

### Database Integration
- Uses MySQL/MariaDB for data storage
- Configuration in `config.php` (from `config.php.dist`)
- Authentication systems support LDAP, SAML2, and database auth

### File Upload and Media
- **mediaViewer/**: Media file handling and viewing
- **import/**: Content import functionality  
- File upload security includes ClamAV virus scanning if available

## Configuration Files
- `config.php` - Main configuration (copy from `config.php.dist`)
- `auth_config.php` - Authentication settings
- `api_keys_dist.php` - API keys template

## Key Technologies
- **PHP 7.x+** with MySQL, XML, cURL, mbstring, and zip extensions
- **Apache** web server (with mod_rewrite recommended)
- **Popcorn.js** for multimedia timeline interactions
- **jQuery** and various JavaScript libraries
- **SAML2** authentication support via OneLogin library
- **Bootstrap 2.3.0** for the site template (located in `modules/site/parent_templates/site/common/`)

## Development Notes
- The codebase follows a modular architecture where functionality is separated into modules
- Templates define the structure and behavior of different content types
- The system supports multi-language internationalization
- File permissions are critical - USER-FILES and setup directories need write access during installation
- The application includes comprehensive setup wizards for initial configuration