# Cardiff University theming guide

The current design-system baseline is v1.7. Read [migration status](MIGRATION.md) before
extending unfinished components, and use the [author guide](demos/index.html) for HTML examples.

## Source ownership

| Source | Responsibility |
| --- | --- |
| `tokens/tokens.json` | The theme's `--cu-*` tokens: the source of truth for this theme |
| `scss/_cu-tokens.scss` | Generated from `tokens.json` by `tools/build-tokens.py`; do not edit directly |
| `scss/_allvariables.scss` | The two brand colours, compatibility aliases to shared roles, and Xerte-only component settings |
| Other `scss/` modules | Xerte layout and component implementation |

To change a token, edit `tokens/tokens.json` and run `./build.sh`. A value in braces, such as
`{cu-white}`, refers to another token; the build stops if the target does not exist.

The tokens were seeded on 24 September 2026 from the Cardiff Resource Design System v1.7
(`v1/tokens.css` in the vault's design-system folder) and are now maintained here, separately,
so the theme can differ from the design system where Xerte needs it. Nothing syncs the two
automatically: when the design system changes, decide what the theme should adopt and edit
`tokens.json` by hand.

## Restyle the brand

A project that only needs its own colours sets two values, in the project's *Styles* property
(pasted CSS) or its *Stylesheet* property (an uploaded file). The player loads both after the
theme.

```css
:root {
  --color-brand-primary: #00703C;   /* main brand colour */
  --color-brand-secondary: #1D2B4F; /* dark supporting colour */
}
```

| Colour | What follows it | Cardiff default |
| --- | --- | --- |
| `--color-brand-primary` | Header top edge, navbar current-page marker, the rule under a navbar placed below the header, side-menu selected rule and wash, `.text-brand`, `.bg-brand`. Through the action shades: primary and primary-outline buttons, the feedback tab | Cardiff red (`--cu-red`) |
| `--color-brand-secondary` | Navbar and its hover and current-page fill, footer, secondary and secondary-outline buttons, `.bg-dark`, tab underline and pills, the default progress bar, back-to-top button, Do/Don't labels | Ink (`--cu-ink`) |

These do not follow the brand: body text and headings (always ink), focus rings, links,
fields, error red and the required-field asterisk, the Warning callout, charts, the skip link,
glossary tip, reverse and ghost button text, inverse and warning badges, and logos.

The action shades are mixed from the primary: 85% and 70.5% of it with black for the button
and its hover, and a 17% tint with white for the outline-button hover. The navbar's hover
and current-page fill is the secondary with 14% white. For Cardiff these land on the design
system's values (the action reds one step off in the blue channel: `#C21F17` and `#A11A13`
against `#C21F16` and `#A11A12`).

Check contrast before publishing:

- White text on the darker primary (the button) needs 4.5:1. A light brand colour such as a
  yellow will not reach it; set `--color-action` and `--color-action-hover` yourself.
- White navbar text on the secondary, and on the secondary with 14% white, needs 4.5:1, and
  the footer's grey-30 text needs 4.5:1 on the secondary. Choose a dark secondary.
- Pill and secondary-outline text in the secondary needs 4.5:1 on white, and the tab underline
  and the progress bar need 3:1 against white and the grey progress track.
- The primary as a 4px edge or marker needs 3:1 against white or the navbar.

`--cu-red` still works as an override, because the brand primary reads it by default, but
`--color-brand-primary` is the supported name. Overriding `--cu-action` no longer reaches the
buttons: they follow the brand primary.

## Project overrides

Load project CSS after the theme. New rules should use semantic `--cu-*` roles:

```css
.project-note {
  color: var(--cu-ink);
  background: var(--cu-surface);
  border-left: 4px solid var(--cu-border);
  padding: var(--cu-space-6);
}
```

For a project-wide adjustment, override the shared role **once at `:root`**, after the
theme. Existing aliases follow it automatically:

```css
:root {
  --cu-body: system-ui, sans-serif;
  --cu-text-body: 19px;
}
```

This updates reading copy through `--font-size-body` as well as any new rules that use
`--cu-text-body` directly. You do not need to redeclare `--font-family-primary` or
`--font-size-body`. Apply the same approach to shared spacing, heading sizes, weights,
control radius, shadows and motion roles.

```text
tokens/tokens.json
    → generated _cu-tokens.scss (--cu-* roles)
        → newer theme rules
        → _allvariables.scss (existing names) → existing components
```

`_tokens.scss` has been removed: it had no genuine Sass-only consumers. Its shared values
are now aliases; settings without a shared role live directly in `_allvariables.scss`.
These include intermediate utility weights, extra line-height steps, structural zero radii,
border widths, control dimensions, z-indexes and the existing outline-button tint.
Component geometry is not automatically a spacing role just because its number matches one.

| To change | Override at `:root` |
| --- | --- |
| Brand colours | `--color-brand-primary`, `--color-brand-secondary` (see [Restyle the brand](#restyle-the-brand)) |
| Primary action and hover, when the derived shades fail contrast | `--color-action`, `--color-action-hover` |
| Reading copy and font | `--cu-text-body`, `--cu-body` |
| Display, section and component headings | `--cu-text-display`, `--cu-text-section`, `--cu-text-component` |
| Shared spacing step | `--cu-space-4`, etc. |
| Control corners | `--cu-radius` (structural panels remain square) |
| Overlay shadow | `--cu-shadow-lg`, etc. |
| Fast motion | `--cu-fast`, `--cu-ease` |
| Xerte-only focus geometry | `--focus-ring-width`, `--focus-ring-offset` |

Existing local overrides of names such as `--font-size-body` still work for their existing
consumers. Prefer the shared roles when the change should reach both old and new components.
Subtree theme switching is not this adapter's supported workflow: inherited aliases resolve
where declared, so a subtree override can need additional local alias declarations.
For an optional page-wide variant, use `:root[data-theme="variant-name"]` and set that
attribute on `<html>`; a `data-theme` attribute alone does not activate any built-in variant.

To create another institution's theme, fork the theme, provide a separate token source and
review its full palette and role mapping. Do not change Cardiff's `tokens.json` or its
generated partial just to recolour that fork. Brand colours, error, callout and chart roles are
separate decisions, so changing the two brand colours alone is not a complete rebrand. Cardiff logos
and other identity assets also need replacing. Alternate brands and dark mode are not
validated features of this migration.

For shared Cardiff changes, update `tokens/tokens.json` and rebuild.
The theme does not redefine `--cu-*` values in its adapter. The default fonts remain system
and Franklin Gothic fallback stacks, with no web-font fetch.

### Header colourways

By default the header is white and the navbar is ink with a red rule underneath. A project can
switch to one of the colourways below by pasting its snippet into the project's **Styles**
property (in the editor, open the project's top-level properties and add the optional
Styles property). The player adds these styles after the theme, so they override the
defaults for that project only. The red rule appears only when the navbar sits below the header.

| Token | Default | Controls |
| --- | --- | --- |
| `--color-header-bg`, `--color-header-text`, `--color-header-subtext`, `--color-header-border` | white, ink, muted grey, border grey | The header behind the logo, title and subtitle |
| `--color-navbar-bg`, `--color-navbar-text` | ink, white | The navbar |
| `--color-navbar-item-hover` | grey-90 | Hover and current-page fill |
| `--color-navbar-rule` | brand red | The 4px rule under the navbar |
| `--color-navbar-focus` | white | The keyboard focus ring on navbar items |

**Light grey nav** (white header, light grey navbar with black text and rule):

```css
:root {
  --color-navbar-bg: #E6E6E6;
  --color-navbar-item-hover: #FFFFFF;
  --color-navbar-text: #121212;
  --color-navbar-rule: #121212;
  --color-navbar-focus: #121212;
}
```

**Charcoal header** (charcoal header above the default ink navbar and red rule):

```css
:root {
  --color-header-bg: #1F1F1F;
  --color-header-text: #FFFFFF;
  --color-header-subtext: #C8C8C8;
  --color-header-border: #1F1F1F;
}
```

**Charcoal header, light nav** (a mix of the two, with the red rule kept):

```css
:root {
  --color-header-bg: #1F1F1F;
  --color-header-text: #FFFFFF;
  --color-header-subtext: #C8C8C8;
  --color-header-border: #1F1F1F;
  --color-navbar-bg: #E6E6E6;
  --color-navbar-item-hover: #FFFFFF;
  --color-navbar-text: #121212;
  --color-navbar-focus: #121212;
}
```

Every colourway keeps text at 4.5:1 or better against its background. If you choose other
colours, check the contrast yourself.

## Build and checks

Run from this folder (`theme-src/cardiffuniversity/`):

```bash
./build.sh              # tokens.json -> _cu-tokens.scss, then compile into themes/site/cardiffuniversity/
./build.sh package      # compile and zip the runtime folder into dist/ for upload
python3 tests/check_theme.py
python3 tools/build-tokens.py --check
python3 tools/build-reference.py
python3 tools/build-reference.py --check
python3 tools/build-reference.py --coverage
git diff --check
```

The Chrome runner defaults to macOS Google Chrome. Set `CHROME` to another Chrome binary
when needed. Named groups such as `focus`, `headings` and `stickynav` can be passed to the
runner for focused checks. The fixture uses selected player styles and a jQuery/scrollspy
stub; it does not replace a test in the real player. Resize observer delivery is explicitly
triggered in the fixture to avoid virtual-time rendering ambiguity; native delivery still
needs a real-player check. Coverage currently counts class mentions
as well as examples, so a clean coverage report is not proof that every class is demonstrated.

Commit the compiled CSS with SCSS changes. No source map is built: the runtime folder ships
only what Xerte loads, because the player copies the whole theme folder into every export. Regenerate the reference
after changes that affect it. Hard-refresh the Docker player to inspect the result.

## Adding a component

Add its SCSS module under `scss/components/`, import it from `_custom-components.scss`,
and provide an example in the author guide. Use existing roles rather than inventing new
colour values. Check keyboard focus, narrow widths, zoom, long labels and editor save/reopen
behaviour where applicable. Keep project-specific interactive patterns in project code unless
there is an explicit decision to make them shared theme features.

Record player and export results in the commit message or [migration status](MIGRATION.md),
including browser, date and any untested paths. [Migration status](MIGRATION.md) lists the
remaining work.
