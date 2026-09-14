# Migration to Odoo 19.0 (OCA)

Source: <https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-19.0>
(check the source for the latest revision — this is a snapshot, not a live mirror)

## Before migrating

- Review current OCA conventions: <https://odoo-community.org/page/contributing>.
- Subscribe to relevant project mailing lists: <https://odoo-community.org/groups>.
- Announce the module migration on the repo's "Migration to version 19.0" GitHub issue.
- Install pre-commit tools.

## Key tasks

- **Version**: bump manifest `version` to `19.0.1.0.0`; remove previous
  migration scripts and obsolete `CREDITS.rst` entries.
- **Permissions**: `category_id` on groups is replaced by a new `privilege_id`
  field pointing at `res.groups.privilege`.
- Replace the `groups_id` field with `group_ids` everywhere it's referenced —
  views, menus, actions, reports.
- Internal shortcut attributes are removed — use the explicit form:
  `self._cr` → `self.env.cr`, `self._uid` → `self.env.uid`,
  `self._context` → `self.env.context`.
- **Domains**: replace `odoo.osv.expression` helpers with `odoo.fields.Domain`
  expressions; computed-field `search` methods should now return `Domain`
  objects instead of plain list-of-tuples domains.
- Replace `_sql_constraints` dict entries with model-level `models.Constraint`
  or `models.Index` instances.
- Use `self.env.tz` instead of manually juggling `pytz` for the current
  timezone.
- Field definitions: `auto_join` is replaced by `bypass_search_access`.
- Replace `read_group` with `_read_group` for internal/backend use, or
  `formatted_read_group` for anything exposed publicly.
- **Controllers**: `type="json"` routes become `type="jsonrpc"` (mirrors the
  general RPC-layer rename).
- Replace `toggle_active` with explicit `action_archive`/`action_unarchive`
  methods.
- Import `SUPERUSER_ID` from `odoo.api`, not from the `odoo` package root.
- Replace the `@ormcache_context` decorator with plain `@ormcache`.
- Use `odoo.tools.urls.urljoin` instead of `urllib.parse.urljoin`.
- Replace the `args` parameter with `domain` in `name_search` overrides.
- Remove the `@api.returns` decorator (no longer needed/respected).
- Remove `string`/`expand` attributes from `<group>` tags in search views.

## Testing

- Add tests, increase coverage.
- Disable tracking in tests via context, or use `BaseCommon`.
- Prefer creating dedicated test data over relying on demo data.
- Native fake-model loading replaces the external `odoo-test-helper` library —
  drop that dependency if the module still has it.

## Not to do

- Don't update copyright years.
- Don't change original author attributions.

## Technical process

```sh
git clone https://github.com/OCA/$repo -b 19.0
cd $repo
git checkout -b 19.0-mig-$module origin/19.0
git format-patch --keep-subject --stdout origin/19.0..origin/18.0 -- $module | git am -3 --keep
pre-commit run -a
git add -A
git commit -m "[IMP] $module: pre-commit auto fixes" --no-verify
```

Adapt the code per the checklist above, then:

```sh
git add --all
git commit -m "[MIG] $module: Migration to 19.0"
git remote add $user_org <your-fork-url>
git push $user_org 19.0-mig-$module --set-upstream
```

PR title: `[19.0][MIG] <module>: Migration to 19.0`

**Troubleshooting**: if patches fail to apply because a file was deleted
upstream, add `--ignore-whitespace` to `git am` and resolve the remaining
conflicts by hand.
