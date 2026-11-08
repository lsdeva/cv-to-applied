# Ashby (jobs.ashbyhq.com)

- Last used: (not yet)
- Account needed: no. Single-page form at `jobs.ashbyhq.com/<company>/<job-uuid>/application`
- Typical flow: one page with Legal Name, Preferred Name, Email, Resume, Phone, custom questions, an optional "Additional Information" textarea, a certification checkbox, then "Submit Application". Success replaces the form with "Success. Your application was successfully submitted."

## Field mechanics
- React-controlled inputs: `locator.fill()` on the system fields (name, email) did NOT register, and submit failed with "Missing entry for required field: Legal Name". Type every text input with `click` + Ctrl+A + Backspace + `pressSequentially` + Tab.
- Resume input is `input#_systemfield_resume` (id, not name). The other file input at the top is "Autofill from resume", so skip it (it would overwrite fields).
- Fields are `[class*="fieldEntry"]` blocks, so map by index after listing their labels.
- Yes/No questions are buttons, and the chosen one has `aria-pressed="true"`.
- Location is an autocomplete. Type the city and click the `[role=option]` (e.g. "<City>, <Country>").
- "When can you start" can be a date input (placeholder "Pick date..."). Type `MM/DD/YYYY` and press Enter.
- No cover letter upload: paste the letter text into Additional Information with `tools/letter_text.py <ws> --js <file> --label "Additional Information"`.
- reCAPTCHA Enterprise is invisible. No challenge appeared.

## Run log
