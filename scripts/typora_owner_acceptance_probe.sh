#!/usr/bin/env bash
set -euo pipefail
export DISPLAY=:99
OUT="$RUNNER_TEMP/typora-owner-probe"
RAW="$OUT/raw"; STAGED="$GITHUB_WORKSPACE/typora-owner-stage"
mkdir -p "$RAW" "$STAGED" "$OUT/work"
GUARD=scripts/typora_spike_evidence.py
PROFILE="$HOME/.config/Typora/profile.data"
: >"$RAW/results.txt"
: >"$RAW/theme-verification.txt"
record(){ printf '%s\n' "$*" | tee -a "$RAW/results.txt"; }
snapshot(){ scrot -z -a 0,0,1440,825 "$RAW/$1.png"; python3 "$GUARD" screenshot "$RAW/$1.png" >/dev/null; }
select_theme(){
  xdotool mousemove --sync 315 55 click 1
  sleep 1
  xdotool mousemove --sync 397 "$2" click 1
  local ok=0
  for i in 1 2 3 4 5 6; do
    if python3 "$GUARD" theme "$PROFILE" "$1" >>"$RAW/theme-verification.txt" 2>&1; then ok=1; break; fi
    sleep 1
  done
  test "$ok" -eq 1
  xdotool mousemove --sync 1210 760
  xdotool mousemove --sync 315 55 click 1
  sleep 1
  snapshot "$3-menu"
  xdotool key Escape
  xdotool mousemove --sync 1210 760
  record "NATIVE_SELECTION_CONFIRMED $3 $1"
}
set_scheme(){
  if gsettings set org.gnome.desktop.interface color-scheme "$1"; then
    record "GSETTINGS_COLOR_SCHEME_$2 $(gsettings get org.gnome.desktop.interface color-scheme)"
  else record "GSETTINGS_COLOR_SCHEME_$2 NOT_PROVEN"; fi
}
mkdir -p "$HOME/.config/Typora/themes"
cp themes/persiannew/legacy/PersianNew2.css "$HOME/.config/Typora/themes/persiannew-legacy.css"
cp themes/persiannew/persiannew.css "$HOME/.config/Typora/themes/persiannew-candidate.css"
{
  echo "PR3_EXACT_BASELINE=1ae0da970be18b90859e50b4228771a35608b49b"
  echo "PROBE_HEAD=$(git rev-parse HEAD)"
  lsb_release -ds
  dpkg-query -W typora
  sha256sum themes/persiannew/legacy/PersianNew2.css themes/persiannew/persiannew.css
  for font in Vazir Vazirmatn "Amazon Ember Display"; do
    printf 'fc-match(%s): ' "$font"
    fc-match -f '%{family}\n' "$font"
  done
} >"$RAW/environment.txt"
Xvfb :99 -screen 0 1440x900x24 -nolisten tcp >"$OUT/xvfb.log" 2>&1 &
sleep 2
openbox >"$OUT/openbox.log" 2>&1 &
sleep 2
set_scheme default LIGHT
typora "$(realpath tests/fixtures/rtl-ltr.md)" --disable-gpu >"$OUT/typora.log" 2>&1 &
PID=$!
sleep 12
kill -0 "$PID"
wmctrl -lxp >"$RAW/windows-main.txt"
WID=$(python3 "$GUARD" window "$RAW/windows-main.txt" 'rtl-ltr.md - Typora')
wmctrl -ir "$WID" -e 0,50,40,1300,820
xdotool windowactivate --sync "$WID"
for theme in legacy candidate; do
  if test "$theme" = legacy; then y=215; else y=182; fi
  select_theme "persiannew-$theme.css" "$y" "$theme-rtl"
  sleep 4; snapshot "$theme-light"
  set_scheme prefer-dark DARK
  sleep 7; snapshot "$theme-dark-attempt"
  set_scheme default LIGHT
  sleep 5; snapshot "$theme-light-restored"
done
xdotool mousemove --sync 65 55 click 1
sleep 1; snapshot file-menu
xdotool mousemove --sync 90 684
sleep 1; snapshot export-submenu
xdotool key Escape Escape
xdotool key --clearmodifiers alt+shift+p
sleep 3; snapshot print-dialog-attempt
xdotool key Escape
record 'PRINT: native print dialog observed; print-to-file not asserted'
mkdir -p "$OUT/pdf"
: >"$RAW/pdf-results.txt"
# Same real RTL fixture, same viewport, verified native theme, native File > Export > PDF.
for theme in legacy candidate; do
  if test "$theme" = legacy; then y=215; else y=182; fi
  xdotool windowactivate --sync "$WID"
  select_theme "persiannew-$theme.css" "$y" "$theme-export"
  xdotool mousemove --sync 65 55 click 1
  sleep 0.7
  xdotool mousemove --sync 90 684
  sleep 0.7
  xdotool mousemove --sync 367 349 click 1
  sleep 3
  snapshot "$theme-export-dialog"
  # GTK Save dialog: Ctrl+L enables absolute destination. Never overwrite fixture.
  xdotool key --clearmodifiers ctrl+l
  sleep 0.5
  xdotool type --clearmodifiers --delay 15 "$OUT/pdf/$theme.pdf"
  xdotool key Return
  sleep 4
  if ! test -s "$OUT/pdf/$theme.pdf"; then
    xdotool key Return
    sleep 3
  fi
  snapshot "$theme-export-after"
  if test -s "$OUT/pdf/$theme.pdf" && head -c 5 "$OUT/pdf/$theme.pdf" | grep -q '%PDF-'; then
    pdfinfo "$OUT/pdf/$theme.pdf" >"$RAW/$theme-pdf-metadata.txt"
    pdftotext "$OUT/pdf/$theme.pdf" "$OUT/pdf/$theme.txt"
    printf 'PDF_ACTUALLY_EXPORTED %s sha256=' "$theme" >>"$RAW/pdf-results.txt"
    sha256sum "$OUT/pdf/$theme.pdf" | cut -d' ' -f1 >>"$RAW/pdf-results.txt"
    printf 'PAGES %s ' "$theme" >>"$RAW/pdf-results.txt"
    pdfinfo "$OUT/pdf/$theme.pdf" | awk '/^Pages:/{print $2}' >>"$RAW/pdf-results.txt"
    printf 'EXTRACTED_TEXT_CHARS %s ' "$theme" >>"$RAW/pdf-results.txt"
    wc -m <"$OUT/pdf/$theme.txt" >>"$RAW/pdf-results.txt"
    pdftoppm -f 1 -l 1 -scale-to 1000 -png -singlefile "$OUT/pdf/$theme.pdf" "$RAW/$theme-pdf-preview"
  else
    printf 'PDF_EXPORT_NOT_PROVEN %s: no verified file\n' "$theme" >>"$RAW/pdf-results.txt"
  fi
  xdotool key Escape Escape
done
xdotool windowactivate --sync "$WID"
xdotool key --clearmodifiers ctrl+slash
sleep 2; snapshot source-mode-attempt
xdotool key --clearmodifiers ctrl+slash
sleep 2; snapshot source-mode-return
record "SOURCE_MODE_AND_DARK: status requires independent screenshot inspection"
set_scheme default LIGHT
for theme in legacy candidate; do
  if test "$theme" = legacy; then y=215; else y=182; fi
  cp tests/fixtures/code-fences.md "$OUT/work/$theme-edit.md"
  typora "$OUT/work/$theme-edit.md" --disable-gpu >"$OUT/typora-$theme.log" 2>&1 &
  sleep 7
  wmctrl -lxp >"$RAW/windows-$theme.txt"
  WID=$(python3 "$GUARD" window "$RAW/windows-$theme.txt" "$theme-edit.md - Typora")
  wmctrl -ir "$WID" -e 0,50,40,1300,820
  xdotool windowactivate --sync "$WID"
  select_theme "persiannew-$theme.css" "$y" "$theme-code"
  snapshot "$theme-code-before-focus"
  xdotool mousemove --sync 265 392 click 1
  sleep 1; snapshot "$theme-code-focused"
  xdotool key --clearmodifiers End
  printf ' ab-سلام-CD' | xclip -selection clipboard -i
  xdotool key --clearmodifiers ctrl+v
  xdotool key --clearmodifiers Left Left
  xdotool type --clearmodifiers --delay 70 'Z'
  sleep 1; snapshot "$theme-bidi-caret-after"
  xdotool key --clearmodifiers ctrl+s
  sleep 2
  python3 -c 'import pathlib,sys,hashlib;p=pathlib.Path(sys.argv[1]);s=p.read_text();l=[x for x in s.splitlines() if "ab-سلام-" in x];pathlib.Path(sys.argv[2]).write_text("SHA256="+hashlib.sha256(p.read_bytes()).hexdigest()+"\nMIXED_LINE="+repr(l)+"\n");sys.exit(0 if l else 4)' "$OUT/work/$theme-edit.md" "$RAW/$theme-edit-result.txt"
  record "REAL_MIXED_CARET_SAVE $theme"
done
python3 "$GUARD" compare "$RAW/legacy-light.png" "$RAW/candidate-light.png" >"$RAW/comparisons.txt"
python3 "$GUARD" compare "$RAW/legacy-dark-attempt.png" "$RAW/candidate-dark-attempt.png" >>"$RAW/comparisons.txt"
python3 "$GUARD" compare "$RAW/legacy-code-focused.png" "$RAW/candidate-code-focused.png" >>"$RAW/comparisons.txt"
# Explicit publication allowlist: no profile, cache, local font or license data.
for path in "$RAW"/*.png "$RAW"/environment.txt "$RAW"/results.txt "$RAW"/theme-verification.txt "$RAW"/comparisons.txt "$RAW"/*-edit-result.txt "$RAW"/pdf-results.txt "$RAW"/*-pdf-metadata.txt; do
  test -s "$path"
  cp "$path" "$STAGED/"
done
find "$STAGED" -mindepth 1 ! -type f | grep -q . && exit 1 || true
test "$(find "$STAGED" -maxdepth 1 -type f | wc -l)" -ge 20
record "PROBE_COMPLETE; PDF_EXPORT_STATUS_IN_PDF_RESULTS; DARK_MODE_REQUIRES_IMAGE_INSPECTION"
cp "$RAW/results.txt" "$STAGED/results.txt"
