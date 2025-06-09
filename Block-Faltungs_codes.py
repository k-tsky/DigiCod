#Blockcode
#Beispielaufruf mit m=10, k=5, h=4 -> binf(m=10, k=5, h=4)
def binf(m, k, h):
    valid_codewords = 2 ** m
    all_codewords = 2 ** (m + k)

    detectable_errors = h - 1
    correctable_errors = (h - 2) // 2

    correction_radius = correctable_errors
    volume = 0
    for w in range(correction_radius + 1):
        volume += comb(m + k, w)
    total_volume = valid_codewords * volume
    densely_packed = total_volume >= all_codewords

    print("1) Anzahl gültiger Codeworte: ", valid_codewords)
    print("   Anzahl möglicher Codeworte: ", all_codewords)
    print("2) Sicher erkennbare Fehler: ", detectable_errors)
    print("   Sicher korrigierbare Fehler: ", correctable_errors)
    print("4) Ist der Code dichtgepackt? ", "Ja" if densely_packed else "Nein")
    print("   Volumen aller Korrigierkugeln: ", total_volume)
    print("   Vergleich: ", total_volume, "<" if not densely_packed else ">=", all_codewords)

def comb(n, k):
    if k < 0 or k > n:
        return 0
    result = 1
    for i in range(1, k + 1):
        result = result * (n - i + 1) // i
    return result

#Zyklischer Hammingcode
#Beispiel: haut([1, 0, 1, 1]) entspricht g(x) = 1 + x + x³
def poly_div(dividend, divisor):
    remainder = dividend[:]
    while len(remainder) >= len(divisor):
        if remainder[0] == 1:
            for i in range(len(divisor)):
                if i < len(remainder):
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

def int_to_bitlist(x, length):
    bits = []
    for i in range(length - 1, -1, -1):
        bits.append((x >> i) & 1)
    return bits

def generate_codewords(generator, m):
    codewords = []
    for i in range(2 ** m):
        msg = int_to_bitlist(i, m)
        codeword = encode(generator, msg)
        codewords.append(codeword)
    return codewords

def syndrome(generator, pos, n):
    # Erzeuge Fehlervektor mit einem 1-bit an der gegebenen Position
    error = [0] * n
    error[pos] = 1

    # Division des Fehlerpolynoms durch Generator
    remainder = poly_div(error[:], generator)

    # Padding: Stelle sicher, dass das Syndrom die richtige Länge hat
    while len(remainder) < len(generator) - 1:
        remainder.insert(0, 0)

    return remainder

def build_H_matrix(generator, n):
    syndromes = []
    for i in range(n):
        syndromes.append(syndrome(generator, i, n))
    H = []
    for col in zip(*syndromes):
        H.append(list(col))
    return H, syndromes

def haut(generator):
    k = len(generator) - 1
    n = 2 ** k - 1
    m = n - k

    print("Gegebener Generator:", generator)
    print("Kontrollstellen (k):", k)
    print("Länge des Codeworts (n):", n)
    print("Nachrichtenstellen (m):", m)

    codewords = generate_codewords(generator, m)
    print("\nGültige Codewörter:")
    for w in codewords:
        print(''.join([str(b) for b in w]))

    H, syndromes = build_H_matrix(generator, n)

    print("\nFehler   Resultat                  Syndrom")
    print("--------------------------------------------")

    for i, s in enumerate(syndromes):
        fehler = "x^{}".format(n - 1 - i)
        resultat = ""
        if s[0]: resultat += "x^2 "
        if s[1]: resultat += "+ x " if resultat else "x "
        if s[2]: resultat += "+ 1" if resultat else "1"
        resultat = resultat.strip()
        if not resultat:
            resultat = "Rest 0"
        else:
            resultat = "Rest " + resultat

        syndrom_str = "[" + " ".join(str(bit) for bit in s) + "]"
        print("{:<7} {:<25} {}".format(fehler, resultat, syndrom_str))


    print("\nPrüfmatrix H:")
    for row in H:
        print(row)


#CRC Code
# Beispielaufruf rcc([1, 1, 0, 0, 1]) -> 1 + x + x^4
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
    n = 2 ** (k - 1) - 1
    m = n - k
    codewords = []
    for i in range(min(2 ** m, 6)):
        msg = int_to_bitlist(i, m)  
        codeword = encode(generator, msg)
        codewords.append(codeword)
    return codewords, m, n, k

def rcc(generator_base_poly):
    g_crc = poly_multiply_mod2(generator_base_poly, [1, 1])
    k = len(g_crc) - 1
    n = 2 ** (k - 1) - 1
    m = n - k
    h = 4

    print("Gegebenes primitives Polynom:", generator_base_poly)
    print("CRC Generatorpolynom:", g_crc)
    print("Anzahl Kontrollstellen (k):", k)
    print("Hammingdistanz (bei CRC immer 4):", h)
    print("Abramson Code (n):", n)
    print("Gültige Codewörter:", 2 ** m)
    print("Mögliche Codewörter:", 2 ** n)

    codewords, _, _, _ = generate_codewords_crc(g_crc)
    print("\nBeispiele gültiger Codewörter (nur die ersten 6):")
    for word in codewords:
        print(''.join([str(bit) for bit in word]))

#Faltungscodes
#Beispielaufruf gsm([1, 1, 0], [1, 1, 1], 185) 1 + x^3 + x^4 => [1, 0, 0, 1, 1]
def gsm(g1, g2, input_bits_length):
    m = max(len(g1), len(g2)) - 1
    tailbits = m

    total_input_bits = input_bits_length + tailbits
    total_output_bits = 2 * total_input_bits
    code_rate = input_bits_length / total_output_bits

    print("Generatorpolynom g1(x):", g1)
    print("Generatorpolynom g2(x):", g2)
    print("Encodergedächtnis (m):", m)
    print("Anzahl Tailbits:", tailbits)
    print("Länge der codierten Nachricht (inkl. Tailbits):", total_input_bits)
    print("Gesendete Bits:", total_output_bits)
    print("Block-Coderate R =", input_bits_length, "/ (2 *", total_input_bits, ") =", round(code_rate, 3))