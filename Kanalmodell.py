import math

#Kanalmatrix basic
#Input: bk([[0.9, 0.1],[0.1, 0.9]], [0.3, 0.7], 1000)
#Input: 1. Kanalmatrix, 2. Auftrittswahrscheinlichkeit, 3. Übertragungsrate (1kbit/s = 1000)
    # Berechnung der bedingten Entropie H(Y|X)
def bhy(P_Y_given_X, p_x):
    H_Y_given_X = 0
    for i in range(len(p_x)):
        for j in range(len(P_Y_given_X[i])):
            p = P_Y_given_X[i][j]
            if p > 0:
                H_Y_given_X -= p_x[i] * p * math.log(p, 2)
    return H_Y_given_X

# Berechnung der Transinformation T = H(Y) - H(Y|X)
def bht(H_Y, H_Y_given_X):
    return H_Y - H_Y_given_X

def bk(P_Y_X, p_x, uebertragungsrate):
    # 1. Eingangs-Entropie H(X)
    H_X = -sum(p * math.log(p, 2) for p in p_x if p > 0)

    # 2. Wahrscheinlichkeiten p(y)
    p_y = [sum(p_x[i] * P_Y_X[i][j] for i in range(2)) for j in range(2)]

    # 3. Ausgangsentropie H(Y)
    H_Y = -sum(p * math.log(p, 2) for p in p_y if p > 0)

    # 4. Bedingte Entropie H(Y|X)
    H_Y_given_X = bhy(P_Y_X, p_x)

    # 5. Transinformation T
    T = bht(H_Y, H_Y_given_X)

    # 6. Maximale Symbolrate
    R_max = T * uebertragungsrate

    print("Eingangs-Entropie H(X):", round(H_X, 4), "bit/Zeichen")
    print("Ausgangs-Entropie H(Y):", round(H_Y, 4), "bit/Zeichen")
    print("Irrelevanz H(Y|X):", round(H_Y_given_X, 4), "bit/Zeichen")
    print("Transinformation T(X→Y):", round(T, 4), "bit/Zeichen")
    print("Maximale Symbolrate R_max:", round(R_max, 2), "bit/s")

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


#Kanalmatrix bei gegebenen Wahrscheinlichkeiten (Kanal Ein- und Ausgang)
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

    # Symmetrische Kanalmatrix berechnen
    a = (py0 * px1 - py1 * px0) / (px1**2 - px0**2)
    b = 1 - a

    P_Y_given_X = [
    [b, a],  # P(Y=0|X=0), P(Y=1|X=0)
    [a, b]   # P(Y=0|X=1), P(Y=1|X=1)
    ]

    # Ausgangsentropie
    H_Y = -sum([p * math.log(p, 2) for p in p_y if p > 0])

    # Bedingte Entropie & Transinformation
    H_Y_given_X = bhy(P_Y_given_X, p_x)
    T = bht(H_Y, H_Y_given_X)

    R_max = T * kanalrate_kbps * 1000
    L = blocksize_mbit * 1_000_000
    t = L / R_max
    t_h = t / 3600

    print("Kanalmatrix P(Y|X):")
    for row in P_Y_given_X:
        print(" ", [round(p, 4) for p in row])

    print("Ausgangsentropie H(Y):", H_Y)
    print("Irrelevanz H(Y|X):", H_Y_given_X)
    print("Transinformation:", T)
    print("Max. Rate (bit/s):", R_max)
    print("Zeit (s):", t)
    print("Zeit (h):", t_h)

btk([0.3, 0.7], [0.34, 0.66], 140, 500)





