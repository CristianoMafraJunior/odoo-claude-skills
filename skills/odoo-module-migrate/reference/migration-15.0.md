# Migration to Odoo 15.0 (OCA)

Source: <https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-15.0>
(check the source for the latest revision — this is a snapshot, not a live mirror)

## Before migrating

- Review current OCA conventions: <https://odoo-community.org/page/contributing>.
- Subscribe to the relevant project's mailing list.
- Announce the module migration on the repo's "Migration to version 15.0" GitHub issue.
- Install pre-commit tools.

## Key tasks

- **Version**: bump manifest `version` to `15.0.1.0.0`.
- **Administration**: delete any `migrations/` folder left from a previous
  version's data migration; squash administrative commits; consider bumping
  `development_status` if the module has matured.
- **QWeb templates**: replace `t-raw` with `t-out` (wrap with `markupsafe.Markup`
  when the value is genuinely trusted HTML); replace `t-esc` with `t-out` too
  (the old directives still work as deprecated aliases, don't rely on that).
- **Access control**: direct access to `ir.model*` objects is removed — use
  `sudo()`, or the existing high-level methods, instead of reading those models
  directly.
- **Mail templates**: `body` stays QWeb; `subject`/`email_from`/`email_to` move
  to inline_template syntax with `{{ ... }}` delimiters instead of the old
  `${ ... }`.
- **JS/assets**: ES modules get the `.esm.js` extension; assets are now declared
  directly in `__manifest__.py` under an `"assets"` key, pointing at bundles
  like `"web.assets_backend"` / `"web.assets_qweb"` — remove the old `qweb` manifest
  key, link XML template files into the `web.assets_qweb` bundle instead. Asset
  paths are relative to the addon **root**, not to the module folder, and glob
  patterns are supported.
- **Tests**: replace `SavepointCase` with `TransactionCase`; drop
  `Environment.manage()` context managers when creating new environments (no
  longer needed); prefer `@api.ondelete` over overriding `unlink()` for
  deletion-guard logic; move `setUp` logic to `setUpClass` where possible for
  speed; add tests to raise coverage.

## Not to do

- Don't update copyright years.
- Don't change original author attributions.

## Technical process

```sh
git clone https://github.com/OCA/$REPO -b 15.0
cd $REPO
git checkout -b 15.0-mig-$MODULE origin/15.0
git format-patch --keep-subject --stdout origin/15.0..origin/14.0 -- $MODULE | git am -3 --keep
pre-commit run -a
git add -A
git commit -m "[IMP] $MODULE: black, isort, prettier" --no-verify
```

Then adapt the code per the checklist above and:

```sh
git add --all
git commit -m "[MIG] $MODULE: Migration to 15.0"
git remote add $USER_ORG https://github.com/$USER_ORG/$REPO.git
git push $USER_ORG 15.0-mig-$MODULE --set-upstream
```

PR title: `[15.0][MIG] <module>: Migration to 15.0`

**Troubleshooting**: if `git am` fails to apply a patch, add `--ignore-whitespace`
and resolve the remaining conflicts by hand.
