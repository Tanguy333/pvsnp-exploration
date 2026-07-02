"""
TACHE AS-039 -- l'analyse du specialiste : ce que la boite a outils
theta standard PEUT et NE PEUT PAS faire pour Theta(s) < 1.

1. THEOREME D'OBSTRUCTION (verifie par temoin) : dans le MEME reseau
   (meme Q, meme lambda_1, meme det, meme r), il existe des cosets de
   minval = 0 — les seuils exactement representables d'AS-011. Donc
   AUCUNE estimee n'utilisant seulement la geometrie (lambda_1, det, r)
   ne peut prouver Theta < 1 pour le coset MAJ : l'arithmetique du
   coset (les signes de Lucas) est IRREDUCTIBLE. Les methodes cibles-
   generiques (Banaszczyk, comptage, lissage) sont hors jeu seules.

2. LA GEOMETRIE EST FAVORABLE (calculable) : l'echelle x90 ~ 1/r est
   l'echelle de Banaszczyk (s^2 = 4D/r), et les deux comparaisons du
   squelette tiennent avec marge :
   - det(4Q)^{1/r} vs 4D/r (le test de volume au bon exposant) ;
   - lambda_1(4Q) homogene vs 4D (packing vs shift).
   L'echec n'est PAS geometrique — il est arithmetique.

Mesures : cellules (9..13, d=2,3) — lambda_1 exact (SVP homogene),
det^{1/r}/(4D/r), et le temoin de coset nul dans le meme reseau.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb, exp, log, pi, sqrt

sys.path.insert(0, "checks")
from task_as035 import enum_vecs, inv_rat  # noqa: E402


def lambda1(Q4rat):
    """Plus court vecteur non nul de 2Z^r sous Q (= min 4 z^T Q z),
    par rayons croissants."""
    r = len(Q4rat)
    R = F(1, 4)
    while True:
        pts = enum_vecs(Q4rat, R)
        nz = [v for v, z in pts if any(zz != 0 for zz in z)]
        if nz:
            return min(nz)
        R = R * 4


def main():
    from task_as006b import weight_form, solve_weight
    print("== 2. la geometrie est favorable (les deux comparaisons) ==")
    cells = [(9, 2, 4.365), (11, 2, 20.10), (13, 2, 89.44),
             (9, 3, float(F(387, 512))), (11, 3, float(F(63, 16))),
             (13, 3, float(F(9749, 512)))]
    for n, d, Dv in cells:
        t0 = time.time()
        C, Cm, Qb = weight_form(n, d)
        r = len(C)
        Qrat = [[F(int(Qb[i, j].p), int(Qb[i, j].q)) for j in range(r)]
                for i in range(r)]
        Q4 = [[4 * Qrat[i][j] for j in range(r)] for i in range(r)]
        from sympy import Matrix, Rational
        det4Q = float(Matrix([[Rational((Q4[i][j]).numerator,
                                        (Q4[i][j]).denominator)
                               for j in range(r)]
                              for i in range(r)]).det())
        l1 = float(lambda1(Q4))
        fourD = 4.0 * Dv
        geo = det4Q ** (1.0 / r)
        print(f"  (n={n:>2}, d={d}) r={r:>2} : det^(1/r) = {geo:8.2f} vs "
              f"4D/r = {fourD/r:8.2f}  [marge x{geo/(fourD/r):.1f}] ; "
              f"lambda_1 = {l1:8.3f} vs 4D = {fourD:8.2f} "
              f"[l1/4D = {l1/fourD:.3f}] ({time.time()-t0:.0f}s)",
              flush=True)

    print("== 1. le temoin d'obstruction : coset NUL dans le meme "
          "reseau ==")
    # AS-011 : THR_w exactement representable ssi la fenetre
    # [max(0,w-n+d), min(d,w-1)] ne contient aucun r avec C(d,r) impair.
    # Exemple : (n,d) = (11,3), w = 1 : fenetre [0? max(0,1-8)=0, min(3,0)=0]
    # -> contient r=0 (C(3,0)=1 impair) : PAS exact. Chercher (n,d,w) nul :
    found = []
    for (n, d) in [(9, 2), (11, 2), (13, 2), (9, 3), (11, 3), (13, 3)]:
        for w in range(1, n + 1):
            lo, hi = max(0, w - n + d), min(d, w - 1)
            if lo > hi:
                window_ok = True
            else:
                window_ok = all(comb(d, rr) % 2 == 0
                                for rr in range(lo, hi + 1))
            if window_ok:
                Dw, nodes, capped = solve_weight(n, d, w)
                found.append((n, d, w, Dw, capped))
                break
    for (n, d, w, Dw, capped) in found:
        ok = (Dw == 0) and not capped
        print(f"  (n={n}, d={d}, w={w}) : D = {Dw} "
              f"[{'TEMOIN NUL confirme' if ok else 'a verifier'}]",
              flush=True)
    print()
    print("CONSEQUENCE (theoreme d'obstruction) : meme reseau, meme")
    print("(lambda_1, det, r) — cosets a minval 0 ET le coset MAJ a")
    print("minval ~ 2^n/poly : toute preuve de Theta < 1 DOIT utiliser")
    print("l'arithmetique du coset (signes de Lucas), pas seulement la")
    print("geometrie. Banaszczyk/comptage/lissage seuls : HORS JEU.")


if __name__ == "__main__":
    main()
