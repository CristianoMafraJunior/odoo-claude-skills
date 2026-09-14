---
name: odoo-module-create
description: >-
  Scaffold a new Odoo module that follows OCA conventions, then bring it up to
  full OCA shape (manifest, readme fragments, security, tests) and pass
  standard OCA lint checks. Use when asked to create, add, or scaffold a new
  Odoo module/addon.
metadata:
  odoo-versions: "14-19"
---

# Create an OCA-style module

## 1. Decide where it lives

- A first-party module for your own project → your project's custom addons
  path (e.g. `odoo/custom/src/private` in Doodba-based projects).
- A module meant to eventually live in an OCA (or other) repo → create it
  inside that repo's own checkout, and register it wherever your project's
  addon-path mechanism expects it (e.g. `addons.yaml` in Doodba-based
  projects).

## 2. Scaffold

```
odoo-bin scaffold <module_name> <path>
```

This is Odoo's own scaffolding command — it gives you the base skeleton
(`__init__.py`, `__manifest__.py`, `models/`, `views/`, `security/`, `demo/`,
`tests/`). Many project setups wrap it (e.g. Doodba's `invoke scaffold`,
usually run inside a container) — use your project's wrapper if it has one,
the result is the same. Treat the output as a starting point, not the final
shape — fix it up per the checklist below.

## 3. Manifest (`__manifest__.py`)

A standard OCA `.pylintrc` (loading the `pylint_odoo` plugin) enforces:

- `license` key is **required**, and must be one of: `AGPL-3`, `GPL-2`,
  `GPL-2 or any later version`, `GPL-3`, `GPL-3 or any later version`, `LGPL-3`,
  `OPL-1`, `OEEL-1`.
- `description` and `active` keys are **deprecated** — don't add them
  (description goes in `readme/DESCRIPTION.md`/`.rst`, see below; use
  `auto_install` for install-state logic, not `active`).
- If the repo's `.pylintrc` sets `manifest-required-authors` (or the pre-16
  `manifest_required_authors`), that author string is **required** in
  `author` — typically `"<author>, Odoo Community Association (OCA)"` for a
  module meant for an OCA repo.
- `version` must follow Odoo's `X.Y.Z.W.V` manifest-version format and start
  with the target Odoo series (e.g. `18.0.1.0.0`).
- On Odoo ≥16 additionally: `development_status` must be one of the allowed
  OCA values (`Alpha`/`Beta`/`Production/Stable`/`Mature`), and `maintainers`
  should be a list of GitHub handles.
- Other standard OCA keys worth setting even where lint doesn't force them:
  `summary` (one-liner), `category`, `website` (repo/addon URL),
  `external_dependencies` (`{"python": [...], "bin": [...]}`), `application`
  (only `True` for a real top-level app, not a technical/integration module).

## 4. README, not `description`

Never hand-write `README.rst` — OCA's `oca-gen-addon-readme` tool (from
[`OCA/maintainer-tools`](https://github.com/OCA/maintainer-tools), usually
wired as a pre-commit hook) generates it from fragment files under
`<module>/readme/`. Recognized fragment names, in the order they appear in
the generated README:

- `DESCRIPTION` — what the module does (the only one effectively required —
  an empty README fails the `missing-readme` pylint-odoo check).
- `CONTEXT` — use cases/context, optional.
- `INSTALL` — extra install steps beyond normal dependency install, optional.
- `CONFIGURE` — configuration steps, optional.
- `USAGE` — how to use it, optional but recommended for anything with a
  non-obvious UI flow.
- `DEVELOP` — notes for future contributors, optional.
- `ROADMAP` — known issues/planned work, optional.
- `HISTORY` — changelog, optional (some OCA repos wire a towncrier/
  `newsfragments` automation for this instead of hand-editing it).
- `CONTRIBUTORS` — one line per contributor, optional.
- `CREDITS` — funders/sponsors, optional.

Fragments can be written as `.rst` or `.md` — `oca-gen-addon-readme`
auto-detects the format and can auto-convert one to the other. **Check the
target repo's own `.pre-commit-config.yaml`** for a
`--convert-fragments-to-markdown` flag before picking one; don't assume —
plenty of OCA repos still use `.rst`.

Module icons (`static/description/icon.png`) can be generated with
`oca-gen-addon-icon`, also from `maintainer-tools` — reuse the standard OCA
icon unless the module needs a custom one.

## 5. Code structure

- One model per file, file name matches the model's main purpose
  (`models/<model_name>.py`), each file imported from `models/__init__.py`.
- Every override of `create`/`write`/`unlink`/`compute`/`search`/`inverse`
  methods must call `super()` (`method-required-super`) and compute/inverse/search
  methods must actually be wired to the right `@api.depends`/`@api.depends_context`
  decorators (`method-compute`, `method-inverse`, `method-search` checks).
- No `eval`/`exec` on untrusted input (`eval-used`, `eval-referenced`).
- No raw string-interpolated SQL (`sql-injection` — parametrize `cr.execute` calls).
- On Odoo ≥16: don't put wizards inside `models/` (`no-wizard-in-models`), don't
  write to fields inside a `@api.depends` compute (`no-write-in-compute`), and any
  outbound HTTP call needs an explicit `timeout=` (`external-request-timeout`).
- Don't set manifest/field values equal to their default —
  `OCA/odoo-pre-commit-hooks`' `oca-checks-odoo-module` auto-fixes (and will
  just strip) redundant entries like `"installable": True` or `"data": []`
  (`manifest-superfluous-key`) and a field's `string=` when it only restates
  the Title-Case of the field name (`field-string-redundant`) — don't add
  either in the first place.
- Don't leave an unused `_logger = logging.getLogger(__name__)` in a model
  (`unused-logger`) — only declare it where actually used.

## 6. Security

- `security/ir.model.access.csv` — every new model needs at least one access
  line; see the `odoo-module-security` skill for the full checklist.
- Add `security/<module>_security.xml` for record rules/groups if the module
  needs access control beyond basic CRUD.

## 7. Tests

Add a `tests/` package (`__init__.py` importing `test_*` modules) — see the
`odoo-module-test` skill for conventions, then run it using your project's
Odoo test runner (e.g. `invoke test -m <module_name>` in Doodba-based
projects, or `odoo-bin -i <module_name> --test-enable --test-tags
/<module_name> --stop-after-init` otherwise) before considering the module
done.

## 8. Finish

```
pre-commit run -a
```

(or your project's wrapper for it, e.g. Doodba's `invoke lint`) — this runs
the full OCA pre-commit suite, not just `pylint-odoo`: `ruff`/`black`+`isort`+
`flake8` (formatting), `prettier` (XML/JS/etc.),
`OCA/odoo-pre-commit-hooks`' `oca-checks-odoo-module` (structural OCA checks)
and `oca-checks-po --fix` (translation file hygiene), and — if configured —
`oca-gen-addon-readme` (regenerates `README.rst`/`README.html` from the
fragments in step 4). Fix everything it reports before calling the module
done — this is the same check that runs in CI.

If the module lives in an upstream OCA repo checkout, also make sure it's
registered wherever your project's addon-path mechanism expects (e.g.
`addons.yaml` in Doodba-based projects) so it actually gets installed.
