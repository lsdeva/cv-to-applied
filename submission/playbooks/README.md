# ATS Playbooks

One file per applicant-tracking system / careers platform (`workday.md`, `smartrecruiters.md`,
`breezy.md`, `oracle-hcm.md`, `zoho-recruit.md`, `linkedin-easy-apply.md`, `successfactors.md`,
`greenhouse.md`, ...). `/submit` reads the matching playbook before touching a form and updates
it after every run, so each platform gets faster and needs fewer interventions.

Playbooks hold **platform mechanics only**: page order, how fields behave, upload quirks, what
breaks. Personal answers live in `../answers.md` (gitignored), never here.

## How to identify the platform

| URL contains | Playbook |
|---|---|
| `myworkdayjobs.com`, `wd1/wd3/wd5.myworkdayjobs` | `workday.md` |
| `smartrecruiters.com` | `smartrecruiters.md` |
| `join.com` | `join.md` |
| `jobs.ashbyhq.com` | `ashby.md` |
| `teamtailor.com` | `teamtailor.md` |
| `breezy.hr` | `breezy.md` |
| `oraclecloud.com/hcmUI/CandidateExperience` | `oracle-hcm.md` |
| `zohorecruit.com` | `zoho-recruit.md` |
| `linkedin.com/jobs` (Easy Apply button) | `linkedin-easy-apply.md` |
| `successfactors`, `jobs.sap.com`, `career*.sapsf` | `successfactors.md` |
| `greenhouse.io`, `boards.greenhouse` | `greenhouse.md` |
| `lever.co` | `lever.md` |
| `ashbyhq.com` | `ashby.md` |
| `icims.com` | `icims.md` |
| `taleo.net` | `taleo.md` |
| `pinpointhq.com` | `pinpoint.md` |
| `workable.com` | `workable.md` |
| `salesforce-sites.com/recruit` (PeopleCore) | `peoplecore.md` |
| Avature (employer-branded apply sites, e.g. `apply.<employer>.com`) | `avature.md` |
| Eightfold (`careers.<employer>.com/careers/apply?pid=`) | `eightfold.md` |
| `recruitingbypaycor.com` (Paycor / Newton) | `paycor.md` |
| `cloud.infor.com/lmghr/CandidateSelfService` | `infor-css.md` |
| `bamboohr.com/careers` | `bamboohr.md` |
| `jobs.personio.de` | `personio.md` |
| anything else | `<host>.md` (create it) |

## Playbook template

```markdown
# <Platform>

- Last used: (not yet)
- Account needed: yes/no (login method; the user logs in manually, credentials are never stored)
- Typical flow: 1. ... 2. ... 3. ...

## Field mechanics
- <field>: <how it behaves; e.g. "Country is a type-ahead: type your country, wait, pick the option">

## Uploads
- <how the CV/cover-letter upload works; whether it parses the CV and pre-fills fields to re-check>

## Known traps
- <what failed and the fix>

## Run log

> Note: some playbooks mention helper scripts such as `wd_myinfo2.js` or `gh_basic.js`. Those came from an earlier private setup and are not included here. Treat them as descriptions of the steps to take with the Playwright tools.
