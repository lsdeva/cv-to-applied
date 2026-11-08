# Paycor Recruiting / Newton (recruitingbypaycor.com)

- Account needed: no
- Typical flow: the employer careers page embeds a `recruitingbypaycor.com` iframe -> "Apply for this Position" (text link inside the iframe) -> one long SubmitResume form -> "Submit" -> ShowConfirmation.action "Your information has been uploaded successfully."

## Field mechanics
- Navigating straight to the iframe URL redirects back to the parent page, so work inside `page.frames().find(f => /recruitingbypaycor/.test(f.url()))`.
- Resume upload (`fileUpload`) parses and prefills name, email, phone and three employers (dates as YYYY-MM-DD or MM/DD/YYYY; fields want MM/YY).
- Custom fields are named `gnewton_section_<S>_question_<Q>_answer`. Radios have values `gnewton_answer_img_yes/no`. Setting values in-page with `evaluate` plus change events works.
- Country = <country> disables the US-only State select.
- Required extras: high school name/city/graduate, desired compensation, start date, typed signature + date, disclaimer and CCPA checkboxes.

## Run log
