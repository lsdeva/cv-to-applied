# BambooHR (<company>.bamboohr.com/careers/<id>)

- Account needed: no
- Typical flow: job page -> "Apply for This Job" -> one form (First, Last, Email, Phone, Resume upload, LinkedIn, sometimes custom questions) -> "Submit Application" -> a reCAPTCHA v2 checkbox appears only after the first submit click (the user's step) -> "Thank You. Your application was submitted successfully".

## Field mechanics
- `#nickname_hpcsaf` is a honeypot ("Please leave this field blank"). Never fill it.
- One file input (Resume). No cover-letter slot on this tenant, so upload a merged PDF (letter first, then CV) made with pypdf.

## Run log
