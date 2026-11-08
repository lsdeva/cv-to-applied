"""tools/portal_password.py keeps passwords in the system keychain, never in a file.

A fake in-memory keyring stands in for the OS credential store, so these tests never touch the
real Windows Credential Manager, macOS Keychain or Secret Service.
"""
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import portal_password as pp  # noqa: E402


class KeyringError(Exception):
    pass


class PasswordDeleteError(KeyringError):
    pass


def fake_keyring(broken=False):
    store = {}
    kr = types.SimpleNamespace(store=store)
    kr.errors = types.SimpleNamespace(KeyringError=KeyringError, PasswordDeleteError=PasswordDeleteError)

    def get_password(service, user):
        if broken:
            raise KeyringError("no backend")
        return store.get((service, user))

    def set_password(service, user, pw):
        if broken:
            raise KeyringError("no backend")
        store[(service, user)] = pw

    def delete_password(service, user):
        if (service, user) not in store:
            raise PasswordDeleteError("missing")
        del store[(service, user)]

    kr.get_password, kr.set_password, kr.delete_password = get_password, set_password, delete_password
    return kr


class PortalPasswordTests(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        self.tmp = tempfile.TemporaryDirectory()
        os.chdir(self.tmp.name)

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def all_text(self):
        root = Path(self.tmp.name)
        return "".join(p.read_text(encoding="utf-8") for p in root.rglob("*") if p.is_file())

    def test_new_password_goes_to_keychain_and_index_has_no_password(self):
        kr = fake_keyring()
        pw, status = pp.get_or_create(kr, "acme-workday", "me@example.com")
        self.assertEqual(status, "new")
        self.assertEqual(kr.store[("cv-to-applied:acme-workday", "me@example.com")], pw)
        self.assertIn("acme-workday | me@example.com", self.all_text())
        self.assertNotIn(pw, self.all_text())

    def test_existing_password_is_reused(self):
        kr = fake_keyring()
        first, _ = pp.get_or_create(kr, "acme", "me@example.com")
        second, status = pp.get_or_create(kr, "acme", "me@example.com")
        self.assertEqual((second, status), (first, "existing"))

    def test_generated_password_mixes_character_classes(self):
        pw = pp.generate(16)
        self.assertEqual(len(pw), 16)
        for group in ("ABCDEFGHJKLMNPQRSTUVWXYZ", "abcdefghijkmnopqrstuvwxyz", "23456789", "!@#$%*-_"):
            self.assertTrue(any(c in group for c in pw), group)

    def test_no_backend_stops_and_writes_nothing(self):
        with self.assertRaises(SystemExit) as ctx:
            pp.get_or_create(fake_keyring(broken=True), "acme", "me@example.com")
        self.assertEqual(ctx.exception.code, 3)
        self.assertEqual(self.all_text(), "")

    def test_legacy_plain_text_store_is_migrated_and_deleted(self):
        legacy = Path(pp.LEGACY_STORE)
        legacy.parent.mkdir(parents=True)
        legacy.write_text("# date | site | login | password\n2026-10-01 | acme | me@example.com | Old-Pass_123\n",
                          encoding="utf-8")
        kr = fake_keyring()
        self.assertEqual(pp.migrate_legacy(kr), 1)
        self.assertFalse(legacy.exists())
        self.assertEqual(kr.store[("cv-to-applied:acme", "me@example.com")], "Old-Pass_123")
        self.assertNotIn("Old-Pass_123", self.all_text())

    def test_legacy_store_kept_when_keychain_unavailable(self):
        legacy = Path(pp.LEGACY_STORE)
        legacy.parent.mkdir(parents=True)
        legacy.write_text("2026-10-01 | acme | me@example.com | Old-Pass_123\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            pp.migrate_legacy(fake_keyring(broken=True))
        self.assertTrue(legacy.exists())


if __name__ == "__main__":
    unittest.main()
