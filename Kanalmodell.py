import math

def berechne_kanalinformationen(P_Y_X, p_x, uebertragungsrate):
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

# Beispielwerte laut Aufgabenstellung
P_Y_X = [
    [0.9, 0.1],  # P(y1|x1), P(y2|x1)
    [0.1, 0.9]   # P(y1|x2), P(y2|x2)
]
p_x = [0.3, 0.7]
uebertragungsrate = 1000  # Zeichen pro Sekunde

# Funktionsaufruf
berechne_kanalinformationen(P_Y_X, p_x, uebertragungsrate)


