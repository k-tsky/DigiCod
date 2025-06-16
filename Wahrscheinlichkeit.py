#Berechnung
#Input: Beispiel: 6 aus 49 die Wahrscheinlichkeit 4 Richtige zu erhalten
#Nur alle Ergebnisse: blk(49, 6) -> Ohne Beachtung der Reihenfolge und Rückweg
#Bestimmte Anzahl richtige Erhalten: bkw(N=49, M=6, n=6, k=4)
def fakultaet(n):
    if n == 0 or n == 1:
        return 1
    produkt = 1
    for i in range(2, n + 1):
        produkt *= i
    return produkt

def blk(n, k):
    if k < 0 or k > n:
        return 0
    return fakultaet(n) // (fakultaet(k) * fakultaet(n - k))

def bkw(N, M, n, k):
    # N: Grundgesamtheit (z. B. 49)
    # M: Anzahl "Erfolge" in der Grundgesamtheit (z. B. 6 gezogene)
    # n: Stichprobengröße (z. B. 6 getippte Zahlen)
    # k: Anzahl Treffer
    if k > M or (n - k) > (N - M):
        print("Ungültiger Wert für k – zu viele Treffer möglich.")
        return
    guenstig = blk(M, k) * blk(N - M, n - k)
    gesamt = blk(N, n)
    p = guenstig / gesamt
    print("P(", k, "Richtige ) = ", "{:.8f}".format(p))

# Beispielaufruf: Lotto 6 aus 49, 4 Richtige
bkw(N=15, M=2, n=6, k=2)
