Piccolo script per analizzare un log .ADIF  ed estrarre gli elementi utili alla Maratona DX 2025 di ARI Roma.

1- se non lo avete, installare Python (In Windows è disponibile nello store)

2- scaricare il file maratona.py in una cartella dove metterete anche il vostro log in formato .ADIF

3- in una finestra terminale (in Windows: tasto Win, scrivere CMD nella finestra di ricerca e dare invio) navigare fino alla cartella dove avete salvato il log in formato .ADIF

4- eseguire con:
  python maratona.py [nome del log]
sotto Windows potrebbe funzionare con
 py maratona.py [nome del log]

5- il software stampa a schermo le decisioni relative a ogni singolo QSO, i risultati ed eventuali avvisi.
   Se volete salvare questo output in un file da leggere con calma, eseguire ridirigendo l'output. 
   Esempio: salvo nel file pippo.txt
   python maratona.py [nome del log] > [pippo.txt]

6- viene generato un rapportino nel file "calcolo-maratona.csv" che può essere poi copiato e incollato nel file Excel ufficiale

Testato con .adi generati da QLog, BBLOGGER, QARTest (a seconda del contest non include la zona CQ) e QRZLog
