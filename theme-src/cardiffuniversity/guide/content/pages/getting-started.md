+++
name = "getting-started"
title = "Getting started"
lead = "Switch a Xerte site project to the Cardiff University Theme, then set its logos and colours."
+++

## Choose the theme

1. Open your site project in the Xerte editor.
2. Open the project's top-level properties.
3. Set **Theme** to **Cardiff University Theme**.
4. Preview the project to check the new look.

## Logos

The header shows a logo on the left by default. Use the **Left Logo** and **Right Logo** properties to change the logos:

- **File** sets the image.
- **Description** is the logo's text for screen readers. Fill it in for every logo.
- **Hide Default Logo** removes that side's default logo.

## Brand colours

The theme uses two brand colours. To change them for one project, add the optional **Styles** property to the project's top-level properties and paste:

```css
:root {
  --color-brand-primary: #00703C;   /* main brand colour */
  --color-brand-secondary: #1D2B4F; /* dark supporting colour */
}
```

Change the two values to your colours. Then check the contrast: white text on a button in your primary colour needs a ratio of at least 4.5:1, and so does white navbar text on your secondary colour.

## Header colourways

By default the header is white and the navbar is ink with a red rule underneath. To switch one project to another colourway, paste one of these into its **Styles** property.

### Light grey nav

```css
:root {
  --color-navbar-bg: #E6E6E6;
  --color-navbar-item-hover: #FFFFFF;
  --color-navbar-text: #121212;
  --color-navbar-rule: #121212;
  --color-navbar-focus: #121212;
}
```

### Charcoal header

```css
:root {
  --color-header-bg: #1F1F1F;
  --color-header-text: #FFFFFF;
  --color-header-subtext: #C8C8C8;
  --color-header-border: #1F1F1F;
}
```

### Charcoal header, light nav

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

Every colourway keeps text at 4.5:1 or better against its background. If you choose other colours, check the contrast yourself.

## The page frame

The player draws the page frame around your content: the header and logos, the navbar, the section menu, the footer, the feedback tab, the back-to-top button and the glossary tip. You set these in the project's properties in Xerte. You do not paste them into a Text content item, so the guide has no component pages for them.
