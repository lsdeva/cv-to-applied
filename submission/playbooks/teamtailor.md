# Teamtailor (<company>.teamtailor.com)

- Last used: (not yet)
- Account needed: no
- Flow: job page -> "Apply for this job" (opens an in-page modal form; the element has no href, so click its text) -> screening text questions + personal info + CV + optional additional files + cover letter textarea + privacy consent -> submit -> optional Equal Opportunities survey ("I don't want to participate" is a link-like element, click by text) -> `/applications/<id>/thanks` "Thanks for applying".

## Field mechanics
- Inputs use Rails names: `candidate[answers_attributes][N][text]`, `candidate[first_name]`, `candidate[email]`, `candidate[phone]`, `textarea[name="candidate[job_applications_attributes][0][cover_letter]"]`.
- Files: `candidate_resume_remote_url` (CV), `candidate_file_remote_url` (additional files, put the cover letter PDF here).
- Consent checkboxes: `candidate[consent_given]` (required), `candidate[consent_given_future_jobs]` (talent pool, standing Yes).

## Run log
