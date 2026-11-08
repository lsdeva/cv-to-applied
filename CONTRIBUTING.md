# Contributing to cv-to-applied

Thanks for helping. Bug reports, platform playbooks and focused pull requests are all welcome.

## Before you open an issue or PR

- **Never include personal data.** Issues and PRs are public. Leave out CVs, profile details, tracker
  rows, saved answers, employer names and screenshots of filled forms. Describe the problem and the
  platform (for example "Workday, the date field on page 3") instead.
- **One concern per PR.** Small, focused changes get reviewed quickly.

## What fits here

- **Autopilot and submission fixes:** the one-prompt flow (`AUTOPILOT.md`), the helper agents
  (`.claude/agents/`), `/submit`, and robustness fixes with the failing case described.
- **Platform playbooks:** mechanics for an applicant tracking system (`submission/playbooks/<platform>.md`).
  Field behaviour, traps and fixes only, never personal data.
- **Token and cost savings** that keep application quality the same.
- **Docs** that close a real gap for a new user.

Changes to the underlying framework (scraping, ranking, CV templates, the `/apply` drafter-reviewer
workflow) help more people when sent to the upstream project,
[ai-job-search](https://github.com/ai-job-search-dev/ai-job-search). Useful upstream changes are
merged here from time to time.

## Checks to run

CI runs these, so run them before you push:

```bash
python3 tools/lint_skills.py
python3 tools/check_framework_version.py
python3 tools/security_guards.py
python3 -m unittest discover -s tests
```

On Windows, use `python` instead of `python3`. In a portal CLI you changed, also run `bun run typecheck`
and `bun test`.

`tools/security_guards.py` fails on any new permission, hook or agent tool it doesn't know. If a new
grant is intentional, add it to the allowlist in that file in the same PR and explain why. See
[SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
