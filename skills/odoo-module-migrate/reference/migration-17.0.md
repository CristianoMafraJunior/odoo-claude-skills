# Migration to Odoo 17.0 (OCA)

Source: <https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-17.0>
(check the source for the latest revision — this is a snapshot, not a live mirror)

## Before migrating

- Review current OCA conventions: <https://odoo-community.org/page/contributing>.
- Subscribe to the relevant project's mailing list.
- Announce the module migration on the repo's "Migration to version 17.0" GitHub issue.
- Install pre-commit tools.

## Key tasks

- **Version**: bump manifest `version` to `17.0.1.0.0`.
- Replace `name_get` overrides with `_compute_display_name`, adding whatever
  fields the computation needs to its `@api.depends`.
- **Module hooks**: pre-init/post-init/uninstall hooks now take `env` as their
  argument instead of the old `(cr, registry)` signature.
- Replace `get_resource_path` with `file_path` (new argument syntax — check the
  updated signature, it isn't a drop-in rename).
- **View context**: replace `active_id` with plain `id`; replace `active_model`
  with the model name hardcoded directly where it was only ever used for that
  one model.
- **`attrs`/`states` removal** (the big one): convert every
  `attrs="{'invisible': [('name', '=', 'red')]}"` into the direct Python-expression
  attribute it replaces — `invisible="name == 'red'"` (same idea for `required=`
  and `readonly=`). This reverses the `attrs` introduction from the 13→14
  migration.
- In list (`<tree>`) views specifically, a column that should be hidden without
  hiding the row uses `column_invisible="1"`, not `invisible="1"`.
- **Settings views**: restructure the markup —
  `<div class="app_settings_block">` → `<app>`,
  `<div class="o_settings_container">` → `<block>` (and the other
  `o_setting_*` wrapper divs get analogous new tags — check a already-migrated
  OCA settings view for the full mapping).
- **Tests**: mock `requests` calls instead of letting tests hit real external
  services.
- **OWL**: remove now-unnecessary `owl="1"` template attributes.

## Not to do

- Don't update copyright years.
- Don't change original author attributions.

## Technical process

Same shape as other versions: clone the `17.0` branch, create a
`17.0-mig-$module` branch, apply the `16.0` module's history via
`git format-patch ... | git am -3 --keep`, run `pre-commit run -a`, adapt the
code per the checklist above, then push and open a PR titled:

```
[17.0][MIG] <module>: Migration to 17.0
```
