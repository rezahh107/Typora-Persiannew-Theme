#!/usr/bin/env python3
"""Review-only evidence assertions for the experimental real-Typora workflow.

Only OBSERVE Typora's native state. Never mutate or publish its profile/cache.
"""
import argparse
import filecmp
import json
import shutil
import struct
import tempfile
from pathlib import Path

SHOTS = (
    "typora-12s.png", "themes-menu.png",
    "candidate-rtl-6s.png", "candidate-rtl-18s.png",
    "candidate-selected-menu.png", "legacy-rtl-6s.png", "legacy-rtl-18s.png",
    "legacy-selected-menu.png", "code-menu-before-legacy-rtl.png", "legacy-code-early.png", "legacy-code-late.png",
    "legacy-code-focus-1s.png", "legacy-code-focus-13s.png",
    "code-menu-before-candidate.png", "candidate-code-early.png",
    "candidate-code-late.png", "candidate-code-focus-1s.png",
    "candidate-code-focus-13s.png", "code-candidate-selected-menu.png",
    "legacy-again-code-rest.png", "legacy-again-selected-menu.png",
    "code-menu-before-legacy-again.png", "code-menu-before-candidate-edit.png",
    "code-candidate-edit-selected-menu.png", "code-menu-before-legacy-edit.png",
    "code-legacy-edit-selected-menu.png",
    "candidate-code-edit.png", "legacy-code-edit.png", "typora-30s.png",
)
TEXTS = (
    "environment.txt", "comparison.txt", "windows-12s.txt",
    "windows-code.txt", "windows-edit.txt", "windows-30s.txt",
    "edit-results.txt", "state-report.txt",
)
ALLOWLIST = frozenset((*SHOTS, *TEXTS))


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def window_id(listing: Path, exact_title: str) -> str:
    # "wmctrl -lxp": window-id desktop pid wm-class hostname window-title.
    require(listing.is_file(), "target-window listing missing")
    matches = []
    for line in listing.read_text(encoding="utf-8").splitlines():
        parts = line.split(maxsplit=5)
        if len(parts) == 6 and parts[3] == "typora.typora" and parts[5] == exact_title:
            require(int(parts[2]) > 0, "Typora window without a PID")
            matches.append(parts[0])
    require(len(matches) == 1, f"expected exactly one native Typora window: {exact_title!r}; found {len(matches)}")
    return matches[0]


def selected_theme(profile: Path, expected: str):
    require(profile.is_file() and not profile.is_symlink(), "native Typora profile absent/unverified")
    try:
        raw_hex = profile.read_bytes().strip().decode("ascii")
        data = json.loads(bytes.fromhex(raw_hex).decode("utf-8"))
    except (ValueError, UnicodeError, OSError) as exc:
        raise ValueError("native Typora selected theme unreadable/unverified") from exc
    require(isinstance(data, dict), "native Typora profile not an object")
    actual = data.get("theme")
    require(actual == expected, f"WRONG_THEME: expected {expected!r}, native Typora selected {actual!r}")
    return actual


def screenshot(path: Path):
    require(path.is_file() and not path.is_symlink(), f"required screenshot absent: {path.name}")
    with path.open("rb") as stream:
        header = stream.read(24)
    require(len(header) == 24 and header[:8] == b"\x89PNG\r\n\x1a\n"
            and header[12:16] == b"IHDR", f"invalid screenshot header: {path.name}")
    width, height = struct.unpack(">II", header[16:24])
    require((width, height) == (1440, 900),
            f"wrong screenshot viewport: {path.name}: {width}x{height}")


def comparison(left: Path, right: Path, expected_equal: bool):
    screenshot(left)
    screenshot(right)
    same = filecmp.cmp(left, right, shallow=False)
    if expected_equal:
        require(same, f"unexpected visual difference: {left.name} vs {right.name}")
    return "IDENTICAL_PNG" if same else "OBSERVED_DIFFERENCE_NOT_PARITY"


def audit_staged(folder: Path):
    require(folder.is_dir() and not folder.is_symlink(), "artifact upload directory missing/invalid")
    names = set()
    for p in folder.rglob("*"):
        require(p.is_file() and not p.is_symlink() and p.parent == folder,
                f"non-allowlisted directory/symlink/profile/cache in artifact: {p}")
        names.add(p.name)
    require(names == ALLOWLIST,
            f"artifact inventory mismatch: missing={sorted(ALLOWLIST - names)} "
            f"unexpected={sorted(names - ALLOWLIST)}")
    for name in SHOTS:
        screenshot(folder / name)
    for name in TEXTS:
        require((folder / name).is_file() and (folder / name).stat().st_size > 0,
                f"missing/empty evidence text: {name}")
    return len(names)


def stage(source: Path, destination: Path):
    require(not destination.exists(), "refusing to stage over a preexisting artifact")
    require(source.is_dir(), "raw evidence directory missing")
    for name in SHOTS:
        screenshot(source / name)
    for name in TEXTS:
        require((source / name).is_file() and (source / name).stat().st_size > 0,
                f"required evidence text missing/empty: {name}")
    destination.mkdir(parents=True)
    for name in sorted(ALLOWLIST):
        src = source / name
        require(not src.is_symlink(), f"symlinked source forbidden: {name}")
        shutil.copyfile(src, destination / name)
    return audit_staged(destination)


def negative_controls():
    # Deliberately invalid, synthesized guard inputs: tests gates, NOT Typora parity.
    def must_reject(label, callback):
        try:
            callback()
        except (ValueError, OSError) as exc:
            print(f"EXPECTED_FAIL {label}: {exc}")
            return
        raise AssertionError(f"NEGATIVE_CONTROL_FAILED_TO_REJECT: {label}")

    with tempfile.TemporaryDirectory(prefix="typora-guard-tests-") as t:
        root = Path(t)
        windows = root / "windows.txt"
        windows.write_text("0x0010 0 123 typora.typora host other.md - Typora\n")
        must_reject("missing target Typora window",
                    lambda: window_id(windows, "code-fences.md - Typora"))

        profile = root / "profile.data"
        profile.write_text(json.dumps({"theme": "persiannew-legacy.css"}).encode().hex())
        must_reject("wrong native theme",
                    lambda: selected_theme(profile, "persiannew-candidate.css"))
        profile.write_text("not hexadecimal")
        must_reject("unverified native theme",
                    lambda: selected_theme(profile, "persiannew-candidate.css"))

        must_reject("missing required screenshot", lambda: screenshot(root / "missing.png"))
        must_reject("missing comparison input",
                    lambda: comparison(root / "missing-1.png", root / "missing-2.png", True))
        must_reject("missing artifact upload path", lambda: audit_staged(root / "missing-stage"))

        staged = root / "stage"
        staged.mkdir()
        (staged / "config" / "Typora" / "Cache").mkdir(parents=True)
        (staged / "config" / "Typora" / "Cache" / "profile").write_text("not for upload")
        must_reject("unexpected profile/cache in staged artifact", lambda: audit_staged(staged))
    print("NEGATIVE_CONTROLS: 7 deterministic rejection cases passed")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    w = sub.add_parser("window")
    w.add_argument("listing", type=Path)
    w.add_argument("exact_title")
    th = sub.add_parser("theme")
    th.add_argument("profile", type=Path)
    th.add_argument("expected")
    sc = sub.add_parser("screenshot")
    sc.add_argument("path", type=Path)
    cp = sub.add_parser("compare")
    cp.add_argument("left", type=Path)
    cp.add_argument("right", type=Path)
    cp.add_argument("--must-equal", action="store_true")
    st = sub.add_parser("stage")
    st.add_argument("source", type=Path)
    st.add_argument("destination", type=Path)
    au = sub.add_parser("audit")
    au.add_argument("folder", type=Path)
    sub.add_parser("negative-controls")
    args = parser.parse_args()

    try:
        if args.command == "window":
            print(window_id(args.listing, args.exact_title))
        elif args.command == "theme":
            print("VERIFIED_NATIVE_THEME:", selected_theme(args.profile, args.expected))
        elif args.command == "screenshot":
            screenshot(args.path)
            print("VERIFIED_SCREENSHOT:", args.path.name)
        elif args.command == "compare":
            print(comparison(args.left, args.right, args.must_equal),
                  args.left.name, args.right.name)
        elif args.command == "stage":
            print("ALLOWLISTED_ARTIFACT_FILES:", stage(args.source, args.destination))
        elif args.command == "audit":
            print("AUDITED_ARTIFACT_FILES:", audit_staged(args.folder))
        else:
            negative_controls()
    except (ValueError, OSError, AssertionError) as exc:
        parser.exit(1, f"EVIDENCE_FAIL: {exc}\n")


if __name__ == "__main__":
    main()
