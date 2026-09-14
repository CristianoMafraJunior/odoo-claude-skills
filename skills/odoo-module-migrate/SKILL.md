---
name: odoo-module-migrate
description: >-
  Port/migrate an existing (usually OCA) Odoo module from one version to
  another, following the OCA [MIG] workflow, with a per-version breaking-change
  checklist for Odoo 14 through 19. Use when asked to migrate, port, or upgrade
  a module/addon to a newer Odoo version.
metadata:
  odoo-versions: "14-19"
---

# Migrate an OCA module between Odoo versions

Make sure `openupgradelib` is available in your project's Python dependencies
(many Doodba-based projects already ship it in `pip.txt`) — use it for data
migrations instead of writing ad hoc SQL.

## Commit workflow (OCA convention)

Keep behavior-preserving cleanup separate from the actual version bump, as
(at least) two commits, following the exact shape OCA's own migration guides
use:

1. `[IMP] <module>: pre-commit auto fixes` (or `black, isort, prettier`) —
   apply the target version's formatting/lint tooling to the still-old-version
   code, without touching behavior or the manifest `version`. Produced by
   porting the module's history onto the new branch
   (`git format-patch ... | git am -3 --keep`, see each version's reference
   file) and then running `pre-commit run -a`.
2. `[MIG] <module>: Migration to <version>.0` — the actual port: manifest
   bump, API/view changes, anything that only works on the new version.

Never squash both into one commit — reviewers rely on the split. Open the pull
request titled `[<version>.0][MIG] <module>: Migration to <version>.0`.

## Manifest

Bump `version` to start with the new series (e.g. `17.0.1.0.0` → `18.0.1.0.0`),
reset the patch/revision segments, and re-check the `license`/`development_status`/
`maintainers` requirements from the `odoo-module-create` skill still hold.

## Per-version breaking-change reference

`reference/` in this skill folder holds one file per Odoo series, condensed
from the official OCA maintainer-tools migration guides — **read the file(s)
for every version you're crossing**, not just the target, since changes are
cumulative and skipping an intermediate version's file means missing its
breaking changes:

- `reference/migration-14.0.md`
- `reference/migration-15.0.md`
- `reference/migration-16.0.md`
- `reference/migration-17.0.md`
- `reference/migration-18.0.md`
- `reference/migration-19.0.md`

Each file also has the exact `git format-patch`/`git am` commands OCA uses to
port a module's commit history onto the new branch before adapting the code —
use those instead of a fresh copy-paste of the old code.

For anything not covered by these files (they're checklists, not an exhaustive
diff), check the module's own upstream OCA repo for sibling modules already
migrated to the target version and follow the same pattern — consistency with
siblings in the same repo matters more than a novel approach.

## Data migrations

If the module has stored fields/models that change shape (renamed field,
merged model, changed selection values), add an OpenUpgrade script under
`migrations/<version>.0.x.y/` using `openupgradelib` helpers
(`openupgrade.rename_fields`, `openupgrade.map_values`, etc.) rather than a
raw SQL migration — wire OpenUpgrade into your project's migration runner
(e.g. via `migration.yaml` + `pip.txt` in Doodba-based projects).

## Finish

```
pre-commit run -a
```
plus the module's tests (e.g. `invoke test -m <module_name>` in Doodba-based
projects). Both must pass before the migration is considered done.
