+++
name = "card"
title = "Cards"
lead = "A card groups a heading, a short description and an optional image into one block."
group = "layout"
status = "current"
related = []
scss = ["scss/components/_cards.scss"]

[parts]
card = "The container: a white block with a thin border."
card__content = "Wraps the text and adds the padding."
card__heading = "The card title. It is smaller than a page heading."
card__metadata = "An optional line for a category, a length or similar."
card__description = "The card's short text."
card__link = "A link in the heading that stretches over the whole card, so the entire card is clickable."

[[examples]]
label = "Basic card"
purpose = "A heading and a short description"
html = '''
<div class="card">
  <div class="card__content">
    <h3 class="card__heading">Card title</h3>
    <p class="card__description">A short description of what the card is about.</p>
  </div>
</div>
'''

[[examples]]
class = "card__image"
label = "With an image"
purpose = "An image at the top, cropped to a widescreen shape. Put card__image on the img element"
html = '''
<div class="card">
  <img class="card__image" alt="A short description of the image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 4 3'%3E%3Crect width='4' height='3' fill='%23ccc'/%3E%3C/svg%3E">
  <div class="card__content">
    <h3 class="card__heading">Card with an image</h3>
    <p class="card__metadata">Category &bull; 5 min read</p>
    <p class="card__description">A card can also have a line of metadata above its description.</p>
  </div>
</div>
'''

[[examples]]
class = "card--clickable"
label = "Clickable"
purpose = "A card that is one link: the whole card is clickable, an arrow sits at the bottom right, and on hover it gets a shadow and its image zooms"
html = '''
<div class="card card--clickable">
  <img class="card__image" alt="A short description of the image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 4 3'%3E%3Crect width='4' height='3' fill='%23ccc'/%3E%3C/svg%3E">
  <div class="card__content">
    <h3 class="card__heading"><a href="https://example.org" class="card__link">Clickable card</a></h3>
    <p class="card__metadata">Online course &bull; 12 weeks</p>
    <p class="card__description">Select anywhere on the card to follow the link.</p>
  </div>
</div>
'''
+++

## When to use it

Use a card to group a heading, a short description and, if you have one, an image into a block the reader can scan. A clickable card turns the whole block into one link.

## When not to use it

A card is not for long text. It holds a heading, a short description and an optional image. Put longer text in the page itself.

## How to use it

Put the heading and the description inside `card__content`. Put `card__image` on the `img` element for a picture: it is cropped to a widescreen shape. For a card that is one link, add `card--clickable` and put the link in the heading with `card__link`. The link stretches over the whole card, so the whole card is clickable.

### Do

- Use a heading for the card title, and put the description under it.
- Give every card image alt text that describes it.
- Put the link in the heading when the whole card is one link.
- Replace the placeholder image in an example with your own.

### Don't

- Put long paragraphs in a card.
- Add `card--clickable` without a `card__link`. The hover effects and the arrow appear, but there is nothing to select.

## Accessibility

- In a clickable card the title is a real link inside a heading, so keyboard and screen reader users reach it as a link.
- Give each image alt text. An image that adds nothing can have an empty `alt=""`.
- The shadow and the image zoom appear only on hover, so they cannot be what tells the reader a card is a link. The arrow and the title do that.
