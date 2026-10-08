+++
name = "table"
title = "Tables"
lead = "A table shows values in rows and columns, with a header row that says what each column holds."
group = "content"
status = "current"
related = []
scss = ["scss/_base-elements.scss", "scss/_bootstrap-components.scss"]

[parts]
table = "Bootstrap's table class. Plain table elements are already styled by the theme; the striped example uses this class with table-striped."

[[examples]]
label = "Standard table"
purpose = "A table with a caption, a header row and a body"
html = '''
<table>
  <caption>Student enrolment by programme, 2024/25</caption>
  <thead>
    <tr>
      <th>Programme</th>
      <th>Year&nbsp;1</th>
      <th>Year&nbsp;2</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Computer Science</td>
      <td>1,234</td>
      <td>456</td>
      <td>1,690</td>
    </tr>
    <tr>
      <td>Engineering</td>
      <td>2,105</td>
      <td>678</td>
      <td>2,783</td>
    </tr>
    <tr>
      <td>Business</td>
      <td>1,876</td>
      <td>892</td>
      <td>2,768</td>
    </tr>
  </tbody>
</table>
'''

[[examples]]
class = "table-striped"
label = "Striped rows"
purpose = "A quiet grey tint on alternate rows"
html = '''
<table class="table table-striped">
  <caption>Assessment weightings</caption>
  <thead>
    <tr>
      <th>Assessment</th>
      <th>Weighting</th>
      <th>Format</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Essay</td>
      <td>40%</td>
      <td>2,500 words</td>
    </tr>
    <tr>
      <td>Presentation</td>
      <td>20%</td>
      <td>10 minutes</td>
    </tr>
    <tr>
      <td>Exam</td>
      <td>40%</td>
      <td>Two hours</td>
    </tr>
  </tbody>
</table>
'''

[[examples]]
class = "cu-table-scroll"
label = "Wide table"
purpose = "A wrapper that makes a table wider than the page scroll inside itself, so the page does not stretch"
html = '''
<div class="cu-table-scroll" tabindex="0" role="region" aria-label="Module results by week">
  <table>
    <caption>Module results by week</caption>
    <thead>
      <tr>
        <th>Module</th>
        <th>Week&nbsp;1</th>
        <th>Week&nbsp;2</th>
        <th>Week&nbsp;3</th>
        <th>Week&nbsp;4</th>
        <th>Week&nbsp;5</th>
        <th>Week&nbsp;6</th>
        <th>Week&nbsp;7</th>
        <th>Week&nbsp;8</th>
        <th>Week&nbsp;9</th>
        <th>Week&nbsp;10</th>
        <th>Week&nbsp;11</th>
        <th>Week&nbsp;12</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Assessment design</td>
        <td>72</td>
        <td>68</td>
        <td>75</td>
        <td>81</td>
        <td>79</td>
        <td>64</td>
        <td>70</td>
        <td>77</td>
        <td>83</td>
        <td>85</td>
        <td>80</td>
        <td>88</td>
      </tr>
    </tbody>
  </table>
</div>
'''
+++

## When to use it

Use a table for values that line up in rows and columns, such as dates, scores or a comparison between options.

## When not to use it

Do not use a table to lay out a page. A table is for data.

## How to use it

Give the table a caption that names it, a `thead` with `th` header cells, and a `tbody`. If the table may be wider than the page, wrap it in `.cu-table-scroll`, and give the wrapper `tabindex="0"`, `role="region"` and an `aria-label` that names the table.

### Do

- Use a caption, a `thead` with `th` header cells, and a `tbody`.
- Wrap a table that may be wide in `.cu-table-scroll`, with `tabindex="0"`, `role="region"` and an `aria-label` that names the table.
- Add `table-striped` for a quiet grey tint on alternate rows.

### Don't

- Leave a wide table unwrapped. It does not scroll by itself and stretches the whole page.
- Leave out the wrapper's `tabindex`, `role` or `aria-label`. Nothing checks them, and without `tabindex="0"` a keyboard user may not be able to scroll the table.
- Use `table-bordered`, `table-hover` or `table-condensed` without checking them in the player first. The theme has not reviewed them.

## Accessibility

- A caption gives screen reader users the context of the table, and header cells in a `thead` say what each column holds.
- The wrapper takes keyboard focus with `tabindex="0"` and shows the theme's focus ring, so a keyboard user can scroll a wide table.
- Striped rows are a grey tint with ink text, which measured 16.7:1 in September 2026. A caption is grey on white, which measured 5.7:1.
