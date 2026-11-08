# Personio (<company>.jobs.personio.de/job/<id>)

- Account needed: no
- Typical flow: job page -> Apply -> `/job/<id>/apply` single form (first_name, last_name, email, phone, location, available_from, custom_attribute_<n> fields such as LinkedIn/GitHub/expected salary) -> file inputs `documents.cv` and `documents.other` (cover letter) -> "Send application" -> "THANK YOU. We have received your application".

## Field mechanics
- Plain inputs with `name` attributes; `fill()` works. Salary fields are free text (enter digits only).
- No CAPTCHA seen.

## Run log
