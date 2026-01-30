## Old project structure

Google Fonts
Custom Properties
XERTE GENERAL FIXES
Typography
Header and Footer
Base
media
layout
    flex
    grid    
jquery ui
    buttons
    accordion
    tab


## XOT Theme Document

This document outlines the folder structure of XOT Sass folder structure

XOT SASS Structure
XOT/
    xot_main.scss
    
    /abstract
        _openProps.scss
        _xibit.scss
    /base
        _index.scss
        _customProperties.scss
        _overall-reset.scss
        _xot-reset.scss
        _header.scss
        _footer.scss
        _base.scss
    /components
        _index.scss
        _forms.scss
    /layouts
        _index.scss
        _contentMenu.scss
        _flex.scss
        _grid.scss
    /pages
        _index.scss
        _titlePage.scss
        _graphicPage.scss
        _mediaPage.scss
        _navigatorsPage.scss
        _quizPage.scss
        _textPage.scss
    /utility
        _utilityClass.scss
    /vendors
        _index.scss
        _jquery-ui.scss


sass/
|
|– base/
|   |– _reset.scss       # Reset/normalize
|   |– _typography.scss  # Typography rules
|   ...                  # Etc…
|
|– components/
|   |– _buttons.scss     # Buttons
|   |– _carousel.scss    # Carousel
|   |– _cover.scss       # Cover
|   |– _dropdown.scss    # Dropdown
|   ...                  # Etc…
|
|– layout/
|   |– _navigation.scss  # Navigation
|   |– _grid.scss        # Grid system
|   |– _header.scss      # Header
|   |– _footer.scss      # Footer
|   |– _sidebar.scss     # Sidebar
|   |– _forms.scss       # Forms
|   ...                  # Etc…
|
|– pages/
|   |– _home.scss        # Home specific styles
|   |– _contact.scss     # Contact specific styles
|   ...                  # Etc…
|
|– themes/
|   |– _theme.scss       # Default theme
|   |– _admin.scss       # Admin theme
|   ...                  # Etc…
|
|– utils/
|   |– _variables.scss   # Sass Variables
|   |– _functions.scss   # Sass Functions
|   |– _mixins.scss      # Sass Mixins
|   |– _helpers.scss     # Class & placeholders helpers
|
|– vendors/
|   |– _bootstrap.scss   # Bootstrap
|   |– _jquery-ui.scss   # jQuery UI
|   ...                  # Etc…
|
|
`– main.scss             # Main Sass file


## Using comments
