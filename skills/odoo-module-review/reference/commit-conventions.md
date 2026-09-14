# OCA commit & PR title conventions

Shared reference for the `odoo-module-review` and `odoo-pr-contribution`
skills. Source: OCA conventions (<https://odoo-community.org/page/contributing>)
and the per-version migration guides in `odoo-module-migrate/reference/`.

## Commit message prefix taxonomy

Every commit subject starts with one bracketed tag, then `<module>: <what changed>`
in the imperative mood:

| Tag | Meaning | Example |
|---|---|---|
| `[ADD]` | New module, or new feature inside an existing one | `[ADD] sale_order_type: initial version` |
| `[FIX]` | Bug fix (behavior wasn't matching the intent) | `[FIX] stock_picking_batch: wrong domain on user filter` |
| `[IMP]` | Improvement to existing, working behavior — including formatting/pre-commit-only commits | `[IMP] account_move_line_tax_editable: allow editing on draft only` |
| `[REF]` | Refactoring with no functional change | `[REF] product_pricelist_direct_print: extract helper method` |
| `[REM]` | Removing a module or dead code | `[REM] website_sale_legacy: unmaintained, superseded by website_sale_v2` |
| `[MOV]` | Moving code/files without changing them (e.g. splitting a module) | `[MOV] partner_contact_gender: move to base repo` |
| `[REL]` | Version/release-only change (bumping `version` without other changes) | `[REL] partner_statement: 17.0.1.1.0` |
| `[MIG]` | Version migration/port — see `odoo-module-migrate` skill | `[MIG] partner_statement: Migration to 18.0` |
| `[REV]` | Reverting a previous commit | `[REV] Revert "[FIX] ...": broke stock valuation` |

Multiple modules touched by one commit: comma-separate them —
`[IMP] module_a, module_b: shared helper update`.

## PR title convention

```
[<version>.0][<TAG>] <module>: <short description>
```

e.g. `[18.0][MIG] partner_statement: Migration to 18.0`, or
`[17.0][FIX] stock_picking_batch: wrong domain on user filter`.

## What never belongs in a commit/PR, regardless of tag

- Don't update copyright years as a side effect of an unrelated change.
- Don't change original author attribution in `__manifest__.py`/file headers —
  add yourself as a contributor/maintainer instead, don't replace existing
  names.
- Don't mix an `[IMP]`/formatting-only commit with functional changes in the
  same commit — keep them separable (mirrors the pre-migration-cleanup vs.
  actual-migration split in `odoo-module-migrate`).
