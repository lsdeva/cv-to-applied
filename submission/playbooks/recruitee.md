# Recruitee (<company>.recruitee.com)

- Account needed: no
- Finding the job: company careers pages may not link the board. List offers with `GET https://<company>.recruitee.com/api/offers/` (fields: title, careers_url, careers_apply_url, location, published_at). Apply form: `/o/<slug>/c/new`.
- Typical flow: cookie banner ("Agree to necessary") -> single page: Full name, Email, Phone (+ country calling code), SMS consent (optional), CV (required file), Cover letter (file or "Write it here instead"), custom questions, "Send".

## Field mechanics
- Phone: the calling-code dropdown is a virtualised list; instead type the full international number (`<your-phone>`) into Phone number and the country code switches automatically.
- `getByLabel('Full name *')` etc. work. Custom questions: radios (Yes/No pairs in order), text inputs, a numeric salary field (EUR), location checkboxes (required group).
- Two `input[type=file]`: index 0 CV, index 1 cover letter; `setInputFiles` works, shows the filename with "Change file".

## Known traps
- **hCaptcha on Send** (image challenge). the user must solve it. On 2026-10-26 the captcha check returned HTTP 400 after solving and the Send button spun forever (`aria-busy=true`) with no confirmation email: the application did not go through. Fix: reload the form, refill (all fields are lost on reload), and let the user click Send and solve the challenge. Never re-click Send without checking for a confirmation (page text and Gmail) first.

## Run log
