# Eightfold (careers.<employer>.com/careers)

- Last used: (not yet)
- Account needed: no
- Typical flow: `/careers/job/<pid>` -> "Apply now" (`/careers/apply?pid=<pid>`) -> single page (Resume, Contact Information, Export Control, Diversity, Contact Consent, Position Specific Questions) -> "Submit application" -> `/careers/apply/success` "Thank you for your application, <name>!"

## Field mechanics
- Cookie banner: `#truste-consent-required` (Decline all).
- Resume: click "Select file - Upload resume", then browser_file_upload. A "Data Privacy Agreement" dialog follows and the upload only completes after "I Acknowledge". The parse fills name, email and phone.
- Dropdowns are comboboxes `#input-N`: click, optionally type, then click `getByRole('option', {name, exact: true})`. Picking a country reveals a State/Province combobox ("Not Applicable" for <country>).
- Export Control lists only restricted countries plus "Other".
- Some tenants have no cover letter field.

## Run log
