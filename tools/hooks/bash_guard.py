#!/usr/bin/env python3
"""PreToolUse hook for Bash: block shell patterns that hang or clobber files.

Why: a drafting agent once wrote a letter with `cat > file <<EOF`, the heredoc never
closed and `cat` waited on stdin for over two hours, burning the session. Files should
be written with the Write/Edit tools instead.

Blocked:
  cat > file / cat >> file / cat <<EOF      (write files with the Write tool)
  tee file                                  (same)
  a bare `cat` with no input                (waits on stdin forever)
Allowed: reading with cat (`cat file`, `cat a b | grep`), `python - <<'EOF'` scripts,
everything else.

Exit 2 with a message on stderr blocks the call and tells the agent what to do instead.
It never approves anything, and on malformed input it lets the call through.
"""
import json
import re
import sys

RULES = [
    (re.compile(r"(^|[;&|(]\s*|\bthen\s+|\bdo\s+)cat\s*(>>?|<<)"), "cat > file / cat <<EOF"),
    (re.compile(r"(^|[;&|(]\s*)cat\s+<<"), "cat <<EOF"),
    (re.compile(r"\|\s*tee\s+(-a\s+)?[^\s|&;-]"), "tee file"),
    (re.compile(r"(^|[;&(]\s*)cat\s*($|[;&)])"), "bare cat (reads stdin)"),
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001  malformed input: never block on our own bug
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = (data.get("tool_input") or {}).get("command") or ""
    for rx, what in RULES:
        if rx.search(cmd):
            print(f"Blocked by tools/hooks/bash_guard.py: `{what}` can hang on stdin or clobber files. "
                  "Write or edit files with the Write/Edit tools, then pass the file path to the script "
                  "(e.g. posting_guard.py --in <file>). Add `</dev/null` and `timeout 300` to commands that "
                  "might wait.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
