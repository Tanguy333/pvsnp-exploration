"""
TACHE AS-026 -- les deux morceaux restants du programme b_d >= c :

(A) ZONE DYADIQUE BASSE : extraire les certificats optimaux exacts a
    d = 8, 16, 17, 32 (machinerie AS-024), les factoriser par
    (1+x)^{d+1} (division exacte, garantie par le lemme de structure
    AS-025) et tester l'hypothese PADE : R = troncature de la serie
    (1-x)^alpha (1+x)^{-beta} (petits alpha, beta) a un facteur pres.

(B) LEMME DE NORME : N(d, s) = somme_j C(d+1,j)^2 / C(2d+1, s+j) pour
    s ~ d/2 — evaluation lgamma jusqu'a d = 2048 (aucun bigint), pour
    etablir la constante et le comportement (l'argument gaussien predit
    N ~ constante ; la preuve ecrite est un lemme de Stirling local).
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb, exp, lgamma, log

sys.path.insert(0, "checks")


def lnC(m, k):
    if k < 0 or k > m:
        return float("-inf")
    return lgamma(m + 1) - lgamma(k + 1) - lgamma(m - k + 1)


def norm_lgamma(d, s):
    """N(d,s) = somme_j C(d+1,j)^2/C(2d+1,s+j) en flottant stable."""
    tot = 0.0
    for j in range(0, d + 2):
        e = 2 * lnC(d + 1, j) - lnC(2 * d + 1, s + j)
        if e > -745:
            tot += exp(e)
    return tot


def poly_divide_exact(A, D):
    """A / D exacte sur Q (echec = None). A, D listes int (bas degre
    en tete)."""
    A = [F(x) for x in A]
    q = []
    # division par le haut
    A = A[:]
    da, dd = len(A) - 1, len(D) - 1
    for i in range(da - dd, -1, -1):
        c = A[dd + i] / D[dd]
        q.append(c)
        for j in range(dd + 1):
            A[i + j] -= c * D[j]
    if any(x != 0 for x in A):
        return None
    q.reverse()
    return q


def series(alpha, beta, deg):
    """Coefficients de (1-x)^alpha (1+x)^{-beta} jusqu'a x^deg (exact,
    alpha entier >= 0, beta entier >= 0)."""
    # (1-x)^alpha : fini ; (1+x)^{-beta} = somme C(beta+m-1, m)(-x)^m
    a = [F((-1) ** i * comb(alpha, i)) for i in range(alpha + 1)]
    out = [F(0)] * (deg + 1)
    for m in range(deg + 1):
        c = F((-1) ** m * comb(beta + m - 1, m)) if beta > 0 else \
            (F(1) if m == 0 else F(0))
        for i, ai in enumerate(a):
            if m + i <= deg:
                out[m + i] += ai * c
    return out


def main():
    from task_as024 import mu_d

    print("== (A) certificats optimaux zone basse : factorisation ==")
    for d in [8, 16, 17]:
        t0 = time.time()
        val, a, info = mu_d(d)
        n = 2 * d + 1
        # normaliser le signe et couper les zeros de tete
        lead = next(i for i in range(n + 1) if a[i] != 0)
        sgn = 1 if a[lead] > 0 else -1
        a = [sgn * x for x in a]
        A = a[lead:]
        while A and A[-1] == 0:
            A.pop()
        D = [comb(d + 1, i) for i in range(d + 2)]
        R = poly_divide_exact(A, D)
        print(f"  d={d} : mu = {float(val):.4f} ({info}, "
              f"{time.time() - t0:.0f}s)")
        print(f"    a (des k={lead}) = {A}")
        if R is None:
            print("    division par (1+x)^{d+1} INEXACTE ?!")
            continue
        den = 1
        for c in R:
            den = den * c.denominator // __import__('math').gcd(
                den, c.denominator)
        Ri = [int(c * den) for c in R]
        print(f"    R x {den} = {Ri}")
        # hypothese Pade : R ~ troncature de (1-x)^al (1+x)^{-be}
        best = None
        for al in range(0, 4):
            for be in range(0, d + 4):
                S = series(al, be, len(R) - 1)
                if S[0] == 0:
                    continue
                lam = R[0] / S[0]
                dev = sum(abs(float(R[i] - lam * S[i]))
                          for i in range(len(R)))
                scale = sum(abs(float(x)) for x in R) + 1e-30
                if best is None or dev / scale < best[0]:
                    best = (dev / scale, al, be, lam)
        devr, al, be, lam = best
        print(f"    Pade la plus proche : (1-x)^{al} (1+x)^-{be} "
              f"x {lam} ; deviation relative = {devr:.4f}"
              f"{'  <-- MATCH EXACT' if devr < 1e-12 else ''}",
              flush=True)

    print("== (B) lemme de norme : N(d, s~d/2) jusqu'a d = 2048 ==")
    print("  d | N(d, d/2-2..d/2+2) | max")
    for d in [10, 20, 50, 100, 200, 500, 1000, 2048]:
        c = d // 2
        vals = [norm_lgamma(d, c + off) for off in range(-2, 3)]
        print(f"  d={d:>5} : " +
              " ".join(f"{v:.4f}" for v in vals) +
              f" | centre {vals[2]:.4f}", flush=True)
    print("  (l'argument gaussien predit N -> constante ; la parite")
    print("   exige s sous-masque : la zone certifiee = d dont un")
    print("   sous-masque tombe a O(1) de d/2)")


if __name__ == "__main__":
    main()
