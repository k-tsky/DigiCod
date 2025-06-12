import math

#Kanalmatrix basic
#Input: bk([[0.9, 0.1],[0.1, 0.9]], [0.3, 0.7], 1000)
#Input: 1. Kanalmatrix, 2. Auftrittswahrscheinlichkeit, 3. Übertragungsrate (1kbit/s = 1000)
def bk(P_Y_X, p_x, uebertragungsrate):
    # 1) Entropie H(X)
    H_X = 0
    for i in range(2):
        if p_x[i] > 0:
            H_X -= p_x[i] * math.log(p_x[i]) / math.log(2)

    # 2) Wahrscheinlichkeiten p(y1), p(y2)
    p_y = [0, 0]
    for j in range(2):
        for i in range(2):
            p_y[j] += p_x[i] * P_Y_X[i][j]

    # 3) Entropie H(Y)
    H_Y = 0
    for j in range(2):
        if p_y[j] > 0:
            H_Y -= p_y[j] * math.log(p_y[j]) / math.log(2)

    # 4) Bedingte Entropie H(Y|X)
    H_Y_given_X = 0
    for i in range(2):
        for j in range(2):
            p = P_Y_X[i][j]
            if p > 0:
                H_Y_given_X -= p_x[i] * p * math.log(p) / math.log(2)

    # 5) Transinformation
    T = H_Y - H_Y_given_X

    # 6) Maximale Symbolrate
    R_max = T * uebertragungsrate

    # Ausgabe
    print("H(X) =", round(H_X, 4), "bit/Zeichen")
    print("H(Y) =", round(H_Y, 4), "bit/Zeichen")
    print("H(Y|X) =", round(H_Y_given_X, 4), "bit/Zeichen")
    print("T =", round(T, 4), "bit/Zeichen")
    print("R_max =", round(R_max, 2), "bit/s")

#Entscheider und Fehlerwahrscheinlichkeit
#Input: euf([[0.2, 0.5, 0.3], [0.7, 0.2, 0.1], [0.4, 0.0, 0.6]], [550, 1200, 3000])
def euf(P_Y_given_X, haeufigkeiten):
    # 1. Entscheider (Maximum-Likelihood): Für jede Zeile den Index des Maximums bestimmen
    # Dies bedeutet: Für jedes y_i -> bestes x_j
    entscheider = []
    for i in range(len(P_Y_given_X[0])):  # Spaltenweise durchgehen (y_i)
        max_prob = 0
        max_index = 0
        for j in range(len(P_Y_given_X)):  # Zeilenweise durchgehen (x_j)
            if P_Y_given_X[j][i] > max_prob:
                max_prob = P_Y_given_X[j][i]
                max_index = j
        entscheider.append(max_index)  # y_i wird zu x_max_index zugeordnet

    # 2. Auftretenswahrscheinlichkeiten aus Häufigkeiten berechnen
    gesamt = sum(haeufigkeiten)
    p_x = [h / gesamt for h in haeufigkeiten]

    # 3. Wahrscheinlichkeit für "Kein Fehler"
    # D.h. Wahrscheinlichkeit, dass der Entscheider die richtige Entscheidung trifft
    # Dafür nehmen wir P(y_i | x_j) * P(x_j), wobei y_i -> x_j gemappt wird im Entscheider
    p_keine_fehler = 0
    for y_i, x_j in enumerate(entscheider):
        p_keine_fehler += P_Y_given_X[x_j][y_i] * p_x[x_j]

    # 4. Fehlerwahrscheinlichkeit
    p_fehler = 1 - p_keine_fehler

    resultat = {
        "entscheider": entscheider,
        "p_x": p_x,
        "p_keine_fehler": p_keine_fehler,
        "p_fehler": p_fehler
    }

    print("Entscheider (y_i -> x_j):", resultat["entscheider"])
    print("P(x):", resultat["p_x"])
    print("P(Keine Fehler):", resultat["p_keine_fehler"])
    print("P(Fehler):", resultat["p_fehler"])


#Kanalmatrix bei gegebenen Wahrscheinlichkeiten
#Input: btk([0.3, 0.7], [0.34, 0.66], 140, 500)
"""
p_x = [0.3, 0.7]
p_y = [0.34, 0.66]
kanalrate_kbps = 140
blocksize_mbit = 500
"""
def btk(p_x, p_y, kanalrate_kbps, blocksize_mbit):
    px0, px1 = p_x
    py0, py1 = p_y

    # LGS lösen (symbolisch hergeleitet)
    a = (py0 * px1 - py1 * px0) / (px1**2 - px0**2)
    b = 1 - a  # da symmetrisch: a + b = 1

    # 1. Kanalmatrix
    P_Y_given_X = [
        [a, b],
        [b, a]
    ]

    # 2. Ausgangsentropie H(Y)
    H_Y = -sum([p * math.log(p, 2) for p in p_y if p > 0])

    # 3. Bedingte Entropie H(Y|X)
    H_Y_given_X = 0
    for i in range(len(p_x)):
        for j in range(len(p_y)):
            p_y_given_x = P_Y_given_X[i][j]
            if p_y_given_x > 0:
                H_Y_given_X += p_x[i] * p_y_given_x * math.log(p_y_given_x, 2)
    H_Y_given_X = -H_Y_given_X

    # 4. Transinformation
    T = H_Y - H_Y_given_X

    # 5. Maximale Übertragungsrate
    R_max = T * kanalrate_kbps * 1000  # in bit/s

    # 6. Minimale Zeit zur Übertragung
    L = blocksize_mbit * 1_000_000
    t = L / R_max
    t_h = t / 3600

    result = {
        "P_Y_given_X": P_Y_given_X,
        "H_Y": H_Y,
        "H_Y_given_X": H_Y_given_X,
        "T": T,
        "R_max_bit_s": R_max,
        "Übertragungszeit_s": t,
        "Übertragungszeit_h": t_h
    }

    print("P(Y|X):", result["P_Y_given_X"])
    print("Ausgangsentropie H(Y):", result["H_Y"])
    print("Irrelevanz H(Y|X):", result["H_Y_given_X"])
    print("Transinformation:", result["T"])
    print("Max. Rate (bit/s):", result["R_max_bit_s"])
    print("Zeit (s):", result["Übertragungszeit_s"])
    print("Zeit (h):", result["Übertragungszeit_h"])






