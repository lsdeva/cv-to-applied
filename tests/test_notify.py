"""tools/notify.py builds the right desktop-notification command per OS and never fails a run."""
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import notify  # noqa: E402


class NotifyTests(unittest.TestCase):
    def test_windows_uses_hidden_powershell_popup_and_escapes_quotes(self):
        cmd = notify.command("Sign in: O'Brien Ltd, tab 2", "t", platform="win32")
        self.assertEqual(cmd[0], "powershell")
        self.assertIn("Popup('Sign in: O''Brien Ltd, tab 2'", cmd[-1])

    def test_macos_uses_notification_center(self):
        cmd = notify.command('Say "hi"', "t", platform="darwin")
        self.assertEqual(cmd[0], "osascript")
        self.assertIn('\\"hi\\"', cmd[-1])

    def test_linux_without_notify_send_falls_back_to_bell(self):
        with mock.patch.object(notify.shutil, "which", return_value=None):
            self.assertIsNone(notify.command("x", "t", platform="linux"))

    def test_dry_run_prints_and_exits_zero(self):
        r = subprocess.run([sys.executable, str(REPO / "tools" / "notify.py"), "hello", "--dry-run"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("hello", r.stdout)


if __name__ == "__main__":
    unittest.main()
