+++
name = "button"
title = "Buttons"
lead = "A button starts an action or takes the reader to a clear next step."
group = "interaction"
status = "current"
related = []
scss = ["scss/components/_buttons.scss"]

[parts]
button = "The base class every button needs. It gives the button its shape, size and states."
button__icon = "An optional wrapper for an icon inside a button."
btn-mini = "A small round icon button, kept for older content. The player uses it for the back-to-top button, and the theme restyles that."

[[examples]]
class = "button-primary"
label = "Primary"
purpose = "The main action on the page"
html = '''
<a href="https://example.org" class="button button-primary">Continue</a>
'''

[[examples]]
class = "button-secondary-outline"
label = "Secondary"
purpose = "The design system's secondary button. Pair it with one primary button"
html = '''
<a href="https://example.org" class="button button-secondary-outline">Back</a>
'''

[[examples]]
class = "button-secondary"
label = "Filled black"
purpose = "A filled black button that predates the design system, kept for existing content"
html = '''
<a href="https://example.org" class="button button-secondary">Filled black</a>
'''

[[examples]]
class = "button-success"
label = "Success"
purpose = "A filled button in the success colour"
html = '''
<a href="https://example.org" class="button button-success">Success</a>
'''

[[examples]]
class = "button-primary-outline"
label = "Primary outline"
purpose = "An outlined version of the primary button"
html = '''
<a href="https://example.org" class="button button-primary-outline">Primary outline</a>
'''

[[examples]]
class = "button-success-outline"
label = "Success outline"
purpose = "An outlined version of the success button"
html = '''
<a href="https://example.org" class="button button-success-outline">Success outline</a>
'''

[[examples]]
class = "button-ghost"
label = "Ghost"
purpose = "A button with no fill or border. A light grey background appears on hover"
html = '''
<a href="https://example.org" class="button button-ghost">Ghost</a>
'''

[[examples]]
class = "button-reverse"
label = "Reverse"
purpose = "A filled button for dark backgrounds"
html = '''
<div class="bg-dark p-4">
  <a href="https://example.org" class="button button-reverse">Reverse</a>
</div>
'''

[[examples]]
class = "button-reverse-outline"
label = "Reverse outline"
purpose = "An outlined button for dark backgrounds"
html = '''
<div class="bg-dark p-4">
  <a href="https://example.org" class="button button-reverse-outline">Reverse outline</a>
</div>
'''

[[examples]]
class = "button-sm"
label = "Small"
purpose = "A smaller button. Its text is 14px, below the design system's 16px minimum for buttons"
html = '''
<a href="https://example.org" class="button button-primary button-sm">Small</a>
'''

[[examples]]
class = "button-lg"
label = "Large"
purpose = "A larger button"
html = '''
<a href="https://example.org" class="button button-primary button-lg">Large</a>
'''

[[examples]]
class = "button--block"
label = "Block (older)"
purpose = "A button that fills the width of its container. An older class, kept for older content"
html = '''
<a href="https://example.org" class="button button-primary button--block">Block</a>
'''

[[examples]]
class = "button-icon-left"
label = "Icon on the left"
purpose = "An icon before the label"
html = '''
<a href="https://example.org" class="button button-primary button-icon-left">
  <i class="fa-solid fa-arrow-left" aria-hidden="true"></i> Previous
</a>
'''

[[examples]]
class = "button-icon-right"
label = "Icon on the right"
purpose = "An icon after the label"
html = '''
<a href="https://example.org" class="button button-primary button-icon-right">
  Next <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
</a>
'''

[[examples]]
class = "button-icon-only"
label = "Icon only"
purpose = "A square button with only an icon. It needs an aria-label"
html = '''
<a href="https://example.org" class="button button-primary button-icon-only" aria-label="Search">
  <i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>
</a>
'''
+++

## When to use it

Use a button to take the reader to a clear next step, or to start an action.

## When not to use it

For a link inside a sentence, use a normal text link. A button is for an action or a clear next step, not for running text.

## How to use it

The examples on this page are links with the button classes. A link looks the same as a button, and in a text content item it goes somewhere. A button element starts an action only when something else runs it, such as a script or a Bootstrap data attribute, so use one only for that.

### Do

- Use one primary button for the main action, and pair it with the secondary variant when the reader has a second choice.
- Use a link for a clear next step, and a button element only when something gives it an action.
- Use the reverse variants on dark backgrounds, and check that keyboard focus can be seen on them.
- Give an icon-only button an `aria-label` that says what it does.

### Don't

- Disable a button unless the action is really unavailable.
- Use the filled black variant for the design system's secondary button. Use the secondary variant instead.
- Use the older classes in new content.
- Add gradients, shadows or pill shapes.

## Accessibility

- Buttons with the `button` class are at least 48px high and 44px wide, so they are easy to hit on a touch screen. The older `btn-mini` is smaller.
- Keyboard focus shows a 2px outline in ink. On a dark background, including ink, that outline cannot be seen, so check the reverse variants when you use them.
- To disable a button element, use the `disabled` attribute, so it is also disabled for keyboard and screen reader users.
- Give an icon-only button an `aria-label`, and hide an icon that sits beside a visible label with `aria-hidden="true"`.
