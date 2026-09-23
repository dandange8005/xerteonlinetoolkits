# Supporting assets, secondary buttons, the theming page and the last Bootstrap components

Implemented 23 September 2026. Closes five items on the
[follow-up checklist](../plans/2026-09-21-follow-up.md); decisions by Nan on the same day.

## Secondary buttons: names documented, styles unchanged

The design system's secondary button is white with charcoal text and a 1px charcoal border,
turning `surface` on hover. The theme's `.button-secondary` is a filled black button that predates
the design system; its `.button-secondary-outline` already matches the design system's secondary.

Decision: keep both classes as they are and document the mapping (option A), so no published
content changes appearance. The mapping is in the header comment of `components/_buttons.scss`,
in the Filled and Outline button descriptions on the Components page, and in that page's usage
guidelines (which had called outline buttons "tertiary").

## Preview image

`cardiffuni-v3.jpg` was the original `cardiffuni` theme's screenshot, copied unchanged into v2 and
v3 (2838 × 1896, 304 KB). It is now a screenshot of the author guide's Components page, opened on
the callouts: white header, charcoal navbar with the current-page marker, side menu with the
selected item, and callouts. 805 × 635 like the other Xerte site themes' previews, 80 KB. It was
taken in headless Chrome from the guide, not from a real project.

## Medr override removed

`themes/medr-theme.css` was written for cardiffuni-v2. v3 still read 91 of its 116 variables, but
it set none of the roles v3's red elements use (`--cu-red`, `--cu-action`), so under it the header
edge, navbar marker, primary button and feedback tab would have stayed Cardiff red beside Medr
green. It is removed from v3; v2 keeps its own copy. The new theming page (below) shows how a
project would restyle v3.

## cardiff-design.json removed

Nothing in Xerte, the player or the theme reads it. It was the January v1.0.0 design-system
extraction (from the School of Medicine CPD site), superseded by the design system's
`v1/tokens.css` and identical to v2's copy, which stays. The README and theming guide no longer
mention it.

## Theming page (`demos/theming.html`)

A new author-guide page, last in the navigation:

- **About Theming**: the `--cu-*` roles, the alias layer and why an override at `:root` reaches
  old and new components.
- **Where Overrides Go**: the Xerte project's optional *Styles* (pasted CSS) and *Stylesheet*
  (uploaded file) properties. The player loads both after the theme (`application.js`: theme CSS,
  then the stylesheet, then the inline styles). Two worked examples: a blue brand (`--cu-red`,
  `--cu-action`, `--cu-action-hover`; white on the action colour is 7.23:1) and larger reading
  copy with rounder controls (`--cu-text-body`, `--cu-radius`).
- **Try a Variant**: buttons that apply either example to the whole page through
  `:root[data-theme="…"]`, so the header edge, navbar marker, side-menu rule, buttons and fields
  change live. The Warning callout in the preview stays Cardiff red, to show what does not follow.
- **Roles You Can Override**: the table from the theming guide.
- **What Theming Does Not Change**: logos; error, Warning and chart colours (they read the
  palette's `--cu-brand-red` family, not `--cu-red`); part-of-page overrides; built-in variants
  (none ship); rebranding for another institution.

The Colors page's old "Creating a New Theme" block, which overrode `--color-brand-primary` and put
`[data-theme]` on any element, now points to the new page instead.

**Navigation.** With twelve pages the menu bar wrapped at 1200px, so "Images, Media & Icons" is
now "Media & Icons" in the nav and footers (the page title is unchanged). The menu bar still
wraps between 980px and 1199px, as it already did with eleven pages.

## Wells, lead text and carousel controls (`_bootstrap-components.scss`)

Compared side by side (a private comparison page with contrast figures and focusable carousel
controls); Nan chose the recommended option for each.

| Component | Before | After |
| --- | --- | --- |
| `.well` | Forest Green fill with ink text (4.05:1), Bootstrap's 4px corners and inset shadow | `--cu-surface` grey with ink text (16.73:1); no border, square, no shadow. Coloured emphasis belongs to the callouts |
| `.lead` | Up to 24px, weight 300, grey-60 (3.95:1, failing below 24px), line height 1.2 | DESIGN.md §3: `--cu-text-lead` (20px), regular weight, `--cu-leading-lead` (1.55), `--cu-muted` (5.74:1) |
| `.carousel-control` | 40px circle, grey-80 at 80% opacity, blur, drop shadow; grows and darkens on hover | DESIGN.md §4 icon-only control: 48px square (`--btn-min-height`), white fill, 1px `--cu-border`, 24px ink chevron (`--cu-text-icon`), no shadow; hover is the surface fill. Keyboard focus is a white ring inside an ink ring, so it shows on light and dark slides |

The carousel indicators and caption keep their translucent overlay colours. The Bootstrap page now
has Pills, Panels, Wells, Lead Text and Carousel examples in the player's own markup, and the three
demo pages that set `.lead` sizes and colours inline no longer do, so they show the theme's lead.

**Pills in a section.** The player puts a Navigator page's pills inside a section, where the base
list rule padded each pill 8px to the right, the same fault fixed for breadcrumbs. `ul.nav-pills > li`
now sets `padding-left: 0`.

**Still open: the panel label.** Panels take their frame and corner label from the player's
`custom.css`: 4px corners, a `#ddd` border, and a `#9DA0A4` label on `#F5F5F5`, which is 2.41:1.
The theme only sets the padding. Fixing the label needs a decision and is on the checklist.

## Verification

- 279 automated checks pass (270 before): 8 `bootstrap` checks for the well, lead text and carousel controls, all failing before, and 1 for the pill indent, failing before.
- The generated reference is in sync, no theme class is undocumented, and every nav link, footer
  link and section anchor in the guide resolves (twelve nav links on every page).
- The theming page was rendered with the blue variant applied: the header edge, navbar marker and
  side-menu rule turn blue and the logo does not change.

Not verified: the variant buttons in a real browser by hand, and the preview image inside the
Xerte theme picker.
