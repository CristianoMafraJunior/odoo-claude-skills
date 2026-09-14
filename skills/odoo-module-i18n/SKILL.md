---
name: odoo-module-i18n
description: >-
  Translation workflow for Odoo modules using standard OCA i18n tooling and
  conventions. Use when asked to add/update translations, export a .pot file,
  or fix translation-related lint failures.
metadata:
  odoo-versions: "14-19"
---

# i18n workflow

Most OCA repos wire [`OCA/odoo-pre-commit-hooks`](https://github.com/OCA/odoo-pre-commit-hooks)'
`oca-checks-po --fix` into their pre-commit suite (e.g. via `invoke lint` in
Doodba-based projects), catching/auto-fixing on every commit touching
`.po`/`.pot` files: `po-requires-module` (missing `#. module: MODULE`
comment), `po-python-parse-printf`/`po-python-parse-format` (placeholder
count mismatch between `msgid` and `msgstr` — a real runtime risk, not just
style), `po-duplicate-message-definition`, `po-duplicate-model-definition`,
`po-syntax-error`, and `po-pretty-format` (alphabetical order, 78-column
wrap, clearing a `msgstr` identical to its `msgid`). Regenerate strings first
(below), then run your lint/pre-commit suite to clean up formatting — don't
hand-fix things it already auto-fixes.

## Regenerating `.pot`/`.po` files

Never hand-edit `.pot` files. The underlying OCA tool is `click-odoo-makepot`
(part of [`click-odoo-contrib`](https://github.com/acsone/click-odoo-contrib)):

```
click-odoo-makepot --addons-dir=<path> -m <module_name> \
  --msgmerge --purge-old-translations
```

Many project setups wrap this — e.g. Doodba-based projects expose
`invoke updatepot -m <module_name>` (also `--all`/`-r <repo_name>`), which
additionally stops Odoo first, strips volatile `POT-Creation-Date`/
`PO-Revision-Date` headers (so diffs stay clean), and runs the lint suite
against the touched `i18n/*.po*` files automatically. Use your project's
wrapper if it has one instead of reimplementing this by hand.

`--msgmerge` merges into existing `.po` files instead of clobbering
translator work, and is what you want by default; only skip it if you
deliberately want to regenerate from scratch (rare — it discards existing
translations). Only pass `--fuzzy-matching` when you specifically want Odoo
to guess-match similar strings as fuzzy.

## Writing translatable code

- User-facing strings in Python: wrap with `_("...")` from `odoo.tools.translate`
  (or the model's `env._`), never build the string via f-string/`%`-formatting
  *around* the `_()` call — interpolate *inside* it (`_("Hello %s", name)`),
  not `_("Hello %s") % name`. A standard OCA `.pylintrc` (≥16) enforces this
  family of checks: `translation-format-interpolation`,
  `translation-fstring-interpolation`, `translation-positional-used`,
  `translation-not-lazy`, `translation-contains-variable`,
  `translation-too-few-args`/`translation-too-many-args`,
  `translation-unsupported-format`, `translation-format-truncated`.
- XML: translatable attributes (`string`, `help`, `placeholder`, ...) are
  translated automatically — don't add a manual `t-translation` unless doing
  something unusual with QWeb.
- Never concatenate translated fragments (`_("Foo") + _("Bar")`) — translators
  need the full sentence in one string to produce correct grammar in other
  languages.

## OCA conventions

- `.po` files are typically synced with Weblate by the OCA infra on the actual
  upstream repos — avoid unrelated reformatting of `.po` files beyond what
  your regeneration tool itself produces, to keep diffs reviewable/mergeable
  there.
- Keep the module's own `.pot` up to date whenever translatable strings
  change — don't let it silently drift; regenerate it (e.g.
  `invoke updatepot -m <module>` in Doodba-based projects) as part of
  finishing any change that adds or edits user-facing strings.
