"""Regression protection for PersianNew's immutable legacy source and repaired intake split.

Not a Typora runtime, CSS layout, font licensing or bidirectional editing test.
"""
from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "themes/persiannew/legacy/PersianNew2.css"
CANDIDATE = ROOT / "themes/persiannew/persiannew.css"


class PersianNewIntakeIntegrityTests(unittest.TestCase):
    def test_original_legacy_bytes_are_unchanged(self) -> None:
        self.assertEqual(
            "b114384a1bd9a30f1064e8405d5ce31fef66b4af26bec33d4732b8c4b8a76fb9",
            hashlib.sha256(LEGACY.read_bytes()).hexdigest(),
        )

    def test_install_candidate_does_not_reimport_conversation(self) -> None:
        css = CANDIDATE.read_text(encoding="utf-8")
        self.assertNotIn("```css", css)
        self.assertNotIn("سلام رضا!", css)
        self.assertEqual(1, css.count("0) Font export hints omitted"))
        self.assertIn("#write pre.md-fences", css)
        self.assertIn(".cm-s-inner", css)
        # Presence is only a structural guard; CodeMirror runtime behavior is unverified.

if __name__ == "__main__":
    unittest.main()
