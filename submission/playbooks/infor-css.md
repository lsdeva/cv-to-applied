# Infor Candidate Self Service (`*.cloud.infor.com/lmghr/CandidateSelfService`)

- Account needed: yes (Register: email, first/last, password, "Fill in content by hand" -> Begin). The wizard then requires account security questions. Set them only with the user's say-so, using `tools/security_answers.py <site> "<q1>" ...` (random answers stored in the secrets file, served once). Note: the site sends the answers as GET query params, so they appear in network logs. Never dump network requests after setting them.
- Typical flow: job page (iframe `parentIframe`) -> Apply/Continue -> Application Tasks (Attachments, Contact Information, Education, Employment History, Licenses and Certifications, Questions, Self ID, External Talent Agreement, Attestation) -> Submit Application ("How did you hear" + Additional Information lookup).

## Known traps
- At desktop width the task pane shows "Unsupported type for composite form tab area", and Submit fails with "All tasks must be completed". Resize the viewport to about 760px and the task list renders.
- Dropdowns: Infor `selectedSingle` anchors (`#<name>Container > .selectedSingle`). Escape closes the whole dialog.

## Run log
