# Cards, tabs and accordions

Decided and implemented 21 September 2026. This closes the "tabs, accordions, cards" part of the
remaining-components item in the [follow-up checklist](../plans/2026-09-21-follow-up.md) by
recording what was deliberately not changed, along with the one small change to cards.

## Decisions

Made by Nan on 21 September 2026.

| Component | Decision |
| --- | --- |
| Tabs and accordions | **No change.** They stay as they are in `_bootstrap-components.scss`. |
| Cards | **Only the heading gets smaller.** Nothing else on a card changes. |

For the card heading Nan chose `--font-size-2xl` over the design-system entry size
(`--cu-text-entry`, 20px) that was recommended.

## What changed

- **Card heading** (`scss/components/_cards.scss`). `.card__heading` and a plain `h3` inside
  `.card__content` now use `--font-size-2xl`. The second selector matters because the clickable
  card pattern documented in that file wraps its link in an unclassed `h3`. Line height is
  unchanged.
- **Size.** `--font-size-2xl` is `clamp(1.5rem, 1.30rem + 1vw, 1.75rem)`: 28px from 720px wide
  upwards and 24px on the narrowest screens, working from the formula. The card heading was 30px,
  the global component-heading size, so on a desktop the difference is 2px. A visibly smaller
  heading would need a smaller token, for example `--font-size-xl` (24px on desktop, 20px at the
  narrowest) or `--cu-text-entry` (a fixed 20px). It is one line in `_cards.scss` and one literal
  in the checks.
- **Demo.** The Basic Card block says what the heading size is and which markups it covers.

## Verification

- 171 automated checks pass (166 before), including 5 new `cards` checks. Three failed against
  the old CSS (the card heading and the clickable card's `h3` were 30px, and a card heading was not
  smaller than a plain one). Two guard the scope of the change: a component heading outside a card
  stays 30px, and a card description stays 18px.
- The generated reference is in sync and no theme class is undocumented.
- The cards demo was rendered in headless Chrome and reviewed by eye. I did not look at a heading
  that wraps to two lines.

Not verified: the real Xerte player, or a real project's cards.

## Left as it was

- **Tabs and accordions.** Not reviewed, restyled or tested in this migration. Any hardcoded
  colours, radii or shadows in their sections of `_bootstrap-components.scss` stay unless the
  hardcoded-values audit, the third "Remaining theme migration" item, is later widened to cover
  them.
- **Everything else on cards.** While reading `_cards.scss` I noticed a 3px radius (the design
  system makes structural panels square), a large shadow on `.card--clickable:hover`, a 1.05
  image scale on hover and `transition: all`. None were changed, as instructed.
