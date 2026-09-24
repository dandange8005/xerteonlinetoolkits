# Cardiff University Theme

A Xerte Bootstrap site theme following the Cardiff Resource Design System v1.7.
It provides generated design tokens, 18px reading copy, a white header, charcoal page
navigation, section navigation, horizontal rules and seven callout types. The wider
component migration is still in progress; see [migration status](MIGRATION.md).

This is a prototype design system, not an approved institutional brand standard.
Accessibility checks and their limits are summarised in [migration status](MIGRATION.md);
the theme alone does not establish accessibility conformance for authored content.

## Layout

This folder is the development source. It is never deployed.

```
themes/site/cardiffuniversity/     runtime: the only files Xerte loads
  cardiffuniversity.info           name, display name, preview
  cardiffuniversity.css            compiled from scss/ by build.sh
  cardiffuniversity.js             sticky-menu offset and scrollspy
  cardiffuniversity.jpg            theme picker preview
  logo_left.svg                    default left logo
theme-src/cardiffuniversity/       this folder: tokens/, scss/, demos/, tests/, tools/, build.sh
```

Xerte copies the whole theme folder into every project export, so keep anything else
out of the runtime folder.

## Use the theme

1. Run `./build.sh package` and upload `dist/cardiffuniversity.zip`, or copy
   `themes/site/cardiffuniversity/` into Xerte's `themes/site/` directory.
2. Select **Cardiff University Theme** in the site's theme settings.
3. Use the [author guide](demos/index.html) for supported classes and copyable examples.

Compiled CSS ships with the theme. Recompile only when changing SCSS.
The player also requests `cardiffuniversity.js`: it measures the sticky menu, updates scrollspy
and corrects section landings while content loads. Keep the script with the stylesheet.

For a callout, paste this into a Text element's Source view:

```html
<div class="cu-callout cu-callout-tip">
  <strong class="cu-callout-title">Tip</strong>
  <p>Explain the recommendation here.</p>
</div>
```

The icon is drawn by CSS using the player's Font Awesome. The older `fa-stack` markup
is still supported. The old `.callout` classes are not this theme's callout API.

## Maintain the theme

- [Theming guide](THEMING-GUIDE.md): source ownership, overrides and build commands.
- [Migration status](MIGRATION.md): current state and outstanding work.

`scss/_cu-tokens.scss` is generated from `tokens/tokens.json` by `tools/build-tokens.py`. Theme aliases live
in `scss/_allvariables.scss`, alongside Xerte-only settings. The former `_tokens.scss`
scale has been removed; shared values have one source. Layout and component rules live
in the other SCSS modules.
Compile with `./build.sh`, which writes the runtime CSS without a source map, and commit it. `tools/build-reference.py`
generates the marked reference region in the author guide.

To restyle the theme for a project or another brand, see the [theming page](demos/theming.html)
in the author guide. Browser validation to date is recorded for Chrome on macOS; broader
browser coverage remains to be established.

## Credits and licence

Author: Dan Dange ([@dandange8005](https://github.com/dandange8005)), Cardiff University Digital Education.
Based on Xerte Online Toolkits Bootstrap Sites. For internal Cardiff University use,
as recorded in the original theme README.
