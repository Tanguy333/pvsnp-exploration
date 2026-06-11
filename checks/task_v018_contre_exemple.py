"""
TACHE V-018 -- CONTRE-EXEMPLE a la Conjecture 5 de Krishan-Vishwanathan
(ECCC TR24-074) : cellule (d = 21, n = 30).

ENONCE REFUTE (verbatim, lu visuellement p. 17 du papier) :
  " Conjecture 5. Consider the basis B for any n, d. There exists a
    vector gamma in L(B) with the smallest l2 norm such that
    gamma_n = 1. "

PILE DE VERIFICATION (toutes les etapes rejouees ici) :
 [1] SVP exact en rationnels purs (Gram-Schmidt + Fincke-Pohst en
     Fractions, zero flottant) : le minimum de la cellule est
     517673216, atteint par exactement 2 vecteurs (v et -v), ou v est
     un PALINDROME a gamma_30 = -2.
 [2] Appartenance au reseau verifiee symboliquement (sympy) :
     (1-x)^22 divise le polynome de v.
 [3] ENUMERATION CONTRAINTE INDEPENDANTE (base stencil BRUTE, non
     reduite, code distinct) : aucun vecteur du reseau avec
     gamma_n = +-1 n'a une norme <= 517673216. Le minimum contraint
     est strictement plus grand => aucun plus court vecteur ne
     satisfait gamma_n = 1. QED.

PORTEE (nuance consignee) : la conjecture est ENONCEE pour tout (n, d)
et la cellule (21, 30) la refute telle quelle. Le REGIME UTILE a
l'application ACC de KV (d petit devant n) n'est PAS touche : nos ~290
cellules a d <= 16 avec fenetres plus larges la SOUTIENNENT toutes.
Le bon enonce demande une hypothese n >= f(d) -- nos donnees situent
la frontiere (premiers echecs : d = 21, n - d <= 9 ; echecs
systematiques d >= 22 a n - d = 6).
"""

from __future__ import annotations

from fractions import Fraction

import sympy as sp

from task_v004_kv_conjecture5 import build_basis, lll_reduce
from task_v017c_verif_exacte import exact_shortest

D, N = 21, 30


def main() -> None:
    print("TACHE V-018 -- contre-exemple Conjecture 5 : (d=21, n=30)")
    print("=" * 64)
    Graw = build_basis(N, D)
    G = lll_reduce(Graw)

    print("\n[1] SVP exact (Fractions) :")
    gmin, sols = exact_shortest(G)
    print(f"    min = {gmin}, {len(sols)} minima")
    v = [int(x) for x in sols[0]]
    print(f"    v = {v}")
    print(f"    gamma_n = v[{N}] = {v[N]} ; palindrome : "
          f"{v == v[::-1]}")

    print("\n[2] Appartenance (sympy) :")
    x = sp.symbols('x')
    f = sum(c * x**i for i, c in enumerate(v))
    _, r = sp.div(f, (1 - x)**(D + 1), x)
    print(f"    (1-x)^{D+1} divise v : {sp.expand(r) == 0}")
    print(f"    norme2 recomptee : {sum(c*c for c in v)} == {gmin}")

    print("\n[3] Enumeration contrainte (base brute, gamma_n = 1) :")
    m = len(Graw)
    B = [[Fraction(int(t)) for t in row] for row in Graw]
    Bs, mu = [], [[Fraction(0)] * m for _ in range(m)]
    for i in range(m):
        w = B[i][:]
        for j in range(i):
            num = sum(a * b for a, b in zip(B[i], Bs[j]))
            den = sum(a * a for a in Bs[j])
            mu[i][j] = num / den
            w = [a - mu[i][j] * b for a, b in zip(w, Bs[j])]
        Bs.append(w)
    c = [sum(a * a for a in w) for w in Bs]
    best = Fraction(gmin)
    found = []

    def rec(level, coefs, partial):
        if level < 0:
            vv = [0] * (N + 1)
            for k in range(m):
                if coefs[k]:
                    for t in range(N + 1):
                        vv[t] += coefs[k] * int(Graw[k][t])
            if sum(t * t for t in vv) <= gmin:
                found.append(vv[:])
            return
        rem = best - partial
        if rem < 0:
            return
        center = -sum(mu[k][level] * coefs[k] for k in range(level + 1, m))
        if level == m - 1:
            cand = [1]
        else:
            bound = rem / c[level]
            x0 = int(center)
            xx = x0
            while (Fraction(xx) - center) ** 2 <= bound:
                xx -= 1
            lo = xx + 1
            xx = x0 + 1
            while (Fraction(xx) - center) ** 2 <= bound:
                xx += 1
            hi = xx - 1
            cand = range(lo, hi + 1)
        for xv in cand:
            coefs[level] = xv
            add = (Fraction(xv) - center) ** 2 * c[level]
            rec(level - 1, coefs, partial + add)
        coefs[level] = 0

    rec(m - 1, [0] * m, Fraction(0))
    print(f"    vecteurs gamma_n = +-1 de norme <= {gmin} : {len(found)}")
    print("\n" + "=" * 64)
    if not found and abs(v[N]) != 1:
        print("CONTRE-EXEMPLE ETABLI : a (d=21, n=30), AUCUN plus court")
        print("vecteur n'a gamma_n = +-1 (l'unique minimum, au signe pres,")
        print("a gamma_n = +-2). La Conjecture 5 telle qu'enoncee (for any")
        print("n, d) est FAUSSE. Le regime utile a l'application ACC")
        print("(d << n) n'est pas touche par cette cellule.")
    else:
        print("Verification incoherente -- NE PAS conclure.")


if __name__ == "__main__":
    main()
