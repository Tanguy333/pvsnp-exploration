"""
TACHE V-017c -- RE-VERIFICATION EXACTE des cellules suspectes de
V-017b (d >= 21, " NON " aux bouts +-1).

Deux suspects elimines ici :
 [1] PRECISION : le Fincke-Pohst de V-004 est en flottants ; a d >= 21
     les normes depassent 10^17 > mantisse des doubles -> minima
     potentiellement manques. ICI : Gram-Schmidt et enumeration en
     FRACTIONS EXACTES (rang <= 10, faisable).
 [2] TEST TROP STRICT : notre " bouts +-1 " exige les DEUX bouts ; la
     Conjecture 5 de KV demande seulement gamma_n = 1, soit (a
     decalage/renversement pres, Lemmes S et R) : UN minimum dont le
     DERNIER coefficient non nul vaut +-1. ICI : les deux tests.
"""

from __future__ import annotations

import time
from fractions import Fraction
from math import isqrt

from task_v004_kv_conjecture5 import build_basis, lll_reduce

SUSPECTES = [(21, 30), (22, 28), (22, 31), (23, 29), (23, 32),
             (24, 30), (24, 33), (24, 34), (27, 33), (27, 34),
             (29, 35), (29, 36), (29, 39)]
TEMOINS_OK = [(21, 25), (24, 28), (29, 32)]   # cellules OK, sanite


def exact_shortest(G):
    """ Fincke-Pohst en Fractions exactes sur la base (entiere) G. """
    m = len(G)
    B = [[Fraction(int(x)) for x in row] for row in G]
    # Gram-Schmidt exact
    Bs = []
    mu = [[Fraction(0)] * m for _ in range(m)]
    for i in range(m):
        v = B[i][:]
        for j in range(i):
            num = sum(a * b for a, b in zip(B[i], Bs[j]))
            den = sum(a * a for a in Bs[j])
            mu[i][j] = num / den
            v = [a - mu[i][j] * b for a, b in zip(v, Bs[j])]
        Bs.append(v)
    c = [sum(a * a for a in v) for v in Bs]
    # borne initiale : plus petit vecteur de base
    best = min(sum(int(x) * int(x) for x in row) for row in G)
    sols = []

    def rec(level, coefs, partial):
        nonlocal best, sols
        if level < 0:
            v = [0] * len(G[0])
            for k in range(m):
                if coefs[k]:
                    for t in range(len(v)):
                        v[t] += coefs[k] * int(G[k][t])
            n2 = sum(x * x for x in v)
            if 0 < n2 < best:
                best = n2
                sols = [v]
            elif n2 == best and any(x for x in v):
                sols.append(v)
            return
        rem = Fraction(best) - partial
        if rem < 0:
            return
        center = -sum(mu[k][level] * coefs[k] for k in range(level + 1, m))
        # bornes entieres exactes : (x - center)^2 * c[level] <= rem
        # x in [center - r, center + r], r = sqrt(rem / c[level])
        bound = rem / c[level]
        # encadrement entier de center +- sqrt(bound), en exact
        lo = None
        x0 = int(center)
        x = x0
        while (Fraction(x) - center) ** 2 <= bound:
            x -= 1
        lo = x + 1
        x = x0 + 1
        while (Fraction(x) - center) ** 2 <= bound:
            x += 1
        hi = x - 1
        for xv in range(lo, hi + 1):
            coefs[level] = xv
            add = (Fraction(xv) - center) ** 2 * c[level]
            rec(level - 1, coefs, partial + add)
        coefs[level] = 0

    rec(m - 1, [0] * m, Fraction(0))
    # garder uniquement la norme minimale finale
    sols = [v for v in sols if sum(x * x for x in v) == best]
    return best, sols


def both_ends(v):
    nz = [x for x in v if x != 0]
    return abs(nz[0]) == 1 and abs(nz[-1]) == 1


def kv_cond(sols):
    """ Conjecture 5 (reformulee) : UN minimum a dernier coef non nul
        +-1 (ou premier, par renversement -- on teste les deux). """
    top = any(abs([x for x in v if x != 0][-1]) == 1 for v in sols)
    bot = any(abs([x for x in v if x != 0][0]) == 1 for v in sols)
    return top, bot


def main() -> None:
    print("TACHE V-017c -- re-verification EXACTE (Fractions) des suspects")
    print("=" * 68)
    for (d, n) in TEMOINS_OK + SUSPECTES:
        t0 = time.time()
        G = lll_reduce(build_basis(n, d))
        n2, sols = exact_shortest(G)
        strict = any(both_ends(v) for v in sols)
        top, bot = kv_cond(sols)
        tag = 'TEMOIN' if (d, n) in TEMOINS_OK else 'SUSPECT'
        print(f"  [{tag}] (d={d}, n={n}) : min EXACT = {n2}, "
              f"{len(sols)} minima ; 2-bouts : {'OUI' if strict else 'non'} ; "
              f"KV (haut/bas +-1) : {'OUI' if top else 'NON'}/"
              f"{'OUI' if bot else 'NON'}   ({time.time()-t0:.0f}s)",
              flush=True)
    print("=" * 68)
    print("Lecture : si KV = OUI partout, les NON de V-017b etaient un")
    print("artefact (precision et/ou test trop strict). Si un KV = NON")
    print("subsiste : candidat contre-exemple -- escalade de verification.")


if __name__ == "__main__":
    main()
