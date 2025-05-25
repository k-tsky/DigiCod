import math

# Code nur falls öffentlicher Schlüssel gegeben ist
# Funktion zur Berechnung des ggT mit erweitertem Euklidischem Algorithmus
#Im fall von 47 ∙ 𝑑 ≡ 1 𝑚𝑜𝑑 60 -> phi = 60 und öffentlicher schlüssel=47

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

# Funktion zur Berechnung der modularen Inversen
def modinv(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

# Zusatzfunktion: Nur Entschlüsselung durchführen?
only_decrypt = input("Möchtest du entschlüsseln (e) oder verschlüsseln (v)? (e/v)): ").strip().lower() == 'e'

if only_decrypt:
    use_public = input("Hast du den öffentlichen Schlüssel (e) oder den privaten Schlüssel (d)? (e/d): ").strip().lower()
    if use_public == 'e':
        e = int(input("Gib den öffentlichen Schlüssel e ein: "))
        p = int(input("Gib die Primzahl p ein: "))
        q = int(input("Gib die Primzahl q ein: "))
        n = p * q
        phi_n = (p - 1) * (q - 1)
        d = modinv(e, phi_n)
    else:
        d = int(input("Gib den privaten Schlüssel d ein: "))
        n = int(input("Gib den Wert von n (Modulus) ein: "))

    c = int(input("Gib den verschlüsselten Wert c ein: "))

    if d is None:
        print("Fehler: Der private Schlüssel konnte nicht berechnet werden!")
    else:
        m = pow(c, d, n)
        print(f"\nEntschlüsselung: {c}^{d} mod {n} = {m}")
        print(f"Klartext = {m}")
    exit()

# Benutzereingaben
use_custom_phi = input("Möchtest du Phi(n) manuell eingeben, anstatt p und q zu berechnen? (j/n): ").strip().lower() == 'j'

if use_custom_phi:
    phi_n = int(input("Gib den Wert von Phi(n) ein: "))
    p = q = None
else:
    p = int(input("Gib eine Primzahl p ein: "))
    q = int(input("Gib eine Primzahl q ein: "))
    phi_n = (p - 1) * (q - 1)

key_type = input("Möchtest du öffentliche (e) oder private (d) Schlüssel eingeben? (e/d): ").strip().lower()
keys_input = input("Gib einen oder zwei Schlüssel (durch Komma getrennt) ein: ").split(',')
keys = [int(k.strip()) for k in keys_input if k.strip().isdigit()]
m = int(input("Gib den Klartext m ein (Zahl < n): "))

# Berechnungen
if p and q:
    n = p * q
else:
    n = int(input("Gib den Wert von n (Modulus) ein: "))

print("\n--- RSA-Verschlüsselung und Entschlüsselung ---")
if p and q:
    print(f"p = {p}, q = {q}, n = {n}, Φ(n) = {phi_n}")
else:
    print(f"n = {n}, Φ(n) = {phi_n}")

# Berechnung der fehlenden Schlüssel
public_keys = []
private_keys = []

for i, val in enumerate(keys):
    if key_type == 'e':
        e = val
        d = modinv(e, phi_n)
    else:
        d = val
        e = modinv(d, phi_n)
    public_keys.append(e)
    private_keys.append(d)
    print(f"\nSchlüssel {i+1}:")
    if e is not None and d is not None:
        print(f"Öffentlicher Schlüssel: ({e}, {n})")
        print(f"Privater Schlüssel: ({d}, {n})")
    else:
        print("Fehler bei der Berechnung des inversen Schlüssels!")

# Verschlüsseln und Entschlüsseln
for i, (e, d) in enumerate(zip(public_keys, private_keys)):
    print(f"\nVerschlüsseln mit öffentlichem Schlüssel {i+1} ({e}, {n}):")
    c = pow(m, e, n)
    print(f"{m}^{e} mod {n} = {c}")
    print(f"Geheimtext = {c}")

    print(f"\nEntschlüsseln mit privatem Schlüssel {i+1} ({d}, {n}):")
    m_decrypted = pow(c, d, n) if d is not None else None
    print(f"{c}^{d} mod {n} = {m_decrypted}")
    print(f"Klartext = {m_decrypted}")
