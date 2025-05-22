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

#Polynom-Addition
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

#Polynom-Multiplikation
#Input:
#Output:

def multiply_polynomials_Z2(poly1, poly2):
    result_degree = len(poly1) + len(poly2) - 2  # Maximaler Grad des Produkts
    result = [0] * (result_degree + 1)

    # Polynom-Multiplikation mit Modulo 2
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[i + j] ^= (poly1[i] * poly2[j])  # XOR entspricht + in Z2

    return result