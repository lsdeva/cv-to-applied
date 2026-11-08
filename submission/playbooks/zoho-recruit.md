# Zoho Recruit (<company>.zohorecruit.com)

- Account needed: no ("Easy Apply" sign-in optional)
- Typical flow: job page -> "I'm interested" -> single form: Basic Info (first, last, email, contact number with flag/country-code dropdown), Current Address (City lookup, Province, Country), custom fields (e.g. Dutch proficiency), Social Links, Attachment Information (Resume required, Photo, Cover Letter), **image CAPTCHA**, "Submit Application".

## Field mechanics
- Field ids are `rec-form_<n>`; each id appears twice (a `crux-*` component and a `<template>`), so target `input[id="rec-form_<n>"]:visible` or `[id="rec-form_<n>"] input:visible`. Labels are not linked with `for`.
- Country code: click `.flag-drop-code`, type in the search box, click the country `li`.
- City is a lookup that offers "Locality, City, Country - postcode" suggestions and replaces the value with the locality; typing plain "<city>" then Escape keeps free text.
- File inputs: `input[type=file]` index 0 = autofill resume (optional, parses), 1 = Resume, 2 = Photo, 3 = Cover Letter; `setInputFiles` works and shows a truncated filename chip.

## Known traps
- Image CAPTCHA before submit: the user types it and clicks Submit. Confirmation arrives by email (recruit@<company>) rather than on the page.

## Run log
