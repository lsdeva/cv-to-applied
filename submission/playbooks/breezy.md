# Breezy HR (breezy.hr)

- Last used: (not yet)
- Account needed: no
- Typical flow: job page `<company>.breezy.hr/p/<id>-<slug>` -> "Apply To Position" -> single form at `/apply` -> "Submit Application" -> `/apply/submitted` ("Application Submitted ... Good luck!"). No draft save: keep the tab untouched until submit (open other jobs in new tabs).

## Field mechanics
- Angular form; `fill()` on inputs works. Fields: cName, cEmail, cPhoneNumber, smsConsent (optional), cAddress (single line, required), cSalary + period select (`yearly`), Work History rows, Education rows, cSummary, cCoverLetter (text only, no cover-letter upload), GDPR "Consent to retain your CV" checkbox (required).
- Work History rows: `input[ng-model="candidatePosition.company_name"]`, `.title`, `textarea[ng-model="candidatePosition.summary"]`, `input[type=date][ng-model="candidatePosition.date_start|date_end"]` (YYYY-MM-DD). Clear date_end for a current role.
- Education rows: `candidateSchool.school_name`, `.field_of_study`, `.summary`, `.date_start`, `.date_end`.

## Uploads

## Known traps
- The cover letter goes into a textarea: strip LaTeX comment lines (`%-----`) and escape sequences when converting coverletter.tex to text, and apply the no-semicolon / no-dash rule.
- `browser_run_code_unsafe` with `filename` only reads files under the repo or `submission/screenshots`; build long fill scripts there.

## Run log
