# Cardiff University Theme

A theme for Xerte's Bootstrap site template, following the Cardiff Resource Design System, and
the author guide that teaches content authors how to use it.

## Language

### Xerte

**Xerte page**:
A page a content author builds in a Xerte site project. It holds one or more sections.
_Avoid_: page (on its own), site page

**Section**:
A part of a Xerte page with its own title and entry in the section menu. It holds content items.

**Text content item**:
The content item in a section that holds rich text, and the place where a content author pastes
an example's HTML through the Source view.
_Avoid_: Text element, text block, Text Snippet (a different Xerte field)

**Player**:
The Xerte software that shows a finished Xerte page to its readers.
_Avoid_: viewer, runtime

**Page frame**:
The parts of a Xerte page that the player draws around the content: the header and logos, the
navbar, the section menu, the footer, the feedback tab, the back-to-top button and the glossary
tip. A content author sets these in Xerte rather than pasting them.
_Avoid_: page chrome, chrome

### Theme

**Theme**:
The Cardiff University Theme: the stylesheet, script and images Xerte loads for a site project.
_Avoid_: skin, template (a Xerte template is a different thing)

**Design system**:
The Cardiff Resource Design System, the reference the theme follows. It is a working profile, not
an approved institutional brand standard.
_Avoid_: brand guidelines, brand standard

**Brand colours**:
The primary and secondary colours that restyle every brand-coloured part of the theme, and that a
project can override.

**Colourway**:
A per-project choice of colours for the header and the navbar.
_Avoid_: theme variant, skin

**Theme class**:
A class the theme adds beyond Bootstrap, Xerte's own styles and Font Awesome.

**Author-facing class**:
A theme class a content author may put in their content: every theme class except legacy classes
and those belonging to the page frame.

**Legacy class**:
A theme class kept so older content keeps working, which the author guide does not teach.
_Avoid_: deprecated class, old class

**Utility class**:
A single-purpose author-facing class, such as a spacing or alignment class, taught in a generated
table rather than on a component page.
_Avoid_: helper class

### Author guide

**Content author**:
A person who builds Xerte pages with the theme.
_Avoid_: user (in Xerte, a user is an account with roles), editor

**Author guide**:
The hosted website that teaches content authors what the theme offers and how to use it.
_Avoid_: user manual, demos, style guide, documentation site

**Demo pages**:
The older hand-written pages that showed the theme's classes, which the author guide replaces.
_Avoid_: author guide

**Guide page**:
Any page of the author guide.
_Avoid_: page (on its own)

**Task**:
A job a content author wants to do, such as drawing attention to something, which the author guide
answers with one guide page.
_Avoid_: how-to, recipe

**Component**:
A reusable piece of theme markup that a content author pastes into a text content item, such as a
callout, a button or a card.
_Avoid_: element, block, widget

**Variant**:
One of the alternative looks of a component, chosen by its variant class, such as the Tip callout
or an outline button.
_Avoid_: type, style, modifier

**Part**:
A class inside a component that is not a variant, such as the callout title.
_Avoid_: sub-element, child class

**Example**:
A piece of a component's HTML that the author guide shows both rendered and as code to copy.
_Avoid_: snippet (clashes with Xerte's Text Snippet), demo, sample

**Component record**:
The single source of everything the author guide says about one component: its variants, parts,
examples, advice and editor evidence.
_Avoid_: component file, component doc

**Editor evidence**:
A dated record of whether a component's examples survive the Xerte editor, and in which Xerte
version.
_Avoid_: editor check

**Reference page**:
A guide page generated from the theme itself, such as the colours, the tokens or the utility
classes.

**Drift**:
Any place where the author guide says something the theme no longer does, or the theme offers
something the author guide does not cover.
