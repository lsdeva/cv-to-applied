# Workday (myworkdayjobs.com)

- Account needed: yes, one per tenant (email + password, then email verification link)
- Typical flow:
  1. Find the req on `<tenant>.wd<N>.myworkdayjobs.com/<site>?q=<req number>` (LinkedIn's Apply button needs a LinkedIn login; skip it).
  2. Job page -> "Apply" -> dialog: Autofill with Resume / **Apply Manually** / Use My Last Application. Apply Manually avoids parser errors.
  3. Create Account (email, password, verify password) -> "An email has been sent to you. Please verify your account." -> open the link from `<tenant>@otp.workday.com` ("Verify your candidate account", expires 24 h) -> "Account Activated" -> Sign In.
  4. Steps: My Information -> My Experience -> Application Questions -> Voluntary Disclosures -> Review. "Save and Continue" (`[data-automation-id="pageFooterNextButton"]`) validates each step.

## Account / password
- Password rules: 8+ chars, upper, lower, number, special character.
- Generated per-site passwords live in the system keychain (`tools/portal_password.py`), never in a file. They are served to the page via a one-shot 127.0.0.1 helper and fetched with `page.request.get(...)` inside `browser_run_code_unsafe`, so the value never enters the chat. Never take snapshots while a password field holds a value.
- Sign-in: `fill()` + click on Sign In failed ("wrong email or password"); clearing the fields, typing with `pressSequentially` and pressing **Enter** worked. Workday overlays a click-filter div, so buttons need `click({ force: true })`.
- The verification email can be read with the Gmail connector when the user is away (link must be on the tenant's own myworkdayjobs.com domain).

## Field mechanics
- "How Did You Hear About Us?", Country Phone Code, Field of Study and Skills are multiselect prompts: click the input, `pressSequentially('<text>')`, Enter, then click `[data-automation-id="promptOption"]` with the exact text. Selected values appear as `[data-automation-id="selectedItem"]` pills. An open prompt popup intercepts clicks: click a neutral spot (`page.mouse.click(5, 300)`) to close it.
- Single-select dropdowns: `button[aria-haspopup="listbox"]` -> `[role=option]`. The first such button on the page is the account menu ("Change Email"); skip it.
- Radios (e.g. "previously worked for ..."): Playwright `check()` reports no state change; click the label (`label[for=<id>]`) or the parent element instead.
- Name: Given Name + Family Name (no middle-name field). "I have a preferred name" checkbox reveals a preferred-name block (pre-filled with the legal name; overwrite it).
- Dates in Work Experience: Month/Year spinbutton inputs reported as "outside of the viewport"; use `locator.focus()` then `page.keyboard.type('08')`. "I currently work here" removes the end-date inputs for that row; address rows by id prefix (`workExperience-<n>--`).
- Application Questions free-text boxes: conditional questions appear after answers (e.g. "Are there any restrictions or limitations on your right to work..." after "authorized to work? No"), which shifts box indexes. Always map a box to its label (`closest('[data-automation-id^="formField"]')`) before filling.

## Uploads
- My Experience -> Additional Documents (required): `input[type=file]` accepts several files at once via `setInputFiles([...])`; shows "Successfully Uploaded!" per file.

## Finding a req the site search misses

## Existing accounts
- If the email already has an account on the tenant, "Create Account" silently lands on Sign In with no message and sign-in with the new password fails. Use "Forgot your password?" -> email from `<tenant>@otp.workday.com` (link valid 2 h) -> set the stored generated password -> "Password has been reset".

## Confirmation
- After Submit, Workday lands on Candidate Home (`/jobTasks/completed/application`) with "Thank you for completing the questionnaire..." and the application row (Job Req, status "In Process", date). No reference number beyond the Job Req.


## Option matching (bug found 2026-10-27)

## Run log
