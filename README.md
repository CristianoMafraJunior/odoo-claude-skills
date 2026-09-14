# odoo-claude-skills

**Claude Code skills for OCA-style Odoo module development** — creating,
migrating, testing, securing, translating and reviewing Odoo addons the way
the [Odoo Community Association (OCA)](https://odoo-community.org/) actually
does it.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Odoo versions](https://img.shields.io/badge/Odoo-14.0%20--%2019.0-714B67)
[![Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-D97757)](https://claude.com/claude-code)

---

## Why this exists

Ask an AI coding assistant to "create an Odoo module" and you'll usually get
something that *runs* — and quietly ignores twenty years of OCA convention:
the wrong manifest keys, a hand-written `README.rst`, no OCA commit-tag
discipline, translation strings that break placeholder substitution, a
`sudo()` call nobody can justify in review.

This is a small, focused pack of [Claude Code](https://claude.com/claude-code)
skills that close that gap. Each one is grounded in the **actual** tooling and
conventions the OCA ecosystem runs on — `pylint-odoo`, `OCA/odoo-pre-commit-hooks`,
`OCA/maintainer-tools`' README/icon generators, `click-odoo-makepot`,
`openupgradelib`, the OCA commit-tag taxonomy — not a generic approximation of
"Odoo best practices" from a language model's training data. Where a check
name or CLI flag is quoted, it's quoted because it's real.

## Design principles

- **No bundled scripts, no auto-running hooks.** Every skill is plain
  guidance in a `SKILL.md` file — nothing here executes on its own or needs
  reviewing for what it might do to your repo before you trust it.
- **Cites the real tool, every time.** "Run `pre-commit run -a`" instead of
  "lint your code"; `manifest-required-key`/`sql-injection`/`po-pretty-format`
  by their actual `pylint-odoo`/`odoo-pre-commit-hooks` check names, not a
  paraphrase.
- **Project-agnostic, with concrete examples.** These skills don't assume any
  particular Odoo deployment tooling. Where a workflow needs a concrete
  command, it shows the underlying Odoo/OCA tool (`odoo-bin scaffold`,
  `click-odoo-makepot`, `pre-commit run -a`) and notes common wrappers (e.g.
  [Doodba](https://github.com/Tecnativa/doodba)'s `invoke` tasks) as examples
  — swap in whatever your own project uses.
- **Aggregation over duplication.** `odoo-module-review` doesn't restate the
  security checklist — it tells you to load `odoo-module-security`. Shared
  reference material (the OCA commit-tag taxonomy, per-version migration
  guides) lives once, in one skill's `reference/` folder, and other skills
  point at it.

## The skills

### Module lifecycle

| Skill | Use it to... |
|---|---|
| [`odoo-module-create`](skills/odoo-module-create/SKILL.md) | Scaffold a new module and bring it up to full OCA shape: manifest keys, `readme/` fragments, module structure, the `pylint-odoo`/`oca-checks-odoo-module` checks it needs to pass. |
| [`odoo-module-migrate`](skills/odoo-module-migrate/SKILL.md) | Port an existing module to a newer Odoo version — the OCA `[IMP]`/`[MIG]` commit split, plus a [per-version breaking-change reference](skills/odoo-module-migrate/reference) for 14.0 through 19.0 distilled from OCA's own migration guides. |

### Quality

| Skill | Use it to... |
|---|---|
| [`odoo-module-test`](skills/odoo-module-test/SKILL.md) | Write `TransactionCase`/`HttpCase`/tour tests with the right base class, tags, and coverage expectations. |
| [`odoo-module-security`](skills/odoo-module-security/SKILL.md) | Audit access rules, record rules, `sudo()` usage, controller auth and SQL safety — split into what automated lint already catches vs. what needs a human. |
| [`odoo-module-i18n`](skills/odoo-module-i18n/SKILL.md) | Regenerate `.pot`/`.po` files correctly and write translatable code that survives `po-python-parse-printf`-style checks. |
| [`odoo-module-report`](skills/odoo-module-report/SKILL.md) | Build QWeb PDF reports and email templates that handle multi-record printing and stay translatable. |
| [`odoo-frontend`](skills/odoo-frontend/SKILL.md) | Write OWL components and website-theme code that's correct for the target version's OWL generation (1 / 2 / 3) and RTL/dark-mode conventions. |

### Collaboration

| Skill | Use it to... |
|---|---|
| [`odoo-module-review`](skills/odoo-module-review/SKILL.md) | Review a PR/branch/diff against OCA conventions — commit-tag shape, PR title, and a delegation table to the right skill above for each part of the diff. |
| [`odoo-pr-contribution`](skills/odoo-pr-contribution/SKILL.md) | Prepare and submit a PR to an OCA repo: fork/branch naming, commit shaping, PR description, and what each CI/bot check (Runboat, Weblate, Codecov, pre-commit.ci) actually means. |

All ten skills cover **Odoo 14.0 through 19.0** and call out version-specific
behavior explicitly wherever it applies.

## Installing

There's no package manager involved — a skill is just a folder with a
`SKILL.md` in it that Claude Code reads directly.

### Option 1 — copy what you need

```sh
cp -r skills/odoo-module-create skills/odoo-module-security /path/to/your-project/.claude/skills/
```

### Option 2 — copy all of them

```sh
cp -r skills/* /path/to/your-project/.claude/skills/
```

### Option 3 — vendor as a git submodule (recommended if you maintain a template)

If you maintain a Copier/cookiecutter template (or any repo you regenerate
projects from), pull this in as a submodule and symlink or copy from it, the
same way [`doodba-copier-template`](https://github.com/Tecnativa/doodba-copier-template)
vendors [`OCA/oca-addons-repo-template`](https://github.com/OCA/oca-addons-repo-template):

```sh
git submodule add https://github.com/<you>/odoo-claude-skills.git vendor/odoo-claude-skills
```

then reference `vendor/odoo-claude-skills/skills/<name>` from your template's
own `.claude/skills/` generation step.

### Verifying it worked

Open Claude Code inside a project that has `.claude/skills/odoo-module-create/SKILL.md`
(or any of the others) and ask it to do something the skill covers — e.g.
*"create a new module called `sale_order_priority`"*. Claude Code loads the
matching skill automatically based on its `description` frontmatter; you
don't need to invoke it by name.

## Repository layout

```
skills/
├── odoo-module-create/       SKILL.md
├── odoo-module-migrate/      SKILL.md + reference/migration-{14..19}.0.md
├── odoo-module-test/         SKILL.md
├── odoo-module-security/     SKILL.md
├── odoo-module-i18n/         SKILL.md
├── odoo-module-report/       SKILL.md
├── odoo-frontend/            SKILL.md
├── odoo-module-review/       SKILL.md + reference/commit-conventions.md
└── odoo-pr-contribution/     SKILL.md
```

`reference/` subfolders hold lookup material a skill points to rather than
inlines — keeps the main `SKILL.md` short while still giving Claude the exact
detail when it's actually needed (e.g. the six per-version migration
checklists, or the shared OCA commit-tag table).

## Sources

These skills distill, rather than replace, the real OCA documentation:

- [OCA contribution guidelines](https://odoo-community.org/page/contributing)
- [`OCA/maintainer-tools`](https://github.com/OCA/maintainer-tools) — README/icon
  generation, the module template, the per-version migration wiki
- [`OCA/odoo-pre-commit-hooks`](https://github.com/OCA/odoo-pre-commit-hooks) —
  `oca-checks-odoo-module` / `oca-checks-po` check catalogue
- [`OCA/pylint-odoo`](https://github.com/OCA/pylint-odoo) — the `pylint_odoo`
  check plugin
- [`OCA/openupgradelib`](https://github.com/OCA/openupgradelib) — data
  migration helpers

When in doubt, the source repos above are the ground truth — these skills
will drift from them over time as Odoo/OCA conventions evolve, so treat a
disagreement between a skill and current upstream docs as a bug here, not
there.

## Contributing

Keep new/edited skills:
- **Deployment-agnostic.** Cite the real underlying OCA/Odoo tool; put any
  specific project's wrapper command in an "e.g." aside, never as the only
  form given.
- **Grounded.** If you name a check, a flag, or a file path, it should be
  something you've verified exists — link the source.
- **Non-duplicating.** If another skill in this pack already owns a
  checklist, point to it instead of copying it.

Pull requests welcome.

## License

[MIT](LICENSE)
