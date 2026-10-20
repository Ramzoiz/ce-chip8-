# ce-chip8

Un emulatore **CHIP-8** (la piccola macchina virtuale a 8 bit dei primi videogiochi) scritto in
**[Ce++](https://github.com/Duffionis/Ce-)**, il linguaggio di sistema piccolo, sicuro e tutto
italiano. E' un programma vero di circa 500 righe: usa variabili globali, `scegli`, `Risultato`,
la libreria standard e il collegamento a una libreria C (SDL2).

    ./ce esegui src/principale.ce gioca programma.ch8      # gioca nel terminale
    ./ce esegui src/finestra.ce -l SDL2 programma.ch8      # finestra grafica

Alla prima esecuzione `./ce` scarica il compilatore Ce++ (versione fissata, riga `PIN` in `./ce`).
Servono `git`, `python3` e `gcc` o `clang`.

## Tre modi di usarlo

| modo | comando | serve |
|---|---|---|
| prova | `./ce esegui src/principale.ce prova rom.ch8 [istruzioni]` | niente: stampa lo schermo dopo N istruzioni |
| terminale | `./ce esegui src/principale.ce gioca rom.ch8` | un terminale Linux/Mac (anche quello di un Codespace) |
| finestra | `./ce esegui src/finestra.ce -l SDL2 rom.ch8` | `libsdl2-dev` e uno schermo vero |

In un Codespace la finestra non si puo' aprire (non c'e' uno schermo): usa il modo terminale.
Per la finestra sul tuo computer: `sudo apt install libsdl2-dev`.

Tasti (come sulla tastiera originale a 16 tasti, qui sulla sinistra della tastiera):

    1 2 3 4        1 2 3 C
    q w e r   -->  4 5 6 D        Esc o Ctrl-C = esci (nel terminale)
    a s d f        7 8 9 E
    z x c v        A 0 B F

Il terminale non sa quando lasci un tasto: ogni pressione dura circa un decimo di secondo.

## Provare che funziona

    python3 tests/prova.py

Scarica da GitHub i programmi di prova di [Timendus](https://github.com/Timendus/chip8-test-suite)
(licenza GPLv3, per questo non sono copiati qui), li esegue e confronta lo schermo con
`tests/oro/`. La prova "Corax+" mostra 22 spunte, una per istruzione: le abbiamo controllate a occhio
contro l'immagine ufficiale del test, ed e' per questo che `tests/oro/3-corax.txt` e' considerato giusto.
Verifica anche che il terminale entri e esca dal modo "grezzo" e (se c'e' SDL2) che la finestra giri
per qualche immagine con il driver video finto.

## Com'e' fatto

    src/chip8.ce       la macchina: memoria, registri, 35 istruzioni, timer (schermo e stato sono variabili globali)
    src/terminale.ce   disegno con mezzi blocchi ANSI e tastiera senza Invio (termios di Linux)
    src/finestra.ce    finestra SDL2: le funzioni SDL sono dichiarate con 'esterna', senza header
    src/principale.ce  riga di comando (prova / gioca)
    tests/prova.py     le prove, tests/oro/ gli schermi attesi

## Cosa manca

- Niente suono (il contatore del suono c'e', ma non fa rumore).
- Le istruzioni seguono il comportamento "moderno" (CHIP-48) per gli spostamenti e `Fx55`/`Fx65`;
  alcuni vecchi giochi vogliono quello originale del COSMAC VIP.
- Il terminale non vede il rilascio dei tasti (vedi sopra).
- La finestra non e' stata provata su uno schermo reale con tutti i giochi: solo con un server X finto
  e il test Corax+, che si vede giusto.
