# Pinpoint (<employer>.pinpointhq.com)

- Last used: (not yet)
- Account needed: no
- Typical flow: `/postings/<uuid>/applications/new` is a single page -> SUBMIT APPLICATION -> `/applications/thanks?token=...` "Your application was received successfully."

## Field mechanics
- Text inputs are named `application_form[application][...]`. Custom questions are `answers_attributes][N][text_answer]` textareas (Notice period, Current compensation, Compensation expectation).
- Dropdowns are react-select. The visible `input[role=combobox]` (id like `application_form_equality_monitoring_gender`) sits under a placeholder div, so `click()` times out. Use `focus()`, type, then click the `.react-select__option` whose text equals the target. Setting the hidden `<select>` mirror does not update the widget.
- Country is a react-select sharing its id with a hidden select. Target `input[role=combobox][id="application_form[application][country]"]`.
- Consent checkbox: `#application_process_information` (a hidden input shares the name).

## Uploads
- CV: `input[name="application_form[application][cv]"]`. No cover letter field.

## Run log
