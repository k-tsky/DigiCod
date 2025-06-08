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
def gfe(primitive_polynomial):
    current = [1]
    seen = []

    for _ in range(15):
        current_padded = [0] * (4 - len(current)) + current
        seen.append(current_padded)
        next_poly = current + [0]
        if len(next_poly) > 4:
            _, reduced = divl(next_poly, primitive_polynomial)
        else:
            reduced = next_poly
        current = reduced

    print("Zykluslänge: " + str(len(seen)))
    result = []
    for elem in seen:
        elem_str = ''.join([str(d) for d in elem])
        while len(elem_str) < 4:
            elem_str = '0' + elem_str
        result.append(elem_str)
    return result

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
    bin_str = bin(exzess_wert)[2:]
    while len(bin_str) < wortlaenge:
        bin_str = '0' + bin_str
    print("Dezimal: " + str(dezimalwert) + ", Exzess-" + str(exzess_basis) + ", Binär: " + bin_str)
    return bin_str

def ed(bin_str, exzess_basis):
    dezimalwert = int(bin_str, 2) - exzess_basis
    print("Binär: " + bin_str + ", Exzess-" + str(exzess_basis) + ", Dezimal: " + str(dezimalwert))
    return dezimalwert





