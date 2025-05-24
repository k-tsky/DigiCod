#Division von Binärzahlen
#Input: gf2_div([1, 0, 0, 0, 1], [1, 0, 1])
#Output: Quotient, Rest

def gf2_div(dividend, divisor):
    dividend = dividend.copy()
    divisor = divisor.copy()
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
#Erklärung Notation: u⁴ + u² + u + 1 → [1, 0, 1, 1, 1]#

#Polynom-Addition in Z_2
#Input: add_polynomials_Z2([1, 0, 0, 0, 1], [0, 1, 0, 1, 1])
#Output: [1, 1, 1, 0, 0] d.h Codewort: 11100

def add_polynomials_Z2(poly1, poly2):
    # Maximalgrad beider Polynome bestimmen
    max_degree = max(len(poly1), len(poly2))

    # Beide Polynome auf gleiche Länge bringen
    poly1 = [0] * (max_degree - len(poly1)) + poly1
    poly2 = [0] * (max_degree - len(poly2)) + poly2

    # Addition in Z2 (XOR)
    result = [(a + b) % 2 for a, b in zip(poly1, poly2)]
    return result

#Polynom-Multiplikation in Z_2
#Input: multiply_polynomials_Z2([1, 0, 0, 0, 1], [0, 1, 0, 1, 1])
#Output: [1, 1, 1, 0, 0] d.h Codewort: 11100

def multiply_polynomials_Z2(poly1, poly2):
    result_degree = len(poly1) + len(poly2) - 2  # Maximaler Grad des Produkts
    result = [0] * (result_degree + 1)

    # Polynom-Multiplikation mit Modulo 2
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[i + j] ^= (poly1[i] * poly2[j])  # XOR entspricht + in Z2

    return result

#Polynom-Division in Z_2
#Input: divide_polynomials_Z2([1, 0, 0, 0, 1], [0, 1, 0, 1, 1])
#Output: Quotient, Rest
def divide_polynomials_Z2(dividend, divisor):
    dividend = dividend[:]  # Kopie, um Original nicht zu verändern
    divisor_degree = len(divisor) - 1
    quotient = [0] * (len(dividend) - divisor_degree)

    for i in range(len(quotient)):
        if dividend[i] == 1:
            quotient[i] = 1
            # XOR den Divisor mit entsprechendem Versatz
            for j in range(len(divisor)):
                dividend[i + j] ^= divisor[j]

    # Rest ist das, was nach der Division im Dividend übrig bleibt
    remainder = dividend[-divisor_degree:]
    return quotient, remainder

#Vektoraddition in Z_2
#Input: [[1, 1, 0], [0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 0, 1]]
#Output: [1, 0, 0]

def add_vectors_Z2(vectors):
    # Annahme: alle Vektoren haben die gleiche Länge
    result = [0] * len(vectors[0])

    for vector in vectors:
        for i in range(len(vector)):
            result[i] = (result[i] + vector[i]) % 2  # Addition in Z2

    return result

#Erweiterungskörper (elemente die durch polynom erzeugt werden können)
#Input: [1, 0, 0, 1, 1] -> x^4 + x + 1
#Output: Aufkettung von den Elementen
def generate_field_elements(primitive_polynomial):
    # Startwert a^0 = 1
    current = [1]  # a^0 = 1
    seen = []

    for _ in range(15):  # Zykluslänge in GF(2^4)
        # Pad auf 4 Bits für Anzeige
        current_padded = [0] * (4 - len(current)) + current
        seen.append(current_padded)

        # Multiplizieren mit x: Linksshift um 1
        next_poly = current + [0]

        # Reduktion modulo primitiver Polynom falls Grad ≥ 4
        if len(next_poly) > 4:
            _, reduced = divide_polynomials_Z2(next_poly, primitive_polynomial)
        else:
            reduced = next_poly

        current = reduced

    print("Zykluslänge: " + str(len(seen)))
    return [''.join(map(str, elem)).zfill(4) for elem in seen]

#Reduzible Polynome
#Input: [1, 1, 0] -> x² + x
#Output: true/false
def is_reducible_Z2(poly):
    degree = len(poly) - 1

    # Reduzierbarkeit bei Grad < 2 nicht sinnvoll
    if degree < 2:
        return False

    # Erzeuge alle Polynome geringeren Grades
    for i in range(1, degree):
        # Erzeuge alle Polynome vom Grad i
        for a in range(1, 2**(i+1)):
            factor1 = [int(b) for b in bin(a)[2:].zfill(i+1)]
            if factor1[0] == 0:
                continue  # Führende 0 => nicht gültig

            # Polynome vom Grad (degree - i)
            for b in range(1, 2**(degree - i + 1)):
                factor2 = [int(c) for c in bin(b)[2:].zfill(degree - i + 1)]
                if factor2[0] == 0:
                    continue  # Führende 0 => nicht gültig

                product = multiply_polynomials_Z2(factor1, factor2)

                # Kürzen führender Nullen im Ergebnis
                while product and product[0] == 0:
                    product.pop(0)

                if product == poly:
                    return True

    return False



