#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove di ce-chip8.
  1. i programmi di prova di Timendus (scaricati) devono dare lo schermo in tests/oro/
  2. la modalita' terminale parte, mette il terminale in modo "grezzo", esce con Esc
  3. (se c'e' SDL2) la finestra compila e gira per qualche immagine senza schermo
Uso:  python3 tests/prova.py          (usa ./ce)"""
import os
import select
import shutil
import signal
import subprocess
import sys
import time

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.join(QUI, "..")
CE = os.path.join(RADICE, "ce")
PROVE = [("1-chip8-logo", 20000), ("2-ibm-logo", 3000), ("3-corax", 20000), ("4-flags", 20000)]


def rom(nome):
    return os.path.join(RADICE, "roms", nome + ".ch8")


def main():
    ok = ko = 0

    def esito(nome, bene, dettaglio=""):
        nonlocal ok, ko
        if bene:
            ok += 1
            print(f"ok       {nome}")
        else:
            ko += 1
            print(f"FALLITO  {nome} {dettaglio}")

    subprocess.run([os.path.join(RADICE, "scripts", "scarica_rom.sh")], check=True, capture_output=True)
    # compilare una volta sola e' piu' veloce che compilare a ogni prova
    exe = os.path.join(RADICE, "chip8_prova")
    r = subprocess.run([CE, "compila", os.path.join(RADICE, "src", "principale.ce"), "-o", exe],
                       capture_output=True, text=True, cwd=RADICE)
    esito("compilazione", r.returncode == 0, r.stderr[:500])
    if r.returncode != 0:
        return 1
    for nome, cicli in PROVE:
        r = subprocess.run([exe, "prova", rom(nome), str(cicli)], capture_output=True, text=True)
        atteso = open(os.path.join(QUI, "oro", nome + ".txt"), encoding="utf-8").read()
        esito(f"schermo di {nome}", r.returncode == 0 and r.stdout == atteso)

    # terminale, dentro uno pseudo-terminale
    try:
        import pty
        import termios
        pid, fd = pty.fork()
        if pid == 0:
            os.execv(exe, ["chip8", "gioca", rom("2-ibm-logo")])

        def drain(t):
            out, fine = b"", time.time() + t
            while time.time() < fine:
                pronti, _, _ = select.select([fd], [], [], 0.05)
                if pronti:
                    try:
                        out += os.read(fd, 65536)
                    except OSError:
                        break
            return out

        out = drain(0.8)
        durante = termios.tcgetattr(fd)
        grezzo = not (durante[3] & termios.ICANON) and not (durante[3] & termios.ECHO)
        os.write(fd, b"q")
        out += drain(0.3)
        os.write(fd, b"\x1b")
        out += drain(0.8)
        fatto = os.waitpid(pid, os.WNOHANG)
        if fatto[0] == 0:
            os.kill(pid, signal.SIGKILL)
        esito("terminale: modo grezzo e disegno", grezzo and b"\x1b[H" in out)
        esito("terminale: Esc fa uscire", fatto[0] != 0 and os.WEXITSTATUS(fatto[1]) == 0)
    except ImportError:
        print("saltato  terminale (manca pty)")

    # finestra SDL2, senza schermo (driver finto)
    sdl = shutil.which("pkg-config") and subprocess.run(["pkg-config", "--exists", "sdl2"]).returncode == 0
    if sdl:
        env = dict(os.environ, SDL_VIDEODRIVER="dummy")
        r = subprocess.run([CE, "esegui", os.path.join(RADICE, "src", "finestra.ce"), "-l", "SDL2",
                            rom("2-ibm-logo"), "30"], capture_output=True, text=True, cwd=RADICE, env=env)
        esito("finestra SDL2 (driver finto)", r.returncode == 0, r.stderr[:300])
    else:
        print("saltato  finestra SDL2 (libsdl2-dev non installata)")
    if os.path.exists(exe):
        os.remove(exe)
    print(f"\n{ok} riusciti, {ko} falliti")
    return 1 if ko else 0


if __name__ == "__main__":
    sys.exit(main())
