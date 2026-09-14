---
name: odoo-module-review
description: >-
  Review an Odoo module change (a PR, a branch, or a local diff) against OCA
  conventions, aggregating the checklists from this skill pack's other
  odoo-module-* skills instead of duplicating them. Use when asked to review,
  approve, or comment on a PR/diff touching an Odoo module, or to self-review
  before opening one.
metadata:
  odoo-versions: "14-19"
---

# Review an OCA-style module change

This skill is an *aggregator* — it tells you which other skill covers which
part of the review, and adds the review-specific process (commit/PR shape,
local testing, reviewer etiquette) that the other skills don't.

## 1. Get the actual diff

- On GitHub, with `gh` available: `gh pr view <number>` for the description/
  metadata, `gh pr diff <number>` for the patch, `gh pr checkout <number>` to
  get it locally (needed for step 4).
- Otherwise: whatever the user gave you — a branch, a patch file, a pasted
  diff. Don't guess at content you haven't actually read.

Read the whole diff before starting the checklist below — a review based on a
partial read misses cross-file issues (e.g. a model change whose
`ir.model.access.csv` update is missing).

## 2. Shape checklist (this skill's own scope)

- **Commit messages** follow the tag taxonomy in
  `reference/commit-conventions.md` (`[ADD]`/`[FIX]`/`[IMP]`/`[REF]`/`[REM]`/
  `[MOV]`/`[REL]`/`[MIG]`/`[REV]`) — flag a commit that changes behavior but is
  tagged `[REF]`, or a formatting-only commit mixed into a `[FIX]`.
  - If this is a migration PR, cross-check against `odoo-module-migrate`'s
    two-commit convention (`[IMP] pre-commit auto fixes` then
    `[MIG] <module>: Migration to X.0`) instead of the generic taxonomy.
- **PR title** matches `[<version>.0][<TAG>] <module>: <description>`.
- **Copyright/authorship**: no unrelated copyright-year bumps, no removed/
  replaced original author — see `reference/commit-conventions.md`.
- **Scope**: one logical change per PR. A PR mixing an unrelated `[REF]` with
  the actual `[FIX]` is harder to review and to `git revert` cleanly if it
  breaks something — flag it, don't just wave it through.

## 3. Delegate the rest — don't duplicate these skills' checklists

| Diff touches... | Use skill | What it adds |
|---|---|---|
| New/changed model, manifest, `readme/` | `odoo-module-create` | manifest key requirements, README fragment shape, `pylint-odoo`/`oca-checks-odoo-module` checks |
| Access rules, `sudo()`, controllers, SQL | `odoo-module-security` | the full manual + automated security checklist |
| `tests/` additions or missing coverage | `odoo-module-test` | base class choice, tagging, coverage expectations |
| `i18n/`, `_()` calls, `.po`/`.pot` | `odoo-module-i18n` | translation lint checks, translation-regeneration workflow |
| QWeb reports/email templates | `odoo-module-report` | paper format, multi-record rendering, translation-in-report |
| OWL components, website themes, SCSS | `odoo-frontend` | OWL-version-correct patterns, RTL/dark-mode conventions |
| Version bump / `attrs`→inline / `<tree>`→`<list>` etc. | `odoo-module-migrate` | per-version breaking-change reference |

Actually load and apply each relevant skill instead of reviewing from general
knowledge — they encode the project's exact lint config, which a generic
review would miss or contradict.

## 4. Verify, don't just read

Reading a diff catches obvious issues; running it catches the rest. Pull the
change into a real checkout, install/update the module, and run its tests and
lint suite the way your project normally does — e.g. in a Doodba-based
project:

```
invoke git-aggregate     # if reviewing an addon that lives in an OCA repo checkout
invoke install -m <module_name>
invoke test -m <module_name>
invoke lint
```

If the PR adds a dependency on another repo/addon, confirm it actually
resolves and installs in your project's dependency mechanism (e.g.
`repos.yaml`/`addons.yaml` in Doodba-based projects) — don't approve a
dependency bump you haven't pulled down.

To test a **still-open upstream OCA PR** locally before it's merged, most
[git-aggregator](https://github.com/acsone/git-aggregator)-based setups let
you point at the PR ref directly instead of waiting for merge — e.g. in a
Doodba project's `repos.yaml`:

```yaml
merges:
  - ocb $ODOO_VERSION
  - oca refs/pull/<PR_NUMBER>/head
```

then re-run your aggregation step (`invoke git-aggregate` in Doodba). Revert
this before merging your own change — it's a local testing aid, not something
to ship.

## 5. Giving feedback

- Don't re-flag anything your project's lint/pre-commit suite already catches
  automatically — link to the CI failure instead of restating it by hand.
- Prefer "this breaks X because Y, here's a fix" over a bare "this is wrong" —
  OCA reviews are public and read by the module's future maintainers, not just
  the current author.
- Approve once the checklist above is clean and the tests/lint suite both
  pass — don't hold a PR for stylistic preferences already covered by
  automated formatting (`ruff`/`black`/`prettier`).
