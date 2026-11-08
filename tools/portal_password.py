"""Get-or-create a per-site portal password, store it locally, serve it once on 127.0.0.1.
Never prints the password. Usage: python tools/portal_password.py <site-key> <login-email> [length]"""
import secrets, string, sys, http.server, socketserver, os, datetime
site, email = sys.argv[1], sys.argv[2]
length = int(sys.argv[3]) if len(sys.argv) > 3 else 16
store = 'submission/secrets/portal-passwords.txt'
pw, status = None, 'existing'
if os.path.exists(store):
    for line in open(store, encoding='utf-8'):
        parts = line.rstrip('\n').split(' | ')
        if len(parts) >= 4 and parts[1] == site:
            pw = parts[3]
if pw is None:
    U, L, D, S = 'ABCDEFGHJKLMNPQRSTUVWXYZ', 'abcdefghijkmnopqrstuvwxyz', '23456789', '!@#$%*-_'
    c = [secrets.choice(U), secrets.choice(L), secrets.choice(D), secrets.choice(S)]
    c += [secrets.choice(U + L + D + S) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(c)
    pw, status = ''.join(c), 'new'
    os.makedirs(os.path.dirname(store), exist_ok=True)
    new_file = not os.path.exists(store)
    with open(store, 'a', encoding='utf-8') as f:
        if new_file:
            f.write('# date | site | login | password  (local only, gitignored; move into a password manager)\n')
        f.write(f'{datetime.date.today()} | {site} | {email} | {pw}\n')
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header('Content-Type', 'text/plain'); self.end_headers()
        self.wfile.write(pw.encode())
    def log_message(self, *a): pass
with socketserver.TCPServer(('127.0.0.1', 0), H) as srv:
    print(f'status={status} port={srv.server_address[1]}', flush=True)
    srv.timeout = 300
    srv.handle_request()
