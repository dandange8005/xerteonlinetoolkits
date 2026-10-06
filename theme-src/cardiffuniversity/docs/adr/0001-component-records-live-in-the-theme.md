---
status: accepted
---

# Component records live in the theme, not the design system

The author guide's component records live with the theme's sources in this repository, not in
the Cardiff Resource Design System. The design system is kept in an Obsidian vault outside the
repository, so the build checks and the CI workflow that keep the guide free of drift could not
read records stored there, and the records hold facts that only make sense in Xerte (editor
evidence, Xerte versions, the classes in the theme's compiled CSS). This follows the
24 September 2026 decision that the design system is a reference, not a build input.

## Consequences

Advice about why and when to use a component belongs to the design system. A component record
links to it or summarises it for Xerte, and a change to that advice in the design system is not
picked up by any check. Moving the records later would mean the build reading from outside the
repository.
