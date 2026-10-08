+++
name = "alert"
title = "Alerts"
lead = "A short message that tells the reader the status of something."
group = "emphasis"
status = "current"
related = ["callout"]
scss = ["scss/_bootstrap-components.scss"]

[parts]
alert = "The base class every alert needs. It gives the grey surface, the square edges and the 4px rule."
close = "The dismiss button inside an alert. With data-dismiss=\"alert\", the player's Bootstrap script removes the alert when the reader clicks it."

[[examples]]
class = "alert-success"
label = "Success"
purpose = "A completed action"
html = '''
<div class="alert alert-success">
  <strong>Success!</strong> Your changes have been saved successfully.
</div>
'''

[[examples]]
class = "alert-info"
label = "Info"
purpose = "Neutral information"
html = '''
<div class="alert alert-info">
  <strong>Info:</strong> This course will be available from September 2025.
</div>
'''

[[examples]]
class = "alert-warning"
label = "Warning"
purpose = "Caution needed"
html = '''
<div class="alert alert-warning">
  <strong>Warning!</strong> Your session will expire in 5 minutes.
</div>
'''

[[examples]]
class = "alert-danger"
label = "Danger"
purpose = "An error or a critical issue"
html = '''
<div class="alert alert-danger">
  <strong>Error!</strong> Unable to submit form. Please check required fields.
</div>
'''

[[examples]]
class = "alert-error"
label = "Error"
purpose = "The same as danger"
html = '''
<div class="alert alert-error">
  <strong>Error!</strong> Unable to submit form. Please check required fields.
</div>
'''

[[examples]]
class = "alert-block"
label = "Block"
purpose = "A longer message with a heading, which the reader can dismiss"
html = '''
<div class="alert alert-block alert-info">
  <button type="button" class="close" data-dismiss="alert" aria-label="Close">&times;</button>
  <h4><strong>Info:</strong> Course dates have changed</h4>
  <p>This is a block alert with more content. It can hold more than one paragraph.</p>
  <p>Select the close button to dismiss this alert.</p>
</div>
'''
+++

## When to use it

Use an alert to tell the reader the status of something: a completed action, neutral information, a need for caution, or an error.

## When not to use it

Do not use an alert to point out a tip or the main takeaway of a page. An alert reports a status. A callout draws attention to one idea.

## How to use it

Start the message with a bold word that names the status, such as Success or Warning. The theme adds a glyph at the start of the alert. In a block alert it sits on its own line above the heading. When a message needs more than a sentence, use a block alert with a heading.

### Do

- Choose the variant that matches the status.
- Start the message with a bold word that says the status.
- Use a block alert when the message needs more than a sentence.

### Don't

- Use the danger or error variant for something that is not a real problem. The error red is kept for real problems.
- Rely on the colour of the left rule alone. The glyph and the bold word carry the status.

## Accessibility

- The glyph and the bold word carry the status, so the colour of the rule is never the only cue.
- Alert text is ink on a grey surface, which measured 16.7:1 in September 2026.
- The yellow rule of the warning variant is only 1.6:1 against the grey surface. That is acceptable only because the glyph and the word carry the meaning, so always keep the bold word.
- Give the close button an `aria-label`, because its visible text is only the × sign.
