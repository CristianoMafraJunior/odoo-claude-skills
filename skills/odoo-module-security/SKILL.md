---
name: odoo-module-security
description: >-
  Security review checklist for Odoo modules — access rules, record rules,
  sudo() usage, controller authentication, SQL injection — split into what
  standard OCA lint tooling already catches vs. what needs manual review. Use
  when asked to review, audit, or harden a module's security, or before
  finishing any module that adds models/controllers.
metadata:
  odoo-versions: "14-19"
---

# Security review for an Odoo module

Run your project's lint/pre-commit suite before (and after) a manual review
(`pre-commit run -a`, or your project's wrapper — e.g. Doodba's `invoke lint`)
— a standard OCA `.pylintrc` (loading `pylint_odoo`) already catches a
meaningful chunk of this automatically. Don't re-flag what it already
enforces; focus manual review on the rest.

## Already enforced by pylint-odoo (don't duplicate manually)

- `sql-injection` — string-formatted/concatenated `cr.execute()` calls.
- `no-raise-unlink` — `unlink()` overrides that raise instead of returning.
- `create-user-wo-reset-password` (pre-16) — creating `res.users` without
  forcing a password reset.
- `dangerous-filter-wo-user` (pre-16) — shared `ir.filters` without a `user_id`.
- `external-request-timeout` (≥16) — outbound HTTP calls missing `timeout=`.
- `no-write-in-compute` (≥16) — writes to other records inside a compute method
  (can bypass expected access checks / cause recursion).

Most OCA repos also wire [`OCA/odoo-pre-commit-hooks`](https://github.com/OCA/odoo-pre-commit-hooks)'
`oca-checks-odoo-module` (Odoo ≥14) into the same pre-commit suite, which
additionally catches, among others: `xml-create-user-wo-reset-password` (the
XML-data-file version of the pylint check above), `manifest-syntax-error`,
`xml-syntax-error`/`csv-syntax-error`, `xml-record-missing-id`,
`xml-duplicate-record-id`, `file-not-used` (a file shipped but never
referenced from `__manifest__.py` — dead code is an audit smell), and
`xml-dangerous-qweb-replace-low-priority` (a low-priority `ir.ui.view` XPath
`replace`, which any other module can silently override/break).

## Manual checklist

### Access rules (`security/ir.model.access.csv`)

- Every model defined in this module (and every model it adds fields/behavior
  to that didn't already have suitable access) has at least one line.
- Group-restricted access is scoped as tightly as the feature allows — don't
  default new models to `base.group_user` if only a specific group should
  reach them.
- `perm_unlink` is granted deliberately, not by copy-paste — most models
  shouldn't allow hard deletion by regular users.

### Record rules

- Multi-company: any model that should be company-scoped has a record rule
  filtering on `company_id` (don't rely on `ir.model.access.csv` alone — it
  doesn't scope by record).
- Any record rule using `sudo()`-bypassed domains is double-checked: a record
  rule with an always-true domain for a broad group is equivalent to no rule.

### `sudo()` usage

For every `.sudo()` call in the module, confirm:
1. It's narrowly scoped (call `sudo()` on the specific recordset/operation, not
   on `self.env` broadly at the top of a method).
2. There's a comment or clear reason why the current user's own permissions
   are insufficient (e.g. reading a related record the user shouldn't
   normally see, but the module's own access rules already gate the outer
   action).
3. It isn't used to silently swallow an access error that should actually
   surface to the user.

### Controllers

- Every `@http.route` declares `auth=` explicitly (`user`, `public`, or
  `none`) — never rely on the default.
- `auth="public"` routes: confirm every model/field they touch is safe for an
  anonymous caller, including through `sudo()` if used inside the handler.
- State-changing routes (anything beyond a `GET`-style read) require `csrf=True`
  (the default) unless there's a specific, documented reason to disable it.

### Data files

- No demo/security XML records load with `noupdate="0"` when they set
  sensitive defaults (passwords, API keys) that should survive module
  reinstalls unmodified.

## Finish

```
pre-commit run -a
```

then re-read this checklist once more against the diff before calling the
module done.
