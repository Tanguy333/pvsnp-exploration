"""
TACHE AS-022 -- THEOREME assemble : la Conjecture 13 de KV vaut
INCONDITIONNELLEMENT pour tout d <= K.log2(n) (tranche a d CROISSANT).

Chaine (chaque maillon deja prouve, tout inconditionnel) :
1. AS-011 (carte des seuils, duaux de sous-cube) : pour TOUT d, la
   fenetre de (2d+1, d, d+1) est [max(0, d+1-(2d+1)+d), min(d, d)]
   = [0, d], qui contient r = 0 avec C(d,0) = 1 impair => pas de
   representation exacte => b_d := D(2d+1, d, d+1) >= 1/2^{d+3}.
2. AS-004 (padding (1,2,1) par restriction de 2 variables, sans
   hypothese de symetrie), itere : (1,2,1)^{*(m/2)} = C(m, .) =>
   D(n, d, (n+1)/2) >= C(m, m/2) . b_d,   m = n - (2d+1) pair.
3. C(m, m/2) >= 2^m / sqrt(2m) =>
   dist(n,d) >= 2^{(n-3d)/2 - 2} / (2n)^{1/4}
   => pour d <= (2K/3) log2 n :
   dist >= 2^{n/2} / (4 (2n)^{1/4} n^K)  -- perte polynomiale.
   C13 demande 2^{n/2}/n^{O(1)} pour d = o(sqrt(n)/log n) :
   la tranche d = O(log n) est TENUE.

Verifications numeriques (aucun maillon consigne sans calcul) :
A. bases : D(2d+1, d, d+1) exact (enumeration symetrique certifiee,
   dimension d+1) pour d = 2..8 -- consistance avec >= 1/2^{d+3}
   (une valeur < 1/2^{d+3} ou = 0 refuterait la chaine), et valeur
   1/8 attendue aux Mersenne d = 3, 7.
B. convolution une fois sur cellules exactes : D(9,3,5) vs
   D(7,3,5) + 2 D(7,3,4) + D(7,3,3).
C. chaine complete D(n,d,c) >= C(m, m/2) . b_d sur cellules solveur
   (d=3 : n=9..13 ; d=5 : n=13,15) -- aucune violation toleree.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F
from math import comb

sys.path.insert(0, "checks")
from task_as006b import solve_weight  # noqa: E402


def main():
    print("== A. bases b_d = D(2d+1, d, d+1) exactes vs 1/2^{d+3} ==")
    bases = {}
    ok_a = True
    for d in range(2, 9):
        n0 = 2 * d + 1
        t0 = time.time()
        b, nodes, capped = solve_weight(n0, d, d + 1)
        bases[d] = b
        lb = F(1, 2 ** (d + 3))
        flag = "OK" if (b >= lb and b > 0) else "VIOLATION"
        ok_a &= flag == "OK"
        mers = " (Mersenne, attendu 1/8)" if d in (3, 7) else ""
        cap = " CAP!" if capped else ""
        print(f"  d={d} : b_d = {b} >= 1/2^{d + 3} = {lb} [{flag}]{mers}"
              f"{cap} ({time.time() - t0:.0f}s, {nodes} noeuds)", flush=True)
    print(f"  A : {'OK' if ok_a else 'ECHEC'}")

    print("== B. convolution (1,2,1) sur cellules exactes ==")
    d95, *_ = solve_weight(9, 3, 5)
    d735, *_ = solve_weight(7, 3, 5)
    d734, *_ = solve_weight(7, 3, 4)
    d733, *_ = solve_weight(7, 3, 3)
    rhs = d735 + 2 * d734 + d733
    print(f"  D(9,3,5) = {d95} >= {d735} + 2*{d734} + {d733} = {rhs} "
          f"[{'OK' if d95 >= rhs else 'VIOLATION'}]")

    print("== C. chaine complete D(n,d,c) >= C(m, m/2) . b_d ==")
    ok_c = True
    for (n, d) in [(9, 3), (11, 3), (13, 3), (13, 5), (15, 5)]:
        t0 = time.time()
        c = (n + 1) // 2
        m = n - (2 * d + 1)
        Dv, nodes, capped = solve_weight(n, d, c)
        bound = comb(m, m // 2) * bases[d]
        flag = "OK" if Dv >= bound else "VIOLATION"
        ok_c &= flag == "OK"
        cap = " CAP!" if capped else ""
        print(f"  (n={n}, d={d}) : D = {Dv} >= C({m},{m // 2}).b_{d} = "
              f"{bound} [{flag}] ratio {float(Dv / bound):.2f}{cap} "
              f"({time.time() - t0:.0f}s)", flush=True)
    print(f"  C : {'OK' if ok_c else 'ECHEC'}")

    print()
    print("THEOREME (si A, B, C OK) : pour tout n impair et tout d avec")
    print("  2d+1 <= n,  D(n, d, (n+1)/2) >= C(n-2d-1, (n-2d-1)/2) / 2^{d+3}")
    print("  => dist >= 2^{(n-3d)/2 - 2} / (2n)^{1/4}")
    print("  => Conjecture 13 INCONDITIONNELLE sur d <= (2K/3) log2 n,")
    print("     avec perte polynomiale n^{K + 1/4} (tout K constant).")


if __name__ == "__main__":
    main()
