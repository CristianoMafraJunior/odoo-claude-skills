---
name: odoo-module-test
description: >-
  Write and run Odoo module tests (TransactionCase/HttpCase/tour tests)
  following OCA conventions. Use when asked to add tests, write a test case,
  or run/debug an addon's test suite.
metadata:
  odoo-versions: "14-19"
---

# Testing Odoo modules

## Where tests live

`<module>/tests/__init__.py` importing each `test_*.py` file. Odoo only
discovers tests reachable from that `__init__.py`.

## Which base class

- `odoo.tests.common.TransactionCase` — default for anything that only needs
  ORM access; each test runs in its own rolled-back transaction.
- `odoo.tests.common.HttpCase` (or `HttpCase` + `tour`) — needed for controller
  routes, or for JS/tour tests driven through the browser
  (`start_tour(...)` in a `test_*.js` tour + a Python test that calls it via
  `self.start_tour(...)`).
- Avoid `SavepointCase` in new code on versions where `TransactionCase` already
  does per-test savepoints (14+) — it's a legacy alias.

## Install-time flags

Tag module-level setup with `@tagged("post_install", "-at_install")` for tests
that need other modules fully installed first (the OCA-standard combination
for most functional tests), or leave the default (`at_install`, runs during
module installation) only for lightweight unit tests with no cross-module
dependency.

## What to cover

- Every new/changed compute, constrain (`@api.constrains`), and onchange method.
- Every new access rule / record rule (assert the right user **can't** do
  something, not just that the right user can).
- Every new controller route (status code + payload shape, and — if
  `auth="public"` — that it doesn't leak data it shouldn't).
- Edge cases the OCA reviewers will ask about: empty recordset input, multi-record
  (not just singleton) calls, and (de)activation via `active` field if present.

## Running tests

Run the module's tests the way your project normally does. Common patterns:

```
invoke test -m <module_name>          # Doodba-based projects
odoo-bin -i <module_name> --test-enable --test-tags /<module_name> \
  --stop-after-init --log-level=test  # plain odoo-bin
```

Whichever wrapper your project uses, it should ultimately be running Odoo's
own test runner against the module's `tests/` package — don't invent a raw
`pytest`/manual-import invocation that bypasses it; `TransactionCase`/
`HttpCase` need Odoo's registry/ORM bootstrapped to work at all.

Running tests typically means restarting the target instance into test mode
against a dedicated test/devel database — remember to restart it back to
normal serving mode afterward if your project's runner doesn't already do
that for you.
