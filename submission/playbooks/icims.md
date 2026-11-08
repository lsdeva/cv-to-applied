# iCIMS (careers-<employer>.icims.com)

- Account needed: email-only profile (no password on this tenant)
- Typical flow: `/jobs/<id>/<slug>/login` -> email + recruitment privacy "I agree" -> Next (invisible **hCaptcha**) -> single "Candidate Profile" page -> "Submit Profile" (invisible **hCaptcha** again) -> `/job?mode=submit_apply` showing "Your application was submitted successfully." Confirmation email from `<tenant>+autoreply@talent.icims.com`.

## Field mechanics
- All form content lives in `#icims_content_iframe`; use `page.frameLocator('#icims_content_iframe')`. Navigating to the `?in_iframe=1` URL directly just bounces back to the wrapper.
- Resume upload (`PortalProfileFields.Resume_File`) parses and **replaces** form data: upload it first, then fill fields.
- Extra documents/cover letter: `-1_PersonProfileFields.rcf2014_File` (setInputFiles works).
- Searchable dropdowns (sign-off, Country, Time Zone): hidden `<select>` plus `[id="<id>_icimsDropdown"]`; click it, type into `input.dropdown-search:visible`, click the `[role=option]`.
- Plain selects (phone type, "How did you hear" `rcf3048` + dependent "Please specify" `rcf3049`): `selectOption`. On some tenants, LinkedIn sits under "Job Board", not "Social Media".

## Known traps
- The employer wrapper page throws script errors; after a dismissed or failed hCaptcha the Next/Submit button stays disabled with a spinner. Do not reload (loses uploads). Re-open the challenge in the iframe frame with `window.hcaptcha.execute()`, scroll the page so the challenge header (instruction) is visible below the sticky site header, and hand over to the user.
- Notify the user immediately (push notification) whenever the hCaptcha appears.

- Parsed experience rows get random negative ids (`-644204_PersonProfileFields.rcf3212`). Discover them from `input[id$="_PersonProfileFields.rcf3212"]` and overwrite in order.
- Some combobox options do not match `getByRole('option', {name})` (Degree "Bachelor's Degree"). Click the option by its id `result-selectable_<row>_<field>_<n>`.
- A browser reload loses everything except the login.

## Run log
