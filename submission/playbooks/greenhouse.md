# Greenhouse (job-boards.greenhouse.io, new React UI)

- Last used: (not yet)
- Account needed: no (single-page form, no login; optional "Track your application" sign-in afterwards)
- Typical flow: 1. Open `job-boards.greenhouse.io/<board>/jobs/<id>` (form is on the posting page). 2. Fill identity, upload files, answer custom questions, voluntary self-ID, consent boxes. 3. "Submit application". 4. Redirects to `/jobs/<id>/confirmation` ("Thank you for applying").

## Field mechanics
- Text inputs (`#first_name`, `#last_name`, `#email`, `question_N` text) are React-controlled. `fill()` usually works, but if `pressSequentially` hangs on long URLs, click the field and use `page.keyboard.type(...)` instead.
- `#preferred_name` exists: leave it empty.
- `#country` next to Phone is the **phone country code** combobox (shows "+65"), not the residence country. Type the country name and click the matching `[role=option]`.
- `#candidate-location` (Location (City)) is a geo autocomplete. Typing just the city returns several countries (e.g. "<city>" also matches Brazil), and picking the first option is wrong. Type "City, Country" and click the exact `^City, Country$` option. Read the value back from the react-select control's innerText, because the `<input>` value stays empty.
- Custom questions are react-select comboboxes with ids `question_<N>`. Demographic questions have bare numeric ids (e.g. `4024662004`). Click the input, then click the visible `[role=option]` (use an anchored regex for short "Yes"/"No" options). Verify via the control's innerText.
- GDPR consent checkboxes: `gdpr_retention_consent_given_1`, `gdpr_demographic_data_consent_given_1`.

## Uploads
- `#resume` and `#cover_letter` are hidden file inputs. Use `setInputFiles` with absolute paths. The filename then shows in the page text. No CV parsing or prefill.

## Known traps
- Employer careers wrappers (e.g. Phenom-hosted careers pages) can hang the renderer, and a Greenhouse job URL may redirect back to them. Use the embed form `https://boards.greenhouse.io/embed/job_app?for=<board>&token=<job id>`. Find the id via `boards-api.greenhouse.io/v1/boards/<board>/jobs`. If the browser wedges, run `browser_close` and navigate again.
- After the first load the page may not be hydrated yet (typed text vanishes, dropdowns don't open). Wait until `#first_name` has a `__react*` key, then fill.
- Closed react-select menus stay in the DOM (a hidden 240-country phone list), so always filter `[role=option]:visible`.
- Answering EEO "Hispanic/Latino: No" reveals a required `#race` combobox. Re-check for "This field is required." after the first submit attempt.
- Location picks the first fuzzy match: always select it explicitly and verify it.
- There is no review page, so "Submit application" is final. Take the review screenshot before clicking.

## Run log
