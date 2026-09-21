# Cardiff University v3 theming guide

The current design-system baseline is v1.4. Read [migration status](MIGRATION.md) before
extending unfinished components, and use the [author guide](demos/index.html) for HTML examples.

## Source ownership

| Source | Responsibility |
| --- | --- |
| Design-system `DESIGN.md` | Colour roles, typography and component intent |
| Design-system `v1/tokens.css` | Canonical `--cu-*` tokens |
| `scss/_cu-tokens.scss` | Generated copy at `:root`; do not edit directly |
| `scss/_allvariables.scss` | Compatibility aliases to shared roles, plus Xerte-only component settings |
| Other `scss/` modules | Xerte layout and component implementation |

The design-system folder lives in the vault under
`10 Projects 📋/11 Work Projects/🎨 Cardiff University Design System/design-system/`.
For shared token changes, edit its source and run its `sync-theme.py`, then compile the theme.
Do not substitute `cardiff-design.json` for that source; it is a legacy asset awaiting review.

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
Design-system v1/tokens.css
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
| Brand marks | `--cu-red` |
| Primary action and hover | `--cu-action`, `--cu-action-hover` |
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
review its full palette and role mapping. Do not change Cardiff's canonical source or its
generated copy just to recolour that fork. Brand marks, action, error and callout roles are
separate decisions, so changing `--cu-red` alone is not a complete rebrand. Cardiff logos
and other identity assets also need replacing. Alternate brands and dark mode are not
validated features of this migration.

For shared Cardiff changes, update the canonical design-system source and regenerate it.
The theme does not redefine `--cu-*` values in its adapter. The default fonts remain system
and Franklin Gothic fallback stacks, with no web-font fetch.

## Build and checks

Run from this folder:

```bash
npx -y sass@1 cardiffuni-v3.scss cardiffuni-v3.css --source-map
python3 tests/check_theme.py
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

Commit both compiled CSS and the source map with SCSS changes. Regenerate the reference
after changes that affect it. Hard-refresh the Docker player to inspect the result.

## Adding a component

Add its SCSS module under `scss/components/`, import it from `_custom-components.scss`,
and provide an example in the author guide. Use existing roles rather than inventing new
colour values. Check keyboard focus, narrow widths, zoom, long labels and editor save/reopen
behaviour where applicable. Keep project-specific interactive patterns in project code unless
there is an explicit decision to make them shared theme features.

Record player and export results in `docs/test-rounds/`, including browser, date and any
untested paths. Follow [the release checklist](docs/plans/2026-09-21-follow-up.md) for the
remaining migration and sign-off work.
