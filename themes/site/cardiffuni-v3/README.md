# Cardiff University Theme v3

A Xerte Bootstrap site theme following the Cardiff Resource Design System v1.7.
It provides generated design tokens, 18px reading copy, a white header, charcoal page
navigation, section navigation, horizontal rules and seven callout types. The wider
component migration is still in progress; see [migration status](MIGRATION.md).

This is a prototype design system, not an approved institutional brand standard.
Accessibility checks and their limits are recorded in the [test rounds](docs/test-rounds/2026-09-phase1.md);
the theme alone does not establish accessibility conformance for authored content.

## Use the theme

1. Install the whole `cardiffuni-v3` folder in Xerte's `themes/site/` directory.
2. Select **Cardiff University v3** in the site's theme settings.
3. Use the [author guide](demos/index.html) for supported classes and copyable examples.

Compiled CSS ships with the theme. Recompile only when changing SCSS.
The player also requests `cardiffuni-v3.js`: it measures the sticky menu, updates scrollspy
and corrects section landings while content loads. Keep the script with the stylesheet.

For a callout, paste this into a Text element's Source view:

```html
<div class="cu-callout cu-callout-tip">
  <strong class="cu-callout-title">Tip</strong>
  <p>Explain the recommendation here.</p>
</div>
```

The icon is drawn by CSS using the player's Font Awesome. The older `fa-stack` markup
is still supported. The old `.callout` classes are not the v3 callout API.

## Maintain the theme

- [Theming guide](THEMING-GUIDE.md): source ownership, overrides and build commands.
- [Follow-up checklist](docs/plans/2026-09-21-follow-up.md): outstanding work and validation.
- [Branch review](docs/reviews/2026-09-20-final-branch-review.md): findings and disposition.

`scss/_cu-tokens.scss` is generated from the external design system. Theme aliases live
in `scss/_allvariables.scss`, alongside Xerte-only settings. The former `_tokens.scss`
scale has been removed; shared values have one source. Layout and component rules live
in the other SCSS modules.
Commit `cardiffuni-v3.css` and its source map after compiling. `tools/build-reference.py`
generates the marked reference region in the author guide.

The preview image, Medr override and `cardiff-design.json` still need review; the JSON
file is not the canonical token source. Browser validation to date is recorded for Chrome
on macOS; broader browser coverage remains to be established.

## Credits and licence

Author: Dan Dange ([@dandange8005](https://github.com/dandange8005)), Cardiff University Digital Education.
Based on Xerte Online Toolkits Bootstrap Sites. For internal Cardiff University use,
as recorded in the original theme README.
