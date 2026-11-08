"""Get-or-create a per-site portal password in the OS keychain, serve it once on 127.0.0.1.

The password lives only in the operating system's credential store: Windows Credential Manager,
the macOS Keychain, or the Secret Service on Linux (GNOME Keyring / KWallet), through the `keyring`
package. It is never printed and never written to a file. A small index of site, login and date
(no passwords) is kept in the gitignored submission/secrets/portal-index.txt, because a keychain
cannot list its entries.

Usage:
  python tools/portal_password.py <site-key> <login-email> [length]   get or create, serve once
  python tools/portal_password.py --list                              sites with a stored password
  python tools/portal_password.py --delete <site-key> <login-email>   remove one entry

The serve step prints `status=<new|existing> port=<n>`. The page fetches http://127.0.0.1:<n>/ once
(within 5 minutes) to receive the password. If no keychain is available the helper stops (exit 3)
and the user types the password in the browser. It never falls back to a plain-text file.

A plain-text store left by an earlier version (submission/secrets/portal-passwords.txt) is moved
into the keychain on first run, each entry is read back to verify it, and the file is then deleted.
"""
import datetime
import http.server
import os
import secrets
import socketserver
import sys

SERVICE_PREFIX = "cv-to-applied:"
SECRETS_DIR = os.path.join("submission", "secrets")
INDEX = os.path.join(SECRETS_DIR, "portal-index.txt")
LEGACY_STORE = os.path.join(SECRETS_DIR, "portal-passwords.txt")
NO_KEYRING = ("keyring is not installed. Run `pip install keyring`, or type the password yourself "
              "in the browser.")
NO_BACKEND = ("No system keychain is available (keyring found no backend). Type the password yourself "
              "in the browser, or use your password manager. Nothing was stored.")


def _keyring():
    try:
        import keyring  # noqa: PLC0415  optional dependency, imported on use
        import keyring.errors  # noqa: F401,PLC0415
    except ImportError:
        print(NO_KEYRING, file=sys.stderr)
        sys.exit(2)
    return keyring


def _service(site):
    return SERVICE_PREFIX + site


def _read_index():
    if not os.path.exists(INDEX):
        return []
    rows = []
    with open(INDEX, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(" | ")
            if len(parts) == 3 and not line.startswith("#"):
                rows.append(parts)
    return rows


def _write_index(rows):
    os.makedirs(SECRETS_DIR, exist_ok=True)
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write("# date | site | login  (no passwords: those are in the system keychain)\n")
        for row in rows:
            f.write(" | ".join(row) + "\n")


def _index_add(site, email):
    rows = [r for r in _read_index() if (r[1], r[2]) != (site, email)]
    rows.append([str(datetime.date.today()), site, email])
    _write_index(rows)


def _index_remove(site, email):
    _write_index([r for r in _read_index() if (r[1], r[2]) != (site, email)])


def generate(length=16):
    upper, lower, digits, symbols = "ABCDEFGHJKLMNPQRSTUVWXYZ", "abcdefghijkmnopqrstuvwxyz", "23456789", "!@#$%*-_"
    chars = [secrets.choice(upper), secrets.choice(lower), secrets.choice(digits), secrets.choice(symbols)]
    chars += [secrets.choice(upper + lower + digits + symbols) for _ in range(max(length, 8) - 4)]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def _store(kr, site, email, pw):
    try:
        kr.set_password(_service(site), email, pw)
        ok = kr.get_password(_service(site), email) == pw
    except kr.errors.KeyringError:
        ok = False
    return ok


def migrate_legacy(kr):
    """Move a plain-text store from an earlier version into the keychain, then delete it."""
    if not os.path.exists(LEGACY_STORE):
        return 0
    entries = []
    with open(LEGACY_STORE, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(" | ")
            if len(parts) >= 4 and not line.startswith("#"):
                entries.append((parts[1], parts[2], " | ".join(parts[3:])))
    for site, email, pw in entries:
        if not _store(kr, site, email, pw):
            print(NO_BACKEND + " The old plain-text file was left in place.", file=sys.stderr)
            sys.exit(3)
        _index_add(site, email)
    os.remove(LEGACY_STORE)
    print(f"migrated={len(entries)} (old plain-text file deleted)", flush=True)
    return len(entries)


def get_or_create(kr, site, email, length=16):
    try:
        pw = kr.get_password(_service(site), email)
    except kr.errors.KeyringError:
        print(NO_BACKEND, file=sys.stderr)
        sys.exit(3)
    if pw:
        return pw, "existing"
    pw = generate(length)
    if not _store(kr, site, email, pw):
        print(NO_BACKEND, file=sys.stderr)
        sys.exit(3)
    _index_add(site, email)
    return pw, "new"


def main(argv):
    if not argv:
        sys.exit(__doc__)
    kr = _keyring()
    migrate_legacy(kr)
    if argv[0] == "--list":
        for date, site, email in _read_index():
            print(f"{date} | {site} | {email}")
        return 0
    if argv[0] == "--delete":
        site, email = argv[1], argv[2]
        try:
            kr.delete_password(_service(site), email)
        except kr.errors.PasswordDeleteError:
            pass
        _index_remove(site, email)
        print(f"deleted {site} | {email}")
        return 0
    site, email = argv[0], argv[1]
    length = int(argv[2]) if len(argv) > 2 else 16
    pw, status = get_or_create(kr, site, email, length)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802  http.server naming
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(pw.encode())

        def log_message(self, *args):
            pass

    with socketserver.TCPServer(("127.0.0.1", 0), Handler) as srv:
        print(f"status={status} port={srv.server_address[1]}", flush=True)
        srv.timeout = 300
        srv.handle_request()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
