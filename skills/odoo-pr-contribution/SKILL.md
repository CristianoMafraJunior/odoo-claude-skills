---
name: odoo-pr-contribution
description: >-
  Prepare and submit a mergeable pull request to an OCA (or OCA-style) repo:
  fork/branch setup, commit shaping, PR description, and responding to CI/bot
  checks. Use when asked to open, submit, or prepare a PR for an Odoo module
  change, or to fix a failing PR check (runboat/weblate/pre-commit.ci/codecov).
metadata:
  odoo-versions: "14-19"
---

# Contributing a PR to an OCA repo

Load whichever `odoo-module-*` skill matches the actual change
(`odoo-module-create` for a new module, `odoo-module-migrate` for a version
port, etc.) — this skill covers the *submission process*, not the code
content.

## 1. Fork & branch

Work inside your project's own checkout of the repo (e.g.
`odoo/custom/src/<repo>` in Doodba-based projects, added via `repos.yaml`)
rather than a separate unrelated clone, so your project's own tooling
(install, addon-path resolution) actually sees the module you're changing.

1. Fork the upstream repo on GitHub if you haven't already.
2. Add your fork as a remote: `git remote add <your_org> https://github.com/<your_org>/<repo>.git`.
3. Branch from the target version, named after the change:
   - Migration: `<version>.0-mig-<module>` (e.g. `18.0-mig-partner_statement`).
   - Everything else: `<version>.0-<tag>-<module>` using the tag from
     `reference/commit-conventions.md` in `odoo-module-review`
     (`18.0-fix-stock_picking_batch`, `18.0-add-sale_order_type`).

## 2. Shape the commits

Follow `reference/commit-conventions.md` (in the `odoo-module-review` skill)
for the tag taxonomy. Concretely:

- One commit per logical step, not one giant commit — reviewers read history,
  not just the final diff.
- If pre-commit auto-formats your first commit's code, that's its own
  `[IMP] <module>: pre-commit auto fixes` commit, separate from the functional
  change — same split `odoo-module-migrate` documents for migrations.
- Run your project's lint suite and the module's tests **before** pushing
  (e.g. `invoke lint` / `invoke test -m <module_name>` in Doodba-based
  projects) — don't rely on CI to catch what you could catch locally in
  seconds.

## 3. Open the PR

- Title: `[<version>.0][<TAG>] <module>: <short description>` (see
  `odoo-module-review`'s reference file).
- Description should cover, briefly:
  - What changed and why (link the issue it closes, if any: `Closes #123`).
  - For a UI change: a before/after screenshot — reviewers on OCA PRs
    routinely ask for one if it's missing.
  - For a migration: which version it migrates from, and anything from the
    target version's breaking-change reference that needed a non-obvious
    workaround.
- Push to **your fork's branch**, open the PR against the upstream repo's
  target version branch (not `main`/`master` — OCA repos branch per Odoo
  version).

## 4. CI/bot checks — what they mean and how to fix them

| Check | What it verifies | Typical fix |
|---|---|---|
| `pre-commit.ci` / GitHub Actions lint job | The project's pre-commit suite (pylint-odoo, oca-checks-odoo-module, oca-checks-po, ruff/black, prettier) | Run the lint suite locally and push the fix — don't try to guess the failure from the CI log alone if you can reproduce it locally. |
| Test job | The project's test suite, run in CI across supported DB/Odoo combinations | Reproduce locally first, the way your project runs tests (e.g. `invoke test -m <module_name>` in Doodba-based projects). |
| **Runboat** | Spins up a live preview instance of the PR | Use it to manually click through the change before asking for review — catches things tests don't. |
| **Weblate** bot comment | Notes the module is now tracked for community translation | Informational — no action needed unless it flags a `.po` conflict. |
| **Codecov** | Coverage delta from the PR | A red delta on new code usually means the `odoo-module-test` checklist wasn't fully applied — add the missing test, don't just accept the drop. |
| Bot asking for a rebase/merge conflict resolution | Base branch moved since the PR was opened | `git fetch upstream <version> && git rebase upstream/<version>`, force-push the **same** branch — don't open a new PR. |

## 5. Responding to review feedback

- Push additional commits (or amend + force-push) to the **same branch** — the
  PR updates in place; don't close and reopen.
- If a reviewer asks for a change already covered by one of the
  `odoo-module-*` skills' checklists, fix it per that skill rather than
  improvising a one-off solution — keeps the module consistent with the rest
  of the repo.
- Once approved, OCA maintainer bots typically handle the actual merge
  (squash or merge-commit per repo convention) — you generally don't need to
  merge it yourself.
