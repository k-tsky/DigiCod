# Erweiterter euklidischer Algorithmus
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

# Modulare Inverse (immer positiv!)
def modinv(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

# Hauptlogik
only_decrypt = input("j: Zum entschlüsseln, n: Zum verschlüsseln, (j/n): ").strip().lower() == 'j'

if only_decrypt:
    use_public = input("Öffentlichen Schlüssel (e) oder privater Schlüssel (d) verwenden? (j für e, n für d): ").strip().lower() == 'j'

    if use_public:
        e = int(input("Öffentlicher Schlüssel e: "))
        p = int(input("Primzahl p: "))
        q = int(input("Primzahl q: "))
        n = p * q
        phi_n = (p - 1) * (q - 1)
        d = modinv(e, phi_n)
    else:
        d = int(input("Privater Schlüssel d: "))
        n = int(input("Modulus n: "))

    c = int(input("Verschlüsselter Wert c: "))

    if d is None:
        print("Fehler: Privater Schlüssel konnte nicht berechnet werden!")
    else:
        m = (c ** d) % n
        print("Entschlüsselung:", c, "^", d, "mod", n, "=", m)
        print("Privater Schlüssel: ", d)
        print("Klartext =", m)

else:
    use_custom_phi = input("Phi(n) manuell eingeben? (j/n): ").strip().lower() == 'j'

    if use_custom_phi:
        phi_n = int(input("Phi(n): "))
        p = q = None
    else:
        p = int(input("Primzahl p: "))
        q = int(input("Primzahl q: "))
        phi_n = (p - 1) * (q - 1)

    is_public = input("Öffentlichen Schlüssel (e) oder privater Schlüssel (d) verwenden? (j für e, n für d):  ").strip().lower() == 'j'
    key_input = input("Einen oder zwei Schlüssel (mit Komma): ").split(',')
    keys = [int(k.strip()) for k in key_input]
    m = int(input("Klartext m (Zahl < n): "))

    if p and q:
        n = p * q
    else:
        n = int(input("Modulus n: "))

    for i in range(len(keys)):
        print()
        if is_public:
            e = keys[i]
            d = modinv(e, phi_n)
        else:
            d = keys[i]
            e = modinv(d, phi_n)

        if d is None or e is None:
            print("Fehler bei Inverser!")
        else:
            print("Schlüssel", i+1)
            print("Öffentlich: (", e, ",", n, ")")
            print("Privat: (", d, ",", n, ")")

            c = (m ** e) % n
            print("Verschlüsselt:", m, "^", e, "mod", n, "=", c)

            m_decrypt = (c ** d) % n
            print("Entschlüsselt:", c, "^", d, "mod", n, "=", m_decrypt)