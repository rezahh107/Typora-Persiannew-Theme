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


    def test_string_form_import_is_rejected(self) -> None:
        self.ready('@import "https://example.org/theme.css";')
        self.assertIn("@import", self.errors())

    def test_escaped_import_spellings_are_rejected_with_string_urls(self) -> None:
        spellings = (
            r'@\69mport',
            r'@\000069mport',
            r'@\69 mport',
            '@\\69\tmport',
            r'@im\70ort',
            r'@imp\6f rt',
            r'@i\mport',
            r'@\49MPORT',
            r'@\69\6d\70\6f\72\74',
            r'@im/**/port',
        )
        for spelling in spellings:
            with self.subTest(spelling=spelling):
                self.ready(spelling + ' "https://example.org/other.css";')
                self.assertIn("@import", self.errors())

    def test_escaped_import_with_local_url_form_is_rejected(self) -> None:
        (self.theme / "assets").mkdir()
        (self.theme / "assets" / "good.css").write_text("p{}", encoding="utf-8")
        self.ready(r'@im\70ort url("assets/good.css");')
        self.assertIn("@import", self.errors())

    def test_import_text_in_comments_is_harmless(self) -> None:
        self.ready('/* @import "https://example.org/font.css"; */\n'
                   r'/* @im\70ort "https://example.org/font.css"; */'
                   '\n#write { color: red; }')
        self.assertEqual("", self.errors())

    def test_legitimate_quoted_import_text_is_harmless(self) -> None:
        self.ready(r'''#write::before { content: "@import \69mport \" text"; }''')
        self.assertEqual("", self.errors())

    def test_other_at_keywords_and_prefixed_names_are_not_imports(self) -> None:
        self.ready('@media print { #write { color: black; } }\n'
                   '@import-other { #write { color: red; } }\n'
                   '@importer { #write { color: blue; } }')
        self.assertEqual("", self.errors())

    def test_local_unquoted_url_containing_import_text_is_harmless(self) -> None:
        (self.theme / "assets").mkdir()
        (self.theme / "assets" / "@import.svg").write_text("<svg/>", encoding="utf-8")
        self.ready("#write { background: url(assets/@import.svg); }")
        self.assertEqual("", self.errors())



    def test_ordinary_owned_url_forms_still_pass(self) -> None:
        (self.theme / "assets").mkdir()
        (self.theme / "assets" / "good.svg").write_text("<svg/>", encoding="utf-8")
        for spelling in (
            'url("assets/good.svg")',
            "url('assets/good.svg')",
            "url(assets/good.svg)",
        ):
            with self.subTest(spelling=spelling):
                self.ready(f"#write {{ background: {spelling}; }}")
                self.assertEqual("", self.errors())

    def test_escaped_url_function_with_owned_asset_passes(self) -> None:
        (self.theme / "assets").mkdir()
        (self.theme / "assets" / "good.svg").write_text("<svg/>", encoding="utf-8")
        spellings = (
            r'u\72l',
            r'\75rl',
            r'\000075rl',
            r'\75 rl',
            r'u\72\6c',
            r'\55RL',
            r'u\000072l',
            r'U\72L',
            r'u\rl',
            r'u/**/rl',
        )
        for spelling in spellings:
            with self.subTest(spelling=spelling):
                self.ready(f'#write {{ background: {spelling}("assets/good.svg"); }}')
                self.assertEqual("", self.errors())

    def test_escaped_url_function_external_reference_fails(self) -> None:
        for spelling in (r'u\72l', r'\75rl', r'\000075rl', r'\75 rl', r'u\72\6c', r'\55RL'):
            with self.subTest(spelling=spelling):
                self.ready(f'#write {{ background: {spelling}("https://example.org/x.svg"); }}')
                self.assertIn("external or absolute asset URL", self.errors())

    def test_escaped_url_function_missing_local_reference_fails(self) -> None:
        self.ready(r'#write { background: u\72l("assets/missing.svg"); }')
        self.assertIn("CSS asset not found", self.errors())

    def test_escaped_url_function_cross_theme_reference_fails(self) -> None:
        other = self.root / "themes" / "another"
        (other / "assets").mkdir(parents=True)
        (other / "assets" / "x.svg").write_text("<svg/>", encoding="utf-8")
        (other / "README.md").write_text("# Another\n", encoding="utf-8")
        (other / "theme.json").write_text(
            json.dumps({"id": "another", "css": "another.css", "status": "source-pending"}),
            encoding="utf-8",
        )
        self.ready(r'#write { background: \75rl("../another/assets/x.svg"); }')
        self.assertIn("theme escape", self.errors())

    def test_escaped_url_resource_values_cannot_bypass_policy(self) -> None:
        for resource, error in (
            (r'https\3a //example.org/x.svg', "external or absolute asset URL"),
            (r'\2e \2e /another/assets/x.svg', "theme escape"),
            (r'assets/\6d issing.svg', "CSS asset not found"),
        ):
            with self.subTest(resource=resource):
                self.ready('#write { background: u\\72l("' + resource + '"); }')
                self.assertIn(error, self.errors())

    def test_css_strings_and_comments_with_url_text_are_harmless(self) -> None:
        self.ready(
            r'''#write::before { content: 'u\72l("https://example.org/x.svg") url(assets/missing.svg)'; }'''
            + '\n/* u\\72l("https://example.org/x.svg") */\n'
            + '#write { color: navy; }'
        )
        self.assertEqual("", self.errors())

    def test_mixed_valid_asset_plus_escaped_invalid_resource_fails(self) -> None:
        (self.theme / "assets").mkdir()
        (self.theme / "assets" / "ok.svg").write_text("<svg/>", encoding="utf-8")
        self.ready(
            '#write { background: url("assets/ok.svg"), '
            + r'u\72l("https://example.org/evil.svg")'
            + '; }'
        )
        self.assertIn("external or absolute asset URL", self.errors())

    def test_pending_theme_remains_untouched_by_url_scan(self) -> None:
        self.assertEqual("", self.errors())


    def test_image_set_string_sources_are_owned_local_assets(self) -> None:
        (self.theme / "assets").mkdir()
        for name in ("small.svg", "large.svg"):
            (self.theme / "assets" / name).write_text("<svg/>", encoding="utf-8")
        self.ready(
            '#write { background: image-set("assets/small.svg" 1x type("image/svg+xml"), '
            + "'assets/large.svg' 2x); }"
        )
        self.assertEqual("", self.errors())

    def test_image_set_string_external_sources_are_rejected(self) -> None:
        for css_name in ("image-set", r'im\61ge-set', "-webkit-image-set", r'image\2d set"):
            with self.subTest(css_name=css_name):
                self.ready('#write { background: ' + css_name
                           + '("https://outside.example/missing.svg" 1x); }')
                self.assertIn("external or absolute asset URL", self.errors())

    def test_image_set_string_missing_and_cross_theme_sources_are_rejected(self) -> None:
        self.ready('#write { background: image-set("assets/missing.svg" 1x); }')
        self.assertIn("CSS asset not found", self.errors())
        other = self.root / "themes" / "another"
        (other / "assets").mkdir(parents=True)
        (other / "assets" / "outside.svg").write_text("<svg/>", encoding="utf-8")
        (other / "README.md").write_text("# Another\n", encoding="utf-8")
        (other / "theme.json").write_text(
            json.dumps({"id": "another", "css": "another.css", "status": "source-pending"}),
            encoding="utf-8",
        )
        self.ready('#write { background: image-set("../another/assets/outside.svg" 2x); }')
        self.assertIn("theme escape", self.errors())

    def test_image_set_nested_functions_do_not_hide_string_sources(self) -> None:
        self.ready(
            '#write { background: image-set('
            'linear-gradient(red, blue) 1x, '
            '"https://outside.example/unsafe.svg" 2x); }'
        )
        self.assertIn("external or absolute asset URL", self.errors())

    def test_image_set_strings_in_content_and_comments_are_not_resources(self) -> None:
        self.ready(
            r'''#write::before { content: 'image-set("https://outside.example/x.svg" 1x)'; }'''
            + '\n/* image-set("https://outside.example/y.svg" 2x) */\n'
            + '#write { color: navy; }'
        )
        self.assertEqual("", self.errors())

    def test_unquoted_url_escaped_spaces_and_parentheses_are_valid(self) -> None:
        (self.theme / "assets").mkdir()
        for name in ("a b.svg", "a(b).svg"):
            (self.theme / "assets" / name).write_text("<svg/>", encoding="utf-8")
        for spelling in (
            r'url(assets/a\ b.svg)',
            r'url(assets/a\20 b.svg)',
            r'url(assets/a\(b\).svg)',
            r'url(assets/a\28 b\29 .svg)',
            r'u\72l(assets/a\ b.svg)',
            r'u\72l(assets/a\(b\).svg)',
        ):
            with self.subTest(spelling=spelling):
                self.ready("#write { background: " + spelling + "; }")
                self.assertEqual("", self.errors())

    def test_unquoted_url_invalid_unescaped_space_and_paren_remain_rejected(self) -> None:
        for spelling in ("url(assets/a b.svg)", "url(assets/a(b).svg)"):
            with self.subTest(spelling=spelling):
                self.ready("#write { background: " + spelling + "; }")
                self.assertIn("malformed CSS url()", self.errors())

    def test_unquoted_url_escaped_external_and_missing_are_not_accepted(self) -> None:
        for spelling, error in (
            (r'url(https\3a //outside.example/img.svg)', "external or absolute asset URL"),
            (r'url(assets/does\ not-exist.svg)', "CSS asset not found"),
        ):
            with self.subTest(spelling=spelling):
                self.ready("#write { background: " + spelling + "; }")
                self.assertIn(error, self.errors())

    def test_mixed_valid_image_set_and_invalid_remote_string_fails(self) -> None:
        (self.theme / "assets").mkdir()
        (self.theme / "assets" / "good.svg").write_text("<svg/>", encoding="utf-8")
        self.ready(
            '#write { background: image-set('
            'url("assets/good.svg") 1x, '
            '"https://outside.example/evil.svg" 2x); }'
        )
        self.assertIn("external or absolute asset URL", self.errors())



if __name__ == "__main__":
    unittest.main()
