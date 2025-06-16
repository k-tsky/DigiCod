# 1       Glossar

## 1.1      Gruppen, Ring und Körper / Text, Festkomma- und Gleitkommazahlen (U3 & U4)

File: conversions.py

| Thema | Funktion | Output |
| --- | --- | --- |
| Division von Binärzahlen | Notation: u⁴ + u² + u + 1 → [1, 0, 1, 1, 1]div([1, 0, 0, 0, 1], [1, 0, 1]) | ([Quotient], [Rest]) |
| Addition von Binärzahlen | bad("10111111", "11000011") |  |
| Subtraktion von Binärzahlen | bs("1111", "1010") |  |
| Polynom-Addition in Z_2 | ad2([1, 0, 0, 0, 1], [0, 1, 0, 1, 1]) | [1, 1, 1, 0, 0] d.h Codewort: 11100 |
| Polynom-Multiplikation in Z_2 | mu2([1, 0, 0, 0, 1], [0, 1, 0, 1, 1]) | [1, 1, 1, 0, 0] d.h Codewort: 11100 |
| Polynom-Division in Z_2 (long division) | divl([1, 0, 0, 0, 1], [0, 1, 0, 1, 1]) | ([Quotient], [Rest]) |
| Vektoraddition in Z_2 | addv([[1, 1, 0], [0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 0, 1]]) | [1, 0, 0] |
| Erweiterungskörper (elemente die durch polynom erzeugt werden können) | gfe([1, 0, 0, 1, 1]) -> x^4 + x + 1 | Aufkettung von den ElementenZykluslänge |
| Reduzible Polynome(Ist ein polynom reduzibel?) | isr([1, 1, 0]) -> x² + x | true/false |
| Darstellung negativer Zahlen (bin) | cvb("11111") | Betrag, Betrag mit Vorzeichen, Exzess-4, b-1 (1erKompl.), b (2erKompl.) |
| Komplement von Dezimalzahlen | 9er Komplement: nk(1234)10er: nk(1234) + 1 |  |
| Addition von Komplementen (dez) | 9er: ank(-2, 1)10er: azk(-2, 1) |  |
| Exzess Darstellung | 1. Zahl: Zahl2. Zahl: Exzess (Bias)3. Wortlänge (default=8)Dezimal zu Binär: de(34, 2, 4)Binär zu Dezimal: ed("11111111", 2)Achtung: Das Minus ist implizit, für Exzess--4 also -4eingeben |  |
| Kleinste Festkommazahl | kfi(8, 2)Gesamt Bits: 8 (default=8)Vorkomma bits: 2 (default=2) |  |

## 1.2      Informationstheorie / Quellencodierung und Komprimierung (U7/U8)

File: informationstheorie.py

| Thema | Funktion | Output |
| --- | --- | --- |
| Diskrete Quelle ohne Gedächtnis (Achtung: Funktioniert nicht mit nur einer Wahrscheinlichkeit, dann ist Entropie = 1) | bq([0.3, 0.1, 0.1, 0.2, 0.3]) | EntropieInformationsgehaltEntscheidungsgehaltRedundanz |
| Diskrete Quelle mit Gedächtnis | bqg([    [0.1, 0.5, 0.4],    [0.4, 0.2, 0.4],    [0.3, 0.3, 0.4]]) |  |
| Codierung - bei gegebener Wahrscheinlichkeit | ac([    ["a", "0", 0.3],    ["b", "110", 0.1],    ["c", "1111", 0.1],    ["d", "1110", 0.2],    ["e", "10", 0.3]]) |  |

## 1.3      Blockcodes und Faltungscodes (U11/12)

File: Block-Fatlungs\_codes.py

| Thema | Funktion | Output |
| --- | --- | --- |
| Infos zu Blockcodes: | binf(10, 5, 4)1. m=Nachrichtenstellen2. k=Kontrollstellen3. h=Hammingdistanz | -Anzahl gültige/mögliche Codewörter-Sicher erkennbare Fehlerzahl und sicher korrigierbare Fehler-Dichtgepackt (Ja/Nein) |
| Zyklischer Hammingcode für Generatorpolynom | haut([1, 0, 1, 1]) entspricht g(x) = 1 + x + x³ |  |
| CRC Code | rcc([1, 1, 0, 0, 1]) -> 1 + x + x^4 |  |
| Faltungscodes: GSM | gsm([1, 1, 0], [1, 1, 1], 185)1 + x^3 + x^4 => [1, 0, 0, 1, 1] |  |

## 1.4      Kanalmatrix

File: Kanalmodell.py

| Thema | Funktion | Output |
| --- | --- | --- |
| Kanalmatrix basic berechnung | bk([[0.9, 0.1],[0.1, 0.9]], [0.3, 0.7], 1000)1. Kanalmatrix, 2. Auftrittswahrscheinlichkeit, 3. Übertragungsrate (1kbit/s = 1000) |  |
| Entscheider und Fehlerwahrscheinlichkeit | euf([[0.2, 0.5, 0.3], [0.7, 0.2, 0.1], [0.4, 0.0, 0.6]], [550, 1200, 3000]) |  |
| Kanalmatrix bei gegebenen Wahrscheinlichkeiten (Symmetrisch) | btk([0.3, 0.7], [0.34, 0.66], 140, 500)p_x = [0.3, 0.7]p_y = [0.34, 0.66]kanalrate_kbps = 140blocksize_mbit = 500 | IrrelevanzAusgangsentropieTransinformationP(Y|X) |