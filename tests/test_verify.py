"""Actual verifier regression checks using temporary miniature repositories."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify import inspect_repo


class VerificationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.theme = self.root / "themes" / "persiannew"
        self.theme.mkdir(parents=True)
        fixtures = self.root / "tests" / "fixtures"
        fixtures.mkdir(parents=True)
        (fixtures / "rtl-ltr.md").write_text("فارسی and English\n", encoding="utf-8")
        f = chr(96) * 3
        (fixtures / "code-fences.md").write_text(
            f + "python\nprint(1)\n" + f + "\n" + f + "bash\necho yes\n" + f + "\n",
            encoding="utf-8",
        )
        (self.theme / "README.md").write_text("# PersianNew\n", encoding="utf-8")
        self.manifest("source-pending")

    def manifest(self, status: str, name: str = "persiannew") -> None:
        (self.theme / "theme.json").write_text(
            json.dumps({"id": name, "css": name + ".css", "status": status}),
            encoding="utf-8",
        )

    def ready(self, css: str = "#write { color: #333; }") -> None:
        self.manifest("ready")
        (self.theme / "persiannew.css").write_text(css, encoding="utf-8")

    def errors(self) -> str:
        return " ".join(inspect_repo(self.root))

    def test_pending_is_valid(self) -> None:
        self.assertEqual("", self.errors())

    def test_ready_with_owned_asset_is_valid(self) -> None:
        (self.theme / "assets").mkdir()
        (self.theme / "assets" / "demo.svg").write_text("<svg/>", encoding="utf-8")
        self.ready('#write { background-image: url("assets/demo.svg"); }')
        self.assertEqual("", self.errors())

    def test_ready_missing_css_fails(self) -> None:
        self.manifest("ready")
        self.assertIn("missing declared install CSS", self.errors())

    def test_pending_with_css_fails(self) -> None:
        (self.theme / "persiannew.css").write_text("p{}", encoding="utf-8")
        self.assertIn("pending source cannot contain", self.errors())

    def test_mismatched_name_fails(self) -> None:
        self.manifest("ready", "PersianNew")
        self.assertIn("must match directory", self.errors())

    def test_missing_asset_fails(self) -> None:
        self.ready('#write { background: url("assets/missing.svg"); }')
        self.assertIn("CSS asset not found", self.errors())

    def test_cross_theme_assets_are_rejected_even_if_present(self) -> None:
        other = self.root / "themes" / "another"
        (other / "assets").mkdir(parents=True)
        (other / "assets" / "x.svg").write_text("<svg/>", encoding="utf-8")
        (other / "README.md").write_text("# Another\n", encoding="utf-8")
        (other / "theme.json").write_text(
            json.dumps({"id": "another", "css": "another.css", "status": "source-pending"}),
            encoding="utf-8",
        )
        self.ready('#write { background: url("../another/assets/x.svg"); }')
        self.assertIn("theme escape", self.errors())

    def test_external_url_and_import_are_not_silent(self) -> None:
        self.ready('@import url("https://example.org/font.css");\n#write{color:red}')
        self.assertIn("external or absolute", self.errors())
        self.assertIn("@import", self.errors())

    def test_unbalanced_css_fails(self) -> None:
        self.ready("#write { color: red;")
        self.assertIn("unbalanced CSS braces", self.errors())

    def test_missing_regression_fixture_fails(self) -> None:
        (self.root / "tests" / "fixtures" / "code-fences.md").unlink()
        self.assertIn("missing or empty fixture", self.errors())


if __name__ == "__main__":
    unittest.main()
