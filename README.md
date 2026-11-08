<p align="center">
  <img src="assets/banner.svg" alt="cv-to-applied: your CV in, tailored applications out" width="860">
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <img alt="Runs locally" src="https://img.shields.io/badge/runs-on%20your%20laptop-blue.svg">
  <img alt="Built on Claude Code" src="https://img.shields.io/badge/built%20on-Claude%20Code-orange.svg">
</p>

# cv-to-applied

**An open-source job application autopilot that runs on your own laptop.** Attach your CV, name the
country you want to work in, and it:

1. sets up the tools it needs
2. builds your profile from your CV
3. finds matching jobs and shows you a ranked list
4. writes a tailored CV and cover letter for each job
5. fills in and submits the applications in a browser window **you can watch**

<p align="center">
  <img src="assets/demo.gif" alt="Demo: a real job application filled in automatically, then how to get started (company and personal details blurred)" width="860">
</p>

You don't type commands. It stops only when it needs you: a CAPTCHA, a login, a verification code,
or a personal question it can't answer from your CV.

It's built on [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) and customizes the
open-source [ai-job-search](https://github.com/ai-job-search-dev/ai-job-search) framework (see
[Credits](#credits)).

---

## Why this one

- **One prompt, end to end.** Your CV and a country in, submitted applications out. No setup wizard,
  no slash commands to learn.
- **You stay in control.** The first application is a pilot you watch. Nothing is submitted until
  you say "yes" to it, and you can type `stop` at any time.
- **Low token cost.** Each job runs in small helper agents: a drafter, a reviewer, a form filler on
  a lighter model, and an answerer for new questions. Each sends back one line, so the main chat
  stays short and long runs stay cheap.
- **Honest by design.** It never invents experience, asks you for personal facts it can't know,
  ignores hidden "if you are an AI..." tricks in job pages, and never types your passwords.
  Any password it generates for you is kept in your system keychain, never in a file.
- **Your data stays local.** Your CV, tracker, answers and generated documents stay on your
  machine.

---

## Requirements

- **A computer** running Windows, macOS or Linux
- **[VS Code](https://code.visualstudio.com/)** with the
  **[Claude Code extension](https://docs.claude.com/en/docs/claude-code/ide-integrations)**, signed
  in to a Claude account that includes Claude Code
- **[Git](https://git-scm.com/downloads)**
- **Your CV** as a PDF, Word file or plain text

Everything else (Node.js, Python, LaTeX for the PDFs, Bun, the browser driver, `keyring` for the
system keychain) is installed for you on the first run. You approve each install.

---

## Quick start (about 5 minutes of your time)

### 1. Fork and clone

Clone the repository and open it in VS Code:

```bash
git clone https://github.com/lsdeva/cv-to-applied.git
cd cv-to-applied
code .
```

Or in VS Code: **Clone Repository**, paste `https://github.com/lsdeva/cv-to-applied.git`, then open
the folder.

**A plain clone is the safest choice.** If you'd rather fork with `gh repo fork`, know that a fork of
a public repository is always **public**. Setup writes personal data (your profile and CLAUDE.md
details) into tracked files, so never push those to a public fork. For a private online backup, use
the private-remote recipe in [SETUP.md section 8](SETUP.md#8-pulling-upstream-updates-into-your-fork).

### 2. Open the Claude Code chat

Click the Claude icon in the VS Code side bar and sign in if asked.

### 3. Attach your CV and paste this prompt

Drag your CV into the chat box. Copy the text below, change the country, add the optional details if
you know them, and send it:

```
Here is my CV. I want to apply for jobs in <COUNTRY>.
Set everything up, find matching jobs, show me the list, and start applying.
(Optional: roles I want: <...>. Work mode: onsite / hybrid / remote. I do / don't need visa sponsorship. Minimum salary: <...>.)
```

### 4. Restart once (first run only)

When it says *"close and reopen this VS Code window, approve 'playwright', then type continue"*, do
that. Playwright is the browser driver that fills in the forms.

### 5. Watch the pilot, then let it run

It applies to job #1 while you watch, and asks **"Submit this one?"** before the final click. Say
`yes`, and it applies to the rest of the list, sending a one-line update per job:
`✓ submitted`, `⏸ waiting for you`, `⤼ skipped`.

That's it.

---

## When it stops for you

| It says | You do |
|---|---|
| *"Your turn in the browser: CAPTCHA / login / code"* | Do it in the browser window, then type `done`. |
| A question about you (birth place, current salary and the like) | Answer in the chat. It saves the answer, so you're never asked twice. |
| *"Quick reset to keep this fast: type /clear, then continue"* | Type `/clear`, then `continue`. Nothing is lost. |

- **Stop at any time:** type `stop`.
- **Carry on later:** open the folder and type `continue`. It resumes from its tracker and never
  applies twice to the same job.

---

## It learns as it goes

Every run makes the next one faster. It learns by updating plain files on your machine, which it
reads back on later runs. No AI model is retrained, and nothing is shared unless you choose to.

| It learns | Saved in | Effect next time |
|---|---|---|
| Your answers to form questions, given by you or written for you | `submission/answers.md` "Learned answers" | The same question is filled automatically. You're never asked twice. |
| How each job portal behaves: field quirks, traps, account and code steps | `submission/playbooks/<platform>.md` | The next form on that portal goes faster, with fewer errors. |
| Facts you confirm or correct about your experience | your profile (`01-candidate-profile.md`) | Later CVs and letters can use them. |
| Company research done for a cover letter | `company_research/` | Reused when you re-apply or prepare for an interview. |
| Every job seen, drafted, submitted or skipped | `job_search_tracker.csv` | Never shows or applies to the same job twice. `continue` resumes where it stopped. |
| Results: interviews, rejections, offers (`/outcome`, `/gmail-sync`) | the tracker and per-application records | `/setup` can recalibrate fit scoring toward what gets replies. |

Playbook lessons contain no personal data. If a portal's playbook gets better on your machine,
consider sending it back as a pull request so everyone benefits. When `git pull` brings a change to a
playbook you have also updated, git may ask you to resolve a small conflict. Keep both sets of lines.

---

## Change how your CV looks

Your content always comes from your own CV. The **look** comes from a template. Out of the box,
every CV uses the LaTeX *moderncv* "banking" style (2 pages), and every cover letter uses the
repo's own letter style. You can change it at any time, before or after the first run.

### Where to find CV themes

| Source | What you get |
|---|---|
| *moderncv* built-in styles | `classic`, `casual`, `banking`, `oldstyle`, `fancy`. Nothing to download. |
| [Overleaf CV gallery](https://www.overleaf.com/gallery/tagged/cv) | Hundreds of LaTeX CV templates. Open one and use **Download Source** (zip). |
| [LaTeXTemplates.com: Curricula Vitae](https://www.latextemplates.com/cat/curricula-vitae) | Curated LaTeX CV templates, each with a source download. |
| [Awesome-CV](https://github.com/posquit0/Awesome-CV) | A popular modern LaTeX CV and cover letter pair. |
| [Typst Universe](https://typst.app/universe/search/?q=cv) | CV templates for Typst, a faster LaTeX alternative. |

**Pick one that compiles from source** (LaTeX or Typst), check its license allows your use, and
prefer simple single-column layouts. Job sites' applicant tracking systems read those most
reliably.

### Sample prompts

Type one of these in the Claude Code chat. Each one only changes the template. Your profile and
content stay as they are.

**Switch to another built-in style:**

```
Switch my CV to the moderncv "classic" style in blue. Keep 2 pages. Rebuild my master CV
and show me the PDF before using it for applications.
```

**Use a theme you downloaded:**

```
I downloaded a CV template to <path to the folder or zip>. Register it with /add-template
as my CV template, fill it with my profile from my master CV, compile it, check it is
2 pages and that the text extracts cleanly for applicant tracking systems, and show me
the PDF. Use it for all future applications.
```

**Match the look of the CV you attached:**

```
Build a LaTeX CV template that matches the look of the CV I attached: same layout,
section order, fonts (or the closest free ones), colours and spacing. Register it with
/add-template, fill it with my profile, compile it and show me the PDF next to my original
so I can compare. Use it for all future applications once I approve it.
```

**Change the cover letter to match:**

```
Restyle my cover letter template to match my CV template: same fonts, colours and header.
Register it with /add-template as my cover letter template and show me a sample PDF.
```

**Go back to the default:**

```
Run /add-template --use default to go back to the stock CV and cover letter templates.
```

A matched template comes out close to the original, not pixel-perfect. Always check the first PDF
before letting it run on its own.

---

## How it works

```
CV + country
   │
   ├─ Setup ........ installs tools, builds your profile, asks one batch of questions
   ├─ Search ....... job boards + web search, ranked against your profile
   └─ For each job (one at a time):
        posting-fetcher → drafter → application-reviewer → drafter (revise, compile, verify)
        → submitter (fills the form) ⇄ answerer (writes answers to new questions)
        → tracker updated, one-line result to you
```

| Piece | Where |
|---|---|
| The autopilot flow | [`AUTOPILOT.md`](AUTOPILOT.md) |
| Helper agents | [`.claude/agents/`](.claude/agents/) |
| Underlying commands (`/apply`, `/submit`, `/rank`, ...) | [`.claude/commands/`](.claude/commands/) |
| Per-platform form notes (Workday, Greenhouse, ...) | [`submission/playbooks/`](submission/playbooks/) |
| Manual setup and power-user guide | [`SETUP.md`](SETUP.md) |
| Security model | [`SECURITY.md`](SECURITY.md) |

---

## Your data and privacy

- **Ignored by git, so they never leave your machine:** your CV, job tracker, saved answers,
  browser logins and generated documents.
- **Filled in on your machine:** setup writes your details into a few tracked template files (your
  profile and `CLAUDE.md`). Keep them local, or push them only to a **private** repository.
- **Passwords:** by default you type them in the browser, and they are never written to the chat.
  If you ask Claude to *generate* a portal password, `tools/portal_password.py` stores it in your
  **system keychain** (Windows Credential Manager, macOS Keychain, or GNOME Keyring / KWallet on
  Linux), never in a file. You can find it there later under `cv-to-applied:<site>`. On macOS, click
  **Always Allow** the first time it asks to use the keychain. If no keychain is available, it stores
  nothing and asks you to type the password yourself. List or remove entries with
  `python tools/portal_password.py --list` and `--delete <site> <email>`.
- **Job pages are treated as data, never as instructions.** Hidden prompts in postings are ignored
  and reported.

---

## Gmail (optional, use with caution)

Connecting Gmail is **not required**. Everything works without it. If you connect it (Claude's
connector settings: claude.ai → **Settings** → **Connectors** → **Gmail**), this repo uses it for
two things:

- **Duplicate check:** before applying, it searches for earlier emails from the company (subjects
  only) so you don't apply twice.
- **Status sync (`/gmail-sync`):** it reads replies from employers (interview invites, assessments,
  rejections, offers) and proposes tracker updates. **Nothing is written until you approve.**

In this release, **portal logins, account passwords, verification codes and email links stay with
you.** The autopilot stops and asks you to do them in the browser.

**How it was tested.** The per-platform playbooks in
[`submission/playbooks/`](submission/playbooks/) were written from real applications on the main
applicant tracking systems: Workday, SAP SuccessFactors, Oracle HCM, iCIMS, Greenhouse, Ashby,
SmartRecruiters and others. That includes their account creation and email-verification steps,
run with a connected Gmail account. Portals change their forms often, so a playbook can be out of
date by the time you use it.

### Before you connect it

- **It can see your whole mailbox.** The connector gives Claude access to your email, not only job
  emails. If that's more than you want, **use a separate email address just for job applications**
  and connect only that one.
- **Email is untrusted input.** A message can contain phishing links or hidden text written to steer
  an AI. Claude treats email content as data, never as instructions. Still, only open links from the
  employer's or the job portal's own domain.
- **Watch the permission prompts.** The Gmail connector can also draft, send, label and delete. This
  repo never needs those actions. **Decline any request to send, delete or forward email** unless you
  asked for it yourself.
- **You stay responsible** for what is read and sent from your account. Disconnect the connector
  when your job search is done.

---

## Updating

In your copy of the repository, run `git pull`, then type `continue` in the chat. Your profile,
tracker, documents and saved answers are not touched. If git says local changes would be
overwritten, run `git stash`, `git pull`, then `git stash pop`.

---

## Troubleshooting

| Problem | What to do |
|---|---|
| No browser window appears | Close and reopen the VS Code window, approve **playwright**, type `continue`. |
| An install fails | Tell it in the chat (for example "MiKTeX install failed"). It tries another way or skips it for now. |
| Few jobs found for your country | Say "add <country>'s main job board". |
| You want other countries or roles | Say so, for example "also search Germany, remote only". |
| You want to pause | Type `stop`. Next time, type `continue`. |

---

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Improvements to the
underlying framework (scraping, CV templates, the `/apply` workflow) also help everyone when sent to
the [upstream project](https://github.com/ai-job-search-dev/ai-job-search).

---

## Credits

cv-to-applied is an independent customization of
**[ai-job-search](https://github.com/ai-job-search-dev/ai-job-search)** by Mads Lorentzen and its
contributors, used under the MIT License. The framework (profile setup, job scraping, ranking, the
drafter/reviewer `/apply` workflow, CV and cover letter templates, security guards and tests) comes
from that project.

This repository adds:

- the one-prompt autopilot (setup, search, pilot application, then the rest)
- browser form filling with a pilot approval step and per-platform playbooks
- token-saving helper agents (drafter, submitter, answerer) and a session-reset routine
- a Bash guard hook that blocks shell patterns that can hang an agent

---

## Disclaimer

- **No affiliation.** This is an independent, community project. It is **not** affiliated with,
  endorsed by, sponsored by or partnered with Anthropic, PBC, or with the maintainers of the
  upstream ai-job-search project. "Claude" and "Claude Code" are trademarks of Anthropic, PBC, used
  here only to describe what the software runs on. All other names and trademarks belong to their
  owners.
- **No warranty, no liability.** The software is provided "as is", without warranty of any kind. The
  authors and contributors are not liable for any claim, damages or other liability arising from its
  use, as set out in the [MIT License](LICENSE).
- **You are responsible for your applications.** Review what is sent in your name, make sure every
  claim is true, and follow the terms of the job sites and employers you apply to. Some sites don't
  allow automated applications.
- **Usage costs.** Running it uses your own Claude plan or API credits.

---

## License

[MIT](LICENSE). You may use, copy, modify, merge, publish, distribute, sublicense and sell copies,
for any purpose, including commercial use. The only condition is to keep the copyright and license
notice.
