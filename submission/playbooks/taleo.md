# Taleo (<co>.taleo.net/careersection)

- Account needed: yes (username + password + email, "New User" on the login page)
- Typical flow: privacy notice "I Confirm" -> login or register -> Resume Upload (parses) -> Personal Information -> Education and Experience -> Attachments -> EEO -> eSignature -> Review and Submit. "Save and Continue" saves each step, and drafts appear under My Jobpage > My Submissions.

## Field mechanics
- Residence location is a cascade of three selects (Country -> Province -> Region). Wait about 2 s after each.
- Parsed experience is unreliable (an employer was set to a role name). Fix each row. Job Title has a 50-character limit, reported only after Save.
- Attachments: `input[id$="AttachedFilesBlock-uploadedFile"]` + comment + "Attach". Keep the parsed CV ticked as the Resume.

## Known traps
- The eSignature page requires typing the candidate's full name, which is a legal signature. Leave it for the user. "Save as Draft" on that page also needs the name, but the earlier steps are already saved as a draft.

## Run log
