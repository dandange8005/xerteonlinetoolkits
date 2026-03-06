# GitHub Issue Draft
## For: thexerteproject/xerteonlinetoolkits

---

## Title

**Accessibility themes do not override explicit heading colours set in project custom CSS (`lo_css`)**

---

## Summary

When a user applies a custom stylesheet via the project **Styles** field (stored as `x_params.styles` and injected as `<style id="lo_css">`), any explicit `color` rules on heading elements (`h1`–`h6`) persist when an accessibility theme (Dark mode, High contrast, Light mode, Black on yellow) is activated. This means headings remain in the project's brand colour instead of switching to the accessibility theme's appropriate colour, which can result in poor or failing contrast ratios.

---

## Steps to Reproduce

1. Create or open any Xerte project using the Nottingham template family (XOT1 or similar).
2. In project properties → **Styles**, add a CSS rule that explicitly sets a heading colour, for example:
   ```css
   h1, h2, h3, h4 { color: #0f6b99; }
   ```
3. Publish and open the project at `play.php?template_id=...`
4. Open the Accessibility Options panel (footer icon).
5. Select **Dark mode**, **High contrast**, **Light mode**, or **Black on yellow**.

**Expected:** Headings update to the appropriate colour for the selected theme (e.g. `#E0E0E0` in dark mode, `#ffffff` in high contrast).

**Actual:** Headings remain in the custom project colour (`#0f6b99`), which has insufficient contrast against the accessibility theme's background.

---

## Root Cause

There are two related issues working together.

### Issue 1 — Accessibility theme CSS files do not set explicit heading colours

All four accessibility theme CSS files set `body { color }` and `p { color }` but do **not** set an explicit `color` on `h1`–`h6`. They rely on inheritance from `body`:

| File | `body color` | `p color` | `h1–h6 color` |
|------|-------------|-----------|--------------|
| `darkmode.css` | `#E0E0E0` | `#E0E0E0` | *(not set — relies on inherit)* |
| `highcontrast.css` | `#ffffff` | `#ffffff` | *(not set — relies on inherit)* |
| `lightmode.css` | `#121212` | `#121212` | *(not set — relies on inherit)* |
| `blackonyellow.css` | `#000000` | `#000000` | *(not set — relies on inherit)* |

In CSS, **any explicit `color` rule on an element — regardless of specificity or source order — always overrides an inherited value**. Therefore, if `custom.css` contains `h1 { color: #0f6b99 }`, that rule wins over the inherited `#E0E0E0` from `body { color: #E0E0E0 }` in darkmode.css, even though darkmode.css loads later in the DOM.

This is a standard CSS cascade rule, not a browser bug:

```
Explicit rule (any specificity) > Inherited value
```

`p` works correctly in accessibility modes because `p { color }` is set explicitly in each theme file, giving it a direct rule that matches the same specificity as a project's `p { color }` rule — at which point source order (darkmode.css loads after `lo_css`) decides the winner.

Headings lack this same explicit rule.

**Affected files (all under `themes/Nottingham/`):**
```
darkmode/darkmode.css        — h1, h2, h3 blocks missing color property
highcontrast/highcontrast.css — h1, h2, h3 blocks missing color property
lightmode/lightmode.css      — h1, h2, h3 blocks missing color property
blackonyellow/blackonyellow.css — h1, h2, h3 blocks missing color property
```

---

### Issue 2 — `#lo_css` is not disabled when an accessibility theme is activated

`xenith.js` contains the function `disableBespokeCSS()`, which is called whenever the user switches accessibility theme. It disables `#customHeaderStyle` but does **not** disable `#lo_css` (the inline project styles) for non-xhibit themes:

```javascript
// xenith.js ~ line 7261
function disableBespokeCSS() {
    $("#customHeaderStyle").prop('disabled', XENITH.ACCESSIBILITY.specialTheme !== false);

    // disable xhibit stylesheets when accessibility theme is in use as otherwise the footer buttons icons are messed up
    // perhaps we should always do this (not just for xhibit) & possibly also for #lo_css (css added via styles optional property)
    if (x_params.theme == "xhibit") {
        $("#lo_sheet_css").prop('disabled', XENITH.ACCESSIBILITY.specialTheme !== false);
    }
}
```

The comment in the source code (`"perhaps we should always do this... & possibly also for #lo_css"`) suggests this was a known incomplete area. Because `#lo_css` remains active, all project custom styles — including colour overrides — persist during accessibility mode, compounding the heading colour issue described above.

---

## Proposed Fix

### Fix 1 — Add explicit heading colour to all accessibility theme CSS files (minimal change)

In each accessibility theme file, add `color` to the existing `h1`–`h3` rules and add `h4`–`h6`:

**`darkmode.css`:**
```css
h1 { font-size: 1em;   margin: 0;           color: #E0E0E0; }
h2 { font-size: 1.2em; margin: 5px 0 0 0;   color: #E0E0E0; }
h3 { font-size: 1.2em; margin: 0;            color: #E0E0E0; }
h4, h5, h6 {                                 color: #E0E0E0; }
```

**`highcontrast.css`:**
```css
h1, h2, h3, h4, h5, h6 { color: #ffffff; }
```

**`lightmode.css`:**
```css
h1, h2, h3, h4, h5, h6 { color: #121212; }
```

**`blackonyellow.css`:**
```css
h1, h2, h3, h4, h5, h6 { color: #000000; }
```

This mirrors what is already done for `p { color }` in each file and is consistent with the existing pattern.

---

### Fix 2 — Disable `#lo_css` when an accessibility theme is active (more complete fix)

Extend `disableBespokeCSS()` in `xenith.js` to disable `#lo_css` when any accessibility theme is active, not just for the xhibit theme. This would fully isolate project custom styles from accessibility modes:

```javascript
function disableBespokeCSS() {
    const specialThemeActive = XENITH.ACCESSIBILITY.specialTheme !== false;
    $("#customHeaderStyle").prop('disabled', specialThemeActive);
    $("#lo_css").prop('disabled', specialThemeActive);           // <-- add this
    // keep the existing xhibit-specific lo_sheet_css handling
    if (x_params.theme == "xhibit") {
        $("#lo_sheet_css").prop('disabled', specialThemeActive);
    }
}
```

**Note:** This is the more complete fix and would resolve all colour conflicts (not just headings) between project custom CSS and accessibility themes. It should be tested to confirm it does not break any other functionality (e.g. structural layout CSS in `lo_css` that accessibility themes rely on).

Fix 1 is lower risk and can be shipped independently. Fix 2 is more comprehensive but requires broader testing.

---

## Environment

- Xerte version: `3.14 - unstable (installed from github)`
- Template family: Nottingham (XOT1)
- Browser: tested in Chrome
- Affected themes: `darkmode`, `highcontrast`, `lightmode`, `blackonyellow`

---

## Additional Context

This issue was discovered while applying a project-scoped custom stylesheet to a Xerte XOT1-based learning resource. The custom CSS used brand accent colours on headings (`color: #0f6b99`), which remained visible in dark mode against a `#121212` background — a contrast ratio of approximately 3.3:1, below the WCAG 2.2 AA threshold of 4.5:1 for normal text and technically borderline for large text.

Project authors who follow the Xerte documentation guidance of using the Styles field for custom CSS currently have no pure-CSS workaround for this issue, as CSS provides no mechanism to make an explicit rule yield to an inherited value.

---

*Prepared by: Nan Zhang, Cardiff University*
*Date: 2026-03-06*
*Reference: `PROJECTS/xerte-custom-css-guide.md` in local Xerte instance*
