## Bootstrap SCSS Structure

This is my current structure.

```
Sass/
|- Assets/
|   |- fonts/                   # custom fonts
|   |- images/                  # image assets (logos, etc) 
|   |- icons/                   # svg icons
|   ...                         # other assets
|– base/
|   |– _reset.scss              # Reset/normalize
|   |– _accessibility.scss        # Typography rules
|   |– _typography.scss         # Typography rules
|   |– _base.scss               # Base elements
|   |– _customProperties.scss   # Custom properties
|   |– _colours.scss            # Colours
|   |– _openProps.scss          # OpenProps custom properties
|   |– _breakpoints.scss        # Breakpoints
|   |– _functions.scss          # Functions (optional)
|   |– _mixins.scss             # Mixins (optional)
|   |– _utilities.scss          # Utilities
|   |– _index.scss              # Index file
|   ...                         # Etc…
|- Components/
|   |– _buttons.scss            # Buttons
|   |– _carousel.scss           # Carousel
|   |– _cover.scss              # Cover
|   |– _dropdown.scss           # Dropdown
|   |– _forms.scss              # Forms (optional)
|   |– _callouts.scss           # Callouts
|   |– _cards.scss              # Cards
|   |– _checklist.scss          # Checklist
|   |– _details.scss            # Details
|   |– _dosAndDonts.scss        # Dos and Donts
|   |– _example.scss            # Example
|   |– _forms.scss              # Forms
|   |– _grid.scss               # Grid
|   |– _icons.scss              # Icons
|   |– _images.scss             # Images
|   |– _media.scss              # Media
|   |– _modals.scss             # Modals
|   |– _nav.scss                # Nav
|   |– _pagination.scss         # Pagination
|   |– _panels.scss             # Panels
|   |– _popovers.scss           # Popovers
|   |– _progress.scss           # Progress
|   |– _tables.scss             # Tables
|   |– _tabs.scss               # Tabs
|   |– _tooltips.scss           # Tooltips
|   |– _index.scss              # Index file
|   ...                         # Etc…
|- Layout/
|   |– _header.scss             # Header
|   |– _footer.scss             # Footer
|   |– _mainNav.scss            # Main Navigation
|   |– _sideNav.scss            # Side Navigation
|   |– _section.scss            # Section
|   |– _flex.scss               # Flex
|   |– _grid.scss               # Grid
|   |– _index.scss              # Index file
|   ...                         # Etc…
|- Templates/
|   |– _article.scss            # Article template
|   |– _wide.scss               # Wide template
|   |– _index.scss              # Index file
|   ...                         # Etc…
|- Vendors/
|   |– _bootstrap.scss          # Bootstrap
|   |– _prism.scss              # Prism
|   |– _jquery-ui.scss          # jQuery UI
|   ...                         # Etc…
|
`– bs_main.scss                    # Main Sass file
`_ bs_article.scss                 # Article Sass file
`_ bs_wide.scss                    # Wide Sass file

```

Suggested structure from [Sass Guidelines](https://sass-guidelin.es/#architecture)

```

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
```