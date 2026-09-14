# Migration to Odoo 14.0 (OCA)

Source: <https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-14.0>
(check the source for the latest revision — this is a snapshot, not a live mirror)

## Before migrating

- Review current OCA conventions: <https://odoo-community.org/page/contributing>.
- Subscribe to the relevant project's mailing list.
- Announce the module migration on the repo's "Migration to version 14.0" GitHub issue.
- Install pre-commit tools.

## Key tasks

- **Version**: bump manifest `version` to `14.0.1.0.0`.
- **Administration**: remove previous migration scripts; squash administrative
  commits to reduce noise.
- **Selection fields**: new selection values added via `selection_add` require
  an explicit `ondelete=` behavior, e.g.
  `fields.Selection(selection_add=[("foo", "Foo")], ondelete={"foo": "set null"})`.
- **XML views**: replace dynamic expressions previously in `invisible`/`readonly`
  attributes with `attrs="{...}"` (this is the *introduction* of `attrs` — it
  gets removed again in 16→17, see `migration-17.0.md`).
- Replace shortcut tags `<act_window>` and `<report>` with full `<record>`
  definitions.
- Convert `<button>` `string` attributes to `title` to keep tooltip behavior.
- **Transient models**: add explicit security ACLs — they're no longer implicit.
- Prefer overriding `name_get` (still valid on 14.0; gets replaced by
  `_compute_display_name` starting 17.0) over ad hoc display-name hacks.
- Remove `size=X` on `Char` fields (no longer enforced/meaningful the same way).
- `_name_search` must return IDs, not `(id, name)` tuples.
- Replace `.with_context(force_company=...)` with `.with_company(...)`.
- Remove `global` field assignments in record rules.
- **Access**: `ir.actions.*` objects are no longer directly readable — use
  `sudo()` or go through the `/web/action/load` controller.

## Not to do

- Don't update copyright years.
- Don't change original author attributions.

## Technical process

Clone the `14.0` branch, cherry-pick (or `git format-patch`/`git am`, per the
newer versions' documented flow) commits from `13.0`, run `pre-commit run -a`
(black/isort/prettier), adapt the code per the checklist above, then open a PR
named:

```
[14.0][MIG] <module>: Migration to 14.0
```
