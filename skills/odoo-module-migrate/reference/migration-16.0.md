# Migration to Odoo 16.0 (OCA)

Source: <https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-16.0>
(check the source for the latest revision — this is a snapshot, not a live mirror)

## Before migrating

- Review current OCA conventions: <https://odoo-community.org/page/contributing>.
- Join the relevant project's mailing list.
- Announce the module migration on the repo's "Migration to version 16.0" GitHub issue.
- Install pre-commit tools.

Note: several `pylint-odoo` checks are version-gated around this boundary
(the newer view/API shape introduced in 16.0 enables new checks and retires
old ones) — expect a repo's `.pylintrc` enabled-checks list to differ before
and after 16.0, and modules migrated across this boundary to start being
linted against a different rule set.

## Key tasks

- **Version**: bump manifest `version` to `16.0.1.0.0`; remove any leftover
  `migrations/` folder; squash administrative commits.
- Replace `name_search` overrides with the `_rec_names_search` class attribute
  where the override only changed which fields are searched.
- Move `groups_id` restrictions from the view record level down to individual
  view elements where finer-grained control is actually needed.
- Add `colspan="2"` to one2many fields placed outside a `<notebook>` so they
  render at proper width.
- Replace the deprecated `fields_view_get` with `get_view`.
- Use `get_external_id()` instead of `get_xml_id()`.
- **Cache/flush API**: replace `flush()`/`recompute()` with `flush_model()`,
  `flush_recordset()`, or `env.flush_all()` as appropriate; replace
  `refresh()`/`invalidate_cache()` with `invalidate_model()`,
  `invalidate_recordset()`, or `env.invalidate_all()`.
- Use the `_fields` mapping or `get_views()` instead of the removed
  `fields_get_keys()`.
- **Assets**: move any XML template still declared through the deprecated
  `web.assets_qweb` bundle into the appropriate bundle (manifest `assets` key,
  per the 15.0 asset-declaration change).
- **Bootstrap**: update Bootstrap 4 markup/classes to Bootstrap 5 syntax in any
  custom templates/snippets.
- Add `unaccent=False` on fields where accent-sensitive search actually matters
  (Odoo defaults to accent-insensitive search where the DB extension is
  available).

## Testing

- Increase test coverage.
- Move `setUp` logic into `setUpClass` for faster test runs.
- Use `BaseCommon` as the test base class where applicable.
- Double check overridden methods still match the current base signature
  (parameters get added/renamed across versions).

## Not to do

- Don't update copyright years.
- Don't change original author attributions.

## Technical process

```sh
git clone https://github.com/OCA/$REPO -b 16.0
cd $REPO
git checkout -b 16.0-mig-$MODULE origin/16.0
git format-patch --keep-subject --stdout origin/16.0..origin/15.0 -- $MODULE | git am -3 --keep
pre-commit run -a
```

Adapt the code per the checklist above, then commit and push, opening a PR titled:

```
[16.0][MIG] <module>: Migration to 16.0
```

**Troubleshooting**: on patch-apply failure, add `--ignore-whitespace` to
`git am` and resolve remaining conflicts manually.
