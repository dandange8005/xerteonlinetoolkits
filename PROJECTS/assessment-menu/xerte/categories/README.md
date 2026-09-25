# Category pages, converted for Xerte

Source: `prototypes/2026-09-15_assessment-menu-xerte-prototype-v1.html#page/exams`. All seven category pages
have the same shape, so `build.py` holds the markup once and reads the content from the prototype's
`menuData` JSON. `python3 build.py exams` writes `exams/NN-*.html` (one fragment per Xerte section)
and `exams/local-preview.html` (real `cardiffuniversity` theme CSS). Run it once per category:
`for c in exams class-tests portfolios multimedia oral practical written browse; do python3 build.py $c; done`.

## Where each file goes

| File | Goes in |
| --- | --- |
| `styles.css` | Project > Optional properties > Styles (shared by every category page) |
| `<category>/NN-*.html` | one Text element (Source view) per section, Show Title unticked |
| `browse/01-all-types.html` | one **HTML Code** element (it holds a script), Show Title unticked |

## Page settings

Each category is its own Xerte page. Every element is a Text element (Source view) with Show Title unticked,
except that the Section Title is set as below. The Home finder links to `#page-id|section-id`, so the
IDs must match exactly, and Section IDs must be unique across the whole project.

### Exams

Page ID `exams` · Page Link `Exams` · Page Title Exams  
Page Subtitle: Time-limited assessments completed under set conditions, with or without access to resources.

| # | Fragment | Section ID | Section Title |
| --- | --- | --- | --- |
| 1 | `01-about.html` | `exams-about` | About this category |
| 2 | `02-in-person-invigilated-exam.html` | `in-person-invigilated-exam` | In-person, invigilated exam |
| 3 | `03-open-book-exam.html` | `open-book-exam` | Open-book exam |

### Class tests

Page ID `class-tests` · Page Link `Class tests` · Page Title Class tests  
Page Subtitle: Short tests run in timetabled sessions, from knowledge checks to applied problems.

| # | Fragment | Section ID | Section Title |
| --- | --- | --- | --- |
| 1 | `01-about.html` | `class-tests-about` | About this category |
| 2 | `02-timed-in-class-knowledge-test.html` | `timed-in-class-knowledge-test` | Timed in-class knowledge test (short answer and MCQs) |
| 3 | `03-application-based-problem-test.html` | `application-based-problem-test` | Application-based problem test |
| 4 | `04-mentimeter-conceptual-understanding-check.html` | `mentimeter-conceptual-understanding-check` | Mentimeter conceptual understanding check |

### Portfolios

Page ID `portfolios` · Page Link `Portfolios` · Page Title Portfolios  
Page Subtitle: Collections of work or reflection that show development over time.

| # | Fragment | Section ID | Section Title |
| --- | --- | --- | --- |
| 1 | `01-about.html` | `portfolios-about` | About this category |
| 2 | `02-reflective-portfolio.html` | `reflective-portfolio` | Reflective portfolio |
| 3 | `03-annotated-bibliography.html` | `annotated-bibliography` | Annotated bibliography |
| 4 | `04-professional-portfolio.html` | `professional-portfolio` | Professional portfolio |

### Multimedia assessments

Page ID `multimedia` · Page Link `Multimedia` · Page Title Multimedia assessments  
Page Subtitle: Visual, digital or physical outputs that students design and produce.

| # | Fragment | Section ID | Section Title |
| --- | --- | --- | --- |
| 1 | `01-about.html` | `multimedia-about` | About this category |
| 2 | `02-artefacts.html` | `artefacts` | Artefacts |
| 3 | `03-posters.html` | `posters` | Posters |
| 4 | `04-blog-vlog.html` | `blog-vlog` | Blog/vlog |

### Oral and spoken

Page ID `oral` · Page Link `Oral and spoken` · Page Title Oral and spoken  
Page Subtitle: Assessments where students explain, discuss or defend their thinking out loud.

| # | Fragment | Section ID | Section Title |
| --- | --- | --- | --- |
| 1 | `01-about.html` | `oral-about` | About this category |
| 2 | `02-assessed-seminars.html` | `assessed-seminars` | Assessed seminars |
| 3 | `03-presentation.html` | `presentation` | Presentation |
| 4 | `04-viva-voce.html` | `viva-voce` | Viva voce |

### Practical based

Page ID `practical` · Page Link `Practical` · Page Title Practical based  
Page Subtitle: Assessments of skills and decisions in real or simulated practice.

| # | Fragment | Section ID | Section Title |
| --- | --- | --- | --- |
| 1 | `01-about.html` | `practical-about` | About this category |
| 2 | `02-osces-and-isces.html` | `osces-and-isces` | OSCEs and ISCEs |

### Written assessments

Page ID `written` · Page Link `Written` · Page Title Written assessments  
Page Subtitle: Extended written work built on sources, evidence and argument.

| # | Fragment | Section ID | Section Title |
| --- | --- | --- | --- |
| 1 | `01-about.html` | `written-about` | About this category |
| 2 | `02-essay.html` | `essay` | Essay |
| 3 | `03-report.html` | `report` | Report |

The Page Link text can differ from the name, but the Page ID must stay as shown.

### Browse all

Page ID `browse` · Page Link `Browse all` · Page Title Browse all assessment types  
Page Subtitle: Search the full list or filter by category

| # | Fragment | Element | Section ID | Section Title |
| --- | --- | --- | --- | --- |
| 1 | `01-all-types.html` | HTML Code | `all-types` | All assessment types |

Search box, category filters, a result count and one card per type (17), sorted A to Z. Every card links
to `#category|type-section`. All the records are in the fragment's markup, so the script only shows and hides
cards and there is no data table to keep in step. Search covers name, summary, lane wording and category
names. A type shared between categories (e.g. Posters: Multimedia and Written) appears under both filters.
The cards are the theme's `.card--clickable` and the filters its `.button`s, swapped from outline to filled
when pressed, as on the Home finder.

### Types shared between categories

A type has one page and one section, in its main category. Its other categories list it in their
"About this category" section, linking to the main page, and the Browse page shows every category it belongs to.
The "Back to all assessment types" links on the type sections go to `#browse`.

## Components

Theme components where one fits:

| Prototype | Here |
| --- | --- |
| `.placeholder` (Practical considerations) | `.cu-callout-tip` |
| `blockquote.voice` | `.quote` |
| `.back-link` | `.link-action` |

Custom components in `styles.css`, for things the theme has nothing like:

| Component | Markup |
| --- | --- |
| Lane pills | `.am-pills` > `.am-pill` + `--lane1` / `--lane2` / `--either` / `--muted` |
| "To resolve" note | `p.am-note` |
| Lane cards | `.am-lanes` > `.am-lane.am-lane--1` / `--2`, with `__title`, `__subtitle`, `__label` (Example / Case study), `__not-normally` and `__review` (a `<details>` holding text under review) |

Each variant sets one colour, `--am-tone`, and the tint and border are mixed from it, so a
new variant is one line. The lane blue, lane green and note amber are mixed from the theme's
accent colours with ink for text contrast. The cards' 10px radius (`--am-radius-panel`) is a
deliberate break from the theme's square panels.

## Dropped

The prototype's page shell (navbar, header, section menu, feedback panel), which Xerte supplies,
and the "hide proposal labels" toggle. The "New" badge on "About this category" is dropped
because Xerte's Section Title can't hold markup.
