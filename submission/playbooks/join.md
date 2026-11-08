# JOIN (join.com/companies/<co>/<id>)

- Account needed: passwordless candidate account. Enter email, then JOIN emails a "Sign in and continue" magic link (from noreply@join.com, valid 60 min). Read it with the Gmail connector and open it (join.com domain only).
- Flow: job page "Apply now" -> /apply/authentication (email) -> magic link -> /apply/cv (a stored CV from earlier applications may be pre-attached, so "Remove file" and upload the tailored one) -> /apply/coverLetter -> /apply/question-N (one question per page: free text, date picker, A/B radio) -> review -> success.
- Trap: Continue on the last question went straight through review to "Application sent". Only answer the questions once everything is final.
- Date picker: the grid shows trailing days of the previous month, so click the LAST matching day number for the current month.

## Run log
