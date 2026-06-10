"""
TACHE F-011, etape 6 -- Theoreme de periodicite + lemme de descente (mod 3).

THEOREME T-F011c (periodicite vs prefixe -- PREUVE) :
  Soit P = 3^b. Sur F_3, Delta^P = S^P - id (Lucas : C(P,k) = 0 mod 3
  pour 0 < k < P ; signes : (-1)^{P-k} avec P impair).
  Si deg(g) <= d < P alors Delta^P g = 0 sur [0, n-P], i.e. g est
  P-periodique sur son domaine. Or g(t-1) = 0 (prefixe) et, si
  t-1+P <= n, g(t-1+P) doit etre dans {1,2} (fenetre) : contradiction.
  DONC : deg_3^sym(THR_{t,n}) >= 3^b pour toute puissance 3^b <= n-t+1.
  En particulier deg_3^sym(OR_n) >= 3^floor(log3 n).

LEMME 3 (descente -- PREUVE) :
  Si deg(g) <= d et P = 3^b <= d+1, alors G := g(.+P) - g a un degre de
  Mahler <= d - P sur [0, n-P].
  (Delta^{d+1-P} G = Delta^{d+1-P} (S^P - id) g = Delta^{d+1} g = 0.)

CE QUI RESTE CONJECTURAL : la valeur exacte de la rampe
(deg_3(OR_n) = n - 3^b pour 2*3^b < n < 3^{b+1}) -- confirmee 26/26 a
l'etape 5, la borne inferieure fine n'est pas encore prouvee.

Ce script verifie executablement :
  (1) l'identite Delta^P = S^P - id sur F_3 (P = 3, 9, 27) ;
  (2) T-F011c contre TOUTES les valeurs exactes deja calculees (grille
      etape 4 + OR etape 5) ;
  (3) Lemme 3 sur 2000 fonctions aleatoires de bas degre.
"""

from __future__ import annotations

import random
from math import comb

random.seed(2026)


# ---------------------------------------------------------------- outils

def mahler_eval(coeffs, w):
    """ g(w) = sum_i coeffs[i] C(w,i) mod 3. """
    return sum(c * comb(w, i) for i, c in enumerate(coeffs)) % 3


def mahler_degree(values):
    """ Degre de Mahler d'une suite de valeurs mod 3 (differences finies). """
    vals = list(values)
    deg = -1
    for i in range(len(vals)):
        # coefficient a_i = Delta^i g(0)
        a = sum(((-1) ** (i - k)) * comb(i, k) * vals[k] for k in range(i + 1)) % 3
        if a != 0:
            deg = i
    return deg


# ---------------------------------------------------------------- (1) identite

def check_identity():
    ok = True
    for P in (3, 9, 27):
        for trial in range(50):
            n = P + random.randint(P, 2 * P)
            vals = [random.randint(0, 2) for _ in range(n + 1)]
            for j in range(0, n - P + 1):
                lhs = sum(((-1) ** (P - k)) * comb(P, k) * vals[j + k]
                          for k in range(P + 1)) % 3
                rhs = (vals[j + P] - vals[j]) % 3
                if lhs != rhs:
                    ok = False
    return ok


# ---------------------------------------------------------------- (2) T-F011c vs donnees

def dp_feasible(t, n, d):
    """ DP fenetre glissante (etape 5, validee 126/126). """
    W = d + 2
    coeffs = [((-1) ** (d + 1 - k)) * comb(d + 1, k) % 3 for k in range(W)]
    states = {tuple()}
    for w in range(0, n + 1):
        allowed = (0,) if w < t else (1, 2)
        new = set()
        for st in states:
            for val in allowed:
                seq = st + (val,)
                if len(seq) == W:
                    if sum(c * v for c, v in zip(coeffs, seq)) % 3 != 0:
                        continue
                    seq = seq[1:]
                new.add(seq)
        states = new
        if not states:
            return False
    return True


def dp_deg(t, n, d_cap=15):
    for d in range(t, d_cap + 1):
        if d + 1 > n or dp_feasible(t, n, d):
            return d
    return None


def tf011c_bound(t, n):
    """ Plus grande puissance de 3 <= n - t + 1. """
    P = 1
    while P * 3 <= n - t + 1:
        P *= 3
    return P


def check_tf011c():
    ok = True
    tested = 0
    for t in range(1, 7):
        for n in range(t, 27):
            d = dp_deg(t, n)
            if d is None:
                continue
            tested += 1
            if d < tf011c_bound(t, n):
                print(f"    VIOLATION : t={t}, n={n} : deg={d} < "
                      f"borne={tf011c_bound(t, n)}")
                ok = False
    return ok, tested


# ---------------------------------------------------------------- (3) Lemme 3

def check_lemma3():
    ok = True
    for trial in range(2000):
        P = random.choice([3, 9])
        d = random.randint(P, P + 8)
        n = d + random.randint(P, 2 * P)
        # g aleatoire de degre <= d (coefficients de Mahler aleatoires)
        coeffs = [random.randint(0, 2) for _ in range(d + 1)]
        g = [mahler_eval(coeffs, w) for w in range(n + 1)]
        G = [(g[j + P] - g[j]) % 3 for j in range(n - P + 1)]
        dg = mahler_degree(G)
        if dg > d - P:
            print(f"    VIOLATION Lemme 3 : P={P}, d={d}, n={n}, deg(G)={dg}")
            ok = False
    return ok


def main() -> None:
    print("TACHE F-011 etape 6 -- periodicite + descente (mod 3)")
    print("=" * 66)

    print("\n(1) Identite Delta^P = S^P - id sur F_3 (P = 3, 9, 27, 150 tests)")
    print(f"    {'OK' if check_identity() else 'ECHEC'}")

    print("\n(2) T-F011c : deg >= plus grande puissance de 3 <= n-t+1,")
    print("    contre toutes les valeurs exactes (DP, t <= 6, n <= 26)")
    ok, tested = check_tf011c()
    print(f"    {tested} cellules : {'AUCUNE VIOLATION -- borne prouvee respectee' if ok else 'ECHEC'}")

    print("\n(3) Lemme 3 (descente) : deg(g(.+P) - g) <= deg(g) - P,")
    print("    2000 fonctions aleatoires de bas degre (P = 3, 9)")
    print(f"    {'OK -- 2000/2000' if check_lemma3() else 'ECHEC'}")

    print("\n" + "=" * 66)
    print("PROUVE : T-F011c (periodicite) et Lemme 3 (descente).")
    print("RESTE CONJECTURAL : la valeur exacte de la rampe")
    print("(deg_3(OR_n) = n - 3^b pour 2*3^b < n < 3^{b+1}, 26/26 empirique).")


if __name__ == "__main__":
    main()
