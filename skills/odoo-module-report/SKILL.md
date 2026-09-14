---
name: odoo-module-report
description: >-
  QWeb PDF report and email template conventions for Odoo modules, OCA style.
  Use when asked to create, debug, or migrate a QWeb report or an email
  template.
metadata:
  odoo-versions: "14-19"
---

# QWeb reports & email templates

Load `odoo-module-create` first if this is happening inside a brand-new
module.

## Report definition

- Declare the report as an `ir.actions.report` record (XML), with `report_type`
  (`qweb-pdf` for most, `qweb-text` rarely), `report_name` pointing at the QWeb
  template's full external ID (`<module>.report_<name>`), and `model` set to
  the record the report runs on.
- Template file lives under `report/` (or `views/report_templates.xml` for a
  small module), wrapped in `<t t-call="web.html_container">` →
  `<t t-call="web.external_layout">` (or `web.internal_layout` for internal
  documents) so the company header/footer stay consistent with the rest of the
  database.
- Paper format: use `paperformat_id` on the report action rather than hardcoding
  margins/orientation in CSS, so users can override it per report from the UI.
- Multi-record printing: template must loop over `docs` (the recordset), not
  assume a single record — test printing 0, 1, and >1 records.

## Translations inside reports

Any static label in the template must be a plain translatable string (Odoo
extracts QWeb text nodes automatically) — don't build labels via string
concatenation in Python and pass them in as a pre-formatted, non-translatable
value. See the `odoo-module-i18n` skill for the broader translation workflow
and the `translation-*` lint checks that apply here too.

## Email templates

- Declare as `mail.template` XML records, `email_from` using
  `{{ (object.company_id.email or user.email) }}`-style expressions rather than
  a hardcoded address.
- Keep the HTML close to Odoo's default template structure (reuse
  `mail.mail_notification_light`/`mail.mail_notification_paynow` as a base via
  `t-call` where sensible) instead of a fully custom HTML email — keeps
  rendering consistent across mail clients.
- Any QR/barcode content embedded in a report or email should be generated via
  `report.barcode`/`/report/barcode/...` controller calls already built into
  Odoo, not a custom barcode library dependency, unless there's a concrete
  requirement (e.g. a specific national e-invoicing QR spec) the built-in
  generator can't satisfy.

## Testing

Add a `TransactionCase` test that actually renders the report
(`self.env['ir.actions.report']._render_qweb_pdf(...)` or
`_render_qweb_html(...)`) for at least the empty/one/many-record cases — a
report that only gets manually clicked through the UI regresses silently. See
the `odoo-module-test` skill for base-class conventions.

## Finish

```
pre-commit run -a
```
plus the module's tests (e.g. `invoke test -m <module_name>` in Doodba-based
projects) before calling it done.
