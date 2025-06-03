import math
#Diskrete Quelle ohne Gedächtnis
#Input: berechne_quelleninfo([0.3, 0.1, 0.1, 0.2, 0.3])

def berechne_quelleninfo(p):
    N = len(p)

    # a) Entscheidungsgehalt
    H0 = math.log2(N)
    print("a) Entscheidungsgehalt H0 = log2({}) = {:.2f} bit".format(N, H0))

    # b) Informationsgehalt
    I = [-math.log2(pk) for pk in p]
    print("\nb) Informationsgehalt I(xk) = -log2(p(xk)):")
    for i, (pk, ik) in enumerate(zip(p, I)):
        print("Zeichen {}: p = {:.2f}, I = {:.2f} bit".format(chr(97 + i), pk, ik))

    # c) Entropie mit p * I
    pI = [pk * ik for pk, ik in zip(p, I)]
    H = sum(pI)
    print("\nc) Entropie H(x) = Sum(p * I) = {:.2f} bit/Zeichen".format(H))
    print("p * I je Zeichen:")
    for i, (pk, ik, pik) in enumerate(zip(p, I, pI)):
        print("Zeichen {}: p = {:.2f}, I = {:.2f}, p * I = {:.2f}".format(chr(97 + i), pk, ik, pik))

    # d) Redundanz
    RQ = H0 - H
    print("\nd) Redundanz RQ = H0 - H(x) = {:.2f} - {:.2f} = {:.2f} bit".format(H0, H, RQ))

#Diskrete Quelle mit Gedächtnis
'''Input: berechne_markov_mit_gleichungssystem([
    [0.1, 0.5, 0.4],
    [0.4, 0.2, 0.4],
    [0.3, 0.3, 0.4]
])'''
def berechne_markov_mit_gleichungssystem(P_Y_given_X):
    N = len(P_Y_given_X)

    print("Gegeben: Übergangsmatrix P(Y|X):")
    for zeile in P_Y_given_X:
        print(["{:.3f}".format(x) for x in zeile])
    print()

    # Manuelles Gleichungssystem aus Übergangsmatrix (für 3 Zustände):
    # Wir setzen die Gleichungen gemäß: P = P * A, also:
    # p1 = p1*a11 + p2*a21 + p3*a31
    # p2 = p1*a12 + p2*a22 + p3*a32
    # p3 = p1*a13 + p2*a23 + p3*a33
    # mit Bedingung: p1 + p2 + p3 = 1

    a11, a12, a13 = P_Y_given_X[0]
    a21, a22, a23 = P_Y_given_X[1]
    a31, a32, a33 = P_Y_given_X[2]

    # Setze Gleichungen (ausbalanciert)
    # Wir eliminieren z. B. p3 = 1 - p1 - p2, und setzen es in die anderen beiden ein

    def loese_stationaer():
        # p3 = 1 - p1 - p2
        # p1 = p1*a11 + p2*a21 + (1 - p1 - p2)*a31
        # p2 = p1*a12 + p2*a22 + (1 - p1 - p2)*a32

        # Gleichung 1:
        # p1 = p1*a11 + p2*a21 + a31 - p1*a31 - p2*a31
        # 0 = p1*(a11 - 1 - a31) + p2*(a21 - a31) + a31

        A = (a11 - 1 - a31)
        B = (a21 - a31)
        C = a31

        # Gleichung 2:
        # p2 = p1*a12 + p2*a22 + a32 - p1*a32 - p2*a32
        # 0 = p1*(a12 - a32) + p2*(a22 - 1 - a32) + a32

        D = (a12 - a32)
        E = (a22 - 1 - a32)
        F = a32

        # Jetzt: 2 Gleichungen mit 2 Unbekannten (p1, p2)
        # A*p1 + B*p2 + C = 0
        # D*p1 + E*p2 + F = 0

        # Lösung per Cramer's Rule (determinantenbasiert)
        det = A * E - B * D
        det_p1 = -C * E + B * F
        det_p2 = -A * F + C * D

        p1 = det_p1 / det
        p2 = det_p2 / det
        p3 = 1 - p1 - p2

        return [p1, p2, p3]

    P_X = loese_stationaer()

    print("Stationäre Wahrscheinlichkeiten P(X) gelöst aus Gleichungssystem:")
    for i, px in enumerate(P_X):
        print(f"P(x{i+1}) = {px:.3f}")
    print()

    # Berechne P(X,Y)
    P_XY = [[P_X[i] * P_Y_given_X[i][j] for j in range(N)] for i in range(N)]

    print("Gemeinsame Wahrscheinlichkeiten P(X,Y):")
    for i in range(N):
        print(["{:.3f}".format(pxy) for pxy in P_XY[i]])
    print()

    # Entropie H(X)
    I_X = [-math.log2(px) if px > 0 else 0 for px in P_X]
    H_X = sum(px * ix for px, ix in zip(P_X, I_X))
    print("Entropie H(X):")
    for i in range(N):
        print(f"x{i+1}: P = {P_X[i]:.3f}, I = {I_X[i]:.2f}, P*I = {P_X[i]*I_X[i]:.2f}")
    print("H(X) = {:.3f} bit\n".format(H_X))

    # Entropie H(X,Y)
    H_XY = 0
    print("Verbundentropie H(X,Y):")
    for i in range(N):
        for j in range(N):
            pxy = P_XY[i][j]
            hxy = -pxy * math.log2(pxy) if pxy > 0 else 0
            H_XY += hxy
            print(f"P(x{i+1}, y{j+1}) = {pxy:.3f}, -P*log2(P) = {hxy:.3f}")
    print("H(X,Y) = {:.3f} bit\n".format(H_XY))

    # Bedingte Entropie H(Y|X)
    H_Y_given_X = H_XY - H_X
    print("Bedingte Entropie H(Y|X) = H(X,Y) - H(X) = {:.3f} - {:.3f} = {:.3f} bit".format(H_XY, H_X, H_Y_given_X))

#Codierung - bei gegebener Wahrscheinlichkeit
'''Input:analysiere_code([
    ["a", "0", 0.3],
    ["b", "110", 0.1],
    ["c", "1111", 0.1],
    ["d", "1110", 0.2],
    ["e", "10", 0.3]
])'''
def analysiere_code(kompakt_input):
    mittlere_laenge = 0
    entropie = 0
    zeilen = []

    for eintrag in kompakt_input:
        zeichen, codewort, p = eintrag
        l = len(codewort)
        pL = p * l
        mittlere_laenge += pL
        entropie -= p * (math.log(p) / math.log(2))
        zeilen.append([zeichen, p, l, pL])

    redundanz = mittlere_laenge - entropie

    # Formel-Ausgabe (ASCII)
    print("L = Summe(p(xk) * L(xk)) = %.1f bit\n" % mittlere_laenge)

    # Tabellenkopf
    print("+---------+-----+---+-------+")
    print("| Zeichen |  p  | L | p * L |")
    print("+---------+-----+---+-------+")

    # Tabelleninhalt
    for z in zeilen:
        print("|   %-5s | %.1f | %d | %.1f   |" % (z[0], z[1], z[2], z[3]))

    print("+---------+-----+---+-------+")
    print("|         |     |   | Summe: %.1f |" % mittlere_laenge)
    print("+---------+-----+---+-------+\n")

    # Weitere Ergebnisse
    print("--- Ergebnisse ---")
    print("Mittlere Codewortlänge: %.2f bit" % mittlere_laenge)
    print("Entropie H(X): %.2f bit" % entropie)
    print("Redundanz: %.2f bit" % redundanz)





