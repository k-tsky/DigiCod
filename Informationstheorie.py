import math
#Diskrete Quelle ohne Gedächtnis
#Input: bq([0.3, 0.1, 0.1, 0.2, 0.3])

def bq(p):
    N = len(p)

    # a) Entscheidungsgehalt
    H0 = math.log(N) / math.log(2)
    print("a) Entscheidungsgehalt H0 = log2(%d) = %.2f bit" % (N, H0))

    # b) Informationsgehalt
    print("\nb) Informationsgehalt I(xk) = -log2(p(xk)):")
    for i in range(len(p)):
        pk = p[i]
        ik = -math.log(pk) / math.log(2)
        print("Zeichen %s: p = %.2f, I = %.2f bit" % (chr(97 + i), pk, ik))
        p[i] = (pk, ik)

    # c) Entropie mit p * I
    H = 0
    print("\nc) Entropie H(x) = Sum(p * I):")
    for i in range(len(p)):
        pk, ik = p[i]
        pik = pk * ik
        H += pik
        print("Zeichen %s: p = %.2f, I = %.2f, p * I = %.2f" % (chr(97 + i), pk, ik, pik))
    print("H(x) = %.2f bit/Zeichen" % H)

    # d) Redundanz
    RQ = H0 - H
    print("\nd) Redundanz RQ = H0 - H(x) = %.2f - %.2f = %.2f bit" % (H0, H, RQ))

#Diskrete Quelle mit Gedächtnis
'''Input: bqg([
    [0.1, 0.5, 0.4],
    [0.4, 0.2, 0.4],
    [0.3, 0.3, 0.4]
])'''
def bqg(P_Y_given_X):
    N = len(P_Y_given_X)

    print("Gegeben: Übergangsmatrix P(Y|X):")
    for i in range(N):
        zeile = P_Y_given_X[i]
        print([("%.3f" % x) for x in zeile])
    print()

    a11, a12, a13 = P_Y_given_X[0]
    a21, a22, a23 = P_Y_given_X[1]
    a31, a32, a33 = P_Y_given_X[2]

    def loese_stationaer():
        A = a11 - 1 - a31
        B = a21 - a31
        C = a31
        D = a12 - a32
        E = a22 - 1 - a32
        F = a32
        det = A * E - B * D
        det_p1 = -C * E + B * F
        det_p2 = -A * F + C * D

        p1 = det_p1 / det
        p2 = det_p2 / det
        p3 = 1 - p1 - p2

        return [p1, p2, p3]

    P_X = loese_stationaer()

    print("Stationäre Wahrscheinlichkeiten P(X):")
    for i in range(N):
        print("P(x%d) = %.3f" % (i + 1, P_X[i]))
    print()

    P_XY = []
    for i in range(N):
        zeile = []
        for j in range(N):
            zeile.append(P_X[i] * P_Y_given_X[i][j])
        P_XY.append(zeile)

    print("Gemeinsame Wahrscheinlichkeiten P(X,Y):")
    for i in range(N):
        print([("%.3f" % pxy) for pxy in P_XY[i]])
    print()

    H_X = 0
    print("Entropie H(X):")
    for i in range(N):
        px = P_X[i]
        ix = -math.log(px) / math.log(2)
        pix = px * ix
        H_X += pix
        print("x%d: P = %.3f, I = %.2f, P*I = %.2f" % (i+1, px, ix, pix))
    print("H(X) = %.3f bit\n" % H_X)

    H_XY = 0
    print("Verbundentropie H(X,Y):")
    for i in range(N):
        for j in range(N):
            pxy = P_XY[i][j]
            if pxy > 0:
                hxy = -pxy * math.log(pxy) / math.log(2)
                H_XY += hxy
                print("P(x%d, y%d) = %.3f, -P*log2(P) = %.3f" % (i+1, j+1, pxy, hxy))
    print("H(X,Y) = %.3f bit\n" % H_XY)

    H_Y_given_X = H_XY - H_X
    print("Bedingte Entropie H(Y|X) = H(X,Y) - H(X) = %.3f - %.3f = %.3f bit" % (H_XY, H_X, H_Y_given_X))

#Codierung - bei gegebener Wahrscheinlichkeit
'''Input:ac([
    ["a", "0", 0.3],
    ["b", "110", 0.1],
    ["c", "1111", 0.1],
    ["d", "1110", 0.2],
    ["e", "10", 0.3]
])'''
def ac(kompakt_input):
    mittlere_laenge = 0
    entropie = 0
    zeilen = []

    for eintrag in kompakt_input:
        zeichen = eintrag[0]
        codewort = eintrag[1]
        p = eintrag[2]
        l = len(codewort)
        pL = p * l
        mittlere_laenge += pL
        entropie -= p * (math.log(p) / math.log(2))
        zeilen.append([zeichen, p, l, pL])

    redundanz = mittlere_laenge - entropie

    print("L = Summe(p(xk) * L(xk)) = %.1f bit\n" % mittlere_laenge)

    print("+---------+-----+---+-------+")
    print("| Zeichen |  p  | L | p * L |")
    print("+---------+-----+---+-------+")

    for z in zeilen:
        print("|   %-5s | %.1f | %d | %.1f   |" % (z[0], z[1], z[2], z[3]))

    print("+---------+-----+---+-------+")
    print("|         |     |   | Summe: %.1f |" % mittlere_laenge)
    print("+---------+-----+---+-------+\n")

    print("--- Ergebnisse ---")
    print("Mittlere Codewortlänge: %.2f bit" % mittlere_laenge)
    print("Entropie H(X): %.2f bit" % entropie)
    print("Redundanz: %.2f bit" % redundanz)





