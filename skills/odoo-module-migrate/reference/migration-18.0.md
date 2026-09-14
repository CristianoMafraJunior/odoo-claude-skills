# Migration to Odoo 18.0 (OCA)

Source: <https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-18.0>
(check the source for the latest revision — this is a snapshot, not a live mirror)

## Before migrating

- Review current OCA conventions: <https://odoo-community.org/page/contributing>.
- Subscribe to the relevant project's mailing list.
- Announce the module migration on the repo's "Migration to version 18.0" GitHub issue.
- Install pre-commit tools.

## Key tasks

- **Version**: bump manifest `version` to `18.0.1.0.0`; remove previous
  migration scripts; remove company-financed-migration mentions from
  `CREDITS.rst` if present.
- **`<tree>` → `<list>`**: the root tag of list views changes across Python,
  JavaScript and XML. Odoo ships a helper upgrade script
  (`17.5-01-tree-to-list.py`, run via `odoo-bin`) that automates most of the
  mechanical rename — use it instead of hand-editing every view. The context
  key `tree_view_ref` also becomes `list_view_ref`.
- **Kanban views** simplify significantly: `kanban-box` → `card`; children are
  now regular `<field>` definitions instead of the old templated structure;
  `kanban-tooltip` is removed.
- **Chatter**: the old
  `<div class="oe_chatter"><field name="message_follower_ids"/>...</div>` block
  collapses to a single `<chatter/>` element.
- Replace `user_has_groups` with `self.env.user.has_group`.
- `check_access_rights()` and `check_access_rule()` merge into a single
  `check_access()`.
- Replace `_name_search` with `_search_display_name`.
- Replace the deprecated `_check_recursion()` with `_has_cycle()`.
- Field definitions: `group_operator` renames to `aggregator`.
- Registry import changes: `from odoo import registry` →
  `from odoo.modules.registry import Registry`.
- **JavaScript**: remove `/** @odoo-module **/** headers (no longer needed);
  in test tours, remove `extra_trigger` (split into an independent step
  instead) and remove `test: true,` declarations.

## Testing

- Disable tracking in tests via the `tracking_disable` context key, or use
  `BaseCommon` as the test base class.
- Add tests to increase coverage.

## Not to do

- Don't update copyright years (the year shown is the "from" year, not a
  last-touched date).
- Don't change original author attributions.

## Technical process

Standard flow: clone the `18.0` branch, branch as `18.0-mig-$module`, apply
`17.0` history via `format-patch`/`git am`, run `pre-commit run -a`, adapt per
the checklist above, push to a personal fork, open a PR.

If the module itself is being **renamed** as part of the migration, use
`git filter-branch` to rename it in the commit history before rebasing onto
the target branch, so history/blame follows the new name.

PR title: `[18.0][MIG] <module>: Migration to 18.0`

**Troubleshooting**: on patch-apply failure, add `--ignore-whitespace` to
`git am` and resolve remaining conflicts manually.
