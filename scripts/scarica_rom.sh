#!/usr/bin/env bash
# Scarica i programmi di prova di Timendus (https://github.com/Timendus/chip8-test-suite, licenza GPLv3).
# Non sono inclusi in questo repository: li scarichi tu, per rispettare la loro licenza.
set -e
cd "$(dirname "$0")/.."
mkdir -p roms
BASE="https://raw.githubusercontent.com/Timendus/chip8-test-suite/main/bin"
for f in 1-chip8-logo 2-ibm-logo 3-corax%2B 4-flags; do
  nome="$(echo "$f" | sed 's/%2B//')"
  [ -f "roms/$nome.ch8" ] || curl -sSfL -o "roms/$nome.ch8" "$BASE/$f.ch8"
done
ls roms
