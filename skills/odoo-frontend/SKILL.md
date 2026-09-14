---
name: odoo-frontend
description: >-
  OWL component and website-theme conventions across Odoo 14-19, including the
  OWL 1→2→3 migration shape and SCSS variable conventions. Use when asked to
  build/fix a JS widget, an OWL component, or a website theme/snippet.
metadata:
  odoo-versions: "14-19"
---

# Frontend (OWL & website themes)

Load `odoo-module-create` first if this is happening inside a brand-new module,
and `odoo-module-migrate` if the goal is porting existing frontend code to a
newer version rather than writing new code.

## OWL version by Odoo series

- **14-15**: OWL 1 — components extend `owl.Component`, lifecycle via
  `willStart`/`mounted`/`willUnmount` methods, `useState` from `owl.hooks`.
- **16-17**: OWL 2 — components extend `Component` from `@odoo/owl`, `setup()`
  is the entry point (called once, replaces most lifecycle mixins), hooks
  (`useState`, `useRef`, `onWillStart`, `onMounted`, ...) imported directly
  from `@odoo/owl` and called inside `setup()`, templates use `t-on-click`
  handlers bound via `this.methodName.bind(this)` or arrow-function class
  fields — don't mix OWL 1's `willStart` overrides into an OWL 2 component.
- **18-19**: OWL 3 refinements — same `setup()`-based API as OWL 2; check the
  target version's actual `@odoo/owl` package for any renamed hooks before
  assuming 1:1 compatibility with 16/17 code.

## JS module registration

- Register widgets/fields/components through the appropriate registry
  (`registry.category("fields").add(...)`,
  `registry.category("public_widgets").add(...)`, etc.) instead of the
  legacy `Widget.include()`/global namespace patterns from Odoo ≤13 — those
  don't exist anymore on 14+.
- Static assets are declared in the manifest's `assets` dict, keyed by bundle
  (`web.assets_backend`, `web.assets_frontend`, `website.assets_editor`, ...).
  Add new JS/SCSS files to the right bundle instead of a monolithic custom
  bundle unless there's a real reason to lazy-load separately.

## Website themes

- New color/typography choices go through SCSS variables that already exist in
  the target Odoo version's website theme (`$o-color-1`..`$o-color-5`,
  `$o-website-values-palettes`) rather than hardcoding hex values in a
  component — keeps the theme compatible with the built-in theme customizer.
- Dark mode: check whether the target Odoo version's base theme already
  defines dark-mode variants of the variables in use before writing manual
  `@media (prefers-color-scheme: dark)` overrides.
- RTL: use logical CSS properties (`margin-inline-start` instead of
  `margin-left`, etc.) or Odoo's existing RTL-aware SCSS mixins — Odoo compiles
  a separate RTL asset bundle automatically from LTR SCSS, but only if
  directional properties are written correctly.
- Snippets: register via `<template>` + snippet options JS following an
  existing built-in snippet's structure (`website.s_*` naming for options)
  rather than a fully bespoke snippet system.

## Finish

```
pre-commit run -a
```

Front-end changes should still get at least a smoke test via `odoo-module-test`
conventions (an `HttpCase` + `start_tour` for anything interactive), and a
manual check in the browser — start your project's dev server the way it
normally starts (e.g. `invoke start` in Doodba-based projects) then click
through the actual feature, since lint/unit tests won't catch a broken OWL
render.
