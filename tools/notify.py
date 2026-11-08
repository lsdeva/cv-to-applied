"""Desktop notification with a sound, so the user notices when a run needs them.

Usage: python tools/notify.py "<message>" [--title "<title>"] [--dry-run]

Windows: sound plus a pop-up (auto-closes after 10 minutes). macOS: Notification Center with a sound.
Linux: notify-send when installed, otherwise the terminal bell. Never blocks the run and never fails it:
any error is printed and the exit code is 0.
"""
import shutil
import subprocess
import sys

TITLE = "cv-to-applied needs you"


def command(message, title, platform=sys.platform):
    if platform.startswith("win"):
        msg = message.replace("'", "''")
        ttl = title.replace("'", "''")
        script = (
            "$w=\"$env:WINDIR\\Media\\Windows Notify System Generic.wav\";"
            "if(Test-Path $w){(New-Object Media.SoundPlayer $w).PlaySync()}else{[console]::beep(880,400)};"
            f"(New-Object -ComObject WScript.Shell).Popup('{msg}',600,'{ttl}',0x40+0x1000)|Out-Null"
        )
        return ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", script]
    if platform == "darwin":
        esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')  # noqa: E731
        return ["osascript", "-e", f'display notification "{esc(message)}" with title "{esc(title)}" sound name "Glass"']
    if shutil.which("notify-send"):
        return ["notify-send", "-u", "critical", title, message]
    return None


def main(argv):
    if not argv or argv[0].startswith("--"):
        print(__doc__)
        return 0
    message = argv[0]
    title = argv[argv.index("--title") + 1] if "--title" in argv else TITLE
    cmd = command(message, title)
    if "--dry-run" in argv:
        print(cmd)
        return 0
    if cmd is None:
        print("\a" + message, flush=True)
        return 0
    try:
        flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=flags if sys.platform.startswith("win") else 0)
        print("notified")
    except OSError as e:
        print(f"notify failed ({e}); message: {message}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
