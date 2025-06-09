# DigiCod
# 1       Glossar

## 1.1      Gruppen, Ring und Körper / Text, Festkomma- und Gleitkommazahlen (U3 & U4)

| Thema | Funktion | Output |
| --- | --- | --- |
| Division von Binärzahlen | Notation: u⁴ + u² + u + 1 → [1, 0, 1, 1, 1]div([1, 0, 0, 0, 1], [1, 0, 1]) | ([Quotient], [Rest]) |
| Polynom-Addition in Z_2 | ad2([1, 0, 0, 0, 1], [0, 1, 0, 1, 1]) | [1, 1, 1, 0, 0] d.h Codewort: 11100 |
| Polynom-Multiplikation in Z_2 | mu2([1, 0, 0, 0, 1], [0, 1, 0, 1, 1]) | [1, 1, 1, 0, 0] d.h Codewort: 11100 |
| Polynom-Division in Z_2 (long division) | divl([1, 0, 0, 0, 1], [0, 1, 0, 1, 1]) | ([Quotient], [Rest]) |
| Vektoraddition in Z_2 | addv([[1, 1, 0], [0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 0, 1]]) | [1, 0, 0] |
| Erweiterungskörper (elemente die durch polynom erzeugt werden können) | gfe([1, 0, 0, 1, 1]) -> x^4 + x + 1 | Aufkettung von den Elementen |
| Reduzible Polynome(Ist ein polynom reduzibel?) | isr([1, 1, 0]) -> x² + x | true/false |
| Darstellung negativer Zahlen (bin) | cvb("11111") | Betrag, Betrag mit Vorzeichen, Exzess-4, b-1 (1erKompl.), b (2erKompl.) |
| Komplement von Dezimalzahlen | 9er Komplement: nk(1234)10er: nk(1234) + 1 |  |
| Addition von Komplementen (dez) | 9er: ank(-2, 1)10er: azk(-2, 1) |  |
| Exzess Darstellung (Wortlänge 8Bit) | 1. Zahl: Zahl 2. Zahl: ExzessDezimal zu Binär: de(34, 2)Binär zu Dezimal: ed("11111111", 2) |  |

## 1.2      Informationstheorie / Quellencodierung und Komprimierung (U7/U8)

| Thema | Funktion | Output |
| --- | --- | --- |
| Diskrete Quelle ohne Gedächtnis | bq([0.3, 0.1, 0.1, 0.2, 0.3]) |  |
| Diskrete Quelle mit Gedächtnis | bqg([    [0.1, 0.5, 0.4],    [0.4, 0.2, 0.4],    [0.3, 0.3, 0.4]]) |  |
| Codierung - bei gegebener Wahrscheinlichkeit | ac([    ["a", "0", 0.3],    ["b", "110", 0.1],    ["c", "1111", 0.1],    ["d", "1110", 0.2],    ["e", "10", 0.3]]) |  |

## 1.3      Blockcodes und Fatlungscodes (U11/12)

| Thema | Funktion | Output |
| --- | --- | --- |
| Infos zu Blockcodes:-Anzahl gültige/mögliche Codewörter-Sicher erkennbare Fehlerzahl und sicher korrigierbare Fehler-Dichtgepackt (Ja/Nein) | binf(10, 5, 4)1. m=Nachrichtenstellen2. k=Kontrollstellen3. h=Hammingdistanz |  |
| Zyklischer Hammingcode für Generatorpolynom | haut([1, 0, 1, 1]) entspricht g(x) = 1 + x + x³ |  |
| CRC Code | rcc([1, 1, 0, 0, 1]) -> 1 + x + x^4 |  |
| Faltungscodes: GSM | gsm([1, 1, 0], [1, 1, 1], 185)1 + x^3 + x^4 => [1, 0, 0, 1, 1] |  |
