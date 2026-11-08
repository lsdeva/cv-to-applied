# SAP SuccessFactors (Recruiting / RMK career site)

- Account needed: yes (email + password per employer tenant; the user signs in manually, credentials are never stored here)
- Typical flow:
  1. Employer career site (`careers.<employer>.com/job/<slug>/<id>/`) -> accept cookie banner -> "Apply now".
  2. Redirect to `career<N>.successfactors.eu/careers?company=<tenant>` sign-in page (or straight into the form if already signed in).
  3. Single long application page with collapsible sections: My Documents, Candidate Information, Work Experience, Formal Education, Languages, Certifications/Licenses, Geographic Mobility, Additional Information (employer questionnaire).
  4. Buttons at the bottom: "Save" (draft) and "Apply" (final submit; needs the user's yes).
  5. Confirmation: page title "Successfully Applied to <role> (<req id>)", body "Your application has been sent. Thank you!" No reference number.

## Getting in
- LinkedIn's non-Easy-Apply button forces a LinkedIn login. Go to the employer careers site instead and search the job title (e.g. `careers.<employer>.com/search/?q=<keywords>`); confirm the Job ID matches the posting.
- Clicking "Apply now" via a ref sometimes does nothing; click the link by CSS selector `a[href*="talentcommunity/apply"]`. Navigating directly to the `/talentcommunity/apply/<id>/` URL bounces to the careers home page (needs the click/referrer).
- The tenant may already hold an account for the email from an earlier application: "Create Account" then shows "Account Already Exists". Check `job_search_tracker.csv` for an earlier application before choosing create vs sign in.

## Account creation
- Fields: email x2, password x2, first/last name, country of residence (native select), talent-pool radio, job-alert / career-update checkboxes, Terms of Use dialog (Accept / Decline).
- Password rules seen: 8-18 characters, upper + lower case, at least one number or punctuation, no spaces/unicode.
- If the user asks Claude to generate the password: generate it in-page with `crypto.getRandomValues` inside `browser_run_code_unsafe`, type it with `pressSequentially`, and return only a success flag. **Page snapshots (including the automatic snapshot after any click) record password field values**: avoid snapshots while a password is in the form, and delete any `.yml` in `submission/screenshots/` that captured one.

## Field mechanics
- Profile data persists per tenant: an old application leaves its CV, name, address, nationality and gender pre-filled. Re-check every Candidate Information field; placeholder values ("1", "111111") are common.
- Most dropdowns are custom `rcmpaginatedselect` comboboxes: click the field's button, read options from the listbox named in the combobox `aria-controls` (`[id="NNN:_listSelect"]`, ids contain colons so use attribute selectors), then click the menuitem. Close with a second button click; Escape is unreliable and option reads can lag one dropdown behind.
- Country (address) combobox: clicking an option triggered a server error dialog ("An application error occurred"). Fix: type into the combobox (`fill('')` then `pressSequentially('<first letters of your country>')`), wait ~1.5 s, click the exact visible option. Accept the error dialog if it appears; the rest of the form survives.
- There are two comboboxes named "Language": the page UI language picker at the top and the Languages section row. Scope to `getByRole('group', { name: 'Languages' })`.
- Phone Number: country prefix without "+" (help text: "46 xxxxxxxxx instead of +46 xxxxxxxxx").
- Dates: MM/DD/YYYY text inputs; `fill()` works.
- Field of Study is a fixed list (no "Computer Engineering"); typing filters but does not accept free text.
- Certifications rows: Name, Description and Issue Date are required; Institution and Expiration optional.
- Repeating sections: "Add <section>" button appends a row; fill row i via `.nth(i)` locators scoped to the section group.
- "Save" collapses all sections; click "Expand all sections" again before further edits.
- Required-empty check before Apply: `input[aria-required="true"]` with empty value.

## Uploads
- My Documents: Resume/CV (required), Cover Letter, Additional Attachments. Each opens a "Select a source for your file upload" dialog -> "Upload from Device" -> file chooser -> `browser_file_upload` with absolute path. Success text: "<file> File uploaded successfully."
- Uploading did not parse the CV into the profile sections (Work Experience etc. stayed as entered).

## Known traps
- Snapshots leak typed passwords (see Account creation).
- Address Country dropdown click -> application error dialog; use type-ahead instead.
- Option-list reads lag if a previous dropdown is still open.

- Clicking "Apply now" with a JS `el.click()` from the RMK job page can land on "An error occurred while processing your request". Use a real Playwright click on the visible button (one tenant showed an "Apply now" button that opens an "Apply Now" menu item first).
- Cookie banners (`.cookiemanager`) block clicks; removing them from the DOM works.
- Some tenants use one combined page: account fields + documents + questions + data-privacy dialog + "Apply". Text questions are `textarea#fbjq_question_N` (list textareas too, not just inputs). Length limits are only reported after Apply (e.g. 400 / 50 / 50 chars).
- After Apply these tenants send an email one-time passcode (`#passcode`). On some tenants the codes reach Gmail and can be typed, on others they never arrive. Every failed validation re-renders the page and drops uploaded files, the confirm password and the privacy acceptance: re-check all three before each Apply.
- Browser autofill can pre-fill password / passcode fields; clear them first. Never dump input values without excluding `type=password`.
- Combobox (rcmpaginatedselect) options: click, type a few letters slowly, then click `[role=option]`. Dependent fields (University after Country, disability after consent) stay disabled until the parent is set.

## Run log
