#Vorlesung/Übung 3 & 4 (Festkomma- und Gleitkommazahlen, Gruppe, Ring und Körper)
#
#
#Division von Binärzahlen
#Input: div([1, 0, 0, 0, 1], [1, 0, 1])
#Output: Quotient, Rest

def div(dividend, divisor):
    dividend = list(dividend)
    divisor = list(divisor)
    quotient = []

    while len(dividend) >= len(divisor):
        if dividend[0] == 1:
            quotient.append(1)
            for i in range(len(divisor)):
                dividend[i] ^= divisor[i]
        else:
            quotient.append(0)
        dividend.pop(0)

    return quotient, dividend

#Addition von Binärzahlen
#Input: bad("111", "111")
def bad(bin1, bin2):
    # Umwandlung der Binärstrings in Dezimalzahlen
    dez1 = int(bin1, 2)
    dez2 = int(bin2, 2)

    # Addition der Dezimalzahlen
    summe_dez = dez1 + dez2

    # Rückumwandlung in Binärstring (ohne '0b'-Präfix)
    summe_bin = bin(summe_dez)[2:]

    print("Binär 1:", bin1)
    print("Binär 2:", bin2)
    print("Summe   :", summe_bin)


#Substraktion von Binärzahlen
#Input: bs("1101", "1101")
def bs(a_str, b_str):
    # Gleiche Länge durch manuelles Auffüllen mit führenden Nullen
    max_len = max(len(a_str), len(b_str))
    while len(a_str) < max_len:
        a_str = '0' + a_str
    while len(b_str) < max_len:
        b_str = '0' + b_str

    # 1. Invertieren (Einerkomplement)
    b_invert = ''
    for bit in b_str:
        if bit == '0':
            b_invert += '1'
        else:
            b_invert += '0'

    # 2. Eins hinzufügen (Zweierkomplement)
    def add_bin(bin1, bin2):
        result = ''
        carry = 0
        for i in range(len(bin1) - 1, -1, -1):
            total = int(bin1[i]) + int(bin2[i]) + carry
            result = str(total % 2) + result
            carry = total // 2
        if carry:
            result = '1' + result
        return result

    # Manuelles Auffüllen der 1
    bin_one = ''
    while len(bin_one) < max_len - 1:
        bin_one = '0' + bin_one
    bin_one += '1'

    b_zweierkomplement = add_bin(b_invert, bin_one)

    # 3. Addition a + (-b)
    ergebnis = add_bin(a_str, b_zweierkomplement)

    # 4. Überlauf ignorieren
    if len(ergebnis) > max_len:
        ergebnis = ergebnis[1:]

    # 5. Führende Nullen entfernen
    i = 0
    while i < len(ergebnis) and ergebnis[i] == '0':
        i += 1
    ergebnis = ergebnis[i:] if i < len(ergebnis) else '0'

    return ergebnis


#Berechnungen in Z_2
#Erklärung Notation: u⁴ + u² + u + 1 → [1, 0, 1, 1, 1]

#Polynom-Addition in Z_2
#Input: ad2([1, 0, 0, 0, 1], [0, 1, 0, 1, 1])
#Output: [1, 1, 1, 0, 0] d.h Codewort: 11100

def ad2(poly1, poly2):
    max_degree = max(len(poly1), len(poly2))
    poly1 = [0] * (max_degree - len(poly1)) + poly1
    poly2 = [0] * (max_degree - len(poly2)) + poly2
    result = [(a + b) % 2 for a, b in zip(poly1, poly2)]
    print(result)
    return result

#Polynom-Multiplikation in Z_2
#Input: mu2([1, 0, 0, 0, 1], [0, 1, 0, 1, 1])
#Output: [1, 1, 1, 0, 0] d.h Codewort: 11100

def mu2(poly1, poly2):
    result_degree = len(poly1) + len(poly2) - 2
    result = [0] * (result_degree + 1)
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[i + j] ^= (poly1[i] * poly2[j])
    return result

#Polynom-Division in Z_2 (long division)
#Input: divl([1, 0, 0, 0, 1], [0, 1, 0, 1, 1])
#Output: Quotient, Rest
def divl(dividend, divisor):
    dividend = list(dividend)
    divisor_degree = len(divisor) - 1
    quotient = [0] * (len(dividend) - divisor_degree)

    for i in range(len(quotient)):
        if dividend[i] == 1:
            quotient[i] = 1
            for j in range(len(divisor)):
                dividend[i + j] ^= divisor[j]

    remainder = dividend[-divisor_degree:]
    return quotient, remainder

#Vektoraddition in Z_2
#Input: addv([[1, 1, 0], [0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 0, 1]])
#Output: [1, 0, 0]

def addv(vectors):
    result = [0] * len(vectors[0])
    for vector in vectors:
        for i in range(len(vector)):
            result[i] = (result[i] + vector[i]) % 2
    return result

#Erweiterungskörper (elemente die durch polynom erzeugt werden können)
#Input: gfe([1, 0, 0, 1, 1]) -> x^4 + x + 1
#Output: Aufkettung von den Elementen
def divl(dividend, divisor):
    dividend = dividend[:]
    while len(dividend) >= len(divisor):
        if dividend[0] == 1:
            for i in range(len(divisor)):
                dividend[i] ^= divisor[i]
        dividend.pop(0)
    return [], dividend

def xor(p1, p2):
    # XOR zweier gleichlanger Listen
    return [(a ^ b) for a, b in zip(p1, p2)]

def divl(dividend, divisor):
    # Division modulo 2 (nur Rest liefern)
    dividend = dividend[:]
    while len(dividend) >= len(divisor):
        if dividend[0] == 1:
            for i in range(len(divisor)):
                dividend[i] ^= divisor[i]
        dividend.pop(0)
    return [], dividend

def gfe(primitive_polynomial):
    degree = len(primitive_polynomial) - 1
    current = [0] * (degree - 1) + [1]  # Startwert: a^0 = 1
    seen = []

    while current not in seen:
        seen.append(current)

        # Multiplizieren mit a = Linksshift + 0 anhängen
        next_poly = current + [0]

        # Falls Grad zu groß, modulo reduzieren
        if len(next_poly) > degree:
            _, reduced = divl(next_poly, primitive_polynomial)
        else:
            reduced = next_poly

        # Auffüllen auf 'degree' Stellen
        current = [0] * (degree - len(reduced)) + reduced

    print("Zykluslänge:", len(seen))
    result = []
    for elem in seen:
        bitstring = ''.join(str(x) for x in elem)
        result.append(bitstring)
        print(bitstring)

#Reduzible Polynome
#Input: isr([1, 1, 0]) -> x² + x
#Output: true/false
def isr(poly):
    degree = len(poly) - 1
    if degree < 2:
        return False

    for i in range(1, degree):
        for a in range(1, 2**(i+1)):
            bin_a = bin(a)[2:]
            bin_a = '0' * (i + 1 - len(bin_a)) + bin_a  # manual zfill
            factor1 = [int(b) for b in bin_a]
            if factor1[0] == 0:
                continue

            for b in range(1, 2**(degree - i + 1)):
                bin_b = bin(b)[2:]
                bin_b = '0' * (degree - i + 1 - len(bin_b)) + bin_b  # manual zfill
                factor2 = [int(c) for c in bin_b]
                if factor2[0] == 0:
                    continue

                product = mu2(factor1, factor2)  # use correct function
                while product and product[0] == 0:
                    product.pop(0)

                if product == poly:
                    return True

    return False


#Darstellung negativer Zahlen (bin)
#Input: cvb("11111")
#Output: Betrag, Betrag mit Vorzeichen, Exzess-4, b-1 (1erKompl.), b (2erKompl.)
def cvb(bin_input):
    bin_str = bin_input
    value_unsigned = int(bin_str, 2)
    sign = '-' if bin_str[0] == '1' else '+'
    magnitude = int(bin_str[1:], 2)
    value_signed_magnitude = sign + str(magnitude)
    value_excess_4 = value_unsigned - 4
    if bin_str[0] == '0':
        ones_complement = value_unsigned
    else:
        flipped = ''.join(['1' if b == '0' else '0' for b in bin_str])
        ones_complement = -int(flipped, 2)
    if bin_str[0] == '0':
        twos_complement = value_unsigned
    else:
        n_bits = len(bin_str)
        twos_complement = value_unsigned - (1 << n_bits)

    print("Ausgabe:")

    return {
        "Binaer": bin_str,
        "Betrag": value_unsigned,
        "Betrag mit Vorzeichen": value_signed_magnitude,
        "Exzess-4": value_excess_4,
        "1er-Komplement": ones_complement,
        "2er-Komplement": twos_complement,
    }

#Addition von Komplementen (dez)
#Input: ank(-2, 1)
#       azk(-2, 1)
#Output:
def nk(n):
    n_str = str(n)
    return int(''.join([str(9 - int(c)) for c in n_str]))

def pad_left(s, total_length):
    return '0' * (total_length - len(s)) + s

def ank(a, b):
    stellen = max(len(str(abs(a))), len(str(b)))
    a_str = pad_left(str(abs(a)), stellen)
    b_str = pad_left(str(b), stellen)

    a_komp = nk(a_str)
    summe = a_komp + int(b_str)

    if summe > 10**stellen - 1:
        result = (summe + 1) - 10**stellen
    else:
        result = -nk(pad_left(str(summe), stellen))

    print("(b-1)-Komplement (9er-Komplement):")
    print("  9er-Komplement von " + a_str + " = " + pad_left(str(a_komp), stellen))
    print("  " + str(a_komp) + " + " + b_str + " = " + str(summe))
    print("Ergebnis (Ueberlauf abgeschnitten) = ")
    return result

def azk(a, b):
    stellen = max(len(str(abs(a))), len(str(b)))
    a_str = pad_left(str(abs(a)), stellen)
    b_str = pad_left(str(b), stellen)

    a_komp = nk(a_str) + 1
    summe = a_komp + int(b_str)
    result = summe - 10**stellen

    print("b-Komplement (10er-Komplement):")
    print("  10er-Komplement von " + a_str + " = " + pad_left(str(a_komp), stellen))
    print("  " + str(a_komp) + " + " + b_str + " = " + str(summe))
    print("Ergebnis (Ueberlauf abgeschnitten) = ")
    return result

#Exzess darstellung
#Input: de(34, 2)
#       ed("11111111", 2)
def de(dezimalwert, exzess_basis, wortlaenge=8):
    exzess_wert = dezimalwert + exzess_basis
    if exzess_wert < 0 or exzess_wert >= 2 ** wortlaenge:
        print("Fehler: Exzesswert liegt außerhalb des darstellbaren Bereichs.")
        return None

    bin_str = bin(exzess_wert)[2:]  # Entfernt das '0b' Präfix

    # Manuelles Auffüllen mit führenden Nullen
    while len(bin_str) < wortlaenge:
        bin_str = '0' + bin_str

    print("Dezimal:", dezimalwert,
          "| Exzess-Basis:", exzess_basis,
          "| Exzesswert:", exzess_wert,
          "| Binär:", bin_str)


def ed(bin_str, exzess_basis):
    dezimalwert = int(bin_str, 2) - exzess_basis
    print("Binär: " + bin_str + ", Exzess-" + str(exzess_basis) + ", Dezimal: " + str(dezimalwert))

#Kleinste Fixkommazahl
#Input: kfi(8, 2)
def kfi(gesamt_bits=8, vorkomma_bits=2):
    nachkomma_bits = gesamt_bits - vorkomma_bits
    kleinste_zahl = 2 ** (-nachkomma_bits)
    print("Gesamtbits:", gesamt_bits)
    print("Vorkommabits:", vorkomma_bits)
    print("Nachkommabits:", nachkomma_bits)
    print("Kleinste darstellbare positive Zahl:", kleinste_zahl)
