# SmartRecruiters (jobs.smartrecruiters.com)

- Account needed: no (guest "Easy Apply" at `/oneclick-ui/company/<co>/publication/<uuid>`)
- Typical flow: posting -> "I'm interested" -> one-page form -> Submit -> `/success` "Application submitted!"

## Field mechanics
- Fields are `spl-*` web components with open shadow roots, and each id exists twice (host and inner input). Target the inner element, e.g. `input#first-name-input`, `textarea#hiring-manager-message-input`, `input#spl-form-element_N`.
- City is an autocomplete whose options render empty text to Playwright. Type the city, then ArrowDown + Enter.
- Phone country: click the `combobox "Country code"` (find it with browser_find), fill `input[aria-label="Search by country/region or code"]`, then ArrowDown + Enter.
- Two file dropzones. `spl-dropzone-file-input-2` is the top autofill parser (skip it). `spl-dropzone-file-input-1` is the Resume section.
- "Message to the Hiring Team" takes the full cover letter text (`tools/letter_text.py <ws> --js ...`).

## Run log
