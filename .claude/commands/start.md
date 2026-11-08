---
description: One-time onboarding - check tools, set up the visible browser, build your profile from your CV, pick target countries, and get ready to apply
---

# /start - one-time setup (run once, re-run anytime to fix something)

You're onboarding a new user on their own laptop. Keep it smooth: do the checks yourself, ask only
what you need, one short question at a time, and explain in plain language. Never commit or push the
user's personal data unless they explicitly ask.

## Step 1: Check the laptop (fix what you can, explain the rest)

Detect the OS (`uname -s` or `ver`). Check each item, and for anything missing, give the exact install
command for that OS and wait for "done":
- **git**, **Node.js 18+** (`node -v`, `npx -v`) for the browser server.
- **Python 3.10+** (`python3 --version` or `python --version`), then `pip install pypdf`.
- **A LaTeX distribution with `lualatex`** for compiling the CV and cover letter.
  - Windows: MiKTeX (https://miktex.org/download), with "install missing packages on the fly = Yes".
  - macOS: `brew install --cask mactex-no-gui`.
  - Linux: `sudo apt install texlive-luatex texlive-latex-extra texlive-fonts-extra`.
- **Bun** for the job-board search tools.
  - macOS / Linux: `curl -fsSL https://bun.sh/install | bash`.
  - Windows: `powershell -c "irm bun.sh/install.ps1 | iex"`.
  - Then run `bun install` inside each `.agents/skills/*/cli/` folder that has a `package.json`.
- **A browser:** Google Chrome on macOS/Linux, Microsoft Edge on Windows (already installed there).

## Step 2: Visible browser (so you can watch every application)

- **Windows:** copy `.mcp.windows.json` over `.mcp.json` (it uses `cmd /c npx` and Edge), then run
  `git update-index --assume-unchanged .mcp.json` so the swap is never committed.
- **macOS / Linux:** keep `.mcp.json` (Chrome).
- If `mcp__playwright__*` tools are NOT available in this session, say: "Please restart Claude Code in
  this folder and approve the **playwright** server when asked, then type `/start` again." Then stop.
- If they are available: open `https://example.com` and ask "Do you see a browser window? (yes/no)".
  Close it after a yes. Logins you do in this window are remembered in `submission/browser-profile/`
  (gitignored).

## Step 3: Your CV, then your profile

Ask: **"Please put your current CV (PDF or Word) in the `documents/cv/` folder, or drag it into this
chat. Add your LinkedIn export to `documents/linkedin/` too if you have one. Type done."**

Then run the profile builder: follow `.claude/commands/setup.md`.
- **Path A** if files are in `documents/`.
- **Path B** if the CV was pasted or attached.

Do it all in this run, without asking the user to type `/setup` separately. Ask the follow-up questions
setup.md needs (behaviour, goals, deal-breakers, languages and levels, salary expectations), kept
short.

## Step 4: Where to apply

Ask together, in one message:
1. "Which country or countries do you want to apply in?" (several are fine)
2. "Onsite, hybrid or remote? If remote, from which country will you work?"
3. "Do you already have the right to work there, or do you need visa sponsorship?"
4. "Which roles or job titles should I search for?" (suggest 3-5 from the CV)
5. "Minimum salary, and in which currency?"

Then:
- Write the answers into CLAUDE.md (location tiers, target countries, work authorisation, deal-breakers),
  into `.claude/skills/job-scraper/search-queries.md` (titles and locations), and into
  `submission/answers.md`.
- **Job boards:** `linkedin-search` and `freehire-search` are on by default. If a target is Denmark,
  enable the four Danish portal skills (`enabled: true`). For any other country, offer `/add-portal`
  for its main local job board, and say WebSearch covers the rest meanwhile.
- If sponsorship is needed, add a deal-breaker "role must offer visa sponsorship, or be remote from
  <country>" and make sure `/rank` treats "must already have the right to work" as a skip.

## Step 5: Answer bank and tracker

- Copy `submission/answers.example.md` to `submission/answers.md` (gitignored). Fill in everything
  known from the profile and Step 4. Leave `ASK` where unknown.
- Ask once, optionally: "Want to write a few short stories now for 'describe a time...' questions?
  You can also do it later in `submission/answers.md`."
- Make sure `job_search_tracker.csv` exists with the standard header (the same one `/apply` uses).

## Step 6: Done - show how to use it

Print this, filled in:

> All set, <first name>. Targeting <countries>, <roles>, <work mode>.
>
> **Daily flow**
> 1. `/scrape` finds new jobs.
> 2. `/rank` scores them and makes a shortlist.
> 3. `/apply <job URL>` checks fit, then writes your tailored CV and cover letter.
> 4. `/submit <job URL>` fills the form in the browser you can see. It stops for CAPTCHAs and logins
>    ("solve it, then type done") and for questions it can't answer from your profile. It always asks
>    "Submit now?" before the final click.
>
> Your personal files stay on this laptop (gitignored). Only commit or push them to a **private** repo
> of your own.
