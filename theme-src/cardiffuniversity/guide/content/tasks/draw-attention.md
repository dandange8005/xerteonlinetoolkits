+++
name = "draw-attention"
title = "Draw attention to something"
summary = "Make sure readers notice a tip, a warning or a key point."
icon = "fa-lightbulb"
components = ["callout"]

[example]
label = "An upload reminder"
purpose = "Two short paragraphs with one Important callout between them."
html = '''
<p>Upload your file before the deadline shown on the submission page.</p>
<div class="cu-callout cu-callout-important">
  <strong class="cu-callout-title">Important</strong>
  <p>Check that your upload has finished before you close the page.</p>
</div>
<p>You can upload a new version until the deadline.</p>
'''
+++

## Goal

Make one point stand out from the text around it, so a reader who skims the page still sees it.

## Checklist

- The callout holds one idea, and its title names the variant.
- The point still makes sense without its colour or icon.
- There are no more than two callouts on the screen.
- You chose the Warning variant only for a real risk.
