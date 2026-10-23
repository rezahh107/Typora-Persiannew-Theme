#!/usr/bin/env python3
"""Bounded verification; not a CSS parser, license audit or Typora runtime test."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

SLUG = re.compile(r"[a-z]+(?:-[a-z]+)*\Z")
URL = re.compile(r"""url\(\s*(?P<quote>["']?)(?P<value>.*?)(?P=quote)\s*\)""", re.I | re.S)
KEYS = {"id", "css", "status"}
FIXTURES = ("rtl-ltr.md", "code-fences.md")


def strip_comments_and_check_braces(source: str) -> tuple[str, list[str]]:
    """Lightweight brace/quote/comment sanity, not full syntax validation."""
    result, errors = [], []
    i, depth, quote, comment = 0, 0, "", False
    while i < len(source):
        ch = source[i]
        nxt = source[i + 1] if i + 1 < len(source) else ""
        if comment:
            if ch == "*" and nxt == "/":
                comment = False
                i += 2
            else:
                i += 1
            continue
        if quote:
            result.append(ch)
            if ch == "\\" and nxt:
                result.append(nxt)
                i += 2
                continue
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch == "/" and nxt == "*":
            comment = True
            i += 2
            continue
        if ch in ("'", '"'):
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                errors.append("unexpected closing brace")
                depth = 0
        result.append(ch)
        i += 1
    if comment:
        errors.append("unterminated CSS comment")
    if quote:
        errors.append("unterminated CSS string")
    if depth:
        errors.append("unbalanced CSS braces")
    return "".join(result), errors



# Only enough CSS tokenization to identify import at-keywords accurately.
# CSS Syntax Level 3: https://www.w3.org/TR/css-syntax-3/#tokenization
_CSS_HEX = "0123456789abcdefABCDEF"
_CSS_WHITESPACE = " \t\n\r\f"


def _css_escape(source: str, at: int) -> tuple[str, int]:
    """Decode one valid CSS identifier escape at a backslash index."""
    i = at + 1
    if i >= len(source) or source[i] in "\n\r\f":
        return "", i  # invalid escape (not an identifier character)
    if source[i] not in _CSS_HEX:
        return source[i], i + 1
    start = i
    while i < len(source) and i - start < 6 and source[i] in _CSS_HEX:
        i += 1
    codepoint = int(source[start:i], 16)
    if i < len(source) and source[i] in _CSS_WHITESPACE:
        # CRLF counts as one newline in CSS preprocessing.
        i += 2 if source[i:i + 2] == "\r\n" else 1
    if codepoint == 0 or 0xD800 <= codepoint <= 0xDFFF or codepoint > 0x10FFFF:
        return "\uFFFD", i
    return chr(codepoint), i


def _css_name(source: str, at: int) -> tuple[str, int]:
    """Consume a CSS name with escapes; retain its entire token boundary."""
    pieces: list[str] = []
    i = at
    while i < len(source):
        char = source[i]
        if char == "\\" and i + 1 < len(source) and source[i + 1] not in "\n\r\f":
            decoded, i = _css_escape(source, i)
            pieces.append(decoded)
        elif (char.isascii() and (char.isalnum() or char in "_-")) or ord(char) >= 0x80:
            pieces.append(char)
            i += 1
        else:
            break
    return "".join(pieces), i


def _skip_css_string(source: str, at: int) -> int:
    """Skip quoted CSS text, including escapes that contain quote characters."""
    quote = source[at]
    i = at + 1
    while i < len(source):
        if source[i] == "\\":
            _, i = _css_escape(source, i)
        elif source[i] == quote:
            return i + 1
        else:
            i += 1
    return i


def _skip_css_url(source: str, at: int) -> int:
    """Skip a url(...) token body so embedded @ characters are not at-keywords."""
    i = at
    while i < len(source):
        if source[i] in "'\"":
            i = _skip_css_string(source, i)
        elif source[i] == "\\":
            _, i = _css_escape(source, i)
        elif source[i] == ")":
            return i + 1
        else:
            i += 1
    return i


def _has_css_import_at_keyword(source: str) -> bool:
    """Find a real CSS @import token, not quoted text or an ident prefix."""
    i = 0
    while i < len(source):
        char = source[i]
        if char in "'\"":
            i = _skip_css_string(source, i)
        elif char == "@":
            name, end = _css_name(source, i + 1)
            if name.lower() == "import":
                return True
            i = max(end, i + 1)
        elif char == "\\":
            # An escaped @ is part of an identifier, not an at-keyword.
            _, i = _css_escape(source, i)
        elif (char.isascii() and (char.isalnum() or char in "_-")) or ord(char) >= 0x80:
            name, end = _css_name(source, i)
            if name.lower() == "url" and end < len(source) and source[end] == "(":
                i = _skip_css_url(source, end + 1)
            else:
                i = end
        else:
            i += 1
    return False




def check_css(theme: Path, css: Path) -> list[str]:
    source = css.read_text(encoding="utf-8-sig")
    if not source.strip():
        return ["declared CSS is empty"]
    clean, errors = strip_comments_and_check_braces(source)
    if _has_css_import_at_keyword(clean):
        errors.append("@import requires manual dependency review; unsupported by initial verifier")
    for found in URL.finditer(clean):
        value = found.group("value").strip()
        if not value:
            errors.append("empty CSS url()")
        elif value.startswith(("data:", "#")):
            continue  # inline/fragment; licensing remains unverified
        elif re.match(r"(?i)[a-z][a-z0-9+.-]*:", value) or value.startswith(("/", "\\")):
            errors.append(f"external or absolute asset URL: {value}")
        else:
            local = Path(unquote(value.split("?", 1)[0].split("#", 1)[0]))
            if local.is_absolute() or ".." in local.parts:
                errors.append(f"theme escape in CSS asset URL: {value}")
            elif not (theme / local).resolve().is_relative_to(theme.resolve()) or not (theme / local).is_file():
                errors.append(f"CSS asset not found in owning theme: {value}")
    return errors


def inspect_repo(root: Path) -> list[str]:
    errors: list[str] = []
    themes = root / "themes"
    if not themes.is_dir():
        return ["themes/ is missing"]
    dirs = sorted(p for p in themes.iterdir() if p.is_dir())
    if not dirs:
        errors.append("no theme registered")
    for directory in dirs:
        label = f"themes/{directory.name}: "
        if not SLUG.fullmatch(directory.name):
            errors.append(label + "invalid ID; use lowercase alphabetic words and hyphens")
        if not (directory / "README.md").is_file():
            errors.append(label + "README.md is missing")
        if any(path.is_symlink() for path in directory.rglob("*")):
            errors.append(label + "symlink asset not supported")
        manifest_path = directory / "theme.json"
        if not manifest_path.is_file():
            errors.append(label + "theme.json is missing")
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as exc:
            errors.append(label + f"invalid manifest JSON: {exc}")
            continue
        if not isinstance(manifest, dict) or set(manifest) != KEYS:
            errors.append(label + "manifest needs exactly id, css, status")
            continue
        if manifest["id"] != directory.name or manifest["css"] != directory.name + ".css":
            errors.append(label + "manifest ID/CSS must match directory and install filename")
            continue
        if manifest["status"] not in ("ready", "source-pending"):
            errors.append(label + "invalid status")
            continue
        css = directory / manifest["css"]
        if manifest["status"] == "source-pending":
            if css.exists():
                errors.append(label + "pending source cannot contain declared install CSS")
        elif not css.is_file():
            errors.append(label + "ready theme missing declared install CSS")
        else:
            errors.extend(label + e for e in check_css(directory, css))
    fixture_dir = root / "tests" / "fixtures"
    for filename in FIXTURES:
        fixture = fixture_dir / filename
        if not fixture.is_file() or not fixture.read_text(encoding="utf-8").strip():
            errors.append(f"missing or empty fixture: tests/fixtures/{filename}")
    fences = fixture_dir / "code-fences.md"
    if fences.is_file() and fences.read_text(encoding="utf-8").count(chr(96) * 3) < 4:
        errors.append("code-fences.md needs fenced code examples")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    issues = inspect_repo(root)
    print("Repository structural verification (not actual Typora runtime):")
    for issue in issues:
        print("FAIL:", issue)
    if not issues:
        print("PASS: registered theme/file/asset/fixture contract")
    print("Verifier regression tests:")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"],
        cwd=root, check=False,
    )
    if issues or result.returncode:
        print("FAIL: structural verification")
        return 1
    print("PASS: structural contract and tests; Typora runtime NOT_EXECUTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
