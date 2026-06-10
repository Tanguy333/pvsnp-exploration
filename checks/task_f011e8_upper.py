"""
TACHE F-011, etape 8 -- Bornes superieures : Theoreme F + temoins de rampe.

THEOREME F (construction explicite, regime 1) :
  Pour P = 3^b et P <= n <= 2P, la suite
      g = (0, 1, 1, ..., 1 [P valeurs], 2, 2, ..., 2 [n-P valeurs])
  verifie h(j) := g(j+P) - g(j) = 1 (constante) sur [0, n-P], donc
  Delta^{P+1} g = Delta(h) = 0 : deg(g) <= P. Et g couvre ([1,n] -> {1,2}).
  PREUVE : h(0) = g(P) - g(0) = 1 ; pour j in [1, n-P] (donc j <= P et
  j+P >= P+1), h(j) = 2 - 1 = 1. QED
  COROLLAIRE (avec Theoreme D) : deg_3^sym(OR_n) = 3^b EXACTEMENT pour
  tout n in [3^b, 2*3^b]. -- premiere loi de regime entierement prouvee.

Ce script verifie :
  [A] Theoreme F numeriquement (P = 3, 9, 27 ; tout n in [P, 2P]) ;
  [B] extraction de TEMOINS de la rampe (regime 2P < n < 3P) par DP avec
      reconstruction, et inspection de leur structure h ;
  [C] les certificats MAJ mod 6 : e_8 + e_9 (mod 3) pour MAJ_16 (d=9)
      et recherche du certificat minimal pour MAJ_4 (d=3).
"""

from __future__ import annotations

import itertools
from math import comb


def mahler_degree(vals, m=3):
    deg = -1
    for i in range(len(vals)):
        a = sum(((-1) ** (i - k)) * comb(i, k) * vals[k] for k in range(i + 1)) % m
        if a != 0:
            deg = i
    return deg


# ------------------------------------------------- [A] Theoreme F

def check_theorem_f():
    ok = True
    for P in (3, 9, 27):
        for n in range(P, 2 * P + 1):
            g = [0] + [1] * P + [2] * (n - P)
            assert len(g) == n + 1
            cover = all(v in (1, 2) for v in g[1:])
            d = mahler_degree(g)
            if not (cover and d <= P):
                print(f"  ECHEC : P={P}, n={n} : deg={d}, cover={cover}")
                ok = False
    return ok


# ------------------------------------------------- [B] temoins de rampe (DP)

def dp_witness(t, n, d):
    """ DP avec reconstruction : retourne UNE suite realisable a degre <= d,
        ou None. """
    W = d + 2
    coeffs = [((-1) ** (d + 1 - k)) * comb(d + 1, k) % 3 for k in range(W)]
    # forward : etats -> parent
    layers = [{tuple(): None}]
    for w in range(0, n + 1):
        allowed = (0,) if w < t else (1, 2)
        new = {}
        for st in layers[-1]:
            for val in allowed:
                seq = st + (val,)
                if len(seq) == W:
                    if sum(c * v for c, v in zip(coeffs, seq)) % 3 != 0:
                        continue
                    nxt = seq[1:]
                else:
                    nxt = seq
                if nxt not in new:
                    new[nxt] = (st, val)
        layers.append(new)
        if not new:
            return None
    # backtrack
    st = next(iter(layers[-1]))
    vals = []
    for w in range(n, -1, -1):
        parent, val = layers[w + 1][st]
        vals.append(val)
        st = parent
    return vals[::-1]


def inspect_ramp():
    print("  Temoins du regime de rampe (deg = n - P) et leur structure h :")
    for n in (19, 20, 22):
        P = 9
        d = n - P
        g = dp_witness(1, n, d)
        if g is None:
            print(f"    n={n} : pas de temoin a d={d} ?!")
            continue
        h = [(g[j + P] - g[j]) % 3 for j in range(n - P + 1)]
        dh = mahler_degree(h)
        print(f"    n={n}, d={d} : g = {''.join(map(str, g))}")
        print(f"            h = {''.join(map(str, h))}  (deg(h) = {dh}, "
              f"borne r = {n - 2 * P})")


# ------------------------------------------------- [C] certificats MAJ

def check_maj_certificates():
    ok = True
    # MAJ_16, d = 9 : V = e_8 + e_9 mod 3, u = 0
    t, n = 8, 16
    good = True
    for w in range(0, n + 1):
        V = (comb(w, 8) + comb(w, 9)) % 3
        if w < t and V != 0:
            good = False
        if w >= t and V == 0:
            good = False
    print(f"  MAJ_16, d=9 : V = e8 + e9 (mod 3) : "
          f"{'CERTIFICAT VALIDE' if good else 'ECHEC'}")
    ok &= good
    # MAJ_4, d = 3 : chercher le certificat minimal (u, v) sur {e2, e3}
    t, n = 2, 4
    found = None
    for u2, u3 in itertools.product(range(2), repeat=2):
        for v2, v3 in itertools.product(range(3), repeat=2):
            okc = True
            for w in range(0, n + 1):
                U = (u2 * comb(w, 2) + u3 * comb(w, 3)) % 2
                V = (v2 * comb(w, 2) + v3 * comb(w, 3)) % 3
                if w < t and (U != 0 or V != 0):
                    okc = False
                    break
                if w >= t and (U == 0 and V == 0):
                    okc = False
                    break
            if okc:
                found = (u2, u3, v2, v3)
                break
        if found:
            break
    if found:
        u2, u3, v2, v3 = found
        print(f"  MAJ_4, d=3 : certificat trouve : u = {u2}*e2+{u3}*e3 (mod 2), "
              f"v = {v2}*e2+{v3}*e3 (mod 3) -- VALIDE")
    else:
        print("  MAJ_4, d=3 : AUCUN certificat ?!")
        ok = False
    return ok


def main() -> None:
    print("TACHE F-011 etape 8 -- bornes superieures")
    print("=" * 66)

    print("\n[A] Theoreme F : g = (0, 1^P, 2^{n-P}) -> deg <= P, n in [P, 2P]")
    print(f"    P = 3, 9, 27, tout n : {'OK' if check_theorem_f() else 'ECHEC'}")
    print("    => deg_3^sym(OR_n) = 3^b EXACTEMENT pour n in [3^b, 2*3^b]")
    print("       (premiere loi de regime entierement prouvee, avec Thm D)")

    print("\n[B] Temoins du regime de rampe (inspection pour la borne sup) :")
    inspect_ramp()

    print("\n[C] Certificats MAJ mod 6 (bornes sup des anomalies) :")
    check_maj_certificates()


if __name__ == "__main__":
    main()
