# Avature (employer-branded apply sites such as `apply.<employer>.com`)

- Account needed: yes, created inside the apply flow (Upload CV -> Register -> questions)

## Field mechanics
- Field names are numeric ids (`[name="1376"]`). Some selects are select2 widgets with empty native options. Click `.select2Container<id>` and pick from `.select2-results__option`.
- The CV selector (`select#fileInput_<id>_oldFilesSelector`) can reset to "Upload a new file" after other fields change. Re-select the uploaded CV before Next.

## Run log
