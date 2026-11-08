# PeopleCore (peoplecore.my.salesforce-sites.com/recruit)

- Last used: (not yet)
- Account needed: passwordless. Register once, then sign in with a 6-digit email code from `peoplecore@<employer>.com` (valid 15 min)
- Typical flow: `fRecruit__ApplyJob?vacancyNo=VN...` -> Apply -> Register (or Login with email) -> code -> open `fRecruit__Apply?vacancyNo=...` -> questions + resume -> Submit Application -> My Application row "Application No 2026.10 #NNNNN, Status New".

## Field mechanics
- Visualforce ids. Register rows are `...:j_id209:<row>:j_id210:...` and apply rows are `...:j_id205:<row>:j_id206:j_id219`. Address line 2 is required.
- "Availability to start" has maxlength 20 ("Immediately"). "Desired basic salary" is numeric only (no currency text).

## Known traps
- On the code screen, do not click buttons by a loose regex: one click hit "Go back" to registration. Use `input[id$="pinInput"]` and `input[id$="submitButton"]`.

## Run log
