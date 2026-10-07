+++
name = "callout"
title = "Callouts"
lead = "Pull one key idea out of the page with a short title and a few lines of text. The theme draws the icon."
group = "emphasis"
status = "current"
since = "v1.4"
tasks = ["draw-attention"]
related = []
scss = ["scss/components/_callout.scss"]

[editor]
survives = true
checked = 2026-09-20
xerte = "3.14"

[parts]
cu-callout = "The container. On its own it gives the Key point variant."
cu-callout-title = "The short bold title. Always say the variant in words."
cu-callout-icon = "Only for the older fa-stack icon markup, which still works. Leave it out of new callouts."

[[examples]]
class = "cu-callout-tip"
label = "Tip"
purpose = "A recommendation or shortcut"
html = '''
<div class="cu-callout cu-callout-tip">
  <strong class="cu-callout-title">Tip</strong>
  <p>Keep a callout to two or three lines so it stays easy to scan.</p>
</div>
'''

[[examples]]
class = "cu-callout-info"
label = "Information"
purpose = "Extra context that helps but is not essential"
html = '''
<div class="cu-callout cu-callout-info">
  <strong class="cu-callout-title">Information</strong>
  <p>Extra context.</p>
</div>
'''

[[examples]]
class = "cu-callout-good"
label = "Good practice"
purpose = "The preferred approach"
html = '''
<div class="cu-callout cu-callout-good">
  <strong class="cu-callout-title">Good practice</strong>
  <p>The preferred approach.</p>
</div>
'''

[[examples]]
class = "cu-callout-important"
label = "Important"
purpose = "Something that needs the reader's attention"
html = '''
<div class="cu-callout cu-callout-important">
  <strong class="cu-callout-title">Important</strong>
  <p>Something requiring attention.</p>
</div>
'''

[[examples]]
class = "cu-callout-warning"
label = "Warning"
purpose = "A risk or problem the reader must avoid"
html = '''
<div class="cu-callout cu-callout-warning">
  <strong class="cu-callout-title">Warning</strong>
  <p>A risk or problem.</p>
</div>
'''

[[examples]]
class = "cu-callout-example"
label = "Example"
purpose = "A worked example"
html = '''
<div class="cu-callout cu-callout-example">
  <strong class="cu-callout-title">Example</strong>
  <p>A worked example.</p>
</div>
'''

[[examples]]
class = "cu-callout-key"
label = "Key point"
purpose = "The main takeaway. Leaving the variant class off gives the same result"
html = '''
<div class="cu-callout cu-callout-key">
  <strong class="cu-callout-title">Key point</strong>
  <p>The main takeaway.</p>
</div>
'''
+++

## When to use it

Use a callout when one idea must stand out from the text around it, so a reader who skims still sees it.

## When not to use it

Do not use a callout for text that every reader needs anyway, such as the main instructions on a page. Put that in the body text, where people expect to find it. If everything on a page stands out, nothing does.

## How to use it

Choose the variant that matches the kind of message, give the callout a short title that names it, and keep the text short. The variants are listed under Variants.

### Do

- Keep each callout to one idea.
- Start with a short title that names the variant, such as Tip or Warning.
- Keep the text to two or three lines.

### Don't

- Put more than one or two callouts on a screen.
- Use the Warning variant for something minor. Keep it for a real risk.
- Put long paragraphs, tables or other callouts inside a callout.

## Accessibility

- The title says the variant in words, so the meaning never depends on colour or the icon.
- The theme draws the icon as decoration, so screen readers skip it.
- Keep the title. Without it, a callout is only a coloured box to someone using a screen reader.
