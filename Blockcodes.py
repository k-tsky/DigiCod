from math import comb

#Blockcode
#Beispielaufruf mit m=10, k=5, h=4 -> blockcode_info(m=10, k=5, h=4)
def blockcode_info(m, k, h):
    # 1. Anzahl gültiger und möglicher Codeworte
    valid_codewords = 2 ** m
    all_codewords = 2 ** (m + k)

    # 2. Fehlererkennung und Fehlerkorrektur
    detectable_errors = h - 1
    correctable_errors = (h - 2) // 2  # ganzzahlig, da h gerade ist

    # 4. Dichtgepacktheit überprüfen
    correction_radius = correctable_errors
    volume = sum([comb(m + k, w) for w in range(correction_radius + 1)])
    total_volume = valid_codewords * volume
    densely_packed = total_volume >= all_codewords  # Prüfen, ob alle Kugeln den Raum füllen

    # Ergebnisse ausgeben
    print("1) Anzahl gültiger Codeworte: ", valid_codewords)
    print("   Anzahl möglicher Codeworte: ", all_codewords)
    print("2) Sicher erkennbare Fehler: ", detectable_errors)
    print("   Sicher korrigierbare Fehler: ", correctable_errors)
    print("4) Ist der Code dichtgepackt? ", "Ja" if densely_packed else "Nein")
    print("   Volumen aller Korrigierkugeln: ", total_volume)
    print("   Vergleich: ", total_volume, "<", all_codewords if not densely_packed else ">=", all_codewords)


#Zyklischer Hammingcode
#Beispiel: run_hamming_code_auto([1, 0, 1, 1]) entspricht g(x) = 1 + x + x³
def poly_div(dividend, divisor):
    remainder = dividend[:]
    while len(remainder) >= len(divisor):
        if remainder[0] == 1:
            for i in range(len(divisor)):
                if i < len(remainder):  # Sicherstellen, dass Index gültig ist
                    remainder[i] ^= divisor[i]
        remainder.pop(0)
    return remainder


def message_to_polynomial(msg_bits, r):
    return msg_bits + [0] * r

def encode(generator, message_bits):
    r = len(generator) - 1
    poly = message_to_polynomial(message_bits, r)
    remainder = poly_div(poly[:], generator)
    return message_bits + remainder

def generate_codewords(generator, m):
    codewords = []
    for i in range(2**m):
        msg = [int(b) for b in bin(i)[2:].zfill(m)]
        codeword = encode(generator, msg)
        codewords.append(codeword)
    return codewords

def syndrome(generator, pos, n):
    error = [0] * n
    error[pos] = 1
    s = poly_div(error, generator)
    s = [0] * (len(generator) - 1 - len(s)) + s
    return s

def build_H_matrix(generator, n):
    syndromes = [syndrome(generator, i, n) for i in range(n)]
    H = [list(row) for row in zip(*syndromes)]  # Transponieren
    return H, syndromes

def run_hamming_code_auto(generator):
    # Grad des Generatorpolynoms = k
    k = len(generator) - 1
    n = 2**k - 1
    m = n - k

    print("Gegebener Generator:", generator)
    print(f"Kontrollstellen (k): {k}")
    print(f"Länge des Codeworts (n): {n}")
    print(f"Nachrichtenstellen (m): {m}")

    # 1) Codewörter
    codewords = generate_codewords(generator, m)
    print("\nGültige Codewörter:")
    for w in codewords:
        print(''.join(map(str, w)))

    # 2) Syndrome
    H, syndromes = build_H_matrix(generator, n)
    print("\nSyndrome bei Einzelbitfehlern:")
    for i, s in enumerate(syndromes):
        print(f"Fehler an Position {i}: {s}")

    # 3) Prüfmatrix
    print("\nPrüfmatrix H:")
    for row in H:
        print(row)


#CRC Code
# Beispielaufruf run_crc_code([1, 1, 0, 0, 1]) -> 1 + x + x^4
def poly_add(p1, p2):
    max_len = max(len(p1), len(p2))
    p1 = [0] * (max_len - len(p1)) + p1
    p2 = [0] * (max_len - len(p2)) + p2
    return [a ^ b for a, b in zip(p1, p2)]

def poly_multiply_mod2(p1, p2):
    result = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        if p1[i] == 1:
            for j in range(len(p2)):
                result[i + j] ^= p2[j]
    return result

def generate_codewords_crc(generator):
    k = len(generator) - 1
    n = 2 ** (k-1) - 1
    m = n - k
    codewords = []
    for i in range(min(2 ** m, 6)):
        msg = [int(b) for b in bin(i)[2:].zfill(m)]
        codeword = encode(generator, msg)
        codewords.append(codeword)
    return codewords, m, n, k

def run_crc_code(generator_base_poly):
    # Berechne CRC-Generatorpolynom: (primitive_polynomial) * (1 + x)
    g_crc = poly_multiply_mod2(generator_base_poly, [1, 1])

    # Berechne m, n, k
    k = len(g_crc) - 1
    n = (2 ** (k-1)) - 1
    m = n - k
    h = 4  # Per Definition für CRC

    print("Gegebenes primitives Polynom:", generator_base_poly)
    print("CRC Generatorpolynom:", g_crc)
    print("Anzahl Kontrollstellen (k):", k)
    print("Hammingdistanz (bei CRC immer 4):", h)
    print("Abramson Code (n):", n)
    print("Gültige Codewörter:", 2 ** m)
    print("Mögliche Codewörter:", 2 ** n)

    codewords, _, _, _ = generate_codewords_crc(g_crc)
    print("\nBeispiele gültiger Codewörter (nur die ersten 6):")
    for word in codewords[:]:
        print(''.join(str(bit) for bit in word))
