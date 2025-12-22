# Customise Bootstrap Template

The LTA (Learning and Teaching Academy) Bootstrap theme is a customised version of the default Xerte Bootstrap template. It allows you create professional looking Xerte resources with a consistent look and feel.

The template is based on the [Bootstrap v2.3.2 framework](https://getbootstrap.com/2.3.2/) and uses the Bootstrap CSS and JavaScript files to provide a responsive layout and a range of interactive components.

The template has got everything you need out of the box, but it is possible to customise the template to suit your needs. This guide will show you how to download the template, apply it to your Xerte project and customise it to suit your needs.

## Typeface

The template uses system fonts for the body text and headings. This means that the text will be displayed in the font that the user has set as their default font in their browser. This is usually a sans-serif font such as Arial or Helvetica. This is a good thing as it means that the text will be displayed in a font that the user is familiar with and is easy to read. And it also means that they don't have to download any additional fonts to view the resource. In a way to make the resource more accessible.

```css
font-famly: system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif;
```

However, it doesn't mean you can't use other fonts in your resource to make it more exciting. For example, you can use the [Google Fonts](https://fonts.google.com/) service to import fonts into your resource. You can then use these fonts in your resource by setting the `font-family` property in your CSS.

For example, if you wanted to use the [Inter](https://fonts.google.com/specimen/Inter) font in your resource, you can do so by following these steps:

### Step 1: Import Google Fonts

1. Go to the [Inter](https://fonts.google.com/specimen/Inter) page on the Google Fonts website.
2. **Select** the font style you want to use. For example, the **Regular 400** style.
3. Go to the **Use on the web** tab.
4. Copy the `<link>` rule from the **Use on the web** tab.
5. Paste the `<link>` rule into the **Script** field in the tab in the Xerte editor.

### Step 2: Set the font family

The template uses css [custom properties]([https:](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)) to set the font family for the body text and headings. This means that you can easily change the font family for the whole resource by changing the custom property values in the `:root` selector.

1. Go to the **Styles** section in the Xerte editor.
2. Change the value of the `--ff-body` and `--ff-heading` properties to the name of the font you want to use. For example,

    ```css
    :root {
        --ff-body: 'Inter', sans-serif; /* This controls the font family for the content body */
        --ff-heading: 'Inter', sans-serif; /* This controls the font family for the headings */
    }
    ```
3. Preview and publish the changes.

### Accessibility considerations

Please note when choosing fonts for your resource, there are a number of accessibility considerations to take into account. These include:

- **Readability**: The font should be easy to read. It should be clear and legible.
- **Accessibility**: The font should be accessible. It should be easy to read for people with visual impairments.
- **Consistency**: The font should be consistent. It should be used consistently throughout the resource.
- **Availability**: The font should be available. It should be available on the device that the resource is being viewed on.
- **Performance**: The font should be performant. It should not affect the performance of the resource.

For more information on choosing fonts for your resource, please see the [Choosing Fonts](https://www.w3.org/WAI/tutorials/fonts/) tutorial on the W3C website.

## Colours

The template uses a range of colours to style the resource. Again, These colours are defined in the `:root` selector in the `css/style.css` file. Similar with the `font-family`, you can easily change the colours by changing the custom property values in the `:root` selector.


### Header Background gradient

The header background gradient is defined using the `--header-bg` custom property. This is a linear gradient that goes from the top to the bottom of the header. The gradient is made up of two colours. The first colour is the top colour and the second colour is the bottom colour. The gradient is defined using the `linear-gradient()` function. The first argument is the direction of the gradient. The second argument is the top colour. The third argument is the bottom colour.

```css
:root {
    --header-bg: linear-gradient(to bottom, #1e5799, #2989d8);
}
```

### Accent Colours

The accent colour is defined using the `--clr-accent` custom property. This is a single colour that is used to style a number of elements. For example, 

- The active state of the side menu items.
- The section titles.
- Buttons.


```css
:root {
--clr-accent: rgb(78,88,147);
}
```

To combine all the changes 

```css
:root {
    --ff-body: 'Inter', sans-serif; /* This controls the font family for the content body */
    --ff-heading: 'Inter', sans-serif; /* This controls the font family for the headings */
    --header-bg: linear-gradient(to bottom, #1e5799, #2989d8);
    --clr-accent: rgb(78,88,147);
}
```

## Additional customisable properties

The template also has a number of additional customisable properties that you can use to customise the template. These include:

## Open Props

The template includes [Open-props](https://openprops.org/) that allows you to create custom components with consistent tokens and properties. These components can then be used in your resource to create custom interactions. 

### Utility classes

The template includes a number of utility classes that you can use to style your content. These classes are defined in the `css/utility.css` file. 

