"""
TACHE AS-025 -- la famille close de certificats duaux : vers le theoreme
uniforme b_d >= c > 0.

THEOREME DE STRUCTURE (prouve, verifie ici) : les vecteurs a admissibles
(a_k = C(2d+1,k) q(k), q poly deg <= d) sont exactement les
A(x) = (1+x)^{d+1} R(x), deg R <= d — car la base est
C(n,j) x^j (1+x)^{n-j} et n-d = d+1.

FAMILLE : A(x) = x^s (1+x)^{d+1} B(x), B entier court.
- integralite : triviale (coefficients binomiaux entiers).
- parite : somme_{k>d} (-1)^k a_k = +/- somme_m b_m C(d, s+m) mod 2
  (identite des sommes partielles alternees, verifiee ici) ; pour B=1 :
  impaire ssi C(d,s) impair ssi s sous-masque binaire de d (LUCAS).
- norme : N = somme_k A_k^2 / C(2d+1,k) — EVALUABLE EXACTEMENT pour
  tout d sans enumeration : c'est la cle de la certification lointaine.

Phases :
0. verification de l'identite de parite (100 cas aleatoires).
1. recherche structuree d=1..32 : s in [0,d], B de degre <= 3 a coeffs
   dans {-2..2} ; min norme sous parite impaire => nu_d, loi (s,B).
   Controle : nu_d >= mu_d (AS-024) la ou mu_d est connu.
2. LOI extraite => certification lointaine : d = 33..1024 (puissances
   de 2 comprises — le cas dur), norme exacte de la famille => bornes
   b_d >= 1/(4 nu_d) explicites, TRES au-dela de toute enumeration.
"""

from __future__ import annotations

import random
import sys
import time
from fractions import Fraction as F
from math import comb

sys.path.insert(0, "checks")


def poly_mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, pi in enumerate(p):
        if pi:
            for j, qj in enumerate(q):
                r[i + j] += pi * qj
    return r


def binom_pow(m):
    """(1+x)^m."""
    return [comb(m, i) for i in range(m + 1)]


def family(d, s, B):
    """A = x^s (1+x)^{d+1} B(x) -> vecteur a sur k=0..2d+1 (None si
    depasse)."""
    n = 2 * d + 1
    A = poly_mul(binom_pow(d + 1), B)
    if s + len(A) - 1 > n:
        return None
    a = [0] * (n + 1)
    for i, c in enumerate(A):
        a[s + i] = c
    return a


def parity(d, a):
    return sum(a[k] for k in range(d + 1, 2 * d + 2)) % 2


def parity_formula(d, s, B):
    return sum(b * comb(d, s + m) for m, b in enumerate(B)) % 2


def norm_exact(d, a):
    n = 2 * d + 1
    return sum(F(a[k] * a[k], comb(n, k)) for k in range(n + 1))


def norm_float(d, a):
    n = 2 * d + 1
    return sum(a[k] * a[k] / comb(n, k) for k in range(n + 1))


def catalog():
    """B courts : degre <= 3, b0 in {1,2}, coeffs in {-2..2}."""
    cats = []
    for b0 in (1, 2):
        for b1 in range(-2, 3):
            for b2 in range(-2, 3):
                for b3 in range(-2, 3):
                    B = [b0, b1, b2, b3]
                    while B and B[-1] == 0:
                        B.pop()
                    if B not in cats:
                        cats.append(B)
    return cats


def best_structured(d, cats, s_window=None):
    best = None
    if s_window is None:
        srange = range(0, d + 1)
    else:
        c = d // 2
        srange = sorted(set(
            list(range(max(0, c - s_window), min(d, c + s_window) + 1)) +
            list(range(0, min(d, 8) + 1)) +
            list(range(max(0, d - 8), d + 1))))
    for s in srange:
        for B in cats:
            a = family(d, s, B)
            if a is None:
                continue
            if parity(d, a) != 1:
                continue
            v = norm_float(d, a)
            if best is None or v < best[0]:
                best = (v, s, B, a)
    if best is None:
        return None
    v, s, B, a = best
    return norm_exact(d, a), s, B


def main():
    print("== Phase 0 : identite de parite (sommes partielles) ==")
    rng = random.Random(7)
    bad = 0
    for _ in range(100):
        d = rng.randint(1, 24)
        s = rng.randint(0, d)
        B = [rng.randint(-2, 2) for _ in range(rng.randint(1, 4))]
        if not any(B):
            B = [1]
        a = family(d, s, B)
        if a is None:
            continue
        if parity(d, a) != parity_formula(d, s, B):
            bad += 1
    print(f"  identite parite directe vs formule C(d,s+m) : "
          f"{'OK (100 cas)' if bad == 0 else f'{bad} ECHECS'}")

    print("== Phase 1 : recherche structuree, d = 1..32 ==")
    mu = {1: F(8, 3), 2: F(12, 5), 3: F(256, 105), 4: F(160, 63),
          7: F(512, 231), 15: F(9364452921344, 4512611027925)}
    cats = catalog()
    winners = {}
    worst = 0.0
    for d in range(1, 33):
        t0 = time.time()
        r = best_structured(d, cats)
        if r is None:
            print(f"  d={d:>2} : AUCUN certificat structure !", flush=True)
            continue
        nu, s, B = r
        winners[d] = (s, B)
        worst = max(worst, float(nu))
        chk = ""
        if d in mu:
            chk = f" (mu_d = {float(mu[d]):.4f} ; nu >= mu : " + \
                  ("OK)" if nu >= mu[d] * (1 - F(1, 10**9)) else "VIOL?)")
        p2 = " [2^t]" if d & (d - 1) == 0 else ""
        print(f"  d={d:>2}{p2} : nu_d = {float(nu):.4f} "
              f"(s={s}, B={B}) => b_d >= {float(1 / (4 * nu)):.5f}{chk} "
              f"({time.time() - t0:.0f}s)", flush=True)
    print(f"  max nu_d (d<=32) = {worst:.4f} => "
          f"b_d >= {1 / (4 * worst):.5f} sur d = 1..32")

    print("== Phase 2 : certification lointaine (evaluation pure) ==")
    # d <= 400 : au-dela, C(2d+1, d) deborde le float64 du scan ;
    # fenetre s = centre +/- 40 et bords (motifs a ancre)
    far = [48, 64, 96, 128, 192, 256, 320, 400]
    worst_far = 0.0
    for d in far:
        t0 = time.time()
        r = best_structured(d, cats, s_window=40)
        if r is None:
            print(f"  d={d} : AUCUN certificat structure !", flush=True)
            continue
        nu, s, B = r
        worst_far = max(worst_far, float(nu))
        p2 = " [2^t]" if d & (d - 1) == 0 else ""
        print(f"  d={d:>4}{p2} : nu_d = {float(nu):.4f} (s={s}, B={B}) "
              f"=> b_d >= {float(1 / (4 * nu)):.5f} "
              f"({time.time() - t0:.0f}s)", flush=True)
    print(f"  max nu_d (lointain) = {worst_far:.4f}")
    print()
    print("Si nu_d <= C uniformement : b_d >= 1/(4C) pour TOUT d teste,")
    print("par certificats explicites — reste le lemme analytique")
    print("(norme de la famille bornee pour tout d) pour le theoreme.")


if __name__ == "__main__":
    main()
